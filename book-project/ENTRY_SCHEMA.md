# ENTRY SCHEMA - Mandatory Structure for Every Entry

> Version: 1.0-pilot
> Status: UNLOCKED (will be locked after pilot evaluation)

Every final entry in The Abstraction Dictionary must contain all of the following sections. Sections marked [OPTIONAL] may be omitted for entries where they are genuinely inapplicable, but omission must be justified.

---

## Entry Metadata (YAML front matter)

```yaml
---
headword: ""
slug: ""
family: ""  # core_abstraction | instructional_action | context_architecture | agent_workflow | quality_control | tone_style | failure_mode
status: ""  # draft | reviewed | final
version: 1
created: ""
last_modified: ""
author_agent: ""
reviewer_agent: ""
related_entries: []
cross_links: []
tags: []
has_note_box: false
note_box_type: ""  # which_word | workflow_note | model_note | common_trap | upgrade_prompt | fun_aside
---
```

## 1. Headword

The primary term. Lowercase unless it is a proper noun. If the abstraction has multiple valid names, list alternatives in section 9.

## 2. One-Sentence Elevator Definition

A single sentence that a competent reader can absorb in under five seconds. Must be precise enough to distinguish this abstraction from its neighbors.

**Constraint:** Maximum 30 words.

## 3. Expanded Definition

Two to four paragraphs that unpack the abstraction fully. Must cover:
- What the abstraction means in the context of language-as-programming
- How it differs from ordinary usage of the same word (if applicable)
- Its scope and boundaries

**Constraint:** 150–400 words.

## 4. Why This Matters for LLM Prompting

One to two paragraphs explaining the operational relevance when constructing prompts for language models.

## 5. Why This Matters for Agentic Workflows

One to two paragraphs explaining relevance for multi-agent systems, delegation, tool use, and orchestrated workflows.

## 6. What It Does to Model Behavior

A concise, evidence-informed explanation of how deploying this abstraction in a prompt or instruction changes what the model produces. No invented claims.

## 7. When to Use It

Bullet list of situations, task types, or contexts where this abstraction is the right tool.

## 8. When NOT to Use It

Bullet list of situations where this abstraction is counterproductive, redundant, or harmful to output quality.

## 9. Strong Alternatives / Adjacent Abstractions / Contrast Set

A structured comparison with related terms. Format:

| Term | Relationship | Key Difference |
|------|-------------|----------------|
| ... | synonym / parent / child / contrast / overlaps | ... |

## 10. Failure Modes / Misuse Patterns

Two to four concrete ways this abstraction can go wrong when applied poorly, with brief explanations of why each fails.

## 11. Minimal Prompt Example

A short, realistic prompt (3–8 lines) that demonstrates basic correct use of this abstraction.

**Format:**
```
[ROLE/CONTEXT if needed]
[PROMPT using the abstraction]
```

## 12. Strong Prompt Example

A more sophisticated prompt (8–20 lines) demonstrating expert use, ideally combining this abstraction with one or two related ones.

## 13. Agent Workflow Example

A realistic multi-step agent instruction or workflow fragment (8–20 lines) showing how this abstraction appears in delegation, handoff, or orchestrated agent behavior.

## 14. Model-Fit Note

Which model tiers or capabilities this abstraction benefits most from. Must follow the Model-Fit Note Policy in BOOK_BIBLE.md.

**Allowed tier labels:** small open model, midsize open model, large open model, frontier proprietary model, reasoning-specialized model, code-specialized model

## 15. Evidence / Provenance Note

Brief description of the evidence base for claims made in this entry. Must reference specific source_ids from the corresponding `.sources.json` file.

## 16. Related Entries

Ordered list of 3–8 related headwords from the dictionary, with one-line descriptions of the relationship.

## 17. Cross-Links

Inline cross-references used throughout the entry text. Format: `→ headword` for forward references.

## 18. Note Box [OPTIONAL]

One of the following types, used sparingly (see BOOK_BIBLE.md note box policy):

### Which Word?
Clarifies a common confusion between this abstraction and a similar one.

### Workflow Note
A practical tip for incorporating this abstraction into a real workflow.

### Model Note
A specific behavioral observation tied to a model tier.

### Common Trap
A frequently encountered mistake when using this abstraction.

### Upgrade This Prompt
A before/after showing how adding this abstraction improves a weak prompt.

### Fun Aside
A brief, lightly witty observation. Maximum 50 words. Use very sparingly.

---

## File Naming Convention

- Draft: `entries/drafts/{slug}.md`
- Reviewed: `entries/reviewed/{slug}.md`
- Final: `entries/final/{slug}.md`
- Sources: `entries/final/{slug}.sources.json`
- Eval: `entries/final/{slug}.eval.json`

## Provenance File Schema (.sources.json)

```json
{
  "headword": "",
  "sources": [
    {
      "claim_id": "c001",
      "source_id": "src_001",
      "claim_text": "",
      "quote_or_evidence_span": "",
      "confidence": "high|medium|low",
      "last_verified_at": "2026-03-27"
    }
  ]
}
```

## Eval File Schema (.eval.json)

```json
{
  "headword": "",
  "eval_date": "",
  "schema_complete": true,
  "banned_phrases_found": [],
  "unsupported_claims": [],
  "repetition_score": 0.0,
  "citation_count": 0,
  "cross_link_integrity": true,
  "readability_score": 0.0,
  "acceptance": "accepted|needs_revision|rejected",
  "notes": ""
}
```
