# decomposition

> Break the hard thing into easy things. Then do the easy things.

## The Scene

Andrej Karpathy published his `autoresearch` project and the whole thing clicked. The entry point is a single file: `program.md`. It's not code. It's a decomposition — a multi-step research workflow written in plain English, with phases, sub-tasks, verification gates, and rollback conditions. The LLM reads `program.md` and executes it step by step: search, read papers, extract claims, evaluate novelty, write sections, verify citations, compile.

Here's the thing that hit me: `program.md` IS the program. Not a description of the program. Not a planning document that precedes the program. The decomposition *is* the executable artifact. Every phase has an input, an output, and a completion criterion. Every transition has a condition. The model doesn't need to figure out how to do research. It needs to execute a recipe that's been broken down into steps it can handle individually.

I immediately borrowed this pattern for Form8, my n8n workflow for market research. The original Form8 prompt was a monolith: "Research this market, analyze competitors, identify gaps, and write a strategy brief." The model produced something that looked like each of those things squished into a blender. When I decomposed it into four sequential nodes — each with its own prompt, its own output schema, and its own pass/fail check — the quality of every individual piece went up, and the assembled whole actually *read* like a strategy document.

## What This Actually Is

Decomposition is the discipline of not asking a model to do six things at once. You wouldn't write a single function that reads a file, parses it, validates it, transforms it, writes it, and sends a notification. You'd write six functions. Same principle, applied to prompts.

The key insight from `program.md` is that decomposition isn't just a technique for making prompts better. It's an *architecture*. When you decompose a task into phases with defined inputs, outputs, and gates, you've built a pipeline. Each phase can be tested independently. Each phase can be assigned to a different model or agent. And when something breaks, you know exactly which phase broke — because you numbered them.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Analyze and summarize this report" | "Step 1: Extract the 5 key findings. Step 2: For each, write one sentence. Step 3: Rank by business impact" | Serializes attention instead of splitting it |
| "Do a code review" | "Pass 1: structural issues. Pass 2: correctness. Pass 3: recommendation. Complete each before starting the next" | Named passes with an explicit sequence |
| "Research this topic" | "Phase 1 (search): Find 10 sources. Phase 2 (filter): Keep the 5 most relevant. Phase 3 (extract): Pull key claims. Phase 4 (write): Draft using only extracted claims" | Karpathy pattern: each phase has one job |
| "Help me plan this project" | "First, list the deliverables. Then for each deliverable, list the tasks. Then for each task, estimate effort. Don't skip ahead" | Forces sequential elaboration |
| "Write a report" | "Section by section: write the intro, then stop. I'll review before you continue" | Human-in-the-loop decomposition |

**Power verbs for decomposition:** split, phase, serialize, isolate, sequence, stage, layer, separate, order, gate.

## Before → After

From my Form8 market research workflow — the actual architecture change:

> **Before (monolith)**
> ```
> You are a market research analyst. Given this product description
> and target market, produce a comprehensive competitive analysis
> with market sizing, competitor profiles, gap analysis, and
> strategic recommendations.
> ```
>
> **After (decomposed into n8n nodes)**
> ```
> NODE 1 — Market Scanner
> Input: product description + target market
> Task: Return 8-10 active competitors with name, URL, and
>   one-sentence positioning. No analysis yet.
> Output: JSON array of competitor objects.
> Gate: At least 6 competitors found. If fewer, flag and halt.
>
> NODE 2 — Competitor Profiler
> Input: competitor array from Node 1
> Task: For each competitor, extract pricing tier, key features,
>   and target customer segment from their public materials.
> Output: Enriched competitor JSON.
> Gate: Every competitor has all three fields populated.
>
> NODE 3 — Gap Analyzer
> Input: enriched competitors + original product description
> Task: Identify 3-5 gaps where our product could differentiate.
>   Each gap needs: description, evidence, and confidence level.
> Output: Gap analysis JSON.
>
> NODE 4 — Strategy Writer
> Input: all upstream outputs
> Task: Write a 500-word strategy brief for the product team.
>   Cite specific competitors and gaps by name.
> Gate: Every recommendation traces to a specific gap from Node 3.
> ```
>
> **What changed:** One impossible task became four possible tasks. Each node has one job, one output schema, and one gate. When Node 2 fails (a competitor's site has no pricing), it fails *there*, not in the middle of a 2,000-word blob.

## Try This Now

Take the hardest prompt you've written recently — the one that produced mushy results — and paste it into ChatGPT with this wrapper:

```
I have a prompt that tries to do too much in one shot.
Break it into 3-5 sequential steps. For each step:
- Name it (Step 1: Extract, Step 2: Evaluate, etc.)
- Define the input (what it receives)
- Define the output (what it produces)
- Define one gate (how you'd know if this step failed)

Here's my prompt:
[paste your prompt here]

Don't execute the steps. Just design the decomposition.
```

The decomposition itself is often more valuable than running it. It shows you what you were actually asking the model to juggle simultaneously.

## From the Lab

We compared single-pass prompts against decomposed multi-step versions across reasoning tasks (math, logic, code review, document analysis). The gap was consistent:

![Reasoning Task Techniques](../art/figures/exp_reasoning_task_techniques.png)

**Key finding:** Chain-of-thought decomposition improved accuracy by 10-40% depending on task complexity. The benefit was largest for tasks requiring 3+ reasoning steps — exactly the tasks where monolithic prompts fail hardest. Interestingly, for simple 1-step tasks, decomposition added overhead without improving quality. Don't decompose what doesn't need decomposing.

## When It Breaks

- **Over-decomposition** → You broke the task into 15 micro-steps and now the reassembly is harder than the original problem. Each step is locally correct but the whole thing reads like it was written by a committee of ants. If a step is trivial, merge it with its neighbor.
- **Decomposition without dependency mapping** → You parallelized steps that actually depend on each other. Step 3 needs Step 2's output, but you launched them simultaneously. Result: inconsistent, contradictory outputs.
- **Decomposition as procrastination** → The planner agent produces ever-more-detailed task breakdowns but never actually triggers execution. Planning is not progress. At some point, the model needs to write the thing.

## Quick Reference

- **Family:** Core abstraction
- **Adjacent:** → delegation (decomposition produces the tasks that delegation assigns), → pipeline (decomposition hardened into permanent architecture), → hierarchy (decomposition creates hierarchy), → specificity (each sub-task is more specific than the monolith)
- **Model fit:** Benefits all tiers. Small models benefit most — they can't juggle 4 tasks but handle 1 well. Frontier models benefit from decomposition as a verification surface (check each step before proceeding). Reasoning models (o1/o3) decompose internally but still benefit from explicit phase structure.
- **Sources:** Wei et al. (2022) chain-of-thought, Zhou et al. (2022) least-to-most, Karpathy (2025) autoresearch
