---
headword: "framing"
slug: "framing"
family: "core_abstraction"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["perspective", "scope", "context", "specificity", "register", "audience specification", "reframing"]
cross_links: ["perspective", "scope", "context", "specificity", "register", "audience specification", "reframing", "constrain", "decomposition", "role prompting"]
tags: ["core-abstraction", "prompting-fundamental", "cognition", "rhetoric"]
has_note_box: true
note_box_type: "which_word"
---

# framing

**Elevator definition**
Framing is the choice of angle, emphasis, and interpretive lens through which you present a task to a model, shaping what the model treats as relevant before it generates a single word.

## What it is

Before a model writes anything, it has already decided what the question is about. That decision — which aspects of the input are central, which are peripheral, which are invisible — is determined by the frame.

Framing is a concept borrowed from cognitive science and rhetoric, where it describes how the presentation of a problem shapes the conclusions people draw. Tversky and Kahneman demonstrated decades ago that the same medical outcome described as "a 90% survival rate" versus "a 10% mortality rate" produces reliably different decisions, even among experts. The facts are identical. The frame is not. And the frame wins.

Language models are susceptible to the same mechanics, though for different reasons. A model does not have preferences or risk aversion. But it does have statistical associations. When you frame a task as "identify the risks in this proposal," the model activates patterns associated with risk identification — skepticism, qualification, caution. When you frame the same material as "identify the opportunities in this proposal," it activates a different constellation: optimism, potential, upside. The underlying document has not changed. The model's attention to it has.

This makes framing a *steering* abstraction. Where → specificity narrows what the model considers and → constrain bounds what the model may produce, framing orients *how* the model considers it. It is the difference between handing someone a telescope and telling them to look at the night sky versus pointing the telescope at the moon. The instrument is the same. The observation changes.

Framing operates through several mechanisms. **Role framing** sets the model's interpretive persona: "You are a defense attorney" produces different analysis than "You are a prosecutor" on the same case file. The Prompt Report catalogues role prompting as one of the most frequently discussed prompt components, noting that it improves both writing quality and stylistic alignment [src_paper_schulhoff2025]. **Task framing** sets the interpretive goal: "Summarize" and "Critique" applied to the same text produce fundamentally different outputs, because the model treats the text as content-to-compress in one case and content-to-evaluate in the other. **Contextual framing** sets the interpretive backdrop: "This email is from a frustrated customer" versus "This email is from a new user exploring the product" changes how every sentence in the email reads.

## Why it matters in prompting

Most prompt failures blamed on the model are actually framing failures. The model did exactly what the frame asked for. The human just set the wrong frame.

Consider: "Review this code." That is an instruction with no frame. The model might check for bugs, comment on style, suggest architectural changes, or all three. Add a frame: "Review this code from the perspective of a security auditor looking for input validation vulnerabilities." Now the model has a lens. It knows what to look at, what to weight, and what to ignore. The output will be narrower, more relevant, and more actionable.

Debnath et al. (2025) catalog several prompting techniques that are, at root, framing operations: System 2 Attention (S2A) prompting reframes the input by asking the model to regenerate only the relevant context before answering, effectively stripping the frame of irrelevant noise [src_paper_debnath2025]. Take a Step Back prompting asks the model to reframe a specific question as a more general one before answering, which improves reasoning on questions that are too narrow to trigger the right knowledge [src_paper_sahoo2025]. Both techniques work because they change the frame before the model reasons, not after.

## Why it matters in agentic workflows

In agent architectures, framing is how you make the same model behave differently in different roles. A research agent and a critique agent might use the same underlying model, but their system prompts frame the task differently: one is framed as "find and collect information," the other as "find weaknesses and contradictions." The frame defines the agent's personality within the pipeline.

Framing also governs how agents interpret ambiguous inputs from upstream. When a planner agent passes "the data suggests moderate growth" to an analyst agent framed as a risk assessor, the analyst will probe what "moderate" means and where the uncertainty lies. The same input passed to an analyst framed as a growth strategist will be treated as a green light. The data has not changed. The frame determines the response.

## What it changes in model behavior

Framing shifts the distribution of model attention and the selection of response patterns. Role frames measurably change output vocabulary, structure, and depth — a model framed as a "senior researcher" produces longer, more cited, more qualified text than one framed as a "junior assistant," even when the underlying instruction is identical [src_paper_schulhoff2025]. Task frames change what the model treats as the success criterion: "summarize" optimizes for compression, "evaluate" optimizes for judgment, "compare" optimizes for contrast.

The effect is not cosmetic. It reaches into the substance of the output. A model framed to look for problems will find problems that a model framed to describe strengths will miss entirely — not because the second model lacks the ability, but because the frame directed its attention elsewhere.

## Use it when

- The same material could be analyzed from multiple valid perspectives and you need a specific one
- The model is producing generic or unfocused output because it does not know what angle you want
- You are assigning different agents to the same material for different purposes (bullish vs. bearish analysis, legal vs. technical review)
- The task involves judgment and the criteria for judgment need to be oriented before generation begins
- You want to bias the model toward a particular cognitive mode: skepticism, creativity, precision, empathy

## Do not use it when

- The task is purely mechanical (format conversion, data extraction) and framing adds no information
- You want an unbiased overview and any frame would tilt the output
- The frame you would choose is so obvious that stating it is redundant ("You are a translator. Translate this.")
- You are unsure which frame is correct and risk steering the model toward a misleading interpretation

## Contrast set

**Closest adjacent abstractions**

- → perspective — Perspective is what you see from a particular position; framing is the act of choosing that position. Framing is the verb. Perspective is the result.
- → scope — Scope limits how *much* the model considers. Framing determines *how* the model considers it. A tight scope with no frame produces narrow but unfocused output.
- → context — Context provides *information* to the model. Framing provides *orientation*. You can have rich context with bad framing — the model will know a lot and still analyze it from the wrong angle.

**Stronger / weaker / narrower / broader relatives**

- → role prompting — Narrower. A specific technique for framing via persona assignment.
- → reframing — The act of changing a frame mid-conversation or mid-pipeline.
- → audience specification — A type of framing that orients the output toward a particular reader.
- → register — The tonal consequence of framing choices; how the frame changes the voice.

## Common failure modes

- **Unexamined default frame** → Every prompt has a frame, even when you don't set one. The model's default frame is "helpful general assistant," which is the wrong frame for almost every specialized task. If you did not set a frame, you are using the default, and the default is mediocre.

- **Frame-task mismatch** → Setting a frame that contradicts the task. "You are a creative storyteller. Now audit this financial statement for compliance." The model will either ignore the frame (wasting the tokens) or try to satisfy both (producing a whimsical audit no one asked for).

- **Frame without grounding** → Telling the model it is an "expert in quantum computing" without providing any quantum computing source material. The frame creates expectations the model cannot meet from its general training, increasing hallucination risk. Frames should match the material available.

## Prompt examples

### Minimal example

```text
You are a structural engineer reviewing a building plan for seismic safety.

Review the attached plan and identify any load-bearing elements
that do not meet the seismic requirements for Zone 4.
```

### Strong example

```text
I will give you the same customer complaint email three times.
Each time, analyze it from a different frame:

Frame 1 — Product team perspective:
What product deficiencies does this complaint reveal?
What feature gaps or UX failures are described?

Frame 2 — Support operations perspective:
What was the customer's journey? Where did the support process
fail them? What should the support team have done differently?

Frame 3 — Retention risk perspective:
How likely is this customer to churn based on the language
and specifics of the complaint? What would you offer to
retain them, and why?

For each frame, write 3-4 sentences. Do not repeat observations
across frames — each should surface something the others miss.
```

### Agentic workflow example

```text
Pipeline: Multi-Frame Analysis

Goal: Evaluate a proposed company acquisition from three perspectives.

Agent 1 — Bull Case Analyst (frame: opportunity)
System prompt: You are an M&A analyst building the strongest
possible case FOR this acquisition. Identify synergies, market
advantages, and strategic value. Be specific and cite the data
provided. You are not lying — you are advocating.

Agent 2 — Bear Case Analyst (frame: risk)
System prompt: You are an M&A analyst building the strongest
possible case AGAINST this acquisition. Identify integration risks,
cultural mismatches, regulatory hurdles, and valuation concerns.
Be specific and cite the data provided.

Agent 3 — Decision Synthesizer (frame: judgment)
System prompt: You are the CFO. You have received the bull case
and the bear case. Synthesize them into a one-page recommendation.
Do not average the two positions — weigh them against the company's
stated strategic priorities. Conclude with: PROCEED, RENEGOTIATE,
or WALK AWAY, with one paragraph of justification.

Each agent receives the same source material.
The frame is the only difference.
```

## Model-fit note

Role-based framing works reliably across all model tiers but with different depth. Frontier proprietary models internalize complex frames (multi-faceted professional roles, nuanced analytical stances) and maintain them across long outputs. Midsize open models follow explicit role frames but may drift from subtle framing cues in longer generations. Small open models respond to simple role frames ("You are a teacher") but lose more complex orientations ("You are a regulatory expert who prioritizes consumer safety over industry efficiency"). Reasoning-specialized models benefit from task framing (analytical vs. evaluative vs. comparative) more than role framing.

## Evidence and provenance

Role prompting as a major prompt component is documented in The Prompt Report's terminology and taxonomy [src_paper_schulhoff2025]. System 2 Attention and Take a Step Back prompting, both framing operations, are catalogued in Debnath et al. (2025) [src_paper_debnath2025] and Sahoo et al. (2025) [src_paper_sahoo2025]. The cognitive science of framing effects draws from Tversky and Kahneman's foundational work on prospect theory (1979, 1981), which is not repeated here but is cited as the intellectual origin of the concept. The observation that models respond to role frames with measurable vocabulary and depth changes is supported by Schulhoff et al.'s discussion of persona prompting and its effects [src_paper_schulhoff2025].

## Related entries

- **→ perspective** — the viewpoint that a frame produces
- **→ scope** — limits coverage; framing orients interpretation
- **→ context** — provides information; framing provides orientation
- **→ register** — the voice that results from framing choices
- **→ role prompting** — the most common framing technique
- **→ reframing** — changing the frame mid-task

---

> **Which Word?**
>
> *Framing* or *context*? Context is what the model knows — the documents attached, the conversation history, the system prompt. Framing is how the model *looks at* what it knows. You can have excellent context (all the right information is present) and terrible framing (the model treats it as background instead of foregrounding the part you care about). If your prompt has the right information but the wrong output, the problem is usually framing, not context.
