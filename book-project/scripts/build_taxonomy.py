#!/usr/bin/env python3
"""
Taxonomy Builder

Clusters candidate abstractions, proposes synonyms, overlaps,
and parent-child relations. Outputs taxonomy JSON files.

Usage:
    python scripts/build_taxonomy.py
    python scripts/build_taxonomy.py --headwords-file taxonomy/candidate_headwords.txt
"""

import argparse
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TAXONOMY_DIR = PROJECT_ROOT / "taxonomy"
TAXONOMY_DIR.mkdir(parents=True, exist_ok=True)

FAMILIES = {
    "core_abstraction": {
        "description": "Fundamental concepts for language-as-programming",
        "examples": ["specificity", "framing", "decomposition", "hierarchy", "grounding"],
    },
    "instructional_action": {
        "description": "Verbs that direct model behavior",
        "examples": ["constrain", "compare", "rank", "justify", "critique", "synthesize"],
    },
    "context_architecture": {
        "description": "Structures for managing information flow",
        "examples": ["context windowing", "retrieval scaffolding", "memory cueing", "source anchoring"],
    },
    "agent_workflow": {
        "description": "Multi-agent orchestration patterns",
        "examples": ["delegation", "handoff", "verification loop", "watchdog", "planner-executor split"],
    },
    "quality_control": {
        "description": "Evaluation and assurance mechanisms",
        "examples": ["audit trail", "falsifiability", "rubric", "test harness", "regression check"],
    },
    "tone_style": {
        "description": "Register, voice, and stylistic control",
        "examples": ["register", "warmth", "authority", "terseness", "narrative glue"],
    },
    "failure_mode": {
        "description": "Named ways prompting and agent instructions fail",
        "examples": ["vagueness", "hallucination bait", "overcompression", "underspecification", "prompt drift"],
    },
}


def load_headwords(filepath: str = None) -> list[str]:
    if filepath and Path(filepath).exists():
        with open(filepath) as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []


def classify_headword(headword: str, families: dict) -> str:
    """Heuristic classification. In production, use an LLM agent for this."""
    headword_lower = headword.lower()
    for family_id, family_data in families.items():
        if headword_lower in [e.lower() for e in family_data["examples"]]:
            return family_id
    return "unclassified"


def build_abstractions(headwords: list[str]) -> dict:
    abstractions = {}
    for hw in headwords:
        family = classify_headword(hw, FAMILIES)
        slug = hw.lower().replace(" ", "_").replace("-", "_")
        abstractions[slug] = {
            "headword": hw,
            "slug": slug,
            "family": family,
            "synonyms": [],
            "parent": None,
            "children": [],
            "overlaps_with": [],
            "contrast_set": [],
            "status": "candidate",
        }
    return abstractions


def build_relations(abstractions: dict) -> list[dict]:
    """Stub for relation extraction. In production, use an LLM agent."""
    relations = []
    return relations


def save_taxonomy(abstractions: dict, relations: list[dict]):
    abs_path = TAXONOMY_DIR / "abstractions.json"
    rel_path = TAXONOMY_DIR / "relations.json"
    fam_path = TAXONOMY_DIR / "families.json"

    with open(abs_path, "w") as f:
        json.dump(abstractions, f, indent=2)
    with open(rel_path, "w") as f:
        json.dump(relations, f, indent=2)
    with open(fam_path, "w") as f:
        json.dump(FAMILIES, f, indent=2)

    print(f"Saved {len(abstractions)} abstractions to {abs_path}")
    print(f"Saved {len(relations)} relations to {rel_path}")
    print(f"Saved {len(FAMILIES)} families to {fam_path}")


def main():
    parser = argparse.ArgumentParser(description="Build abstraction taxonomy")
    parser.add_argument("--headwords-file", type=str, help="File with candidate headwords")
    args = parser.parse_args()

    headwords = load_headwords(args.headwords_file)
    if not headwords:
        print("No headwords file provided. Using family examples as seeds.")
        for family_data in FAMILIES.values():
            headwords.extend(family_data["examples"])

    print(f"Processing {len(headwords)} candidate headwords...")
    abstractions = build_abstractions(headwords)
    relations = build_relations(abstractions)
    save_taxonomy(abstractions, relations)


if __name__ == "__main__":
    main()
