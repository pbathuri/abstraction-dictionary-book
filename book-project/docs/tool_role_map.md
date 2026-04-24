# Tool Role Map - Pipeline Stage Assignments

> Each pipeline stage maps to one or more external repos for tooling, patterns, or reference.

| Pipeline Stage | Primary Repo | Role | Integration Type |
|---|---|---|---|
| **Source Acquisition** | Scrapling | Fetch and parse web sources | Python dependency |
| **Agent Orchestration** | openai-agents-python | Multi-agent runtime with handoffs, tools, tracing | Python dependency |
| **Operating Procedure** | autoresearch-macos | `program.md` loop discipline, TSV logging | Pattern only |
| **Agent Personas** | agency-agents | Curated specialist prompts for pipeline agents | Adapted markdown |
| **Editorial De-AI Pass** | humanizer | Post-draft narrative cleanup skill | Skill/prompt content |
| **File Organization** | novelWriter | VCS-friendly per-entry file structure | Pattern only |
| **Cross-reference Model** | org-novelist | Glossary/index generation patterns | Pattern only |
| **Compile & Export** | book-generator | Markdown → EPUB/PDF via Pandoc/LaTeX | Forked scripts |
| **Tool-Call QA** | LLMToolCallingTester | Model/tool regression testing | Forked harness |
| **Asset Editing** | filerobot-image-editor | Cover/figure touch-up in browser | Optional web UI |
| **Architecture Reference** | ai-book-writer | Planner/writer/editor separation patterns | Pattern only |

## Agent Pipeline (built on openai-agents-python)

```
Corpus Planner → Source Scout → Source Auditor
                                      ↓
                              Taxonomist → Lexicographer
                                                ↓
                              Prompt Engineer ← Agentic Workflow Analyst
                                      ↓
                              Example Crafter → Technical Annotator
                                      ↓
                     Counterexample Editor → Consistency Editor
                                      ↓
                     Humanizer Pass Editor → Citation/Provenance Checker
                                      ↓
                              Book Architect → Export Manager
```

## Data Flow

```
Web Sources (Scrapling)
    → /corpus/raw/
    → /corpus/normalized/
    → /corpus/source_cards/

Source Cards + Taxonomy
    → /taxonomy/abstractions.json
    → /taxonomy/relations.json

Entry Packets
    → /entries/drafts/<slug>.md

Reviewed Entries
    → /entries/reviewed/<slug>.md

Final Entries + Provenance
    → /entries/final/<slug>.md
    → /entries/final/<slug>.sources.json
    → /entries/final/<slug>.eval.json

Compiled Book
    → /exports/abstraction-dictionary.md
    → /exports/abstraction-dictionary.epub
    → /exports/abstraction-dictionary.pdf
```
