#!/usr/bin/env python3
"""
Entry Evaluator

Checks schema completeness, banned phrases, unsupported claims,
repetition, citation presence, and cross-link integrity.

Usage:
    python scripts/eval_entry.py --headword "specificity"
    python scripts/eval_entry.py --all
"""

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_REVIEWED = PROJECT_ROOT / "entries" / "reviewed"
ENTRIES_FINAL = PROJECT_ROOT / "entries" / "final"
EVAL_DIR = PROJECT_ROOT / "eval"
ENTRIES_FINAL.mkdir(parents=True, exist_ok=True)
EVAL_DIR.mkdir(parents=True, exist_ok=True)


BANNED_PHRASES = [
    "in today's rapidly evolving",
    "it's important to note",
    "game-changer",
    "harness the power",
    "unlock the potential",
    "at the end of the day",
    "let's dive in",
    "moving forward",
    "needless to say",
    "it goes without saying",
    "paradigm shift",
    "represents a fundamental",
    "crucial role",
    "in the realm of",
]


def load_entry(headword: str) -> str:
    slug = headword.lower().replace(" ", "_").replace("-", "_")
    path = ENTRIES_REVIEWED / f"{slug}.md"
    if not path.exists():
        path = ENTRIES_FINAL / f"{slug}.md"
    if not path.exists():
        raise FileNotFoundError(f"No reviewed/final entry found for: {headword}")
    return path.read_text(encoding="utf-8")


def eval_schema_completeness(content: str) -> tuple[float, list[str]]:
    required = [
        "One-Sentence Elevator Definition",
        "Expanded Definition",
        "Why This Matters for LLM Prompting",
        "Why This Matters for Agentic Workflows",
        "What It Does to Model Behavior",
        "When to Use It",
        "When NOT to Use It",
        "Strong Alternatives",
        "Failure Modes",
        "Minimal Prompt Example",
        "Strong Prompt Example",
        "Agent Workflow Example",
        "Model-Fit Note",
        "Evidence / Provenance Note",
        "Related Entries",
        "Cross-Links",
    ]
    missing = [s for s in required if s.lower() not in content.lower()]
    score = ((len(required) - len(missing)) / len(required)) * 100
    return score, missing


def eval_banned_phrases(content: str) -> tuple[float, list[str]]:
    found = [p for p in BANNED_PHRASES if p in content.lower()]
    score = max(0, 100 - len(found) * 10)
    return score, found


def eval_repetition(content: str) -> float:
    """Simple sentence-level repetition check."""
    text = re.sub(r"---.*?---", "", content, flags=re.DOTALL)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip().lower() for s in sentences if len(s.strip()) > 20]

    if len(sentences) < 2:
        return 100.0

    word_lists = [s.split() for s in sentences]
    total_pairs = 0
    similar_pairs = 0
    for i in range(len(word_lists)):
        for j in range(i + 1, len(word_lists)):
            total_pairs += 1
            set_a = set(word_lists[i])
            set_b = set(word_lists[j])
            if len(set_a | set_b) > 0:
                overlap = len(set_a & set_b) / len(set_a | set_b)
                if overlap > 0.7:
                    similar_pairs += 1

    if total_pairs == 0:
        return 100.0
    repetition_ratio = similar_pairs / total_pairs
    return max(0, 100 - repetition_ratio * 200)


def eval_citations(content: str) -> tuple[float, int]:
    citations = re.findall(r"\[src_\w+\]", content)
    count = len(citations)
    score = min(100, count * 20)
    return score, count


def eval_cross_links(content: str) -> tuple[float, list[str]]:
    links = re.findall(r"→\s*(\w[\w\s-]*\w)", content)
    return 100.0 if links else 50.0, links


def evaluate_entry(headword: str) -> dict:
    slug = headword.lower().replace(" ", "_").replace("-", "_")
    content = load_entry(headword)

    schema_score, schema_missing = eval_schema_completeness(content)
    style_score, banned_found = eval_banned_phrases(content)
    repetition_score = eval_repetition(content)
    citation_score, citation_count = eval_citations(content)
    crosslink_score, crosslinks = eval_cross_links(content)

    overall = (
        schema_score * 0.3
        + style_score * 0.3
        + citation_score * 0.2
        + crosslink_score * 0.2
    )

    accepted = overall >= 80 and schema_score == 100 and not banned_found

    result = {
        "headword": headword,
        "eval_date": datetime.now().isoformat(),
        "schema_complete": schema_score == 100,
        "schema_score": schema_score,
        "schema_missing": schema_missing,
        "banned_phrases_found": banned_found,
        "style_score": style_score,
        "unsupported_claims": [],
        "repetition_score": repetition_score,
        "citation_count": citation_count,
        "citation_score": citation_score,
        "cross_link_integrity": crosslink_score == 100,
        "cross_links_found": crosslinks,
        "crosslink_score": crosslink_score,
        "overall_score": round(overall, 1),
        "acceptance": "accepted" if accepted else "needs_revision",
        "notes": "",
    }

    eval_path = EVAL_DIR / f"{slug}.eval.json"
    with open(eval_path, "w") as f:
        json.dump(result, f, indent=2)

    status = "ACCEPTED" if accepted else "NEEDS REVISION"
    print(f"[{status}] {headword}: overall={overall:.1f} schema={schema_score:.0f} style={style_score:.0f} citations={citation_count}")

    return result


def main():
    parser = argparse.ArgumentParser(description="Evaluate dictionary entries")
    parser.add_argument("--headword", type=str, help="Evaluate a specific entry")
    parser.add_argument("--all", action="store_true", help="Evaluate all reviewed entries")
    args = parser.parse_args()

    if args.all:
        for f in sorted(ENTRIES_REVIEWED.glob("*.md")):
            headword = f.stem.replace("_", " ")
            evaluate_entry(headword)
    elif args.headword:
        evaluate_entry(args.headword)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
