---
headword: "progressive disclosure"
slug: "progressive_disclosure"
family: "context_architecture"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# progressive disclosure

**Elevator definition**
Progressive disclosure is the practice of revealing information to a model in stages, giving it what it needs when it needs it rather than everything at once.

## What it is

The instinct when prompting a language model is to front-load. Dump everything into the context window — the background, the data, the constraints, the examples, the edge cases — and hope the model sorts it out. For simple tasks, this works. For complex ones, it fails in a specific and predictable way: the model drowns.

Progressive disclosure is the antidote. Borrowed from user interface design — where it describes showing only the controls a user needs at each step, revealing complexity gradually — the concept translates directly to prompt engineering and agent architecture. Instead of giving a model all information in a single context, you structure the interaction so that each stage receives only the information relevant to that stage's task.

The principle rests on a hard constraint and a soft one. The hard constraint is the context window. Every model has a finite number of tokens it can process, and stuffing the window with irrelevant material pushes out material that matters. Even with 128K or 200K token windows, attention is not uniform. Research on long-context models consistently shows that information in the middle of a long context is retrieved less reliably than information at the beginning or end — the "lost in the middle" phenomenon documented by Liu et al. (2023) [src_paper_sahoo2025]. Progressive disclosure sidesteps this entirely by never putting the information in a position where it can be lost.

The soft constraint is → salience. Even within the attention window, a model's ability to identify what matters degrades as irrelevant material accumulates. A 500-token prompt with 300 tokens of relevant context has a signal-to-noise ratio of 0.6. A 5,000-token prompt with the same 300 tokens of relevant context, buried among 4,700 tokens of background, has a signal-to-noise ratio of 0.06. The model must now find the needle. Progressive disclosure keeps the haystack small at every step.

The implementation takes several forms. **Sequential prompting** breaks a task into stages, each with its own prompt that includes only the information for that stage. Stage one might receive the raw data and produce a summary. Stage two receives the summary (not the raw data) and a rubric, and produces an evaluation. Stage three receives the evaluation and the original question, and produces a recommendation. At no point does any stage receive the full context. Each stage receives the minimum viable context for its task.

**Conditional disclosure** reveals information based on the model's intermediate output. If the model's initial analysis identifies a compliance risk, the next prompt discloses the relevant regulatory text. If no compliance risk is identified, the regulatory text is never loaded. This saves tokens, keeps the context focused, and prevents the regulatory text from biasing the analysis toward compliance issues when none exist.

**Layered context** provides a high-level overview first, then allows the model to "drill down" into specific areas. An agent might receive a one-paragraph summary of a 50-page report and be asked to identify which sections warrant detailed review. Only those sections are then provided in full. This mimics how human analysts work: skim first, read deeply second.

Progressive disclosure is not just an efficiency technique. It is a quality technique. A model that receives precisely the context it needs for a specific sub-task consistently outperforms a model that receives everything and is asked to find what it needs. The latter is performing two tasks — retrieval and reasoning — when you only wanted one.

## Why it matters in prompting

Long prompts with front-loaded context are the most common design failure in non-trivial prompt engineering. The prompt author adds context because they are not sure what the model will need, so they include everything. The model, faced with a wall of text, does what any reader does with a wall of text: it skims. Important details are missed. Irrelevant details are incorporated. The output is mediocre not because the model is inadequate but because the prompt architecture is.

Progressive disclosure replaces this with structure. Instead of asking "Did I include enough context?" the question becomes "Does each stage have exactly the context it needs?" This reframing produces prompts that are shorter at each step but collectively more effective than a single monolithic prompt.

The technique also makes prompts more debuggable. When a monolithic prompt produces bad output, the failure could be anywhere. When a staged prompt produces bad output, you can inspect each stage's input and output independently, identify where the failure occurred, and fix that specific stage.

## Why it matters in agentic workflows

In multi-agent systems, progressive disclosure is not optional — it is architectural. An agent that receives the entire pipeline's accumulated context will spend most of its attention on information intended for other agents. The orchestrator's job is to scope each agent's context to precisely what that agent needs.

This is especially critical when agents have different roles. A Research Agent needs source materials. A Verification Agent needs the claims to check and the source excerpts that support them — not the full source documents. A Synthesis Agent needs verified claims and the original question — not the raw sources, not the verification logs. Each agent's context should be assembled specifically for its role, disclosing only what that role requires.

## What it changes in model behavior

Progressive disclosure reduces hallucination, improves factual precision, and increases output relevance. By limiting context to task-relevant information at each stage, the model has fewer opportunities to confabulate from irrelevant material and a higher probability of engaging deeply with the material that matters. Staged prompts also produce more consistent outputs because each stage has a narrower task and less ambiguity about what is expected.

## Use it when

- The total context needed for the task exceeds what a model can attend to effectively in a single pass
- The task has natural stages where intermediate outputs become inputs for subsequent stages
- You are building multi-agent pipelines and need to control what each agent sees
- Previous attempts with monolithic prompts produced output that ignored key details or incorporated irrelevant ones
- The task involves conditional logic — some information is only relevant depending on earlier findings

## Do not use it when

- The task is simple enough that all necessary context fits comfortably in a short prompt
- The information is so interconnected that splitting it across stages would force the model to reason without critical context
- The overhead of managing multi-stage prompts exceeds the benefit (prototyping, one-off queries)

## Contrast set

- → **context windowing** — Context windowing manages how much information fits in the window. Progressive disclosure manages *when* information enters the window. They are complementary: windowing is the budget, disclosure is the spending plan.
- → **salience** — Salience describes the relative importance of information. Progressive disclosure is a technique for maintaining high salience by excluding low-salience material from each stage.
- → **decomposition** — Decomposition breaks a *task* into sub-tasks. Progressive disclosure breaks the *context* into stage-appropriate portions. You often do both together, but they address different things: task structure vs. information structure.
- → **context budget** — The total token allocation. Progressive disclosure is a strategy for spending that budget wisely across stages rather than blowing it all at once.

## Common failure modes

- **Under-disclosure** — Withholding information that a stage genuinely needs, producing outputs that are confidently wrong because the model lacked critical context. Fix: for each stage, explicitly list what information the model needs to perform its task, and verify it is present.

- **Disclosure leakage** — Passing forward not just the intermediate result but the entire context from the previous stage, recreating the monolithic context problem across steps. Fix: each stage should produce a structured output that the next stage consumes. Raw inputs should not propagate forward unless explicitly needed.

- **Premature synthesis** — Asking the model to reach conclusions at an early stage when it has only partial information, then anchoring all subsequent stages on that premature conclusion. Fix: early stages should report findings, not conclusions. Conclusions belong in the final stage when all relevant information has been disclosed.

## Prompt examples

### Minimal example

```text
Stage 1: Read the attached 10-K filing. List the five most
significant risk factors described in the filing, with one
sentence each.

Stage 2: [receives only the five risk factors from Stage 1]
For each risk factor, assess the likelihood (high/medium/low)
and potential financial impact. Use the revenue figures
provided below.
```

### Strong example

```text
This analysis proceeds in three stages. You will receive
information for each stage separately.

Stage 1 — Data Overview
Here is a summary table of customer support tickets from Q4.
Identify the three most common complaint categories and the
average resolution time for each. Output as structured JSON.

[Stage 1 output received]

Stage 2 — Root Cause Analysis
Here are 10 representative tickets from each of the three
categories you identified (30 total). For each category,
identify the underlying root cause. You do not need the
summary table — work from these individual tickets.

[Stage 2 output received]

Stage 3 — Recommendation
Here are your root cause findings and the company's current
support workflow documentation. Recommend three specific
process changes, each tied to a root cause you identified.
Estimate effort (low/medium/high) for each change.
```

### Agentic workflow example

```text
Pipeline: Progressive Legal Document Review

Agent 1 — Triage Agent
Input: Full contract (30 pages)
Task: Read the contract and produce a structured summary:
  - Parties involved
  - Key obligations per party (max 3 each)
  - Termination conditions
  - Flagged clauses: any non-standard or unusual provisions
Output: Structured summary (discard full contract text)

Agent 2 — Risk Analyst
Input: Structured summary from Agent 1 + company risk policy
Task: Evaluate flagged clauses against risk policy. For each:
  classify as acceptable / needs_modification / unacceptable.
Output: Risk assessment table

Agent 3 — Clause Reviewer (conditional)
Input: Only the flagged clauses classified as needs_modification
  or unacceptable, extracted from the original contract
Task: For each problematic clause, draft specific revision
  language that addresses the identified risk while preserving
  the commercial intent.
Output: Revision proposals with tracked changes
```

## Model-fit note

Progressive disclosure benefits all model tiers but is most critical for smaller models with limited context windows or weaker long-context retrieval. Frontier models with 128K+ windows tolerate monolithic prompts better but still produce higher-quality output with staged disclosure, particularly on analytical tasks. For small and midsize models, progressive disclosure is often the difference between useful and useless output on complex tasks. The overhead of managing stages is always repaid in output quality.

## Evidence and provenance

The "lost in the middle" phenomenon is documented by Liu et al. (2023), showing that LLMs struggle to retrieve information from the middle of long contexts [src_paper_sahoo2025]. The UI design principle of progressive disclosure originates with J.M. Keller (1987) and was popularized in software design by Jakob Nielsen. Its application to prompt engineering is a practitioner convention documented across prompt engineering guides and framework documentation, reflecting the general finding that scoped context improves output quality.

## Related entries

- **→ context windowing** — the constraint that progressive disclosure manages
- **→ salience** — what progressive disclosure preserves by limiting context
- **→ decomposition** — breaking tasks into stages, often paired with staged disclosure
- **→ signal-to-noise ratio** — the metric progressive disclosure optimizes
