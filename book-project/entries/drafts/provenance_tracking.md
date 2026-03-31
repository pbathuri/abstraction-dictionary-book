---
headword: "provenance tracking"
slug: "provenance_tracking"
family: "quality_control"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# provenance tracking

**Elevator definition**
Provenance tracking is the practice of recording where each claim, data point, or decision in a model's output originated — the bookkeeping that makes verification possible.

## What it is

A language model can tell you that "the global lithium market is expected to reach $8.2 billion by 2027." What it cannot do, by default, is tell you where that number came from. Did it emerge from a document in the context window? From training data absorbed during pre-training? From a plausible-sounding confabulation that matches the statistical shape of market projections? Without provenance tracking, the consumer of the output cannot tell, and neither can any downstream agent in the pipeline.

Provenance tracking solves this by requiring — through prompt design, structured output schemas, or agentic architecture — that every claim carries a record of its source. At minimum, this means source attribution: "Claim X comes from Document Y, paragraph Z." At full fidelity, it means a chain of custody: "Claim X was extracted by Agent A from Document Y at timestamp T, verified by Agent B against Source Z at timestamp T+1, and included in the final output by Agent C."

The concept is borrowed from data engineering and archival science, where provenance (also called lineage) describes the documented history of a data artifact from its point of origin through every transformation to its final form. In database systems, data lineage tools track which upstream tables contributed to a downstream report. In archives, provenance records who owned a document and when. In LLM systems, provenance tracking answers the same question: where did this come from, and how did it get here?

The need is acute because language models are the most persuasive unreliable narrators ever built. Their outputs read with the confidence and fluency of authoritative text regardless of whether the content is sourced, inferred, or fabricated. Provenance tracking breaks this symmetry. A claim with provenance can be checked. A claim without provenance is a liability.

Implementation ranges from lightweight to comprehensive. **Inline citation** is the simplest form: instruct the model to cite its sources in brackets after each claim, referencing documents provided in the context. This works for single-turn prompts and requires no infrastructure beyond the prompt itself. **Structured source fields** require the model to output each claim as a structured object with dedicated source fields — `{ "claim": "...", "source_id": "...", "source_span": "..." }` — making provenance machine-readable and verifiable. **Pipeline-level lineage** records provenance across multiple agents: which agent produced a claim, from what input, at what stage, validated by what criteria. This requires logging infrastructure but produces an auditable record of the entire system's reasoning.

The choice of implementation depends on the stakes. For an internal research summary read by one person, inline citations suffice. For a regulatory filing, legal brief, or medical recommendation, pipeline-level lineage is not optional — it is a compliance requirement.

## Why it matters in prompting

Without explicit provenance instructions, models will happily present sourced facts and fabricated facts in identical format. The reader cannot distinguish them. This is the fundamental asymmetry that provenance tracking addresses.

Adding provenance requirements to a prompt does three things. First, it forces the model to connect each claim to a source, which makes unsourced claims visible as gaps rather than invisible as assumptions. Second, it anchors the model's generation in the provided materials, reducing hallucination. A model instructed to "cite the source document for every factual claim" will generate fewer unsourced claims than one given no such instruction, because the citation requirement creates a self-check: if the model cannot cite a source, it must either omit the claim or acknowledge the gap. Third, it makes the output auditable — a human reviewer can spot-check any claim by following the citation back to its source.

## Why it matters in agentic workflows

In multi-agent pipelines, provenance tracking is how you prevent fabrication from becoming foundational. When Agent A produces a claim and Agent B builds on it, the absence of provenance means Agent B cannot distinguish between a sourced finding and a hallucination. If Agent B incorporates a fabricated claim and Agent C synthesizes it into a recommendation, the fabrication is now load-bearing — structurally embedded in the output with no visible trace of its illegitimate origin.

Pipeline-level provenance prevents this by tagging every claim with its origin. The → verification loop can then check not just whether a claim is plausible but whether it traces back to a real source. The → watchdog can flag claims whose provenance chains are broken or whose sources fall below trust thresholds.

## What it changes in model behavior

Explicit provenance requirements reduce hallucination rates by forcing the model to ground each claim in provided materials. Models instructed to cite sources produce fewer unsupported claims than unconstrained models, though the effect depends on the specificity of the instruction. "Cite your sources" is weaker than "For each claim, provide the document ID and the paragraph number where the supporting evidence appears."

## Use it when

- The output contains factual claims that a downstream consumer or agent will rely on
- The stakes of factual error are high (legal, medical, financial, regulatory)
- The pipeline has multiple stages and you need to trace claims back through the chain
- You are building a → verification loop and need machine-readable source references to verify against
- The output will be presented to humans who need to trust-but-verify

## Do not use it when

- The task is purely creative (fiction, brainstorming) where sourcing is irrelevant
- The output is a direct transformation of the input with no factual claims (reformatting, translation)
- The overhead of structured provenance exceeds the risk of the task (casual Q&A, internal brainstorming)

## Contrast set

- → **verification loop** — Verification checks whether claims are accurate. Provenance tracking records where claims came from. They are complementary: provenance provides the trail that verification follows.
- → **grounding** — Grounding anchors the model in provided materials. Provenance tracking records the link between output claims and those materials. Grounding is the act; provenance is the receipt.
- → **source anchoring** — Source anchoring is a prompting technique that instructs the model to stay close to source materials. Provenance tracking is the record-keeping that proves it did.
- → **rubric** — A rubric can include provenance requirements as evaluation criteria ("every claim must have a source citation"). Provenance tracking is what satisfies that criterion.

## Common failure modes

- **Citation theater** — The model produces citations that look correct but are fabricated. It cites "Document 3, paragraph 7" when Document 3 has only 4 paragraphs. Fix: use structured output with machine-checkable references (source IDs that can be programmatically validated) rather than free-text citations the model can invent.

- **Selective provenance** — The model cites sources for easy, obvious claims and quietly drops citations for uncertain or fabricated ones. The uncited claims are the dangerous ones, and they are invisible by design. Fix: require provenance for *every* factual claim and flag uncited claims explicitly: "If you cannot cite a source, write [NO SOURCE] and state the basis for the claim."

- **Provenance laundering** — In multi-agent pipelines, Agent A produces a weakly sourced claim. Agent B rewrites it. Agent C cites Agent B's output as the source. The claim now has provenance — pointing to Agent B — but the original source is lost. Fix: propagate original source IDs through the pipeline, not intermediate agent IDs.

## Prompt examples

### Minimal example

```text
Using only the attached report, answer the following question.

For every factual claim in your answer, cite the source in
brackets: [Report, Section X, p. Y]. If you cannot find a
source for a claim, write [NO SOURCE] instead.
```

### Strong example

```text
You are a research analyst producing a sourced briefing.

Source materials:
- [DOC-1] McKinsey Global Energy Report 2025
- [DOC-2] IEA World Energy Outlook 2025
- [DOC-3] Company 10-K Filing (FY2025)

For each paragraph in your briefing:
1. State the key finding in 1-2 sentences.
2. After each factual claim, cite the source as [DOC-X, p.Y]
   or [DOC-X, Section Y].
3. If a claim synthesizes multiple sources, cite all of them.
4. If a claim reflects your inference rather than a direct
   source statement, mark it [INFERENCE: based on DOC-X, DOC-Y].
5. Do not include any claim you cannot trace to at least one
   source document. If the question requires information not
   in these sources, state: "This question cannot be fully
   answered from the provided sources because [reason]."
```

### Agentic workflow example

```text
Pipeline: Sourced Market Analysis with Provenance Chain

Agent 1 — Extraction Agent
Input: Five source documents with unique IDs (SRC-001 to SRC-005)
Task: Extract every quantitative claim (market size, growth
rate, share figures). Output as JSON array:
[{
  "claim_id": "C-001",
  "claim_text": "...",
  "source_id": "SRC-003",
  "source_location": "Table 4, row 2",
  "extraction_confidence": "high | medium | low"
}]

Agent 2 — Verification Agent
Input: Claims array from Agent 1 + original source documents
Task: For each claim, verify that source_location exists and
supports the claim_text. Output:
[{
  "claim_id": "C-001",
  "verified": true | false,
  "evidence_span": "exact quote from source",
  "note": "optional discrepancy note"
}]

Agent 3 — Synthesis Agent
Input: Only verified claims (verified: true) with full
provenance chain intact
Task: Synthesize into a 500-word market overview. Every
sentence must cite at least one claim_id. Append a provenance
table mapping each claim_id to its source_id and verification
status.
```

## Model-fit note

All model tiers can produce inline citations when prompted, but accuracy varies sharply. Frontier models produce correct citations roughly 80–90% of the time when sources are clearly labeled in the context. Midsize models produce correct citations 60–75% of the time and occasionally fabricate plausible-looking source references. Small models produce unreliable citations and should have all source references programmatically validated. For any production system, treat model-generated citations as claims to be verified, not as facts.

## Evidence and provenance

The importance of source attribution in LLM outputs is discussed in the context of reducing hallucination across multiple surveys [src_paper_sahoo2025, src_paper_schulhoff2025]. Chain-of-Verification (Dhuliawala et al., 2023) treats source verification as an explicit step in model reasoning [src_paper_sahoo2025]. Data provenance as a concept originates in database lineage tracking (Buneman et al., 2001) and archival science. Its application to LLM pipelines is a practitioner convention that has become standard in production systems requiring auditability.

## Related entries

- **→ verification loop** — uses provenance records to check claim accuracy
- **→ grounding** — the practice of anchoring generation in sources; provenance records the anchors
- **→ source anchoring** — a prompting technique that provenance tracking documents
- **→ rubric** — provenance completeness as an evaluation criterion
