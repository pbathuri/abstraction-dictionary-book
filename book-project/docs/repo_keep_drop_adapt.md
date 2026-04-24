# Repo Decision Table: Keep / Drop / Adapt / Reference

| Repo | Decision | Rationale |
|------|----------|-----------|
| **Scrapling** | **KEEP** | Mature scraping library; use as Python dependency for source acquisition. |
| **openai-agents-python** | **KEEP** | First-class multi-agent runtime aligned with orchestration requirements. |
| **autoresearch-macos** | **REFERENCE** | ML training loop; only `program.md`-style operating discipline is relevant. |
| **agency-agents** | **ADAPT** | Curate relevant agent personas; do not integrate repo wholesale. |
| **humanizer** | **KEEP/ADAPT** | Ship SKILL.md or equivalent prompts in editorial step. |
| **novelWriter** | **REFERENCE** | VCS-friendly file layout inspiration; novel-first model doesn't fit reference books directly. |
| **book-generator** | **KEEP/ADAPT** | Reuse compile and provider patterns for outline→artifacts pipeline. |
| **org-novelist** | **ADAPT/REFERENCE** | Best glossary/index model; Emacs dependency limits direct use. |
| **LLMToolCallingTester** | **KEEP** | Tool-call eval harness for pipeline CI. |
| **filerobot-image-editor** | **KEEP (conditional)** | Use only if building web UI for asset editing; otherwise ImageMagick suffices. |
| **ai-book-writer** | **REFERENCE** | Illustrates agent roles; code uses outdated AutoGen patterns. |

## Integration Priority

### Tier 1 - Core Dependencies (install and configure first)
1. openai-agents-python
2. Scrapling

### Tier 2 - Adapted Components (port patterns, not code)
3. humanizer (editorial prompts)
4. agency-agents (persona templates)
5. book-generator (compile scripts)

### Tier 3 - Reference Only (read, don't import)
6. autoresearch-macos
7. novelWriter
8. org-novelist
9. ai-book-writer

### Tier 4 - Conditional Use
10. filerobot-image-editor (if web UI needed)
11. LLMToolCallingTester (adapt for CI)
