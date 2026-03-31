# integrate

> Make separately produced pieces read like one mind wrote them — dissolve the seams.

## The Scene

Form8's pipeline fans out: a Market Scanner node, a Competitor Profiler node, a Gap Analyzer node, and a Strategy Writer node. Each produces excellent work in isolation. The first time I assembled their outputs into a single report, the result read like four strangers had written it on the same flight without talking. The Scanner called the metric "market penetration." The Profiler called it "market share." The Gap Analyzer assumed B2B context; the Strategy Writer assumed B2C.

I added a final Integration node. Its job: receive all four sections plus a terminology glossary and a style guide, then rewrite the assembled output as a single coherent document. Not new content. Same facts, same structure. But with aligned vocabulary, smooth transitions, and resolved assumptions. The report went from stapled pages to woven narrative.

## What This Actually Is

Integration is fusion, not assembly. Composition puts parts together with visible architecture — sections remain somewhat distinct. Integration dissolves boundaries so the reader can't tell where one source's contribution ends and another's begins. The emphasis is on structural and stylistic coherence: aligned terminology, smooth transitions, reconciled assumptions, unified voice.

It's one of the most demanding operations because the model must attend to content accuracy (don't lose information), structural coherence (logical flow), stylistic consistency (uniform voice and formality), and transitional fluency — all simultaneously.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Combine these sections" | "Integrate these four sections into a single report. The reader should not be able to tell they were written separately" | Sets the bar at invisible seams |
| "Put these together" | "Rewrite as unified prose. Resolve terminology differences using the glossary below. Ensure smooth logical transitions between every paragraph" | Names the specific integration work |
| "Merge the outputs" | "Integrate, prioritizing: (1) terminological consistency, (2) logical flow, (3) elimination of redundancy. If two sections make the same point, keep the version with stronger evidence" | Ranked integration priorities |
| "Make it flow" | "At every section boundary, write 1-2 sentences connecting the conclusion of the previous section to the opening of the next. The connection must be logical, not procedural" | Specific transition instruction |
| "Clean up the combined doc" | "Every key finding from every input must appear in the integrated output. If two inputs conflict, note the discrepancy explicitly — do not silently drop one" | Prevents information loss during integration |

## Before → After

From Form8 — the integration node that unifies pipeline outputs:

> **Before (concatenated)**
> ```
> ## Market Overview
> [Market Scanner output — uses "market penetration"]
>
> ## Competitor Profiles
> [Profiler output — uses "market share," assumes enterprise]
>
> ## Gap Analysis
> [Gap Analyzer output — assumes SMB context]
>
> ## Strategy
> [Writer output — mixes both contexts]
> ```
>
> **After (integrated)**
> ```
> INTEGRATION NODE:
> Inputs: four section outputs + terminology glossary + style guide
>
> Instructions:
> 1. Build a term-mapping table from the glossary. Replace all
>    variant terms with the standard term (e.g., "market share"
>    throughout, never "market penetration")
> 2. Resolve context assumptions: this report targets mid-market
>    B2B SaaS. Adjust any SMB or enterprise-specific claims to
>    this context, or flag them as out-of-scope
> 3. Rewrite as one continuous document. No "[Section by Agent X]"
>    headers. Organize by business question, not by source
> 4. Every quantitative finding from every section must survive.
>    If two sections cite different numbers for the same metric,
>    note both and the source
>
> Output: Single document, 1,000-1,500 words, reads as if written
> by one analyst in one sitting.
> ```
>
> **What changed:** The report stopped contradicting itself. "Market penetration" and "market share" collapsed into one term. B2B and B2C assumptions were resolved instead of coexisting in the same paragraph.

## Try This Now

Take two paragraphs from different sources on the same topic (two articles, two reports, two LLM outputs). Paste them with this prompt:

```
Integrate these two paragraphs into one. Requirements:
- If they use different terms for the same concept, pick one
- If they contradict each other, note the contradiction
- The result should read as one continuous thought
- Do not simply place them in sequence — rewrite as unified prose
```

Check: can you still tell where paragraph 1 ends and paragraph 2 begins? If yes, the integration failed.

## When It Breaks

- **Integration as concatenation** — The model places sections in sequence without weaving them. You get five paragraphs with abrupt transitions. Fix: explicitly instruct "do not simply place these in sequence — rewrite as a single cohesive narrative."
- **Information loss** — The model drops content from one source while resolving conflicts with another. Fix: require the model to account for all sources. "Every key finding must appear. If inputs conflict, note the discrepancy."
- **Forced coherence** — The model imposes a narrative that distorts the source material, smoothing contradictions into blandness. Fix: distinguish between stylistic integration (align voice) and content integration (preserve substance and tensions).

## Quick Reference

- **Family:** Instructional action
- **Adjacent:** → compose (assembles with visible architecture; integrate fuses invisibly), → narrative glue (the transitions that make integration feel seamless), → formality (consistency is a primary challenge when integrating across agents)
- **Model fit:** Among the most capability-demanding operations. GPT-4-class and Claude 3.5+ handle multi-source integration well with explicit instructions. Mid-range models handle two sources but degrade with three or more. For smaller models, integrate pairwise in sequence rather than all-at-once.
