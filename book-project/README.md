# The Abstraction Dictionary

**Natural Language as the New Programming Language**

**By Kastle Light**

An interactive, source-grounded reference book that teaches readers exactly which words, verbs, phrases, and sentence structures to use when prompting LLMs and building agentic workflows. Built from 11,400 prompt experiments across four model families. 75 named abstractions, each with real project examples, before-and-after comparisons, and paste-into-your-LLM exercises.

## Project Structure

```
book-project/
├── corpus/              # Research corpus
│   ├── raw/             # Unprocessed source material
│   ├── normalized/      # Clean markdown/json extractions
│   ├── snapshots/       # Reproducible source snapshots
│   └── source_cards/    # Structured source metadata
├── taxonomy/            # Abstraction classification system
├── prompts/             # Prompt templates for all pipeline stages
├── agents/              # Agent definitions and persona configs
├── entries/             # Entry lifecycle
│   ├── drafts/          # First-pass entries
│   ├── reviewed/        # Post-review entries
│   └── final/           # Accepted entries + provenance
├── front_matter/        # Preface, how-to-use, editorial method
├── appendices/          # Model matrix, phrasebook, indexes
├── style/               # Style assets and templates
├── eval/                # Evaluation results and model comparisons
├── art/                 # Visual assets
│   ├── covers/          # Cover prototypes
│   ├── figures/         # Diagrams and workflow figures
│   └── callouts/        # Note-box icons and decorations
├── exports/             # Final compiled outputs (md, epub, pdf)
├── scripts/             # Pipeline scripts
├── logs/                # Run logs and audit trails
├── tests/               # Test suites
├── docs/                # Project documentation
└── external/            # Cloned dependency repos
```

## Core Thesis

Natural human language is now the most powerful programming interface for AI systems. This book provides a precise, operational vocabulary for wielding that interface well.

## Quick Start

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run source collection for a topic
python scripts/collect_sources.py --topic "prompt engineering"

# Generate an entry packet
python scripts/generate_entry_packet.py --headword "specificity"

# Write a draft entry
python scripts/write_entry.py --headword "specificity"

# Review an entry
python scripts/review_entry.py --headword "specificity"

# Compile the book
python scripts/compile_book.py --format markdown
```

## Pipeline Overview

1. **Collect** — Acquire sources via Scrapling
2. **Audit** — Score trust tiers, detect duplicates
3. **Taxonomy** — Cluster abstractions, map relations
4. **Packet** — Assemble entry research packets
5. **Draft** — Multi-agent entry generation
6. **Review** — Consistency, provenance, humanization
7. **Evaluate** — Schema, style, citation checks
8. **Compile** — Assemble and export final book

## Governing Documents

- `BOOK_BIBLE.md` — Canonical reference for what this book is
- `ENTRY_SCHEMA.md` — Required structure for every entry
- `STYLE_GUIDE.md` — Voice, banned patterns, tone targets
- `SOURCE_POLICY.md` — How sources are acquired, scored, cited
- `EVAL_POLICY.md` — Acceptance criteria for entries
- `ROADMAP.md` — Production schedule and milestones
- `program.md` — Living operating doctrine for the authoring system
- `AGENTS.md` — Agent definitions and handoff protocol

## License

All original content in this repository is proprietary. External dependencies retain their own licenses. See `external/` for repo-specific license files.
