#!/usr/bin/env python3
"""
Entry Writer

Calls orchestrated agents to produce a draft entry from a research packet.
Uses openai-agents-python for multi-agent pipeline.

Usage:
    python scripts/write_entry.py --headword "specificity"
    python scripts/write_entry.py --packet entries/drafts/specificity.packet.json
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DRAFTS = PROJECT_ROOT / "entries" / "drafts"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def load_packet(headword: str = None, packet_path: str = None) -> dict:
    if packet_path:
        path = Path(packet_path)
    else:
        slug = headword.lower().replace(" ", "_").replace("-", "_")
        path = ENTRIES_DRAFTS / f"{slug}.packet.json"

    if not path.exists():
        raise FileNotFoundError(f"No packet found at {path}. Run generate_entry_packet.py first.")

    with open(path) as f:
        return json.load(f)


def load_prompt(name: str) -> str:
    path = PROMPTS_DIR / f"{name}.md"
    if path.exists():
        return path.read_text()
    return ""


def build_entry_prompt(packet: dict) -> str:
    """Construct the full prompt for entry generation from a packet."""
    schema_prompt = load_prompt("entry_drafting")
    style_prompt = load_prompt("style_enforcement")

    return f"""You are the Lexicographer agent for The Abstraction Dictionary.

## Task
Write a complete dictionary entry for the headword: **{packet['headword']}**

## Entry Family
{packet['family']}

## Research Context
- Sources available: {packet['source_digest']['source_count']}
- Source IDs: {', '.join(packet['source_digest']['source_ids'])}
- Contrast terms: {', '.join(packet['contrast_terms']) if packet['contrast_terms'] else 'None identified yet'}
- Taxonomy parent: {packet['taxonomy_context'].get('parent', 'None')}
- Synonyms: {', '.join(packet['taxonomy_context'].get('synonyms', []))}

## Open Questions to Address
{chr(10).join('- ' + q for q in packet['open_questions'])}

## Schema Requirements
Follow ENTRY_SCHEMA.md exactly. Include all 17 mandatory sections plus YAML front matter.

## Style Requirements
Follow STYLE_GUIDE.md. No banned phrases. No AI-writing tells. Target 1,200-2,500 words.

{schema_prompt}

{style_prompt}
"""


def write_entry_with_agents(packet: dict) -> str:
    """
    Production implementation uses openai-agents-python for multi-agent drafting.
    This stub generates a skeleton; replace with agent pipeline when configured.
    """
    headword = packet["headword"]
    slug = packet["slug"]
    family = packet["family"]
    now = datetime.now().isoformat()

    skeleton = f"""---
headword: "{headword}"
slug: "{slug}"
family: "{family}"
status: "draft"
version: 1
created: "{now}"
last_modified: "{now}"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: []
cross_links: []
tags: []
has_note_box: false
note_box_type: ""
---

# {headword}

## One-Sentence Elevator Definition

[DRAFT] {headword.capitalize()} is ...

## Expanded Definition

[DRAFT] ...

## Why This Matters for LLM Prompting

[DRAFT] ...

## Why This Matters for Agentic Workflows

[DRAFT] ...

## What It Does to Model Behavior

[DRAFT] ...

## When to Use It

- [DRAFT] ...

## When NOT to Use It

- [DRAFT] ...

## Strong Alternatives / Adjacent Abstractions / Contrast Set

| Term | Relationship | Key Difference |
|------|-------------|----------------|
| ... | ... | ... |

## Failure Modes / Misuse Patterns

1. [DRAFT] ...
2. [DRAFT] ...

## Minimal Prompt Example

```
[DRAFT]
```

## Strong Prompt Example

```
[DRAFT]
```

## Agent Workflow Example

```
[DRAFT]
```

## Model-Fit Note

[DRAFT] ...

## Evidence / Provenance Note

[DRAFT] Sources: {', '.join(packet['source_digest']['source_ids'])}

## Related Entries

- [DRAFT] ...

## Cross-Links

[DRAFT] ...
"""
    return skeleton


def save_draft(headword: str, content: str):
    slug = headword.lower().replace(" ", "_").replace("-", "_")
    path = ENTRIES_DRAFTS / f"{slug}.md"
    path.write_text(content, encoding="utf-8")
    print(f"Draft saved: {path}")


def main():
    parser = argparse.ArgumentParser(description="Write a dictionary entry")
    parser.add_argument("--headword", type=str, help="Headword to write")
    parser.add_argument("--packet", type=str, help="Path to entry packet JSON")
    args = parser.parse_args()

    if not args.headword and not args.packet:
        parser.print_help()
        return

    packet = load_packet(headword=args.headword, packet_path=args.packet)
    print(f"Writing entry for: {packet['headword']}")

    prompt = build_entry_prompt(packet)
    log_path = LOGS_DIR / f"write_{packet['slug']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    log_path.write_text(prompt, encoding="utf-8")

    content = write_entry_with_agents(packet)
    save_draft(packet["headword"], content)


if __name__ == "__main__":
    main()
