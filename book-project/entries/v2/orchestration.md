# orchestration

> The conductor who decides which agent plays when, catches the ones who miss their cue, and knows when the piece is over.

## The Scene

Clap/OpsPilot has six agents. The first version ran them in a hard-coded sequence: SHOT_1 analyzes the repo, SHOT_2 maps gaps, SHOT_3 plans fixes, and so on. No validation between steps. No error handling. When SHOT_1 produced a malformed `REPO_REALITY.md` (it happens — a module directory it couldn't parse), SHOT_2 built an entire gap analysis on top of garbage data. SHOT_3 planned fixes for fictional gaps. The pipeline completed successfully. Every output was wrong.

The fix wasn't better agents. It was orchestration — the control layer between them. A validation check after each shot: does the output match the expected schema? Are all required fields populated? If SHOT_1 fails on a module, it retries with a narrower scope. If it fails again, it marks that module BLOCKED and proceeds. SHOT_2 receives validated output or a clear signal that data is incomplete. The agents didn't change. The management of agents changed everything.

## What This Actually Is

Orchestration is the control plane of a multi-agent system. It decides which agent runs when, what information each receives, how results flow between them, what happens when something fails, and when the overall task is done. If agents are musicians, orchestration is the conductor — not playing any instrument, but determining the strings enter at bar four and if the oboist misses a cue, the woodwinds cover.

People say "orchestration" when they mean "I chained three prompts." That's a pipeline. True orchestration implies *active management*: conditional routing, state tracking, error handling, retry logic, and completion detection.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Research, then outline, then write, then edit" | "Send topic to researcher. Validate: ≥5 sourced findings. Send to outliner. Validate: 4-7 sections. For each section, send to writer. Assemble. Send to editor. If editor flags major issues, loop affected sections back to writer" | Validation gates and conditional loops — that's orchestration |
| Running agents in sequence and hoping | "If any agent fails validation, retry once with feedback. If it fails again, report the failure and the partial result" | Error handling is the line between a demo and a product |
| One model does everything | "Route simple classification to Haiku. Route generation to Sonnet. Route final review to Opus" | Orchestration enables per-stage model selection for cost optimization |
| Trusting each agent's output implicitly | "After each agent, validate output against schema. If validation fails: retry with error feedback. If retry fails: escalate to human or halt pipeline" | Validation at every boundary prevents garbage propagation |
| Full shared state passed to every agent | "Orchestrator assembles per-agent context: only the state keys and upstream outputs this agent needs" | Orchestration includes information routing |

## Before → After

From Clap/OpsPilot — adding orchestration logic:

> **Before (chain with no management)**
> ```
> SHOT_1 runs → full output passed to SHOT_2 → full output
> passed to SHOT_3 → ... → final output
> No validation. No error handling. No state tracking.
> ```
>
> **After (orchestrated pipeline)**
> ```
> ORCHESTRATOR:
> 1. Run SHOT_1 (Repo Reality Mapper)
>    Validate: REPO_REALITY.md exists, every src/ directory
>    has a section, no section is empty.
>    On fail: retry with narrower scope. On second fail:
>    mark module BLOCKED, proceed with partial data.
>
> 2. Run SHOT_2 (Gap Analyzer)
>    Input: validated REPO_REALITY.md + product_north_star.md
>    Validate: each gap cites a specific REPO_REALITY section
>    and a specific north_star section.
>    On fail: retry with explicit instruction to cite sources.
>
> 3. Run SHOT_3 (Fix Planner)
>    Input: validated gaps only (exclude BLOCKED modules)
>    Validate: each fix maps to exactly one gap.
>    On fail: escalate to human review.
>
> State: track {completed_shots, blocked_modules,
> validation_failures, retry_count}
>
> Completion: all shots pass validation OR human escalation
> triggered.
> ```
>
> **What changed:** Failures became visible and recoverable. SHOT_2 stopped building on SHOT_1's errors because the orchestrator caught those errors at the boundary. The pipeline went from "completes successfully with wrong answers" to "catches problems and either fixes them or asks for help."

## Try This Now

Take any multi-step prompt chain or agent pipeline you've built. For each step, answer three questions:

```
1. What would happen if this step produced garbage output?
   (Currently: does the next step notice, or does it proceed?)
2. What validation could I add at this boundary?
   (Schema check? Required fields? Minimum quality bar?)
3. What's the retry/fallback if validation fails?
   (Retry with feedback? Skip and flag? Escalate to human?)
```

If you can't answer #1 for any step, you don't have orchestration — you have a sequence and a prayer.

## When It Breaks

- **Over-orchestration** — Building a complex control layer for a task that needs one prompt. The orchestrator becomes the most error-prone component. The discipline is knowing when *not* to orchestrate.
- **Silent failures** — An agent produces bad output, but the orchestrator lacks validation and passes it downstream. Fix: validate outputs against schemas or quality checks at every transition point.
- **State explosion** — Shared state grows without bounds as agents append results. Later agents receive bloated context. Fix: the orchestrator must actively manage state — summarizing, pruning, and scoping what each agent sees.

## Quick Reference

- **Family:** Agent workflow
- **Adjacent:** → pipeline (one pattern an orchestrator can run), → handoff (an event orchestration manages), → planner-executor split (defines roles; orchestration coordinates them), → delegation (assigns tasks; orchestration governs when and how)
- **Model fit:** Orchestration logic is best implemented in code for production systems. When the orchestrator itself is an LLM (useful for prototyping), use the strongest available reasoning model. Reserve lighter models for the leaf agents being orchestrated.
