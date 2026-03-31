---
headword: "analyze"
slug: "analyze"
family: "instructional_action"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# Analyze

**Elevator definition** Breaking something apart to understand its components, relationships, and implications — the decomposition verb that precedes judgment.

## What it is

Analysis is structured disassembly. You take a whole — a text, a dataset, a decision, an argument — and pull it into its constituent parts so you can see how those parts relate, where they support each other, and where they don't.

The word gets used loosely. People write "analyze this" in prompts the way they'd say "look at this" in conversation — as a vague gesture toward attention. But analysis, done properly, is a specific cognitive operation with a specific shape: identify components, examine relationships between them, and surface implications that weren't visible in the whole.

This matters in prompt engineering because "analyze" is one of the most common instructional verbs, and one of the most frequently underspecified. When you tell a model to "analyze this document," you've given it a direction but not a destination. Analyze for what? Along which dimensions? To what depth? The model will fill those gaps with its training priors, which may or may not match your intent.

Effective use of "analyze" in prompts requires you to specify the axis of analysis. Financial analysis looks for cost structures, revenue patterns, risk exposure. Literary analysis looks for theme, structure, voice, rhetorical strategy. Competitive analysis looks for market position, differentiation, vulnerability. The verb is the same; the lens changes everything.

Analysis also has a natural place in a sequence of operations. It typically follows retrieval or observation (you need something to analyze) and precedes synthesis or recommendation (analysis feeds judgment). When you place "analyze" correctly in an operational chain, the model produces structured intermediate reasoning. When you skip it, you get conclusions without foundations.

The output shape of analysis matters as much as the instruction. Bullet points encourage surface-level decomposition. Tables force dimensional comparison. Prose allows nuanced relationship-mapping. Choose the output format deliberately — it steers the depth of the analysis.

## Why it matters in prompting

"Analyze" is a load-bearing verb. Used well, it produces the structured intermediate reasoning that makes downstream steps — comparison, recommendation, decision — reliable. Used poorly, it produces hand-wavy summaries dressed up as insight.

The fix is always specificity. Don't say "analyze this proposal." Say "analyze this proposal along three axes: financial viability, technical feasibility, and organizational readiness. For each axis, identify the strongest supporting evidence and the most significant risk." Now the model has a structure to fill rather than a void to improvise in. The quality difference is dramatic and consistent across model families.

## Why it matters in agentic workflows

In agent pipelines, analysis is the step that converts raw information into structured intermediate representations. A research agent retrieves documents; an analysis agent extracts the relevant dimensions; a planning agent acts on the structured output. Without a well-defined analysis step, agents pass unstructured blobs between stages, and each downstream agent must re-derive structure from noise.

Analysis agents benefit from explicit output schemas. When the analysis step produces a typed, structured object — not free-form prose — downstream agents can parse it mechanically rather than interpretively. This reduces cascading ambiguity, the single largest failure mode in multi-agent systems.

## What it changes in model behavior

Specifying "analyze" with explicit dimensions activates the model's capacity for structured decomposition rather than narrative summarization. Without dimensions, models default to a shallow overview. With them, models produce categorized observations, evidence citations, and qualified assessments — substantially more useful intermediate artifacts.

## Use it when

- You need structured understanding before making a decision or recommendation
- The input is complex enough that a summary would lose critical nuance
- You want the model to show its reasoning, not just its conclusions
- Multiple dimensions of evaluation are relevant and should be examined separately
- You're building an intermediate step in a chain that feeds downstream operations

## Do not use it when

- You actually want a summary (use `summarize` — analysis and summary are different operations)
- The input is simple enough that decomposition adds no value
- You need creative generation, not decomposition (use `generate` or `compose`)
- Speed matters more than depth and a quick classification would suffice

## Contrast set

- **Summarize** → Summary compresses; analysis decomposes. Summary asks "what is this about?" Analysis asks "what are the parts and how do they relate?"
- **Evaluate** → Evaluation renders judgment; analysis provides the evidence for judgment. Analysis is pre-evaluative.
- **Contrast** → Contrast examines differences between two or more items; analysis examines the internal structure of a single item.
- **Critique** → Critique is analysis with a normative frame — it decomposes in order to judge quality. Analysis can be purely descriptive.

## Common failure modes

- **Dimension-free analysis → "Analyze this" with no specified axes.** The model produces a generic overview that reads like a book report. Fix: always specify 2-5 dimensions or lenses for the analysis.
- **Analysis-as-summary → the model compresses instead of decomposes.** You asked for analysis but got three sentences of paraphrase. This happens when the prompt lacks structural cues (tables, categories, explicit decomposition instructions). Fix: request structured output with named categories.
- **Infinite recursion → analysis of the analysis.** In agent loops, an analysis step can trigger re-analysis of its own output if the stopping condition is vague. Fix: define what "done" looks like — a specific output schema or completeness criterion.

## Prompt examples

### Minimal example

```
Analyze this customer review along three dimensions:
1. Product satisfaction (what they liked/disliked about the product)
2. Service experience (interactions with support or delivery)
3. Purchase intent (likelihood of repurchase or recommendation)
```

### Strong example

```
You are a policy analyst. Analyze the following proposed regulation.

Dimensions:
- Economic impact: who bears costs, who captures benefits, estimated magnitude
- Implementation feasibility: what infrastructure exists, what must be built
- Political viability: likely supporters and opponents, coalition dynamics
- Unintended consequences: second-order effects the drafters may not have considered

For each dimension, provide:
- 2-3 key observations with supporting evidence from the text
- A confidence level (high/medium/low) based on evidence quality
- One question that would need answering before recommending action

Regulation text: {input}
```

### Agentic workflow example

```
agent: market_analyst
trigger: new competitor product launch detected
steps:
  1. retrieve: gather product specs, pricing, press coverage, user reviews
  2. analyze:
     dimensions:
       - feature_comparison: map features against our product matrix
       - pricing_position: where does it sit relative to market segments
       - target_audience: who is this built for, overlap with our users
       - threat_level: what would we lose if we did nothing for 6 months
     output_schema:
       type: structured_report
       fields: [dimension, findings, evidence, confidence, recommended_action]
  3. route: if threat_level.confidence >= high → escalate to strategy team
           else → log to competitive intelligence dashboard
```

## Model-fit note

All current-generation models handle dimensional analysis well when given explicit axes. GPT-4o and Claude 3.5 Sonnet produce particularly well-structured analytical outputs. Smaller models (7B-13B parameter range) benefit from few-shot examples showing the desired decomposition format. Without examples, they tend to collapse analysis into summary.

## Evidence and provenance

Bloom's taxonomy (1956, revised 2001) places analysis as a higher-order cognitive operation above comprehension and application. In prompt engineering, the importance of specifying analytical dimensions emerged from early chain-of-thought research (Wei et al., 2022) and has been reinforced by systematic prompt comparison studies showing 30-60% quality improvements when analysis axes are explicit.

## Related entries

- → **contrast** — A specialized form of analysis that focuses on differences between items rather than internal structure.
- → **explicitness** — Analysis quality depends directly on how explicit the dimensional specification is.
- → **checkpoint** — Analysis outputs often serve as checkpoint artifacts in agentic workflows.
- → **falsifiability** — The best analyses produce claims that can be checked, not just assertions.
