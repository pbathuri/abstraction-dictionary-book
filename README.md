# Book authoring pipeline

This repository holds the **tooling** used to build a long-form reference manuscript: source acquisition, auditing, taxonomy, entry packets, drafting/review automation, evaluation gates, and compilation—not the manuscript, assets, or research corpus themselves.

## What lives here

| Path | Purpose |
|------|--------|
| `book-project/scripts/` | Pipeline: collect, audit, taxonomy, packets, write/review/eval hooks, compile drivers, prompt experiments |
| `book-project/prompts/` | Stage prompts for agents / CLI steps |
| `book-project/docs/` | Tool audits, role maps, repo keep/drop notes |
| `book-project/` + `*.md` | Pipeline contracts: `ENTRY_SCHEMA.md`, `SOURCE_POLICY.md`, `EVAL_POLICY.md`, `ROADMAP.md`, `AGENTS.md`, `program.md` |

## What stays local only (gitignored)

- Entry text (`entries/`), front matter, appendices, cover/figure art, compiled exports  
- `corpus/` (raw, normalized, snapshots, source cards)  
- Taxonomy outputs, eval run artifacts, `BOOK_BIBLE` / style / entry templates  

Clone this repo, then restore or generate those directories on your machine if you need a full build.

## Quick start

```bash
cd book-project
python -m venv .venv && source .venv/bin/activate  # optional
pip install -r requirements.txt

# Example pipeline steps (see script `--help` where available)
python scripts/collect_sources.py --topic "prompt engineering"
python scripts/audit_sources.py
python scripts/build_taxonomy.py
python scripts/generate_entry_packet.py --headword "specificity"
python scripts/eval_entry.py --headword "specificity"
python scripts/compile_book.py --format markdown
```

Scraping integrations (e.g. Scrapling) and external tool repos are documented in `book-project/docs/`; dependency clones go under `book-project/external/` (ignored).

## License

Original **code and pipeline documentation** in this repository: use per your project policy. Manuscript and corpus you generate locally are separate. Third-party code under `external/` retains its own licenses.
