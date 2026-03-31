# Tool Audit — External Repositories

> Audited: 2026-03-27
> Purpose: Evaluate each cloned repo for use in the Abstraction Dictionary authoring pipeline.

---

## A. Scrapling

| Field | Detail |
|-------|--------|
| **URL** | https://github.com/D4Vinci/Scrapling |
| **Description** | Python web-scraping framework with adaptive parsing, stealth fetchers, and spider layer for crawls with proxy rotation. |
| **Stack** | Python 3.10+, lxml, optional Playwright/Patchright/curl_cffi |
| **Maturity** | Active / production-oriented (PyPI, CI, extensive docs) |
| **Usable components** | `Fetcher`, `StealthyFetcher`, `DynamicFetcher`, `Spider` API, CLI |
| **Patterns to borrow** | Adaptive CSS selection; separation of fetch vs parse; optional heavy deps behind extras |
| **Skip** | Sponsored proxy pitches; full spider stack if single-URL fetch suffices; MCP server |
| **Decision** | **KEEP** — Use as dependency for source acquisition |

---

## B. openai-agents-python

| Field | Detail |
|-------|--------|
| **URL** | https://github.com/openai/openai-agents-python |
| **Description** | Official OpenAI Agents SDK: agents with tools, handoffs, guardrails, sessions, tracing. Provider-agnostic with optional LiteLLM. |
| **Stack** | Python 3.10+, openai, pydantic, mcp |
| **Maturity** | Active / production (maintained by OpenAI, versioned 0.13.x) |
| **Usable components** | `Agent`, `Runner`, tools, handoffs, guardrails, tracing |
| **Patterns to borrow** | Handoffs for subagents; guardrails; tracing for debugging long pipelines; sessions for multi-step loops |
| **Skip** | Lock-in assumptions if using non-OpenAI endpoints |
| **Decision** | **KEEP** — Primary orchestration runtime |

---

## C. autoresearch-macos

| Field | Detail |
|-------|--------|
| **URL** | https://github.com/miolini/autoresearch-macos |
| **Description** | Minimal autonomous LLM training research loop (Karpathy fork): fixed prepare.py, agent-editable train.py, human/agent-editable program.md, 5-minute runs, results.tsv logging. |
| **Stack** | Python, PyTorch, uv |
| **Maturity** | Active niche / reference |
| **Usable components** | `program.md` discipline only |
| **Patterns to borrow** | Single-writable-artifact for agents; time-bounded runs; TSV experiment logs; read-only harness / editable strategy file split |
| **Skip** | Entire ML training stack |
| **Decision** | **REFERENCE** — Pattern library for agent operating procedures |

---

## D. agency-agents

| Field | Detail |
|-------|--------|
| **URL** | https://github.com/pbathuri/agency-agents |
| **Description** | Large collection of markdown-defined agent personas (engineering, design, marketing) with conversion scripts for Cursor, Claude, Aider, Windsurf. |
| **Stack** | Markdown, Bash |
| **Maturity** | Active community content |
| **Usable components** | Persona markdown templates; convert.sh for multiple platforms |
| **Patterns to borrow** | Specialist roster + "when to use" tables; consistent structure (identity, deliverables, metrics) |
| **Skip** | Treating every persona as production-vetted without review |
| **Decision** | **ADAPT** — Curate relevant personas for book pipeline agents |

---

## E. humanizer

| Field | Detail |
|-------|--------|
| **URL** | https://github.com/blader/humanizer |
| **Description** | Claude Code skill (SKILL.md) that rewrites text to remove AI writing tells, based on Wikipedia's signs-of-AI-writing list, with second-pass audit. |
| **Stack** | Markdown skill only |
| **Maturity** | Stable artifact (v2.3.0) |
| **Usable components** | SKILL.md as editorial checklist; anti-pattern tables |
| **Patterns to borrow** | Numbered anti-patterns (significance inflation, em dash overuse, rule of three); before/after discipline; "add soul" beyond mechanical cleanup |
| **Skip** | No CLI or API exists in-repo |
| **Decision** | **KEEP** — Use as editorial skill content; port prompts to pipeline |

---

## F. novelWriter

| Field | Detail |
|-------|--------|
| **URL** | https://github.com/vkbo/novelWriter |
| **Description** | Desktop novel writing app (Python + Qt6): project tree, plain-text documents, minimal markup, synopsis/comments, indexing. Designed for version control. |
| **Stack** | Python, PyQt6, PDM |
| **Maturity** | Production (multi-OS CI, translations, active maintenance, GPLv3) |
| **Usable components** | Authoring UI; specimen of on-disk project layout |
| **Patterns to borrow** | Small files per scene/chapter; index built from project; VCS-first storage philosophy |
| **Skip** | GPL license implications; fiction-first assumptions |
| **Decision** | **REFERENCE** — Borrow file organization discipline; optional as human editor |

---

## G. book-generator

| Field | Detail |
|-------|--------|
| **URL** | https://github.com/wesleyscholl/book-generator |
| **Description** | Shell-driven end-to-end pipeline: topic/outline, multi-provider AI helpers, chapter handling, plagiarism/LanguageTool hooks, compile to EPUB/PDF/MOBI/HTML/Markdown via Pandoc/TeX. |
| **Stack** | Bash, Python, Pandoc, LaTeX, ImageMagick |
| **Maturity** | Active / pragmatic production (author has KDP-published books from this toolkit) |
| **Usable components** | Compile pipeline, provider wrapper patterns, appendices generator, manuscript versioning |
| **Patterns to borrow** | Env-based provider selection; versioned manuscript; single book directory as source of truth |
| **Skip** | KDP/market-scraping pieces; tight Bash coupling |
| **Decision** | **KEEP/ADAPT** — Fork compile scripts for our export pipeline |

---

## H. org-novelist

| Field | Detail |
|-------|--------|
| **URL** | https://github.com/sympodius/org-novelist |
| **Description** | Emacs Lisp package for novel writing in Org mode: project tree, character/place/prop notes, glossary/index generators, cross-references, export templates. |
| **Stack** | Emacs Lisp, Org mode, Pandoc |
| **Maturity** | Active |
| **Usable components** | Glossary/index generation patterns; Org linking model |
| **Patterns to borrow** | Per-story folder; indices subfolder; glossary sections; automatic reference updating |
| **Skip** | Emacs dependency if team refuses it; fiction naming |
| **Decision** | **ADAPT/REFERENCE** — Best cross-reference model among candidates |

---

## I. LLMToolCallingTester

| Field | Detail |
|-------|--------|
| **URL** | https://github.com/adamwlarson/LLMToolCallingTester |
| **Description** | CLI harness for conversational tool-calling scenarios against OpenAI-compatible APIs. Scores precision/recall/F1, structural parameter accuracy. |
| **Stack** | Python 3, openai client, requests |
| **Maturity** | Prototype / useful internal tool |
| **Usable components** | Regression suite for tool surface; capability probing |
| **Patterns to borrow** | Capability probe before tests; emulated tool calls; weighted complexity score |
| **Skip** | Treating aggregate score as prose quality metric |
| **Decision** | **KEEP** — Fork/adapt for pipeline CI |

---

## J. filerobot-image-editor

| Field | Detail |
|-------|--------|
| **URL** | https://github.com/adamwlarson/filerobot-image-editor |
| **Description** | Web image editor (React + Konva): crop, resize, filters, annotate, watermark, history, export. Vanilla JS bridge available. |
| **Stack** | TypeScript/JavaScript, React 17+, monorepo |
| **Maturity** | Production (npm package, wide usage) |
| **Usable components** | Embed in web app for cover/figure touch-up |
| **Patterns to borrow** | Operation history; export pipeline; React vs vanilla bridge |
| **Skip** | Heavy React deps if only needing server-side ImageMagick |
| **Decision** | **KEEP** — Use if building web UI for asset editing |

---

## K. ai-book-writer

| Field | Detail |
|-------|--------|
| **URL** | https://github.com/adamwlarson/ai-book-writer |
| **Description** | AutoGen 0.2 multi-agent book generator: story_planner, outline_creator, memory_keeper, writer, editor via GroupChat round-robin. |
| **Stack** | Python, autogen |
| **Maturity** | Prototype / sample (README inconsistencies, thin tests, API drift risk) |
| **Usable components** | Patterns and prompt shapes; role separation; outline-as-context injection |
| **Patterns to borrow** | Explicit agent roles; outline in system messages; capped editor-writer iterations |
| **Skip** | Running as-is; AutoGen API is outdated |
| **Decision** | **REFERENCE** — Lift prompts/structure into openai-agents orchestration |

---

## Organizational Model Recommendation

**novelWriter vs org-novelist** for a version-control-friendly, cross-reference-heavy, modular reference book:

| Dimension | novelWriter | org-novelist |
|-----------|-------------|--------------|
| Plain-text / Git | Strong: VCS-first design | Strong: Org files, divide-and-conquer |
| Cross-references | Story-centric tags; narrative index | Glossary/index generators; Org links |
| Modular reference fit | Optimized for novels | Built-in glossary/index maps to reference tomes |
| Tooling lock-in | Qt desktop app (GPLv3) | Emacs + Elisp |

**Decision:** Use **Markdown + Pandoc** as the primary organizational model (no Emacs dependency, maximum portability, Git-native). Borrow novelWriter's file-per-entry granularity and org-novelist's glossary/index generation patterns. Implement our own cross-reference and index pass in `scripts/compile_book.py`.
