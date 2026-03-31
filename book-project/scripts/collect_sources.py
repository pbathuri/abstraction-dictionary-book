#!/usr/bin/env python3
"""
Source Collection Pipeline

Reads topic manifests and fetches sources using Scrapling.
Stores raw content, normalized markdown, and source cards.

Usage:
    python scripts/collect_sources.py --topic "prompt engineering"
    python scripts/collect_sources.py --manifest corpus/raw/manifests/specificity.json
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CORPUS_RAW = PROJECT_ROOT / "corpus" / "raw"
CORPUS_NORMALIZED = PROJECT_ROOT / "corpus" / "normalized"
CORPUS_SNAPSHOTS = PROJECT_ROOT / "corpus" / "snapshots"
SOURCE_CARDS = PROJECT_ROOT / "corpus" / "source_cards"

for d in [CORPUS_RAW, CORPUS_NORMALIZED, CORPUS_SNAPSHOTS, SOURCE_CARDS]:
    d.mkdir(parents=True, exist_ok=True)


def load_manifest(manifest_path: str) -> dict:
    with open(manifest_path) as f:
        return json.load(f)


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def make_source_card(
    source_id: str,
    title: str,
    url: str,
    author: str = "",
    organization: str = "",
    date_published: str = "",
    source_type: str = "",
    trust_tier: str = "T3",
    raw_path: str = "",
    normalized_path: str = "",
    topics: list = None,
) -> dict:
    return {
        "source_id": source_id,
        "title": title,
        "url": url,
        "author": author,
        "organization": organization,
        "date_published": date_published,
        "date_accessed": datetime.now().isoformat(),
        "source_type": source_type,
        "trust_tier": trust_tier,
        "extraction_method": "scrapling",
        "content_hash": "",
        "snapshot_path": raw_path,
        "normalized_path": normalized_path,
        "extraction_notes": "",
        "topics": topics or [],
        "key_claims": [],
    }


def save_source_card(card: dict):
    path = SOURCE_CARDS / f"{card['source_id']}.json"
    with open(path, "w") as f:
        json.dump(card, f, indent=2)
    print(f"  Saved source card: {path}")


def fetch_url(url: str) -> str:
    """Fetch a URL using Scrapling. Falls back to requests if Scrapling unavailable."""
    try:
        from scrapling import Fetcher

        fetcher = Fetcher()
        response = fetcher.get(url)
        return response.text if hasattr(response, "text") else str(response)
    except ImportError:
        import requests

        resp = requests.get(url, timeout=30, headers={"User-Agent": "AbstractionDict/1.0"})
        resp.raise_for_status()
        return resp.text


def normalize_html_to_markdown(html: str, url: str) -> str:
    """Strip navigation, ads, and boilerplate from HTML. Return clean markdown."""
    try:
        from scrapling import Adaptor

        page = Adaptor(html, url=url)
        main = page.css("article, main, .content, .post-body, #content")
        if main:
            text = main[0].text
        else:
            text = page.text
        return text.strip()
    except (ImportError, Exception):
        import re

        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text)
        return text.strip()


def collect_for_topic(topic: str, urls: list[str] = None):
    """Collect sources for a given topic."""
    print(f"Collecting sources for topic: {topic}")
    topic_slug = topic.lower().replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if not urls:
        print("  No URLs provided. Create a manifest or pass --urls.")
        return

    for i, url in enumerate(urls):
        source_id = f"src_{topic_slug}_{i+1:03d}"
        print(f"  Fetching [{i+1}/{len(urls)}]: {url}")

        try:
            raw_html = fetch_url(url)
        except Exception as e:
            print(f"    FAILED: {e}")
            continue

        chash = content_hash(raw_html)
        raw_filename = f"{source_id}_{chash}.html"
        raw_path = CORPUS_RAW / raw_filename
        raw_path.write_text(raw_html, encoding="utf-8")

        snapshot_path = CORPUS_SNAPSHOTS / f"{source_id}_{timestamp}.html"
        snapshot_path.write_text(raw_html, encoding="utf-8")

        normalized = normalize_html_to_markdown(raw_html, url)
        norm_filename = f"{source_id}.md"
        norm_path = CORPUS_NORMALIZED / norm_filename
        norm_path.write_text(normalized, encoding="utf-8")

        card = make_source_card(
            source_id=source_id,
            title=f"[Auto] {topic} - source {i+1}",
            url=url,
            source_type="web_page",
            trust_tier="T3",
            raw_path=str(raw_path.relative_to(PROJECT_ROOT)),
            normalized_path=str(norm_path.relative_to(PROJECT_ROOT)),
            topics=[topic],
        )
        card["content_hash"] = chash
        save_source_card(card)

    print(f"Collection complete for topic: {topic}")


def main():
    parser = argparse.ArgumentParser(description="Collect sources for the Abstraction Dictionary")
    parser.add_argument("--topic", type=str, help="Topic to collect sources for")
    parser.add_argument("--manifest", type=str, help="Path to a topic manifest JSON file")
    parser.add_argument("--urls", nargs="+", help="Specific URLs to fetch")
    args = parser.parse_args()

    if args.manifest:
        manifest = load_manifest(args.manifest)
        collect_for_topic(manifest["topic"], manifest.get("urls", []))
    elif args.topic:
        collect_for_topic(args.topic, args.urls or [])
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
