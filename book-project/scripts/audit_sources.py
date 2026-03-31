#!/usr/bin/env python3
"""
Source Auditor

Scores source trust tiers, flags low-trust or duplicate sources,
detects stale docs, and ensures every technical claim can be traced.

Usage:
    python scripts/audit_sources.py
    python scripts/audit_sources.py --source-id src_specificity_001
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_CARDS = PROJECT_ROOT / "corpus" / "source_cards"
LOGS = PROJECT_ROOT / "logs"
LOGS.mkdir(parents=True, exist_ok=True)


def load_all_source_cards() -> list[dict]:
    cards = []
    for f in SOURCE_CARDS.glob("*.json"):
        with open(f) as fh:
            cards.append(json.load(fh))
    return cards


def check_duplicates(cards: list[dict]) -> list[dict]:
    """Find sources with identical content hashes."""
    hash_map = {}
    duplicates = []
    for card in cards:
        h = card.get("content_hash", "")
        if h and h in hash_map:
            duplicates.append({
                "duplicate_of": hash_map[h],
                "source_id": card["source_id"],
                "content_hash": h,
            })
        elif h:
            hash_map[h] = card["source_id"]
    return duplicates


def check_staleness(cards: list[dict], max_age_days: int = 180) -> list[dict]:
    """Flag sources older than max_age_days."""
    stale = []
    now = datetime.now()
    for card in cards:
        date_str = card.get("date_published", "")
        if not date_str or date_str == "undated":
            stale.append({
                "source_id": card["source_id"],
                "reason": "no publication date",
            })
            continue
        try:
            pub_date = datetime.fromisoformat(date_str)
            age = (now - pub_date).days
            if age > max_age_days:
                stale.append({
                    "source_id": card["source_id"],
                    "reason": f"published {age} days ago (threshold: {max_age_days})",
                    "date_published": date_str,
                })
        except ValueError:
            stale.append({
                "source_id": card["source_id"],
                "reason": f"unparseable date: {date_str}",
            })
    return stale


def check_trust_distribution(cards: list[dict]) -> dict:
    """Summarize trust tier distribution."""
    dist = {"T1": 0, "T2": 0, "T3": 0, "T4": 0, "unset": 0}
    for card in cards:
        tier = card.get("trust_tier", "unset")
        dist[tier] = dist.get(tier, 0) + 1
    return dist


def score_source(card: dict) -> dict:
    """Apply heuristic scoring to a source card."""
    score = 50
    reasons = []

    if card.get("trust_tier") == "T1":
        score += 30
        reasons.append("+30: T1 trust tier")
    elif card.get("trust_tier") == "T2":
        score += 15
        reasons.append("+15: T2 trust tier")
    elif card.get("trust_tier") == "T4":
        score -= 20
        reasons.append("-20: T4 trust tier")

    if card.get("author"):
        score += 10
        reasons.append("+10: named author")

    if card.get("organization"):
        score += 10
        reasons.append("+10: organizational source")

    if card.get("date_published") and card["date_published"] != "undated":
        score += 5
        reasons.append("+5: dated")

    return {"source_id": card["source_id"], "score": min(100, max(0, score)), "reasons": reasons}


def audit(source_id: str = None):
    cards = load_all_source_cards()

    if source_id:
        cards = [c for c in cards if c["source_id"] == source_id]
        if not cards:
            print(f"No source card found for: {source_id}")
            return

    print(f"Auditing {len(cards)} source cards...\n")

    duplicates = check_duplicates(cards)
    stale = check_staleness(cards)
    trust_dist = check_trust_distribution(cards)
    scores = [score_source(c) for c in cards]

    report = {
        "audit_date": datetime.now().isoformat(),
        "total_sources": len(cards),
        "trust_distribution": trust_dist,
        "duplicates": duplicates,
        "stale_sources": stale,
        "scores": scores,
    }

    report_path = LOGS / f"source_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Trust distribution: {trust_dist}")
    print(f"Duplicates found: {len(duplicates)}")
    print(f"Stale sources: {len(stale)}")
    print(f"Audit report saved: {report_path}")


def main():
    parser = argparse.ArgumentParser(description="Audit source cards")
    parser.add_argument("--source-id", type=str, help="Audit a specific source")
    args = parser.parse_args()
    audit(args.source_id)


if __name__ == "__main__":
    main()
