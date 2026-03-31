---
headword: "verification loop"
slug: "verification_loop"
family: "agent_workflow"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["rubric", "self-consistency", "falsifiability", "hallucination bait", "delegation", "decomposition", "escalation"]
cross_links: ["rubric", "self-consistency", "falsifiability", "hallucination bait", "delegation", "decomposition", "escalation", "constrain", "provenance tracking", "audit trail"]
tags: ["agent-workflow", "quality-control", "reliability", "self-criticism", "verification"]
has_note_box: true
note_box_type: "model_note"
---

# verification loop

**Elevator definition**
A verification loop is a structured cycle in which a model or agent checks its own output against explicit criteria before passing it downstream.

## What it is

The deepest flaw in single-pass generation is not that the model gets things wrong. It is that the model does not know when it has gotten things wrong. A language model that produces a plausible-sounding error has no alarm bell, no blinking red light, no internal exception handler that throws before the bad output ships. Verification loops exist to build that alarm bell externally.

A verification loop is a control structure — borrowed from software engineering's test-and-check patterns and transplanted into the world of natural language pipelines. It works like this: the model generates an output, then either the same model or a separate agent reviews that output against a set of criteria, then the output is either accepted, revised, or escalated. The simplest form is a self-critique instruction bolted onto the end of a prompt: "Before returning your response, check that every claim cites a source from the attached document." The most sophisticated form is a multi-agent architecture where a dedicated Verifier agent sits downstream of every Producer agent, applying a → rubric before anything passes forward.

The technique has deep roots in the prompting literature. Wang et al. (2022) introduced *self-consistency*, a decoding strategy that generates multiple reasoning chains for the same prompt and selects the most frequent answer by marginalizing across paths [src_paper_sahoo2025]. On the GSM8K math benchmark, self-consistency improved accuracy by 17.9% over standard chain-of-thought prompting. The improvement did not come from a better model or a better prompt. It came from running the same prompt multiple times and *voting*. That is verification at its most mechanical, and it works.

Madaan et al. (2023) went further with Self-Refine, a three-step loop: generate, critique, revise. The model produces an initial output, then prompts itself to identify weaknesses, then revises based on its own feedback. This cycle repeats until a stopping criterion is met. Self-Refine improved GPT-4 performance by 8.7 points in code optimization, 13.9 points in code readability, and 21.6 points in sentiment reversal [src_paper_sahoo2025]. The numbers are large because the technique addresses a real gap: models are substantially better at *critiquing* an output than they are at producing a correct one on the first attempt.

Chain-of-Verification (CoVe), introduced by Dhuliawala et al. (2023), targets hallucination directly. After generating a response, the model generates verification questions about its own claims, answers those questions independently (to avoid confirmation bias from the original context), and revises any claims that fail the check [src_paper_sahoo2025]. The method treats the model's output not as a finished product but as a draft to be cross-examined.

The pattern across these techniques is consistent: a single pass through a model is a *first draft*, and treating it as a finished product is a design error.

## Why it matters in prompting

In single-turn prompting, a verification loop is easy to add and hard to overvalue. The simplest version is an instruction at the end of the prompt:

"Before returning your answer, verify: (1) every statistic cites a source from the attached data, (2) no two recommendations contradict each other, (3) the total word count is under 300."

This costs a few extra tokens and buys significantly more reliable output. The model does not always catch its own errors — self-verification is not infallible — but it catches enough of them to shift the expected quality upward. For tasks where accuracy matters more than speed, adding a verification step is the single cheapest quality improvement available.

The technique is especially potent when the verification criteria are concrete and checkable. "Make sure this is good" is not a verification loop; it is a vague plea. "Make sure every row in the output table has exactly four columns, every date is in ISO format, and no value exceeds 100" is a verification loop with teeth.

## Why it matters in agentic workflows

In multi-agent pipelines, verification loops are structural. They sit between agents like quality gates in a factory. Without them, errors propagate — an upstream agent's fabrication becomes a downstream agent's premise, and by the final output the original error is load-bearing.

The architecture is straightforward: for every Producer agent (research, writing, analysis, extraction), insert a Verifier agent with a defined → rubric. The Verifier does not redo the work. It checks the output against explicit criteria: schema completeness, source coverage, internal consistency, format compliance. If the output passes, it moves downstream. If it fails, it returns to the Producer with specific revision instructions. If it fails twice, it → escalates.

This pattern costs compute — every verification step is an additional model call. But the alternative is worse: unverified pipelines produce outputs that look professional and are occasionally fabricated, and no one in the pipeline knows which is which until a human reads the final product. The verification loop is the mechanism that converts a pipeline from *hopeful* to *reliable*.

## What it changes in model behavior

Verification loops improve factual accuracy, structural compliance, and internal consistency of model outputs. Self-consistency reduces answer variance by marginalizing across multiple reasoning paths — in effect, it replaces the single most-probable output with the consensus output across diverse reasoning chains [src_paper_sahoo2025]. Self-Refine improves output quality iteratively, with the largest gains occurring in the first revision cycle (subsequent cycles show diminishing returns).

Critically, verification works better when the verification criteria are *different* from the generation instructions. A model asked to "write a paragraph and then check that it is good" often rubber-stamps its own work. A model asked to "write a paragraph" and then separately asked "identify any unsupported claims, logical gaps, or factual errors in this paragraph" applies a distinct cognitive frame and catches more issues. CoVe exploits this by generating verification questions independently, deliberately preventing the model from anchoring on its original justification.

## Use it when

- The output contains factual claims that must be accurate (reports, analyses, citations)
- The output will be consumed by downstream agents that cannot self-correct
- The task involves structured output where schema violations are detectable (JSON, tables, forms)
- Previous pipeline runs produced errors that propagated through multiple stages
- The cost of an error in the final output exceeds the cost of an additional verification call
- You are working with a model tier prone to confident-sounding errors (most tiers, for factual tasks)

## Do not use it when

- The task is creative and "correctness" is not well-defined
- Speed is the binding constraint and the task is low-stakes
- The verification criteria are so vague that the check adds nothing ("make sure it's good")
- You are in an exploratory phase and the output is for your own reading, not for downstream consumption
- The model has already demonstrated near-perfect compliance on a particular task type (check with a sample, not an assumption)

## Contrast set

**Closest adjacent abstractions**

- → rubric — A rubric defines the criteria; a verification loop applies them. The rubric is the checklist. The loop is the checkpoint.
- → self-consistency — A specific verification technique that uses output diversity as the signal. Verification loops are the broader pattern.
- → falsifiability — Making claims checkable is a prerequisite for verification loops to work. Unfalsifiable claims pass any check.

**Stronger / weaker / narrower / broader relatives**

- → audit trail — Broader. The audit trail records what happened across the full pipeline; the verification loop checks what happened at one step.
- → provenance tracking — Complementary. Provenance tracks where claims came from; verification checks whether those claims hold up.
- → escalation — The verification loop's failure branch: what happens when output fails the check.
- → self-refine — Narrower. A specific implementation of the generate-critique-revise loop.

## Common failure modes

- **Rubber-stamp verification** → The model checks its own output using the same framing it used to generate it and predictably approves everything. Fix: use a different prompt, a different model, or a different agent for verification. The verifier must have *adversarial distance* from the producer.

- **Infinite loops** → The verification criteria are strict enough to always fail but the revision instructions are vague enough to never fix the underlying problem. The model generates, fails, revises identically, fails again. Fix: cap iterations (typically 2–3) and → escalate if verification still fails.

- **Verification theater** → Adding a verification step that checks only trivial properties (word count, format) while ignoring the hard ones (factual accuracy, logical coherence). The pipeline now has a quality gate that waves through bad content with a clean stamp. Fix: design verification criteria that target *the failure modes you actually care about*, not the ones that are easy to check.

## Prompt examples

### Minimal example

```text
Answer the following question using only the information in the attached document.

After writing your answer:
1. Verify that every factual claim you made appears in the document.
2. If any claim does not, remove it and note what you removed.
3. Check that your answer is under 150 words.
```

### Strong example

```text
You are a technical fact-checker reviewing a draft product specification.

Step 1: Read the specification below.

Step 2: For each technical claim (performance number, compatibility statement,
or standard compliance assertion), determine whether it is:
  - VERIFIED: matches the data in the attached test results
  - UNVERIFIED: not addressed in the test results
  - CONTRADICTED: conflicts with the test results

Step 3: Produce a verification report as a table:
| Claim | Location | Status | Evidence | Note |

Step 4: Before returning the report, self-check:
  - Did you cover every section of the specification?
  - Does every VERIFIED claim cite a specific test result?
  - Are there any claims you marked VERIFIED that you are not
    confident about? If so, downgrade them to UNVERIFIED.

If more than 30% of claims are UNVERIFIED or CONTRADICTED,
add a summary warning at the top of your report.
```

### Agentic workflow example

```text
Pipeline: Research → Verify → Synthesize

--- VERIFIER AGENT ---

Input: Claims array from Research Agent, each with:
  { claim_id, claim_text, source_id, source_url }

Verification rubric:
1. Source existence: Does source_id resolve to a real source card
   in the corpus? (check corpus/source_cards/{source_id}.json)
2. Claim support: Does the source content support the claim text?
   Read corpus/normalized/{source_id}.md and check.
3. Recency: Was the source published within the last 18 months?
4. Trust tier: Is the source T1 or T2? (T3/T4 sources are
   insufficient for standalone claims)

For each claim, return:
{
  "claim_id": "",
  "verification": "PASS | FAIL_NO_SOURCE | FAIL_UNSUPPORTED |
                   FAIL_STALE | FAIL_LOW_TRUST",
  "evidence_span": "quote from source if PASS",
  "recommendation": "keep | revise_source | drop"
}

Escalation rules:
- If > 25% of claims FAIL, return the full report to Research Agent
  with revision instructions specifying which claims need
  stronger sourcing.
- If > 50% of claims FAIL, escalate to Corpus Planner for
  additional source acquisition before retrying.
- Maximum verification cycles: 3. After 3 failures, flag the
  entry for human review.

Pass criteria: 100% of claims at PASS before forwarding to
Synthesize Agent.
```

## Model-fit note

Verification loops work across all model tiers but their reliability varies. Frontier proprietary models are the most capable self-verifiers — they can apply nuanced rubrics and catch subtle inconsistencies. Midsize open models verify structural properties reliably (format, length, schema) but miss semantic errors at higher rates. Small open models are poor self-verifiers; for these tiers, use a separate, larger model as the verifier or restrict verification to checkable format constraints. Reasoning-specialized models excel at logic-based verification (detecting contradictions, checking arithmetic) but may over-verify, flagging stylistic choices as errors.

## Evidence and provenance

Self-consistency was introduced by Wang et al. (2022) and improves GSM8K accuracy by 17.9% over baseline CoT [src_paper_sahoo2025]. Self-Refine (Madaan et al., 2023) demonstrates iterative improvement with GPT-4 gains of 8.7–21.6 points across code and text tasks [src_paper_sahoo2025]. Chain-of-Verification (CoVe, Dhuliawala et al., 2023) reduces hallucination through independent self-questioning [src_paper_sahoo2025]. The Prompt Report classifies self-criticism as a major category of prompting techniques, including Chain-of-Verification, Self-Calibration, Self-Refine, Self-Verification, and ReverseCoT [src_paper_schulhoff2025]. The architectural pattern of Verifier agents in multi-agent pipelines draws from framework documentation and practitioner patterns.

## Related entries

- **→ rubric** — the criteria set that a verification loop applies
- **→ self-consistency** — a specific verification technique using output diversity
- **→ falsifiability** — claims must be checkable for verification to work
- **→ hallucination bait** — verification loops are the primary architectural defense against fabrication
- **→ delegation** — every delegation should have a paired verification step
- **→ escalation** — what happens when verification repeatedly fails
- **→ audit trail** — records the outcomes of verification across the pipeline

---

> **Model Note**
>
> Self-verification reliability scales with model capability, but not linearly. Frontier models catch roughly 60–80% of their own factual errors when prompted with specific verification criteria. Smaller models catch closer to 30–40% and sometimes introduce *new* errors during the verification step. If your pipeline uses a small model for generation, consider using a larger model exclusively for the verification stage. The cost of one additional call to a frontier model is usually less than the cost of shipping an unverified output.
