#!/usr/bin/env python3
"""
Entry Packet Generator

For a given headword, assembles a research packet containing:
- Source digest
- Contrast terms
- Examples
- Workflow notes
- Model-fit evidence
- Open questions

Usage:
    python scripts/generate_entry_packet.py --headword "specificity"
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_CARDS = PROJECT_ROOT / "corpus" / "source_cards"
TAXONOMY_DIR = PROJECT_ROOT / "taxonomy"
ENTRIES_DRAFTS = PROJECT_ROOT / "entries" / "drafts"
ENTRIES_DRAFTS.mkdir(parents=True, exist_ok=True)


def load_taxonomy() -> dict:
    abs_path = TAXONOMY_DIR / "abstractions.json"
    if abs_path.exists():
        with open(abs_path) as f:
            return json.load(f)
    return {}


def load_relations() -> list[dict]:
    rel_path = TAXONOMY_DIR / "relations.json"
    if rel_path.exists():
        with open(rel_path) as f:
            return json.load(f)
    return []


def find_relevant_sources(headword: str) -> list[dict]:
    """Find source cards relevant to a headword."""
    relevant = []
    for f in SOURCE_CARDS.glob("*.json"):
        with open(f) as fh:
            card = json.load(fh)
        topics = [t.lower() for t in card.get("topics", [])]
        if headword.lower() in topics or any(headword.lower() in t for t in topics):
            relevant.append(card)
    return relevant


def find_contrast_terms(headword: str, taxonomy: dict) -> list[str]:
    """Find terms that contrast with or relate to the headword."""
    slug = headword.lower().replace(" ", "_").replace("-", "_")
    entry = taxonomy.get(slug, {})
    contrast = entry.get("contrast_set", [])
    overlaps = entry.get("overlaps_with", [])
    return list(set(contrast + overlaps))


def generate_packet(headword: str) -> dict:
    slug = headword.lower().replace(" ", "_").replace("-", "_")
    taxonomy = load_taxonomy()
    relations = load_relations()
    sources = find_relevant_sources(headword)
    contrast_terms = find_contrast_terms(headword, taxonomy)

    entry_data = taxonomy.get(slug, {})

    packet = {
        "headword": headword,
        "slug": slug,
        "family": entry_data.get("family", "unclassified"),
        "generated_at": datetime.now().isoformat(),
        "source_digest": {
            "source_count": len(sources),
            "source_ids": [s["source_id"] for s in sources],
            "trust_tiers": {s["source_id"]: s.get("trust_tier", "T3") for s in sources},
        },
        "contrast_terms": contrast_terms,
        "taxonomy_context": {
            "parent": entry_data.get("parent"),
            "children": entry_data.get("children", []),
            "synonyms": entry_data.get("synonyms", []),
        },
        "open_questions": [
            f"What distinguishes {headword} from its closest neighbor?",
            f"What is the most common misuse of {headword} in prompting?",
            f"How does {headword} behave differently across model tiers?",
            f"What agent workflow patterns rely on {headword}?",
        ],
        "writing_guidance": {
            "target_length_words": "1200-2500",
            "schema_reference": "ENTRY_SCHEMA.md",
            "style_reference": "STYLE_GUIDE.md",
        },
    }

    packet_path = ENTRIES_DRAFTS / f"{slug}.packet.json"
    with open(packet_path, "w") as f:
        json.dump(packet, f, indent=2)
    print(f"Entry packet saved: {packet_path}")
    return packet


def main():
    parser = argparse.ArgumentParser(description="Generate entry research packet")
    parser.add_argument("--headword", type=str, required=True, help="Headword to generate packet for")
    args = parser.parse_args()
    packet = generate_packet(args.headword)
    print(f"\nPacket for '{args.headword}':")
    print(f"  Family: {packet['family']}")
    print(f"  Sources: {packet['source_digest']['source_count']}")
    print(f"  Contrast terms: {packet['contrast_terms']}")


if __name__ == "__main__":
    main()
