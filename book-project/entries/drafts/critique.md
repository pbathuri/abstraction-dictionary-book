---
headword: "critique"
slug: "critique"
family: "instructional_action"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["evaluate", "verification loop", "self-refine", "justify", "falsifiability", "rubric", "framing"]
cross_links: ["evaluate", "verification loop", "self-refine", "justify", "falsifiability", "rubric", "framing", "constrain", "compare", "elaborate", "hallucination bait"]
tags: ["instructional-action", "adversarial-reasoning", "quality-control", "self-improvement"]
has_note_box: true
note_box_type: "upgrade_prompt"
---

# critique

**Elevator definition**
To critique is to systematically identify weaknesses, gaps, and failure points in a given work, activating the model's adversarial reasoning rather than its generative compliance.

## What it is

Most of the time, a language model is trying to help you. It is agreeable by training — tuned to produce responses that satisfy, that affirm, that complete requests cooperatively. This is useful when you want something built. It is dangerous when you want something tested.

Critique is the instruction that flips the model's orientation from *ally* to *adversary*. When you ask a model to critique, you are not asking it to describe, improve, or extend a piece of work. You are asking it to find what is wrong with it. The shift is fundamental: generative mode asks "what can I add?"; critique mode asks "what can I break?"

The distinction between critique and casual feedback matters. Feedback is open-ended — "what do you think of this?" — and tends to produce a sandwich of praise, mild suggestion, and more praise, because the model has learned that humans prefer encouragement. Critique is targeted — "identify the weaknesses in this argument, the gaps in this evidence, the failure modes of this design" — and produces output that is genuinely useful for revision precisely because it is uncomfortable to read.

The prompting literature has recognized the power of adversarial self-evaluation. Madaan et al. (2023) formalized this in Self-Refine, a three-step loop in which the model generates output, then critiques its own output, then revises based on that critique [src_paper_sahoo2025]. The critique step is the engine of the whole system. Without it, revision is blind — the model rewrites without knowing what to fix. With it, revision is targeted: the critique identifies specific weaknesses and the revision addresses them. Self-Refine improved GPT-4 performance by 8.7 points in code optimization and 21.6 points in sentiment reversal, and those gains came almost entirely from the quality of the intermediate critique, not from the revision mechanism itself.

What makes critique cognitively distinct from generation is that it requires *evaluative distance*. The model must read its own output (or someone else's) not as a continuation to extend but as an artifact to examine. This is why Self-Refine works better when the critique prompt is phrased differently from the generation prompt — the change in framing forces the model to adopt a different stance. A model asked to "write a paragraph and then improve it" often produces cosmetic edits. A model asked to "write a paragraph" and then separately asked to "identify every unsupported claim, logical gap, and unclear reference in this paragraph" produces substantive revision targets.

## Why it matters in prompting

Critique is the cheapest way to improve output quality without changing models, without adding data, and without redesigning your prompt architecture. Add "now critique your own response" to the end of any generation prompt and you get a free quality pass. The pass is imperfect — models are biased toward approving their own work — but even biased self-critique catches a meaningful fraction of errors.

The instruction is most powerful when it is specific about *what* to critique. "Critique this essay" invites vague commentary. "Identify any claims in this essay that lack supporting evidence, any logical steps that skip a premise, and any conclusions that do not follow from the preceding analysis" invites targeted destruction. The specificity of the critique prompt determines whether you get polite hedging or actionable fault-finding.

The Prompt Report documents self-criticism as a major category of prompting technique, encompassing Chain-of-Verification, Self-Calibration, Self-Refine, and ReverseCoT [src_paper_schulhoff2025]. What these techniques share is the insight that a model's *second* look at its own output is substantially more accurate than its *first* pass at generation. The model is, paradoxically, a better critic than it is an author.

## Why it matters in agentic workflows

In agent architectures, critique is the mechanism that prevents error propagation. A pipeline without a critique step is a pipeline that trusts every intermediate output. A pipeline with a dedicated Critic agent is a pipeline that subjects every intermediate output to adversarial scrutiny before it flows downstream.

The architecture is a natural extension of Self-Refine's generate-critique-revise loop, scaled to multi-agent systems. A Research Agent drafts findings. A Critic Agent identifies unsupported claims, missing sources, and logical gaps. The Research Agent revises. The Critic checks again. This cycle — bounded by iteration limits and → escalation rules — produces outputs that are qualitatively different from single-pass generation. The Critic agent does not need to be a different model. It needs to have a different → framing: adversarial where the producer is cooperative, skeptical where the producer is confident.

## What it changes in model behavior

Critique activates a measurably different output pattern. The model produces more hedged language, more conditional claims, more references to specific flaws. It is less likely to produce false positives (claiming something is good when it is not) and more likely to produce false negatives (flagging something as problematic when it is acceptable). This asymmetry is useful: in quality assurance, false negatives are cheap to dismiss while false positives are expensive to miss. A Critic agent that over-flags is better than one that under-flags.

The activation is prompt-sensitive. "Critique this" produces mild commentary. "Adopt the role of a hostile peer reviewer who has been asked to find every reason to reject this submission" produces sharp, detailed fault-finding. The intensity of the critique frame determines the depth of the adversarial reasoning.

## Use it when

- You have a draft (text, code, plan, design) and need to find its weaknesses before committing to it
- Previous outputs from the model were polished-sounding but contained logical gaps or unsupported claims
- You are building a pipeline and need a quality gate between production and consumption stages
- You want the model to stress-test an argument, proposal, or specification against likely objections
- You are implementing a Self-Refine loop and need the critique step to drive targeted revision
- The work being reviewed was produced by another model or agent, and you need adversarial distance

## Do not use it when

- The work is in an early brainstorming phase and premature critique will kill nascent ideas
- You want improvement suggestions, not fault-finding — that is feedback or revision, not critique
- The author of the work is a human who has asked for encouragement, not demolition (know your audience)
- The critique criteria are undefined and the model would be guessing at what counts as a weakness

## Contrast set

**Closest adjacent abstractions**

- → evaluate — Evaluate applies a rubric to assess overall quality, producing a judgment. Critique finds specific weaknesses. Evaluation says "this is a 7 out of 10." Critique says "paragraph three contradicts paragraph one, and the data in Table 2 does not support the conclusion in Section 4."
- → justify — Justify builds the case *for* a claim. Critique builds the case *against* it. They are adversarial complements.
- → compare — Compare places items side by side without judging. Critique examines a single item and judges harshly.

**Stronger / weaker / narrower / broader relatives**

- → verification loop — Broader. A verification loop includes critique as one step in a generate-critique-revise cycle.
- → self-refine — The full pattern: generate, critique, revise. Critique is the second step.
- → falsifiability — Complementary. A claim must be falsifiable for critique to engage with it. Unfalsifiable claims slip past critique.
- → rubric — A rubric structures what the critique should examine. Critique without rubric is unfocused.

## Common failure modes

- **Politeness override** → The model's helpfulness training overrides the critique instruction. Instead of identifying weaknesses, it says "this is mostly good but could be improved in a few areas" and then offers mild suggestions. Fix: frame the critique adversarially — "your job is to find faults, not to encourage the author" — and provide specific categories of weakness to search for.

- **Critique of surface, not substance** → The model flags formatting issues, word choice, and stylistic preferences while ignoring logical gaps, unsupported claims, and structural failures. This is critique theater: it looks thorough but misses everything that matters. Fix: specify that the critique should address *substance* (logic, evidence, completeness) and ignore *surface* (style, tone, formatting) unless explicitly asked.

- **Self-rubber-stamping** → When a model critiques its own output, it is biased toward approval. It generated the text, so it finds it reasonable. Fix: introduce adversarial distance — use a separate prompt, a separate agent, or a separate model for the critique step. Alternatively, instruct the model to "find at least three specific weaknesses" to force it past the approval bias.

## Prompt examples

### Minimal example

```text
Critique the following business proposal. Focus on:
1. Assumptions that are stated but not supported with evidence
2. Risks that are acknowledged but not mitigated
3. Financial projections that depend on best-case scenarios

Do not comment on writing quality or formatting.
```

### Strong example

```text
You are a senior peer reviewer for a top-tier machine learning
conference. Your reputation depends on catching weak papers.

Review the following paper abstract and methodology section.
For each weakness you identify, provide:
- The specific claim or design choice that is weak
- Why it is weak (missing evidence, logical gap, unstated
  assumption, methodological flaw)
- How severe the weakness is: MINOR (cosmetic), MODERATE
  (affects confidence in results), or MAJOR (invalidates
  a central claim)

Requirements:
- Identify at least 5 specific weaknesses. If you cannot find 5,
  you are not looking hard enough.
- Do not praise any aspect of the work. That is not your job here.
- If a claim is unfalsifiable (cannot be tested or disproven),
  flag it explicitly as UNFALSIFIABLE.
- Quote the exact text you are critiquing.
```

### Agentic workflow example

```text
Agent: Critic Agent
Pipeline position: After Draft Agent, before Revision Agent

Input: Draft output from Draft Agent + original task specification

Task: Critique the draft against the original specification.

Critique rubric:
1. COMPLETENESS — Does the draft address every requirement in
   the specification? List any requirements that are missing
   or partially addressed.
2. ACCURACY — Are factual claims supported by the source material
   provided to the Draft Agent? Flag any claim that cannot be
   traced to a source.
3. INTERNAL CONSISTENCY — Does the draft contradict itself?
   Check that conclusions follow from the analysis.
4. CONSTRAINT COMPLIANCE — Does the draft satisfy all constraints
   from the original prompt (length, format, tone, scope)?

For each issue found:
{
  "issue_id": "",
  "category": "COMPLETENESS | ACCURACY | CONSISTENCY | CONSTRAINT",
  "severity": "MINOR | MODERATE | MAJOR",
  "location": "section or paragraph reference",
  "description": "what is wrong",
  "revision_instruction": "specific fix for Revision Agent"
}

Escalation: If more than 3 MAJOR issues are found, return the
draft to the Draft Agent for full regeneration instead of
passing to Revision Agent for patching.

Maximum cycles: 2 critique-revision loops before escalation
to human review.
```

## Model-fit note

Critique quality varies more by prompt design than by model tier. Frontier models produce incisive, specific critiques when given adversarial framing and explicit criteria — they can catch subtle logical gaps and unstated assumptions. Midsize open models identify structural and factual weaknesses but tend to miss nuanced issues like unstated assumptions or statistical misinterpretation. Small open models produce surface-level critique (formatting, length, obvious omissions) and are poor at detecting logical inconsistencies. All model tiers are biased toward approving their own output; adversarial distance (separate prompt, separate agent) improves critique quality at every level.

## Evidence and provenance

Self-Refine's critique step is documented in Madaan et al. (2023), with performance gains of 8.7–21.6 points across code and text tasks attributed to the quality of the intermediate critique [src_paper_sahoo2025]. The Prompt Report classifies self-criticism as a major prompting category encompassing multiple techniques [src_paper_schulhoff2025]. Chain-of-Verification (Dhuliawala et al., 2023) uses critique in the form of self-generated verification questions to reduce hallucination [src_paper_sahoo2025]. The observation that models are better critics than generators — producing more accurate evaluations of text than original compositions — is a recurring finding across the self-improvement literature.

## Related entries

- **→ evaluate** — assesses overall quality; critique targets specific weaknesses
- **→ verification loop** — the architectural pattern that embeds critique in a pipeline
- **→ self-refine** — the generate-critique-revise loop that depends on critique quality
- **→ justify** — the adversarial complement: justify builds the case, critique tears it down
- **→ falsifiability** — claims must be falsifiable for critique to have purchase
- **→ rubric** — structures what the critique examines
- **→ framing** — adversarial framing is what activates genuine critique vs. polite feedback

---

> **Upgrade This Prompt**
>
> Before: "Review my essay and tell me what you think."
>
> After: "Critique this essay. Identify every claim that lacks supporting evidence, every logical step that assumes what it should prove, and every conclusion that does not follow from the preceding argument. Do not comment on style or tone. For each weakness, quote the exact sentence and explain why it fails. Find at least four problems."
>
> What changed: the instruction shifted from open-ended feedback (which invites praise) to targeted fault-finding (which invites rigor). The criteria are explicit. The minimum count forces the model past its approval bias. The exclusion of style keeps the critique on substance.
