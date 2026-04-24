# program.md - Operating Doctrine

> This file is the evolving operating doctrine for the Abstraction Dictionary authoring system.
> Inspired by autoresearch-macos: keep it narrow, keep it editable, run tight loops.

## Current Phase

**Phase 1: Foundation & Pilot**

## Active Objectives

1. Establish taxonomy of 500–900 candidate abstractions
2. Select 75 flagship headwords
3. Write 10 gold-standard pilot entries
4. Evaluate pilots for quality, consistency, citation sufficiency
5. Lock ENTRY_SCHEMA.md and STYLE_GUIDE.md
6. Prepare scaled production plan

## Operating Rules

- Never mass-generate content. Every entry goes through the full pipeline.
- Every technical claim must have provenance before an entry reaches `final/`.
- The humanizer pass touches narrative prose only, never definitions or citations.
- All runs are logged. All outputs are versioned by stage (draft → reviewed → final).
- If a pipeline step fails, log the failure mode and fix the step before retrying.
- Entry schema and style guide are locked after pilot evaluation. Changes require explicit justification logged here.

## Run Log

| Date | Action | Result | Notes |
|------|--------|--------|-------|
| 2026-03-27 | Project initialization | Complete | Repo structure, external clones, audit docs |
| 2026-03-27 | Tool audit | Complete | 11 repos audited, roles assigned |
| 2026-03-27 | Foundation docs | In progress | Schema, style guide, bible, prompts |

## Known Issues

- None yet. First pipeline run pending.

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-27 | Use Markdown + Pandoc as primary org model | Max portability, Git-native, no Emacs dependency |
| 2026-03-27 | openai-agents-python as orchestration runtime | Official SDK, handoffs, tracing, guardrails |
| 2026-03-27 | Scrapling for source acquisition | Mature, adaptive parsing, Python-native |
| 2026-03-27 | novelWriter org model: REFERENCE only | Fiction-first; borrow file granularity pattern |
