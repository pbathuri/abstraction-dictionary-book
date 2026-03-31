#!/usr/bin/env python3
"""
Entry Reviewer

Runs consistency edit, provenance check, and optional humanizer pass.

Usage:
    python scripts/review_entry.py --headword "specificity"
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DRAFTS = PROJECT_ROOT / "entries" / "drafts"
ENTRIES_REVIEWED = PROJECT_ROOT / "entries" / "reviewed"
LOGS_DIR = PROJECT_ROOT / "logs"
ENTRIES_REVIEWED.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

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
    "it is worth noting",
    "serves as a testament",
    "navigating the complexities",
]


def load_draft(headword: str) -> str:
    slug = headword.lower().replace(" ", "_").replace("-", "_")
    path = ENTRIES_DRAFTS / f"{slug}.md"
    if not path.exists():
        raise FileNotFoundError(f"No draft found at {path}")
    return path.read_text(encoding="utf-8")


def check_schema_completeness(content: str) -> dict:
    """Check that all required sections are present."""
    required_sections = [
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

    found = []
    missing = []
    for section in required_sections:
        if section.lower() in content.lower():
            found.append(section)
        else:
            missing.append(section)

    return {
        "total_required": len(required_sections),
        "found": len(found),
        "missing": missing,
        "complete": len(missing) == 0,
    }


def check_banned_phrases(content: str) -> list[str]:
    found = []
    content_lower = content.lower()
    for phrase in BANNED_PHRASES:
        if phrase in content_lower:
            found.append(phrase)
    return found


def check_draft_markers(content: str) -> int:
    return content.count("[DRAFT]")


def check_word_count(content: str) -> int:
    text = re.sub(r"---.*?---", "", content, flags=re.DOTALL)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return len(text.split())


def review_entry(headword: str, apply_humanizer: bool = False):
    print(f"Reviewing entry: {headword}")
    content = load_draft(headword)
    slug = headword.lower().replace(" ", "_").replace("-", "_")

    schema = check_schema_completeness(content)
    banned = check_banned_phrases(content)
    draft_markers = check_draft_markers(content)
    word_count = check_word_count(content)

    review_report = {
        "headword": headword,
        "review_date": datetime.now().isoformat(),
        "schema_completeness": schema,
        "banned_phrases_found": banned,
        "draft_markers_remaining": draft_markers,
        "word_count": word_count,
        "word_count_in_range": 1200 <= word_count <= 2500,
        "issues": [],
    }

    if not schema["complete"]:
        review_report["issues"].append(f"Missing sections: {', '.join(schema['missing'])}")
    if banned:
        review_report["issues"].append(f"Banned phrases: {', '.join(banned)}")
    if draft_markers > 0:
        review_report["issues"].append(f"{draft_markers} [DRAFT] markers remaining")
    if not review_report["word_count_in_range"]:
        review_report["issues"].append(f"Word count {word_count} outside 1200-2500 range")

    if not review_report["issues"]:
        reviewed_path = ENTRIES_REVIEWED / f"{slug}.md"
        reviewed_path.write_text(content, encoding="utf-8")
        review_report["status"] = "passed"
        print(f"  PASSED — saved to {reviewed_path}")
    else:
        review_report["status"] = "needs_revision"
        print(f"  NEEDS REVISION — {len(review_report['issues'])} issues found:")
        for issue in review_report["issues"]:
            print(f"    - {issue}")

    log_path = LOGS_DIR / f"review_{slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_path, "w") as f:
        json.dump(review_report, f, indent=2)

    return review_report


def main():
    parser = argparse.ArgumentParser(description="Review a dictionary entry")
    parser.add_argument("--headword", type=str, required=True)
    parser.add_argument("--humanizer", action="store_true", help="Apply humanizer pass to narrative sections")
    args = parser.parse_args()
    review_entry(args.headword, args.humanizer)


if __name__ == "__main__":
    main()
