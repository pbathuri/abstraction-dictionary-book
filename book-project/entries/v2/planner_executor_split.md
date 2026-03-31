# planner-executor split

> One agent decides what to do. A different agent does it. Separate the thinking from the doing.

## The Scene

Karpathy's `program.md` is the cleanest example I've seen. It's not code. It's a plan — a multi-step research workflow written in plain English with phases, verification gates, and rollback conditions. The LLM reads `program.md` and executes it step by step: search, read papers, extract claims, evaluate novelty, write sections, verify citations, compile. The plan is the program. The executor follows it.

I borrowed this pattern for Clap/OpsPilot. The first version had a single agent that planned and executed simultaneously. It would start analyzing a module, get distracted by an interesting code pattern, abandon its plan to investigate, lose track of which modules it had covered, and produce a report with three modules analyzed deeply and seven not mentioned at all. Splitting into a Planner (produce a numbered list of modules to analyze with one-sentence scope for each) and an Executor (follow the list, one module at a time, report results) solved it immediately. The Planner can't get distracted because it's not executing. The Executor can't lose the plan because it's written down.

## What This Actually Is

The planner-executor split separates reasoning from action. The Planner analyzes the task, breaks it into steps, sequences them, and produces a plan as a written artifact. The Executor takes that plan and carries it out, step by step, without re-reasoning about whether different steps would be better.

The key insight: when a single model plans and executes in the same context, it frequently abandons its own plan mid-execution. Splitting the roles *externalizes* the plan as an artifact the executor can reference. That externalization is what makes complex tasks reliable. The quality ceiling of the system is set by the plan. A brilliant executor can't salvage a bad plan. A mediocre executor often succeeds with a great one.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Analyze the data and write a report" (plan + execute in one shot) | "STAGE 1: Produce a plan of 4-6 steps. Each step: action, input, output. Do NOT execute. STAGE 2: Follow the plan exactly. For each step, produce the specified output" | Explicit separation prevents plan abandonment |
| "Research competitors and compare pricing" | Planner prompt: "List the 5 steps needed to compare competitor pricing. For each step, name the tool and the expected output." Executor prompt: "Execute step [N] exactly as specified. Return the specified output. Do not add steps" | Different prompts for different roles |
| Giving the executor freedom to improvise | "Do not add steps. Do not skip steps. Do not reinterpret the plan. If you cannot complete a step, report what is missing and stop" | Executor creativity is a bug, not a feature |
| One expensive model doing everything | Planner: strong reasoning model (Opus). Executor: fast/cheap model (Haiku). The plan provides enough scaffolding that the executor doesn't need to reason hard | Asymmetric model allocation — the split's economic advantage |
| A plan that never adapts | "After steps 2 and 4, send executor results to the planner for plan revision. If early results invalidate later steps, the planner updates the plan" | Checkpoints without collapsing back to single-agent |

## Before → After

From Clap/OpsPilot — separating the code analysis planner from executor:

> **Before (single agent, plan + execute)**
> ```
> Analyze the codebase. For each module in src/, describe
> its purpose, dependencies, and test coverage. Produce
> REPO_REALITY.md.
> ```
> (Agent covers 3/10 modules deeply, forgets the rest)
>
> **After (planner-executor split)**
> ```
> PLANNER:
> Input: ls output of src/ directory
> Task: Produce a numbered plan. For each module directory:
>   - Module name
>   - Files to inspect (list them)
>   - Output: one section of REPO_REALITY.md with fields:
>     purpose, dependencies, test_coverage_status
> Do NOT analyze any module. Only produce the plan.
>
> EXECUTOR:
> Input: The plan from Planner + access to source files
> Task: Execute each step in order.
>   - For each module, inspect the actual source files listed
>   - Produce the specified output fields
>   - If a module cannot be analyzed (e.g., binary, empty),
>     mark as BLOCKED with reason and proceed to next
>   - Do not skip steps. Do not add modules not in the plan
>
> CHECKPOINT (after step 5):
> Send partial results to Planner. If any BLOCKED module
> has alternatives, Planner updates remaining plan steps.
> ```
>
> **What changed:** Every module gets analyzed because the plan lists them all and the executor checks them off. No module gets forgotten because the plan is a written artifact, not a mental model. Debugging is easy: was the plan wrong (planner failure) or was the execution wrong (executor failure)?

## Try This Now

Take your most complex recent prompt — the one that tried to do too much. Run it in two stages:

```
STAGE 1 (Planning only):
Break this task into 3-6 steps. For each step:
- Action to perform
- Input required
- Output produced
- How you'd know this step succeeded
Do NOT execute any steps.

STAGE 2 (Execution only):
Here is the plan: [paste Stage 1 output]
Execute each step in order. Produce only the specified
output for each step. If you cannot complete a step,
report what's missing and stop.
```

Compare the result against a single-pass attempt. The split version will be more complete and more consistent.

## When It Breaks

- **Over-granular planning** — The planner produces 47 micro-steps, each trivial. The overhead of managing them exceeds the original task's complexity. Fix: constrain the planner to 3-8 steps with a minimum step complexity.
- **Plan-executor mismatch** — The planner assumes tools the executor doesn't have. "Query the database" when the executor has no database access. Fix: include the executor's available tools in the planner's context.
- **Frozen plans** — The plan doesn't adapt to unexpected early results. The executor follows the plan into a wall. Fix: implement checkpoints where results are reviewed and the plan is revised if needed.

## Quick Reference

- **Family:** Agent workflow
- **Adjacent:** → decomposition (the skill the planner uses), → orchestration (coordinates planner and executor), → pipeline (the planner-executor split is a two-stage pipeline pattern), → delegation (the planner delegates to the executor)
- **Model fit:** Strong reasoning models (GPT-4o, Claude Opus) make the best planners. Executors can use faster, cheaper models since the plan provides scaffolding. This asymmetric allocation is one of the split's main economic advantages.
