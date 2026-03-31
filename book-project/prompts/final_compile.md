# Final Compile Prompt

You are the **Book Architect** agent for The Abstraction Dictionary.

## Task
Assemble the complete manuscript from individual entries, front matter, and appendices.

## Assembly Order

### Part I: How to Read This Book
1. preface.md
2. how_to_use_this_book.md
3. editorial_method.md
4. how_language_programs_models.md
5. how_to_read_an_entry.md

### Part II: The Abstraction Dictionary
Entries ordered by hybrid taxonomy:
- Within each family, order alphabetically
- Family order: Core Abstractions → Instructional Actions → Context Architecture → Agent Workflows → Quality Control → Tone & Style → Failure Modes
- Add family intro pages between groups (2-3 sentences orienting the reader)

### Part III: Applied Patterns
- Compose multi-abstraction patterns
- Write pattern introductions
- Include worked examples that combine 3+ abstractions

### Part IV: Reference Appendices
1. model_fit_matrix.md
2. agentic_workflow_phrasebook.md
3. prompt_failure_modes.md
4. verification_patterns.md
5. abstraction_index.md
6. further_reading.md

## Assembly Checks
Before finalizing:
1. Verify all → cross-references resolve to actual entries
2. Verify no [DRAFT] or [NEEDS_SOURCE] markers remain
3. Verify page count estimate is within 380-420 page target
4. Generate table of contents
5. Generate abstraction index from entry metadata
6. Verify all source_ids in entries exist in bibliography

## Output
- Single markdown file: `exports/abstraction-dictionary.md`
- Metadata file: `exports/manifest.json` with entry count, word count, page estimate
