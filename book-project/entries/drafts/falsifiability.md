---
headword: "falsifiability"
slug: "falsifiability"
family: "quality_control"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# Falsifiability

**Elevator definition** Structuring claims so they can be checked, tested, or disproven — forcing the model to put its assertions where evidence can reach them.

## What it is

A falsifiable claim is one that could, in principle, be shown to be wrong. "The company is doing well" is unfalsifiable — what does "well" mean, by what metric, compared to what? "The company's Q3 revenue was $4.2M, a 15% increase over Q2" is falsifiable — you can check the numbers, verify the calculation, and determine whether the claim is true or false.

Language models are, by nature, generators of plausible text. Plausibility is not the same as accuracy. A model can produce a beautifully fluent paragraph in which every sentence sounds right and none can be verified. This is the fundamental problem that falsifiability addresses: it doesn't make the model more accurate, but it forces the model to produce output in a form where inaccuracy is detectable.

Falsifiability in prompt engineering operates at two levels. At the **claim level**, you instruct the model to make specific, checkable assertions rather than vague generalizations. At the **structural level**, you design prompts and pipelines so that outputs carry the metadata needed for verification — sources, confidence levels, reasoning chains, and falsification criteria.

The concept comes from Karl Popper's philosophy of science, where falsifiability distinguishes scientific claims from non-scientific ones. In LLM work, the bar is lower but the principle is the same: can I check this? If the output makes a claim, can I trace it to a source, test it against data, or evaluate it against a criterion? If not, the claim is decoration — it fills space without adding reliable information.

Falsifiability is closely related to grounding — the practice of anchoring model output in verifiable sources. But it's broader. A grounded claim has a source. A falsifiable claim has a test. "According to the 2024 annual report, revenue was $50M" is grounded. "Revenue exceeded $45M, which can be verified against the filed 10-K on page 23" is grounded and falsifiable — it tells you where and how to check.

In practice, prompting for falsifiability means asking the model to do several things: cite specific sources rather than making unsourced assertions, provide numbers with units and reference points rather than qualitative descriptions, state confidence levels so you know how much to trust each claim, and identify what evidence would change the conclusion.

The result is output that's less fluent and more useful. Falsifiable text is clunkier than unfalsifiable text — specificity has a syntactic cost. But it's dramatically more trustworthy and dramatically easier to verify, correct, and improve.

## Why it matters in prompting

Falsifiability is the antidote to authoritative-sounding nonsense. When you instruct a model to make every claim falsifiable, you raise the cost of hallucination. The model can't easily fabricate a specific number, a specific source, and a specific page reference — any of which can be checked. It can easily fabricate a vague generalization that sounds authoritative but says nothing checkable.

Prompting for falsifiability also makes evaluation possible. If you can't determine whether the output's claims are correct, you can't improve the prompt. By requiring falsifiable claims, you create an output that can be scored, audited, and iteratively improved.

## Why it matters in agentic workflows

In multi-agent pipelines, falsifiability is the mechanism that prevents confident nonsense from propagating through the chain. If Agent A produces unfalsifiable claims ("the market is trending positively"), Agent B has no way to verify them — it simply inherits A's assertions as inputs and builds on them. If A produces falsifiable claims ("the market grew 3.2% in Q3 per BLS data"), Agent B can verify before incorporating.

Falsifiability enables automated verification steps. A fact-checking agent can only check facts that are falsifiable. A contradiction-detection agent can only compare claims that have truth values. The entire quality-control apparatus of an agent system depends on upstream agents producing falsifiable output.

## What it changes in model behavior

Instructing models to produce falsifiable claims shifts output from impressionistic to evidential. The model generates fewer qualitative assessments and more specific, checkable statements. Hedge words decrease. Citation density increases. The output reads less like an essay and more like an analyst's report.

## Use it when

- The output will inform decisions and accuracy matters
- You need to verify, fact-check, or audit the model's output
- The domain has objective standards of correctness (financial, scientific, legal, technical)
- Multiple agents in a pipeline need to trust each other's outputs
- You're building evaluation datasets and need claims with ground-truth-checkable properties

## Do not use it when

- The task is creative or subjective (there's no false answer to "write a poem")
- The model is brainstorming or exploring possibilities, not asserting facts
- Over-specification would kill the exploratory value of the output
- The audience needs accessible narrative, not analyst-grade precision

## Contrast set

- **Explicitness** → Explicitness makes requirements visible; falsifiability makes claims testable. A prompt can be explicit but produce unfalsifiable output. Falsifiability targets the output, not the prompt.
- **Contradiction detection** → Contradiction detection finds conflicting claims; falsifiability makes individual claims checkable. Detection is relational (between claims). Falsifiability is individual (per claim).
- **Grounding** → Grounding anchors claims in sources; falsifiability ensures claims have verification paths. Grounded claims cite where they came from. Falsifiable claims specify how to check them.
- **Audit trail** → An audit trail records what was produced; falsifiability determines whether what was produced can be verified. The trail is the record. Falsifiability is the property.

## Common failure modes

- **Performative falsifiability → claims that look checkable but aren't.** "According to recent studies, the rate is approximately 15-25%." Which studies? What rate? The claim has the syntax of falsifiability (numbers, attribution) without the substance (specific sources, specific measures). Fix: require full citation — author, year, publication — and specific figures, not ranges dressed up as precision.
- **Falsifiability at the wrong level → individual facts are falsifiable but the conclusion isn't.** Each data point is correct, but the interpretive leap from data to conclusion cannot be tested. "Revenue grew 10% and headcount grew 5%, therefore the company is more efficient" — both numbers are checkable, but "more efficient" requires a definition of efficiency that isn't provided. Fix: require falsifiable conclusions, not just falsifiable inputs. The conclusion must state what evidence would disprove it.
- **Precision paralysis → the demand for falsifiability prevents the model from saying anything uncertain.** Not everything can be falsified to the same degree. An honest estimate with stated uncertainty ("between $4M and $5M based on incomplete data") is more useful than silence or false precision. Fix: distinguish between hard claims (must be falsifiable) and estimates (must state confidence and basis).

## Prompt examples

### Minimal example

```
List three risks to this project. For each risk:
- State the risk as a specific, testable prediction
- Name the metric or event that would confirm it
- Estimate the probability (low/medium/high) with one sentence of justification
Do not state risks as vague concerns. Every risk must be falsifiable.
```

### Strong example

```
You are writing a market analysis. Every factual claim must be falsifiable.

Rules for falsifiability:
1. Every statistic must include: the number, the unit, the source, and the time period
2. Every comparison must specify: what is being compared, on what metric, and the direction
3. Every causal claim must specify: what evidence would disprove the causal link
4. Qualitative assessments (e.g., "growing rapidly") must be replaced with quantitative
   equivalents (e.g., "grew 23% YoY per [source]")
5. If a claim cannot be made falsifiable due to data limitations, prefix it with
   [UNFALSIFIABLE ESTIMATE] and state what data would be needed to verify it

Analyze the following market data: {data}
```

### Agentic workflow example

```
pipeline: investment_research
falsifiability_protocol:
  every agent output must tag each claim as:
    VERIFIED: checked against primary source, citation included
    FALSIFIABLE: specific enough to check, not yet verified
    ESTIMATE: best guess with stated confidence and basis
    UNFALSIFIABLE: qualitative judgment, flagged for human review

agents:
  - data_gatherer:
      output: facts with full citations
      falsifiability_target: 100% VERIFIED or FALSIFIABLE
  - analyst:
      input: data_gatherer output
      output: findings with reasoning chains
      falsifiability_target: 80% VERIFIED/FALSIFIABLE, 20% ESTIMATE
  - recommender:
      input: analyst output
      output: recommendation with evidence map
      must_include: "This recommendation would be wrong if [falsification condition]"

quality_gate:
  reject any output where UNFALSIFIABLE claims exceed 10% of total
  escalate any UNFALSIFIABLE claim that drives a key recommendation
```

## Model-fit note

Large models (GPT-4-class, Claude 3.5+) produce more naturally falsifiable output when prompted — they cite more readily, quantify more precisely, and respond well to falsifiability frameworks. Smaller models tend toward vague generalizations even when instructed otherwise. For smaller models, provide explicit templates showing the desired format: "Claim: [specific statement]. Source: [citation]. Verification: [how to check]."

## Evidence and provenance

Falsifiability as an epistemological criterion was articulated by Popper (1934, *The Logic of Scientific Discovery*). Its application to LLM output quality draws on factual consistency research (Maynez et al., 2020), grounding and attribution work (Rashkin et al., 2023, "Measuring Attribution in Natural Language Generation"), and practical guardrail implementations that use verifiability as a quality metric.

## Related entries

- → **contradiction_detection** — Falsifiable claims make contradiction detection possible by providing truth-valued assertions to compare.
- → **audit_trail** — Falsifiable outputs are auditable; unfalsifiable ones can only be logged, not evaluated.
- → **explicitness** — Explicitness in the prompt produces falsifiability in the output; they are input-side and output-side cousins.
- → **anchoring** — Falsifiable numeric claims serve as anchors for downstream analysis steps.
