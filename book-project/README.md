# Authoring workspace (`book-project/`)

Pipeline code, prompts, and governance docs for producing a manuscript. **Manuscript content, corpus, taxonomy outputs, art, and exports are intentionally not tracked** in the parent Git repository-see the [root README](../README.md).

## Layout (conceptual)

- `scripts/` - collect, audit, taxonomy, packets, eval, compile, experiments  
- `prompts/` - stage templates  
- `docs/` - tool audits and integration notes  
- `AGENTS.md`, `program.md` - operating model for the pipeline  
- `ENTRY_SCHEMA.md`, `SOURCE_POLICY.md`, `EVAL_POLICY.md`, `ROADMAP.md` - structural and quality rules  

Ignored locally-populated dirs: `entries/`, `front_matter/`, `appendices/`, `corpus/`, `exports/`, `art/`, `eval/`, `taxonomy/`, `style/`, plus `external/`.
