# pipeline

> Decomposition made permanent — a fixed sequence of stages that runs the same way every time, with each stage doing one thing well.

## The Scene

Form8 started as a single n8n node: "Research this market, analyze competitors, identify gaps, write a strategy brief." The output read like all four tasks had been tossed in a blender. Competitor profiles contained strategy recommendations. Gap analysis contained raw search results. The brief was 2,000 words of everything and nothing.

I split it into four nodes. Node 1 (Market Scanner): return 8-10 competitors as a JSON array — name, URL, positioning. No analysis. Node 2 (Competitor Profiler): enrich each competitor with pricing, features, target segment. Node 3 (Gap Analyzer): identify 3-5 differentiation opportunities, each with evidence. Node 4 (Strategy Writer): produce a 500-word brief citing specific gaps. Each node has one job, one output schema, and one validation gate. When Node 2 can't find pricing for a competitor, it fails *there* — not in the middle of a 2,000-word blob where nobody can tell what went wrong.

## What This Actually Is

A pipeline is a fixed sequence of processing stages where each stage's output becomes the next stage's input. It's decomposition hardened into architecture — reusable, monitorable, debuggable. Each stage can be a different prompt, a different model, a different tool, or even a non-LLM function. The pipeline doesn't care what's inside each box. It only cares that the interfaces between boxes are respected.

The defining characteristic separating a pipeline from a one-off chain is *persistence*. Chains are scripts you execute once. Pipelines are infrastructure you deploy. This distinction justifies engineering investment in monitoring, validation, retry logic, and versioning.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Classify, extract, and summarize this email" (one prompt) | Three stages: CLASSIFY (→ JSON category), EXTRACT (→ structured fields), SUMMARIZE (→ prose brief). Each with its own prompt, schema, and validation | Each stage can be tuned and tested independently |
| Free-text output between stages | JSON or structured output as the intermediate representation | Structured formats are parseable and validatable — free text isn't |
| Same model for every stage | Classification → small/fast model. Generation → frontier model. Validation → rule-based, no model at all | Per-stage model selection is how pipelines optimize cost |
| No error handling between stages | "If Stage N output fails validation: retry once with error feedback. If retry fails: halt and report which stage failed and why" | Error handling at boundaries prevents garbage propagation |
| Monolithic prompt that does everything | Pipeline with interface contracts: each stage declares expected input format and promised output format | The immune system of a pipeline — catches disease at the boundary |

## Before → After

From Form8 — the monolith-to-pipeline conversion:

> **Before (monolith)**
> ```
> You are a market research analyst. Given this product
> description and target market, produce a comprehensive
> competitive analysis with market sizing, competitor profiles,
> gap analysis, and strategic recommendations.
> ```
>
> **After (pipeline with interface contracts)**
> ```
> NODE 1 — Market Scanner
> Input: product description + target market
> Task: Return 8-10 competitors as JSON array
>   [{name, url, one_sentence_positioning}]
> Gate: ≥6 competitors found. If fewer, flag and halt.
>
> NODE 2 — Competitor Profiler
> Input: competitor array from Node 1
> Task: For each, extract pricing_tier, key_features[],
>   target_customer_segment
> Gate: all three fields populated for every competitor
>
> NODE 3 — Gap Analyzer
> Input: enriched competitors + product description
> Task: Identify 3-5 differentiation gaps, each with
>   description, evidence, and confidence level
> Gate: every gap cites at least one competitor by name
>
> NODE 4 — Strategy Writer
> Input: all upstream outputs
> Task: 500-word strategy brief for product team
> Gate: every recommendation traces to a gap from Node 3
> ```
>
> **What changed:** One impossible task became four possible tasks. Each node has one job, one schema, and one gate. When Node 2 fails (a competitor's site has no pricing), the failure is localized, visible, and recoverable.

## From the Lab

We compared single-pass prompts against decomposed multi-step versions across reasoning tasks:

![Reasoning Task Techniques](../art/figures/exp_reasoning_task_techniques.png)

**Key finding:** Multi-step decomposition improved accuracy by 10-40% depending on task complexity. The benefit was largest for tasks requiring 3+ reasoning steps — exactly the tasks where monolithic prompts fail hardest. For simple 1-step tasks, the overhead outweighed the benefit. Don't pipeline what doesn't need pipelining.

## Try This Now

Take any prompt that does more than one thing. Identify the stages by asking: "Where does the task naturally hand off from one cognitive operation to another?" Then sketch the pipeline:

```
For each stage:
- Name it (Classify, Extract, Analyze, Write, Validate)
- Define its input format
- Define its output format
- Define one validation gate (how would you know this stage failed?)
```

You'll often discover that your "one task" was actually three tasks wearing a trenchcoat.

## When It Breaks

- **Stage coupling** — Stage B depends on Stage A's implementation details, not its interface contract. When A changes, B breaks. Fix: enforce explicit schemas and validate at every boundary.
- **Error propagation** — Stage 2 produces garbage, Stage 3 processes it as valid, and the final output is confidently wrong. Fix: validate outputs at every transition. Halt or branch on failure.
- **Brittleness to input variance** — The pipeline handles expected inputs perfectly and collapses on anything unexpected. Fix: include a default/catch-all path and monitoring for unclassified inputs.

## Quick Reference

- **Family:** Agent workflow
- **Adjacent:** → decomposition (the cognitive act; pipeline is the architectural reification), → orchestration (the control layer that manages pipelines and more), → handoff (each stage boundary is a handoff event)
- **Model fit:** Pipelines are model-agnostic by design — that's the point. Each stage uses whatever model fits its task. Classification: small/fast. Generation: frontier. Validation: rule-based, no model. The pipeline pattern turns model diversity from a headache into a cost optimization strategy.
