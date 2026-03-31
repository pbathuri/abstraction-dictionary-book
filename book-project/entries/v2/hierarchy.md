# hierarchy

> Put the important stuff first. The model reads top-down and treats position as priority.

## The Scene

Clap/OpsPilot's original agent instructions were a flat wall of text: role description, output format, constraints, task details, edge cases — all at the same structural level, jumbled into one paragraph. The code-analysis agent would nail the formatting but miss the strategic goal, or follow the constraints but ignore the role entirely. Different runs prioritized different parts of the prompt. The output felt random.

The fix was reorganizing, not rewriting. I stacked the instructions like a military briefing: strategic context first (what OpsPilot is and why this analysis matters), then the operational task (produce REPO_REALITY.md for this specific module), then tactical details (formatting, edge cases, output schema). Same words, different order. The agent stopped contradicting its own purpose because the purpose came first, and everything downstream inherited from it.

## What This Actually Is

Hierarchy is the arrangement of prompt information from general to specific, from non-negotiable to nice-to-have. It exploits how attention works: earlier tokens frame the interpretation of later ones. A system prompt sets the broadest context. The task narrows it. Constraints narrow further. Input data comes last.

This isn't aesthetic preference — it's architectural. When instructions compete (and in long prompts they will), the model resolves conflicts by treating earlier instructions as more authoritative. If your format spec comes before your strategic goal, don't be surprised when the model produces a perfectly formatted answer to the wrong question.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| A flat paragraph mixing role, task, and format | "CONTEXT: [who you are] TASK: [what to do] FORMAT: [how to deliver]" with clear section breaks | Structural layers signal priority |
| "Also, remember you're a financial analyst" (buried in paragraph 3) | Put the role definition as the very first line of the prompt | Position encodes importance |
| Ten instructions at equal weight | Number them, and mark 1-3 as MUST and 4-10 as SHOULD | Explicit priority within a level |
| "Here's some background... and also the question is..." | Separate context from query with a visual break and label: "QUESTION:" | The model should know when background ends and task begins |
| All constraints in one list | Group into hard constraints (non-negotiable) and soft preferences (optimize for) | Two-tier hierarchy inside the constraint block |

## Before → After

From Clap/OpsPilot — reorganizing the code-analysis agent:

> **Before (flat)**
> ```
> Analyze the codebase. You are a senior code analyst. Output
> as markdown. Focus on architecture gaps. Don't speculate
> about intended design. Check each module for test coverage.
> The product north star is in the attached document. Only
> describe what exists. Format as one section per module.
> ```
>
> **After (hierarchical)**
> ```
> ROLE: Senior code analyst producing a reality check — what
> the code actually does today, with no speculation about intent.
>
> STRATEGIC CONTEXT: OpsPilot needs to compare actual code
> behavior against the product north star (attached).
>
> TASK: Produce REPO_REALITY.md — one section per module in src/.
>
> PER MODULE:
> - Purpose (observed, not assumed)
> - Dependencies
> - Test coverage status
>
> CONSTRAINTS:
> - MUST: Inspect source files, not just docs
> - MUST: Include every directory in src/
> - MUST NOT: Speculate about intended architecture
> - SHOULD: Flag modules with zero test coverage
>
> OUTPUT: Markdown, one H2 per module.
> ```
>
> **What changed:** The strategic frame ("reality check, no speculation") now governs every downstream decision. The agent stopped producing aspirational architecture reviews because the prohibition on speculation sits at the top, not buried in a list.

## Try This Now

Take any prompt longer than 100 words. Highlight each sentence and label it: C (context), T (task), F (format), or X (constraint). Now rearrange so all C's come first, then T, then X, then F. Run both versions. The reorganized version will follow constraints more consistently — especially the ones that were buried in the middle before.

## When It Breaks

- **Inverted hierarchy** — Specific instructions first, context last. The model interprets the instructions without the frame, then encounters context too late to reinterpret. Like giving driving directions before the destination.
- **False hierarchy** — Bolding everything, numbering everything as priority 1, using ALL CAPS throughout. If everything is top priority, nothing is. Structural emphasis only works when it's selective.
- **Missing middle level** — Jumping from "you are an analyst" directly to "output as JSON with these 12 fields." The model executes the format but loses the thread of why. Add the task-level instruction between role and format.

## Quick Reference

- **Family:** Core abstraction
- **Adjacent:** → decomposition (produces hierarchy as byproduct), → scope (sets boundaries; hierarchy orders within them), → context (hierarchy determines how context is arranged)
- **Model fit:** Critical for long-context interactions. All models benefit — frontier models tolerate flat prompts better but still perform more consistently with hierarchical structure. Small models with limited context windows benefit most, because hierarchy helps them allocate constrained attention to what matters.
