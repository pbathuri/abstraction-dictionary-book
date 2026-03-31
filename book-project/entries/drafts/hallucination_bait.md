---
headword: "hallucination bait"
slug: "hallucination_bait"
family: "failure_mode"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["grounding", "source anchoring", "verification loop", "confabulation", "vagueness", "specificity", "falsifiability"]
cross_links: ["grounding", "source anchoring", "verification loop", "specificity", "falsifiability", "rubric", "provenance tracking"]
tags: ["failure-mode", "reliability", "trust", "factual-integrity"]
has_note_box: true
note_box_type: "common_trap"
---

# hallucination bait

## One-Sentence Elevator Definition

Hallucination bait is any prompt structure that pressures a model to produce confident-sounding fabrications by demanding specifics it cannot verify.

## Expanded Definition

Language models do not know what they know. They lack a reliable internal signal for "I don't have enough information to answer this accurately." When a prompt demands specific details, names, numbers, citations, or dates and the model's training data does not contain a confident match, the model does not refuse. It generates. What it generates will be fluent, plausible, and wrong.

Hallucination bait is the name for prompt structures that trigger this failure mode. It is not the same as asking a hard question. A hard question has a correct answer that the model might or might not retrieve. Hallucination bait creates conditions where the model is more likely to fabricate than to flag uncertainty, usually because the prompt implicitly or explicitly penalizes refusal.

The most common form is the **specificity-without-source trap**: asking for specific factual details (a statistic, a quote, a citation, a date) without providing reference material and without giving the model permission to say "I don't know." The model, trained on helpfulness, complies. The output looks authoritative. It may be entirely invented.

Hallucination bait matters because it is often unintentional. The prompt writer does not mean to induce fabrication. They just want a precise answer. The mismatch between reasonable expectations and model behavior is the core danger.

## Why This Matters for LLM Prompting

Every prompt that asks for factual specifics without grounding material is a hallucination risk. The risk scales with how specific the request is and how far it falls outside the model's reliable knowledge. Asking "what is the capital of France?" is safe. Asking "what were the Q3 2025 revenue figures for Acme Corp?" without providing the data is not.

The fix is structural, not behavioral. You cannot reliably instruct a model to "only state facts" because the model cannot distinguish its factual recall from its confabulations. Instead, you must structure the prompt to provide the facts (→ grounding) or to include explicit escape hatches ("if you cannot verify this, say so").

## Why This Matters for Agentic Workflows

In agent systems, hallucination bait is amplified by → delegation. When a planner agent asks an executor agent to "find the three most recent studies on X," the executor may fabricate plausible paper titles, author names, and journal references. If the next agent in the pipeline trusts that output, the fabrication propagates. By the time it reaches the final output, the invented citation may be embedded in a confident-looking report.

Agent workflows require → verification loops and → provenance tracking specifically to catch this. The cheapest defense is to build "cite your source or mark the claim as unverified" into every agent's delegation instructions.

## What It Does to Model Behavior

When hallucination bait is present, models shift from retrieval-like behavior to generation-like behavior for factual content. Instead of surfacing information they were trained on with appropriate uncertainty, they construct plausible-sounding text that satisfies the format and specificity of the request. Studies on hallucination in LLMs show that asking for specific numbers, names, or citations when the model lacks confident access to them increases the rate of factual errors by a substantial margin compared to open-ended phrasing about the same topic [src_hallucination_001].

## When to Use It

This is a failure mode entry. You never want to use hallucination bait. But you need to recognize it when you've written it:

- When your prompt asks for specific data points you haven't provided
- When your prompt asks for citations without giving source material
- When your prompt penalizes "I don't know" responses (explicitly or implicitly)
- When your prompt uses phrases like "always provide" or "you must include" for factual claims
- When you chain multiple agents without verification steps between them

## When NOT to Use It

Situations where the failure mode label does not apply:

- When you have provided the source material and are asking the model to extract from it (this is → grounding, not hallucination bait)
- When the task is creative and factual accuracy is not a criterion
- When you have built in explicit verification or refusal mechanisms
- When you are testing hallucination resistance deliberately

## Strong Alternatives / Adjacent Abstractions / Contrast Set

| Term | Relationship | Key Difference |
|------|-------------|----------------|
| → grounding | remedy | Grounding provides source material; it is the primary defense against hallucination bait |
| → source anchoring | remedy | Source anchoring ties claims to specific documents |
| → verification loop | remedy | Verification loops catch hallucinations after generation |
| → confabulation | related failure | Confabulation is the model's behavior; hallucination bait is the prompt's contribution |
| → specificity | tension | Specificity improves outputs but becomes hallucination bait when applied to unsourced facts |
| → falsifiability | defense | Making claims falsifiable invites the model to flag uncertainty |
| → vagueness | contrast | Vague prompts produce generic outputs; hallucination bait produces specific but false ones |

## Failure Modes / Misuse Patterns

1. **The phantom citation.** "Cite three peer-reviewed studies that support this claim." If the model does not have confident access to real citations, it will generate plausible-sounding fake ones: real-looking author names, journal-like titles, and fabricated DOIs. This is the most dangerous form because the output looks verifiable.

2. **The mandatory-answer trap.** "You must provide a definitive answer. Do not say you are unsure." This instruction overrides the model's already-weak uncertainty signals and guarantees fabrication when knowledge is lacking.

3. **The specificity escalation.** Asking follow-up questions that demand increasing factual precision about a topic the model addressed broadly. Each escalation increases hallucination risk because the model has already committed to a general frame and will generate details to support it.

4. **The delegated assumption.** In agent workflows, an upstream agent asks a downstream agent for specific information and the downstream agent treats the request as an instruction to produce output, not to verify availability. The hallucination is invisible to both agents.

## Minimal Prompt Example

**Hallucination bait (bad):**
```
What are the exact parameter counts for GPT-4, Claude 3, and Gemini Ultra?
List each with the number of parameters and the training data size.
```

**Fixed:**
```
What are the publicly disclosed parameter counts for GPT-4, Claude 3, and Gemini Ultra?
If a model's parameter count has not been officially published, say
"not publicly disclosed" instead of estimating.
```

## Strong Prompt Example

```
You are a research assistant preparing a literature review.

Source material: [attached PDF of 12 papers on retrieval-augmented generation]

Task:
1. For each paper, extract: title, authors, year, and the primary finding
   relevant to hallucination reduction.
2. If a paper does not directly address hallucination, mark it as
   "tangential — not directly relevant" and move on.
3. Do NOT cite any paper that is not in the attached PDF.
   If you believe additional papers are relevant but they are not in the
   source material, list them under "Suggested additions (UNVERIFIED)"
   and mark each as unverified.
4. For each finding you extract, include the page number or section
   where you found it.

The goal is zero fabricated citations. If you are uncertain whether a
detail is in the source material, err on the side of omission.
```

## Agent Workflow Example

```
Agent: Fact Checker
Position: inserted after every Research Analyst handoff

Input: claims from Research Analyst with source_ids

For each claim:
1. Verify that the source_id exists in the source_cards corpus
2. Verify that the claim text is supported by the source content
3. Classify:
   - VERIFIED: claim matches source content
   - UNSUPPORTED: source exists but does not support this specific claim
   - MISSING_SOURCE: no source_id provided
   - FABRICATED_SOURCE: source_id does not exist in corpus

Output format:
{
  "claim_id": "",
  "claim_text": "",
  "source_id": "",
  "verification": "VERIFIED|UNSUPPORTED|MISSING_SOURCE|FABRICATED_SOURCE",
  "evidence_span": "quote from source, if VERIFIED",
  "note": ""
}

Escalation: If more than 20% of claims are UNSUPPORTED or FABRICATED_SOURCE,
flag the entire Research Analyst output for re-execution with
stricter grounding instructions.
```

## Model-Fit Note

All model tiers are susceptible to hallucination bait, but the patterns differ. Smaller open models hallucinate more frequently on factual recall tasks and are less responsive to "say I don't know" instructions. Frontier proprietary models hallucinate less often but with higher confidence, making their fabrications harder to detect. Reasoning-specialized models can be prompted to self-check, but this is not reliable without external verification. The most robust defense is architectural: provide source material and verify outputs, regardless of model tier.

## Evidence / Provenance Note

The mechanism of LLM hallucination is documented in survey papers on factual accuracy in language models [src_hallucination_001]. The relationship between prompt specificity and hallucination rate is discussed in Anthropic's research on model honesty and calibration [src_hallucination_002]. The phantom citation pattern is well-documented in library science and legal technology literature on AI-generated references [src_hallucination_003]. Architectural defenses (RAG, verification loops) are supported by retrieval-augmented generation research [src_hallucination_004, src_hallucination_005].

## Related Entries

- **→ grounding** — the primary antidote; provide what you want the model to reference
- **→ source anchoring** — a specific grounding technique that ties claims to documents
- **→ verification loop** — architectural defense against hallucination in agent workflows
- **→ confabulation** — the model-side behavior that hallucination bait triggers
- **→ falsifiability** — making claims checkable reduces hallucination acceptance
- **→ provenance tracking** — the bookkeeping system that catches fabricated sources
- **→ specificity** — a double-edged tool that can either prevent vagueness or induce hallucination

---

> **Common Trap**
>
> "Cite your sources" sounds like good practice. But if you ask a model to cite sources without providing any, you are not asking for citations. You are asking for fabricated citations that look like real ones. Always provide the source material or instruct the model to label any claim it cannot source as `[UNVERIFIED]`.
