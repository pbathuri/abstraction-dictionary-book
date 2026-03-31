# provenance tracking

> Every claim needs a receipt. "Where did this come from?" is the question that separates useful output from expensive guessing.

## The Scene

Form8's strategy briefs cited market data — growth rates, market sizes, competitor revenue figures. They read with authority. The problem: I couldn't tell which numbers came from the search results in the pipeline and which the model invented. A brief claimed "Competitor X's ARR is $45M." Was that extracted from a source in the pipeline? Inferred from partial data? Fabricated from the statistical shape of market projections? Without provenance, all three look identical in the output.

I added provenance requirements to every extraction node. Each claim now carries a source tag: `[SRC-003, Table 2]` or `[INFERENCE: based on SRC-001 revenue + SRC-004 growth rate]` or `[NO SOURCE]`. The strategy writer receives only claims with valid source tags. Claims tagged `[NO SOURCE]` get routed to a human verification queue instead of the final brief. The output still cites market data. Now I can check every number.

## What This Actually Is

Provenance tracking records where each claim, data point, or decision in a model's output originated. At minimum: "Claim X comes from Document Y, paragraph Z." At full fidelity: a chain of custody — "Claim X was extracted by Agent A from Document Y, verified by Agent B, and included in the output by Agent C."

The need is acute because language models are the most persuasive unreliable narrators ever built. Their outputs read with identical confidence whether the content is sourced, inferred, or fabricated. Provenance breaks this symmetry. A claim with provenance can be checked. A claim without provenance is a liability.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Cite your sources" | "For each factual claim, cite as [DOC-X, p.Y] or [DOC-X, Section Y]. If a claim synthesizes multiple sources, cite all. If a claim is your inference, mark it [INFERENCE: based on DOC-X, DOC-Y]" | Distinguishes sourced, multi-sourced, and inferred claims |
| Trusting model citations at face value | "Output claims as structured objects: { claim, source_id, source_location, confidence }. Source IDs must match provided document IDs — do not invent references" | Machine-checkable provenance prevents citation theater |
| "Include references" | "If you cannot cite a source for a factual claim, write [NO SOURCE] and state the basis for the claim. Do not omit the claim silently" | Makes unsourced claims visible instead of invisible |
| No provenance in pipeline handoffs | "Each claim carries its original source_id through the entire pipeline. Intermediate agents may add verification status but must not replace the original source with their own agent ID" | Prevents provenance laundering across agent hops |
| A claim that "the market grew 12%" with no trail | "{ claim: 'market grew 12%', source_id: 'SRC-002', source_location: 'Table 4, row 3', extraction_confidence: 'high', verified_by: 'Agent B', evidence_span: 'Annual growth rate: 12.1%' }" | Full chain of custody from source to output |

## Before → After

From Form8 — adding provenance to the extraction pipeline:

> **Before (no provenance)**
> ```
> Extract key market data from the search results.
> Include market size, growth rate, and competitor revenue.
> ```
> (Output: "The SaaS CRM market is $45B growing at 12% CAGR."
> Source: unknown. Could be real. Could be fabricated.)
>
> **After (structured provenance)**
> ```
> EXTRACTION NODE:
> Source documents are labeled SRC-001 through SRC-005.
>
> For every quantitative claim, output as:
> {
>   "claim_id": "C-001",
>   "claim_text": "SaaS CRM market valued at $45B",
>   "source_id": "SRC-003",
>   "source_location": "Executive Summary, paragraph 2",
>   "exact_quote": "The global SaaS CRM market reached $44.8B
>     in 2025",
>   "extraction_confidence": "high"
> }
>
> Rules:
> - Every claim MUST have a source_id matching a provided doc
> - If you infer a number (e.g., calculating growth rate from
>   two data points), mark confidence as "inferred" and cite
>   both source data points
> - If you cannot source a claim, output with source_id: null
>   and it will be routed to human review — do NOT fabricate
>   a source reference
>
> VERIFICATION NODE (downstream):
> Input: claims array + original source documents
> Task: for each claim, verify source_location exists and
> supports claim_text. Mark as VERIFIED or FAILED.
> ```
>
> **What changed:** Every number in the strategy brief traces to a specific document and location. The verification node catches the 10-15% of claims where the model's extraction was subtly wrong (e.g., confusing Q3 figures for annual figures). Fabricated claims never reach the final output because they hit the null-source filter.

## Try This Now

Take any factual output from a model — a research summary, an analysis, a briefing. Paste it back:

```
For each factual claim in this text:
1. Can you trace it to a specific source I provided? (cite it)
2. Is it an inference from multiple sources? (cite all)
3. Is it from your training data with no specific source?
   (mark [TRAINING DATA])
4. Did you construct it to fit the narrative?
   (mark [CONSTRUCTED])

Be honest. I'd rather know a claim is unsourced than
trust one that seems sourced but isn't.
```

The ratio of [TRAINING DATA] and [CONSTRUCTED] to properly sourced claims tells you how much of the output is actually grounded.

## When It Breaks

- **Citation theater** — The model produces citations that look correct but are fabricated. It cites "Document 3, paragraph 7" when Document 3 has 4 paragraphs. Fix: use structured output with machine-checkable references, not free-text citations the model can invent.
- **Selective provenance** — Sources for easy claims, silent omission for uncertain ones. The uncited claims are the dangerous ones. Fix: require provenance for *every* claim and mandate `[NO SOURCE]` for unsourced ones — visible absence beats invisible absence.
- **Provenance laundering** — In pipelines, Agent A produces a weak claim, Agent B rewrites it, Agent C cites Agent B as the source. The claim now has provenance pointing to an intermediate agent, not the original source. Fix: propagate original source IDs through the pipeline.

## Quick Reference

- **Family:** Quality control
- **Adjacent:** → verification loop (uses provenance records to check claims), → grounding (the practice of anchoring in sources; provenance is the receipt), → justify (provenance supports justification by showing where evidence came from)
- **Model fit:** All tiers can produce inline citations when prompted, but accuracy varies. Frontier models cite correctly ~80-90% of the time with clearly labeled sources. Midsize models ~60-75%, with occasional fabricated references. Small models produce unreliable citations — always validate programmatically. For any production system, treat model-generated citations as claims to be verified, not facts.
