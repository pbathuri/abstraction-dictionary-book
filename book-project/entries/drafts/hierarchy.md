---
headword: "hierarchy"
slug: "hierarchy"
family: "core_abstraction"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# hierarchy

**Elevator definition**
Hierarchy is the organization of prompt information in ordered levels of abstraction, from general context at the top to specific action at the bottom, so the model reads importance structurally.

## What it is

Models read prompts sequentially, and what comes first frames everything that follows. This is not a design preference. It is a consequence of how attention works. Earlier tokens exert disproportionate influence on the interpretation of later tokens. Hierarchy exploits this by arranging information so that the most general, most important framing appears first, and the most specific, most actionable instructions appear last.

In well-structured code, you do not define a variable inside a nested loop and then try to reference it three functions later. You scope it where it belongs. Hierarchy in prompts follows the same logic. A system prompt sets the broadest context: who the model is, what the task domain is, what the general constraints are. The next level narrows: what specific task to perform. The next narrows further: how to format the output, what criteria to apply, what edge cases to handle. The final level is the concrete input data or question.

This is not arbitrary. It mirrors how human experts process briefings. A military intelligence officer reads the strategic picture first, then the operational situation, then the tactical detail, then the specific question. Each level inherits from and is constrained by the level above. A tactically brilliant recommendation that violates the strategic objective is wrong, no matter how internally consistent it is. Hierarchy encodes the same relationship for models: the system prompt constrains the task, the task constrains the instructions, the instructions constrain the output format.

→ Decomposition produces hierarchy as a byproduct. When you break a complex task into sub-tasks, you naturally create levels: the goal, the phases, the steps within each phase, the criteria for each step. But hierarchy is not only a product of decomposition. It is also a design principle applied to individual prompts that are not decomposed at all. Even a single-turn prompt benefits from hierarchical ordering: context first, task second, constraints third, input last.

## Why it matters in prompting

Position effects in language models are well documented. Models attend differently to content at the beginning, middle, and end of a prompt. The beginning sets the interpretive frame. The end receives recency-weighted attention. The middle is where information goes to be underweighted — a phenomenon sometimes called the "lost in the middle" problem in long-context scenarios.

Hierarchy lets you work with these effects instead of against them. Place the most important contextual information at the top where it sets the frame. Place the specific instructions and input near the end where recency helps. Place supporting details, examples, and reference material in the middle, where it is available if the model needs it but does not dominate interpretation.

Without hierarchy, prompts become flat lists of instructions where the model must infer what matters most. This works for short, simple prompts. It fails predictably for anything complex. A 500-word flat prompt with ten instructions at equal structural weight forces the model to prioritize on its own, and its priority ranking may not match yours.

## Why it matters in agentic workflows

Agent architectures are hierarchical by nature. An orchestrator delegates to planners. Planners delegate to executors. Executors delegate to tools. Each level operates at a different abstraction: the orchestrator thinks in goals, the planner thinks in tasks, the executor thinks in actions, the tool thinks in operations.

When hierarchy is explicit in the agent's instruction structure, the agent can reason about which level of abstraction a decision belongs to. Should it retry a failed API call (tactical) or rethink the approach (strategic)? The answer depends on where in the hierarchy the failure occurred. An agent with a flat instruction set treats all failures the same. An agent with hierarchical instructions can escalate appropriately — retry at the action level, replan at the task level, consult the orchestrator at the goal level.

Hierarchy also structures the context that flows between agents. Each handoff should include only the information relevant to that agent's level of abstraction, plus a summary of the level above for orientation. Passing the orchestrator's full context to every executor is like giving every factory worker the CEO's strategic plan — it is not wrong, but it is noise, and noise competes with signal for attention.

## What it changes in model behavior

Hierarchically structured prompts produce more organized outputs. When the prompt moves from general to specific, the model's response tends to mirror that structure — opening with the big picture, then narrowing to details, then delivering the concrete answer. More importantly, hierarchical prompts reduce instruction-following errors in complex tasks because the model can resolve conflicts between instructions by treating higher-level instructions as more authoritative, matching how the hierarchy presented them.

## Use it when

- When the prompt exceeds roughly 200 words and contains multiple instructions at different levels of importance
- When you are writing system prompts for agents that need to distinguish strategic goals from tactical actions
- When the model produces output that addresses details correctly but misses or contradicts the main objective
- When building multi-agent pipelines where context must be filtered by relevance at each handoff
- When you need the model to understand that some constraints are non-negotiable and others are preferences

## Do not use it when

- When the prompt is short and simple enough that ordering does not matter
- When all instructions are genuinely at the same level of importance and imposing a false hierarchy would distort priorities
- When the task is a single atomic operation with no nested structure

## Contrast set

- → decomposition — decomposition breaks a task into pieces; hierarchy arranges those pieces (and everything else) in levels of abstraction. Decomposition is an operation. Hierarchy is a structure that results from decomposition but can also be applied independently.
- → scope — scope defines what is included and excluded; hierarchy orders what is included by importance and abstraction level. A well-scoped prompt still needs hierarchy to signal what matters most within that scope.
- → context — context is the information provided; hierarchy is how that information is arranged. Rich context with flat structure is like a well-stocked library with no catalog.

## Common failure modes

- **Inverted hierarchy** → Putting specific instructions first and context last. The model interprets the instructions without the frame, then encounters the context too late to reinterpret. This is like giving someone driving directions before telling them the destination. They will follow the turns, but they cannot course-correct if they miss one.
- **False hierarchy** → Imposing structural importance (headings, numbered sections, bold text) on content that is actually at the same level. The model reads structural emphasis as a priority signal. If you mark everything as high priority, nothing is.
- **Missing middle level** → Jumping from a high-level goal directly to granular instructions without an intermediate task description. The model executes the instructions but loses the thread of why — producing locally correct steps that do not cohere into a meaningful whole.

## Prompt examples

### Minimal example

```text
You are a senior product manager reviewing a feature proposal.

The company's current priority is reducing churn among
enterprise customers.

Review the attached proposal and answer: does this feature
directly address enterprise churn? Give a yes/no with
a one-paragraph justification.
```

### Strong example

```text
CONTEXT: You are a technical writer for a developer tools company.
Your audience is mid-level backend engineers who use Python daily.
The company style guide requires: active voice, present tense,
code examples for every concept, no marketing language.

TASK: Write a migration guide for users upgrading from v2 to v3
of the authentication library.

STRUCTURE:
1. Opening paragraph: what changed and why (max 60 words)
2. Breaking changes: list each breaking change with:
   - What it was in v2 (code snippet)
   - What it is now in v3 (code snippet)
   - What the user must change in their code
3. New features: list each with a one-sentence description
   and a minimal code example
4. Deprecations: list any v2 features that still work but
   are deprecated, with the recommended replacement

CONSTRAINTS:
- Do not reference internal ticket numbers or roadmap items
- If a change has no direct v2 equivalent, say so explicitly
- Keep total length under 1,500 words
```

### Agentic workflow example

```text
Pipeline: Document Analysis System

LEVEL 1 — Orchestrator
Goal: Produce a risk assessment of the attached contract.
Success criteria: all material risks identified, each with
severity rating and mitigation recommendation.
Escalation policy: if any agent reports low confidence (<0.7),
pause the pipeline and request human review.

LEVEL 2 — Planner Agent
Task: Decompose the risk assessment into analysis phases.
Assign each phase to the appropriate specialist agent.
Ensure phases execute in dependency order.

LEVEL 3 — Specialist Agents
  Agent A (Legal Risk): Identify clauses that expose the
  company to liability. Classify each as HIGH, MEDIUM, or LOW.
  Agent B (Financial Risk): Identify payment terms, penalties,
  and cost escalation clauses. Flag any uncapped obligations.
  Agent C (Operational Risk): Identify delivery timelines,
  SLAs, and performance requirements that may be unachievable.

LEVEL 4 — Synthesis Agent
Input: Combined output from all Level 3 agents.
Task: Merge findings, remove duplicates, rank all risks by
severity, and produce a single-page executive summary with
the top 5 risks and recommended actions.
```

## Model-fit note

Hierarchy is most critical for long-context interactions. Frontier models with large context windows can attend to more content, but their attention is still not uniform — they benefit from hierarchical structure that signals what to prioritize. Smaller models with limited context windows benefit even more, because hierarchy helps them allocate their constrained attention budget to the most important content. For all tiers, hierarchy in the prompt tends to produce hierarchy in the output, which is usually desirable.

## Evidence and provenance

The "lost in the middle" effect — models underweighting information in the middle of long prompts — is documented in Liu et al. (2023) and has been widely replicated. The Prompt Report discusses prompt component ordering and its effects on model performance [src_paper_schulhoff2025]. The principle that hierarchical information organization improves instruction-following is supported by research on structured prompting and instruction decomposition [src_paper_sahoo2025].

## Related entries

- → decomposition — the operation that most often produces hierarchy; decomposition breaks tasks into steps, hierarchy arranges them by level.
- → context — hierarchy determines how context is ordered and weighted within the prompt.
- → scope — scope sets boundaries; hierarchy organizes what is within those boundaries by importance.
