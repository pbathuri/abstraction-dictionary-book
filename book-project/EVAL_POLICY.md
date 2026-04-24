# EVAL POLICY - Entry Acceptance Criteria and Quality Gates

## Acceptance Rubric

A final entry is accepted ONLY if it passes ALL of the following:

### Content Quality
- [ ] **Original** - definition is written from scratch, not paraphrased from existing dictionaries
- [ ] **Operational** - the entry tells the reader how to DO something, not just what something IS
- [ ] **Example-rich** - at least one minimal example AND one advanced example
- [ ] **Dual application** - includes both prompting and agent-workflow application
- [ ] **Contrastive** - includes explicit comparison with adjacent abstractions
- [ ] **Pleasant to read** - a competent professional would not put this down in boredom

### Factual Integrity
- [ ] **No unsupported claims** - every technical claim maps to a source_id
- [ ] **No invented data** - no fabricated parameter counts, benchmark scores, or capabilities
- [ ] **Provenance metadata** - `.sources.json` file exists and is complete

### Style Compliance
- [ ] **Anti-slop check passed** - no banned phrases from STYLE_GUIDE.md
- [ ] **No repetitive cadence** - entry has rhythmic variety
- [ ] **Length within bounds** - total entry 1,200–2,500 words
- [ ] **No AI-writing tells** - passes humanizer anti-pattern scan

### Structural Integrity
- [ ] **Schema complete** - all 17 mandatory sections present (or justified omission for [OPTIONAL] sections)
- [ ] **Cross-links valid** - all → references point to existing or planned entries
- [ ] **Contrast set populated** - at least 3 rows in the comparison table
- [ ] **Failure modes present** - at least 2 concrete failure patterns

## Eval Pipeline

### Automated Checks (scripts/eval_entry.py)

1. **Schema completeness** - parse YAML front matter, verify all sections present
2. **Banned phrase scan** - check against STYLE_GUIDE.md banned patterns
3. **Length validation** - verify each section within target bounds
4. **Repetition score** - measure sentence-level similarity within the entry
5. **Citation count** - verify at least 2 source references per entry
6. **Cross-link integrity** - verify all → references resolve

### Agent-Assisted Checks

7. **Unsupported claim detection** - flag assertions without source backing
8. **Contrast quality** - verify the contrast set contains genuinely different terms
9. **Example quality** - verify examples are realistic and non-trivial
10. **Tonal consistency** - compare against pilot entries for voice drift

### Human Review Triggers

An entry is flagged for human review if:
- Automated checks score below 80% pass rate
- Any unsupported claim is detected
- The entry covers a contentious or rapidly-changing topic
- It is one of the first 10 entries (pilot set)

## Model Comparison Testing

Before scaled production, evaluate candidate models on:

| Test | Measures |
|------|----------|
| Structured output fidelity | Does the model produce all schema sections in correct format? |
| Citation/provenance adherence | Does the model invent sources or correctly tag [NEEDS_SOURCE]? |
| Contrast preservation | Does the model maintain meaningful differences between adjacent entries? |
| AI cliché density | How many banned patterns appear per 1000 words? |
| Instruction following | Does the model respect length bounds and formatting constraints? |

Results stored in `eval/model_comparison.md`.

## Scoring

Each entry receives an eval score:

```
schema_score    = (sections_present / sections_required) * 100
style_score     = 100 - (banned_phrases_count * 10) - (repetition_penalty)
citation_score  = min(100, citation_count * 20)
cross_link_score = (valid_links / total_links) * 100
overall_score   = (schema_score * 0.3) + (style_score * 0.3) + (citation_score * 0.2) + (cross_link_score * 0.2)
```

**Acceptance threshold:** overall_score >= 80 AND no unsupported claims AND schema_score == 100
