# reference

> A pointer to external material the model should treat as ground truth — overriding what it thinks it knows with what you know is right.

## The Scene

In Clap/OpsPilot's SHOT_1 architecture, the system prompt opens: "Read these files for grounding." Then it lists four specific files — the product north star, the control model, two source modules. Those files aren't suggestions. They're the reference corpus. Every claim the model makes should trace back to one of them.

Before I added labeled references, the model produced architectural advice drawn from its training data — generic LangGraph patterns, CrewAI conventions. Technically reasonable. None of it matched our codebase. After references with explicit labels ("[REF-1] product_north_star.md, [REF-2] control_model.md"), the model stopped freelancing. It described what was actually in those files, cited them by label, and said "not addressed in provided sources" when it couldn't find support.

The difference wasn't intelligence. It was material.

## What This Actually Is

A reference is a piece of context with normative authority — the model should not just know about it but *defer* to it over its own training data. Without explicit grounding instructions ("answer only from the provided documents"), the model blends your references with its parametric knowledge seamlessly. You get an output that looks sourced but is actually half-sourced, half-guessed. You can't tell which half is which.

References come in four flavors: document references (reports, specs, datasets), standard references (APA format, OWASP checklist), example references (few-shot patterns to emulate), and constraint references (style guides, boundary definitions).

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Here's some context" | "[REF-1] Q4 Earnings Call Transcript. Answer using ONLY this source" | Labels the reference and closes the door on training data |
| "You know this topic" | "Do not treat this as a cold start. Read these files for grounding: [file list]" | The Clap SHOT_1 pattern: explicit warm-start |
| "What does the research say?" | "Using only the 5 papers below, summarize findings on [topic]. Cite by [REF-X]" | Shuts down parametric supplementation |
| "Answer this question" | "Answer from REF-1 only. If REF-1 doesn't address this, say 'Not covered in provided source'" | Escape hatch prevents hallucination when source is silent |
| "Based on the documents" | "Every factual claim must cite [REF-X, Section Y]. No unsourced claims" | Forces per-claim attribution |

## Before → After

**Before:**
```
You are an expert in AI ethics. What are the key
principles our product should follow?
```

**After:**
```
Sources:
[REF-1] EU AI Act, Articles 9-15 (High-Risk Requirements)
[REF-2] NIST AI RMF 1.0, Govern and Map functions
[REF-3] Our internal AI Ethics Policy v2.1

Using ONLY these three sources, identify the 5 principles
most relevant to our recommendation engine.

Rules:
- Every principle must cite [REF-X, Section/Article Y]
- If two sources conflict, note both positions
- If a principle appears in our internal policy but not
  in the regulatory sources, flag it as INTERNAL_ONLY
- Do not supplement with your own knowledge of AI ethics
```

## Try This Now

```
I'm going to give you a factual question and a short
source document. Answer the question twice:

Round 1: Answer from memory (no source).
Round 2: Answer ONLY from the source below. If the
source doesn't cover it, say "not in source."

Source: "Our return policy allows returns within 30 days
of purchase. Items must be unused with original packaging.
Electronics have a 15-day return window. Gift cards are
non-refundable."

Question: Can I return a laptop I bought 20 days ago?

After both rounds, compare your answers. Where did
Round 1 add information the source doesn't contain?
That's the gap references close.
```

## When It Breaks

- **Ungrounded reference** — You provided a document but never said "use only this." The model treats it as optional context and freely supplements from training data. The output looks grounded but is a blend you can't audit.
- **Reference overload** — Too many documents dilute attention. The model cites the first and last, ignores the middle. Curate to what's directly relevant.
- **Stale reference** — An outdated document produces an outdated answer. Version and date all references. Add: "If the source is older than 12 months, flag potential staleness."

## Quick Reference

- **Family:** Core abstraction
- **Adjacent:** → grounding (the practice references enable), → source anchoring (binds claims to reference passages), → retrieval scaffolding (the architecture that delivers references), → context (broader — references are context with authority)
- **Model fit:** Frontier models follow "answer only from documents" reliably, cite accurately 80-90% of the time. Mid-tier models occasionally leak parametric knowledge despite instructions. Small models need structural enforcement — require JSON output with mandatory source fields, reject anything missing citations.
