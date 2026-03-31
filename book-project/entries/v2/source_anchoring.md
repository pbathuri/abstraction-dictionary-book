# source anchoring

> Tying every model claim to a specific, quotable passage in a provided document — the citation mechanism that turns confident fiction into verifiable fact.

## The Scene

ResumeForge, the moment that almost killed the project. The model rewrote a resume bullet: "Led a cross-functional team of 15 in deploying a cloud migration that reduced infrastructure costs by 34%." Impressive. The source resume said: "Contributed to cloud migration project." No team size. No cost figure. No leadership claim. Every specific detail was fabricated — and formatted identically to the real content.

I added source anchoring: "For every claim in the rewrite, quote the specific passage from the source resume that supports it. If no passage supports a claim, do not make the claim — flag it as {gap: 'description'}." The model stopped inventing. Where the resume said "contributed to," the rewrite said "contributed to." Where there were no metrics, the output flagged the gap and suggested questions to ask the candidate. The model didn't become honest. It became *constrained to cite its sources*, and citation made fabrication structurally impossible.

## What This Actually Is

Models don't distinguish between what they know and what they invent. A model states "revenue grew 14% in Q3" with identical confidence whether the number comes from a provided document, from vaguely similar training data, or from thin air. Source anchoring forces the model to connect each claim to a specific, locatable passage. Not "based on the documents" in a hand-wavy sense — *this claim, from this passage, in this source*.

The technique exploits an asymmetry: models are mediocre at spontaneous factual recall but substantially better at extraction and attribution from provided text. Instead of asking "what do you know?" (unreliable), you ask "what does *this document* say, and where exactly?" (far more reliable). The failure mode shifts from fabrication to omission — and omission is easier to detect and fix.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Summarize the document" | "Summarize using only claims from the document. For each claim, quote the supporting passage in [brackets]" | Anchoring makes every claim checkable |
| "What are the key risks?" | "List risks found in the contract. For each, cite the exact clause: [Section X.X: 'exact quote...']" | Exact quotes prevent paraphrased fabrication |
| "Answer this question" | "Answer using ONLY the attached sources. If the answer isn't in the sources, say 'Not addressed in provided materials'" | Escape hatch prevents cornered fabrication |
| "Cite your sources" | "Quote the specific passage, do not paraphrase. Paraphrased citations cannot be verified" | Quote > paraphrase for auditability |
| "Be accurate" | "After your response, verify: does every factual claim trace to a specific passage? Flag any that don't as [UNVERIFIED]" | Self-check catches lazy anchoring |

## Before → After

**Before:**
```
Summarize the key findings from this audit report.
Be thorough and accurate.
```

**After:**
```
Summarize findings from the attached audit report.

Rules:
- Every finding must quote the exact supporting passage
  from the report: [Page X: "exact quote..."]
- Do NOT paraphrase the source — exact quotes only
- If a finding requires interpretation beyond what the
  text states, label it [INFERENCE] and explain your
  reasoning
- If the report does not address a topic, do not invent
  findings. Say: "The report does not address [topic]"
- Maximum 5 findings. Prioritize by severity.
```

## Try This Now

```
I'll give you a short paragraph of "source material."
Then I'll ask you a question about it.

Source: "Acme Corp reported Q3 revenue of $4.2M, a 12%
increase over Q2. Operating expenses rose to $3.8M due
to a new hire in engineering and expanded cloud costs.
Net income was $400K."

Question: What was Acme's profit margin, and how did
their staffing changes affect profitability?

Answer the question with source anchoring:
- Quote the exact passage supporting each claim
- For any calculation (like margin), show the math
  and cite the numbers used
- If the source doesn't contain enough info to fully
  answer, say what's missing

Then: find ONE claim you could plausibly make that
the source does NOT actually support. Show how easy
it would be to state it confidently without anchoring.
```

## When It Breaks

- **Anchor fabrication** — The model invents the anchor. It writes "According to paragraph 3..." and the quote doesn't appear in paragraph 3. This happens because the model generates plausible-sounding citations without locating the text. Fix: require exact verbatim quotes, not paraphrased references. Fabricated quotes are detectable; fabricated paraphrases are not.
- **Lazy anchoring** — Every claim cites the same source or the first source in the context, regardless of actual support. Fix: require per-claim anchoring with distinct passage references and add a verification step.
- **Anchoring without boundaries** — The model cites sources for some claims and silently generates others from parametric knowledge. The output is a seamless mix of anchored and unanchored claims. Fix: "If you cannot anchor a claim to the provided sources, do not make the claim."

## Quick Reference

- **Family:** Context architecture
- **Adjacent:** → grounding (the broader category; source anchoring is one specific form), → provenance tracking (the bookkeeping that records the anchoring trail), → retrieval scaffolding (organizes retrieved material so anchoring can reference it), → hallucination bait (the conditions that make anchoring most necessary)
- **Model fit:** Frontier models anchor accurately to specific passages and distinguish direct from inferential support. Midsize models anchor reliably with short, single documents but degrade across multiple long documents. Small models struggle with exact quoting — they paraphrase even when told to quote verbatim. For small models, use a two-pass approach: first extract relevant passages, then generate claims from only those passages.
