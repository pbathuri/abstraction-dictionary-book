---
headword: "vagueness"
slug: "vagueness"
family: "failure_mode"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# Vagueness

**Elevator definition** Instructions so broad that the model must invent the specifics you failed to provide, producing output that is technically responsive but practically useless.

## What it is

Vagueness is the most common prompting failure mode, and the most forgivable, which is why it persists. A vague prompt is one that describes a general direction without providing the specifics needed to arrive anywhere in particular. "Analyze this data." "Write something about marketing." "Help me with my code." Each of these is a valid request in the sense that a human colleague would ask follow-up questions to clarify. A language model will not ask. It will answer — confidently, fluently, generically — and you will receive 500 words of well-structured nothing.

Vagueness is not the same as brevity. "Summarize this in three bullet points for a CFO" is brief but not vague. "Summarize this" is both brief and vague. The distinction lies in whether the instruction constrains the output space enough for the model to produce something useful without guessing. Specificity collapses the space of possible responses toward the one you actually want. Vagueness leaves that space wide open, and the model fills it with the most statistically likely response — which is, by definition, the most generic one.

The mechanism is straightforward. Language models generate output by predicting the most probable next token given the context. A vague prompt provides weak context, so the model falls back on broad priors: common phrasings, generic structures, safe opinions, middle-of-the-road analysis. The output reads like it was written by someone who has read a lot but experienced nothing — because that's exactly what happened.

Vagueness compounds in multi-step workflows. If Stage 1 produces a vague output (because its prompt was vague), Stage 2 receives vague input, produces vague output, and Stage 3 receives something so thoroughly diluted that no amount of prompting can rescue it. Vagueness is entropy. Each step increases disorder unless specific instructions at each stage counteract the drift.

There are several species of vagueness worth distinguishing:

**Goal vagueness** — The prompt doesn't specify what success looks like. "Analyze the sales data" could mean: identify trends, find anomalies, compare to benchmarks, project future performance, or calculate summary statistics. Without a stated goal, the model picks one — or worse, tries to do all of them shallowly.

**Audience vagueness** — The prompt doesn't say who the output is for. A summary for a CEO reads differently from a summary for an engineer, which reads differently from a summary for a regulator. When the audience is unspecified, the model writes for no one in particular — which means it writes for everyone poorly.

**Format vagueness** — The prompt doesn't specify the output structure. Should the response be a paragraph, a table, a numbered list, a JSON object, a code block? The model guesses, and its guess may not match your expectation.

**Scope vagueness** — The prompt doesn't bound what should be included or excluded. "Write about the company's performance" — over what period? Compared to what? Including which metrics? Excluding what?

The fix for vagueness is not verbosity. You don't need a 500-word prompt to avoid vagueness. You need the right 30 words: a clear goal, a defined audience, a specified format, and a bounded scope. "Identify the three largest cost drivers in Q4 2025, compare each to Q3, and present findings as a table for the finance team." That's one sentence. It's specific. It works.

## Why it matters in prompting

Vagueness is the default state of human communication. We rely on shared context, body language, and the ability to ask clarifying questions to resolve ambiguity in real time. Prompting strips all of that away. There is no shared context (the model doesn't know your project, your goals, or your preferences unless you state them). There is no back-and-forth (in a single-turn interaction). There is just the prompt and the model's best guess at what you meant.

This means that the prompt must carry the full burden of specification that, in human conversation, is distributed across multiple exchanges. The discipline of prompting is, at its core, the discipline of eliminating vagueness — not perfectly, but sufficiently. You will never specify everything. But you must specify enough that the model's remaining degrees of freedom are small enough to land somewhere useful.

## Why it matters in agentic workflows

In agentic systems, vagueness in the initial task description propagates through every downstream agent. An orchestrator that receives a vague goal produces a vague plan. A planner that receives a vague plan produces vague steps. Executors that receive vague steps produce generic outputs. Each agent does its best, but "its best" is bounded by the specificity of what it received.

The fix is specificity at the source. The system prompt or task description that initializes an agentic workflow must be precise enough that the first agent in the chain can act without guessing. If it can't be precise (because the user's request is genuinely exploratory), the first agent's job should be to disambiguate — to ask clarifying questions or generate a specific interpretation for the user to approve — before any downstream processing begins.

## What it changes in model behavior

Vague prompts activate the model's generic response mode — broad coverage, moderate depth, consensus opinions, safe phrasing. Specific prompts activate a more targeted mode — narrower coverage, greater depth, more decisive claims, more structured output. The same model that produces a forgettable five-paragraph essay from a vague prompt can produce incisive, actionable analysis from a specific one. The model didn't get smarter. The prompt got better.

## Use it when

This is a failure mode entry. You never *want* vagueness. However, recognizing vagueness in your prompts allows you to fix it:

- When model output feels generic, check the prompt for goal vagueness
- When the format is wrong, check for format vagueness
- When the depth is wrong, check for scope vagueness
- When the tone is wrong, check for audience vagueness
- When chained prompts produce degrading quality, check for vagueness at the first stage
- When multiple people get wildly different outputs from the "same" prompt, vagueness is why

## Do not use it when

- You are deliberately leaving the model creative latitude (e.g., brainstorming, free writing) — but even then, constrain the domain
- You are testing a model's default behavior for evaluation purposes
- The task genuinely has no wrong answer and any response is useful (rare)

## Contrast set

- **Underspecification** — Vagueness means the instruction is too broad. Underspecification means specific pieces of information are missing. "Analyze the data" is vague. "Analyze Q4 sales data" is specific but underspecified (missing: for whom? in what format? compared to what?). Vagueness is a wide lens. Underspecification is a missing piece.
- **Ambiguity** — Ambiguity means the instruction can be interpreted in multiple distinct ways. "Review this code" is ambiguous — review for correctness? Performance? Style? Security? Vagueness and ambiguity overlap but aren't identical. A prompt can be vague without being ambiguous (it's clear what general area is meant, just not specific enough). A prompt can be ambiguous without being vague (two very specific interpretations are both plausible).
- **Overspecification** — The opposite of vagueness: so many constraints that the model has no room to produce useful output, or the constraints conflict. The sweet spot is between vagueness and overspecification.
- **Specificity** — The antidote to vagueness. Specificity means providing enough detail about goal, audience, format, and scope that the model's output space collapses toward what you need.

## Common failure modes

- **Vagueness laundering** — The prompt sounds specific because it uses technical or formal language, but the actual instruction is still vague. "Conduct a comprehensive analysis leveraging cross-functional insights" says nothing. The formality masks the emptiness. Fix: strip the jargon and ask: does this prompt tell the model *what to produce, for whom, in what format, at what scope*?
- **Assumed context** — The prompter assumes the model knows their project, their data, their goals — because a colleague would. The model doesn't. It fills the gap with generic assumptions. Fix: state context explicitly. What is this data? What are you trying to decide? What does the reader already know?
- **The vagueness cascade** — Vagueness in an early stage produces generic output, which becomes generic input for the next stage, compounding genericity until the final output is content-free. Fix: enforce specificity gates at each pipeline stage. Validate that each stage's output meets minimum specificity criteria before passing it forward.

## Prompt examples

Minimal (vague — the failure case):

```
Analyze this data and give me insights.
```

Strong (specific — the fix):

```
You are given Q4 2025 sales data for three product lines (Enterprise, Mid-Market, SMB).

Task: Identify the single largest revenue decline across all three product lines.
For that decline:
1. Quantify the drop (absolute and percentage vs. Q3 2025)
2. Identify the top 2 contributing factors based on the data
3. Recommend one specific action the sales team should take in Q1 2026

Format: Numbered list, 150-200 words total.
Audience: VP of Sales (assumes familiarity with product lines, not with raw data).
```

Agentic workflow (specificity enforcement at task intake):

```yaml
task_intake:
  agent: "disambiguator"
  prompt: |
    The user has submitted a task. Before processing, verify it meets minimum specificity:
    - Goal: Is the desired outcome stated? (not just "analyze" or "help with")
    - Scope: Are boundaries defined? (time period, data set, domain)
    - Format: Is the output format specified?
    - Audience: Is the reader/user identified?

    If any element is missing, generate a clarifying question for each gap.
    Do NOT proceed to execution until all four elements are present.

    User task: "{user_input}"

  on_incomplete:
    action: "return_questions_to_user"
  on_complete:
    action: "forward_to_planner"
    context: "{enriched_task_with_specifics}"
```

## Model-fit note

All models suffer from vague prompts, but they suffer differently. Larger models produce more sophisticated-sounding generic output — which is arguably worse, because it's harder to recognize as generic. Smaller models produce obviously shallow output from vague prompts, making the problem visible faster. Neither size compensates for vagueness. Specificity is a prompt property, not a model capability. No model is smart enough to make a vague prompt work consistently.

## Evidence and provenance

The relationship between prompt specificity and output quality is well-documented in the prompt engineering literature (OpenAI Cookbook, 2023; Anthropic prompt design docs, 2024). The taxonomy of vagueness types (goal, audience, format, scope) synthesizes distinctions from writing pedagogy (Strunk & White's "be specific" rule) and requirements engineering (the IEEE 830 standard for software requirements specifications, which defines vagueness as a requirements defect). Empirical work on prompt sensitivity (Debnath et al., 2025) quantifies how minor specificity changes produce large output variance.

## Related entries

- **underspecification**
- **specificity**
- **prompt drift**
- **overcompression**
- **ambiguity**
