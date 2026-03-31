# shared state

> The working memory that lets multiple agents coordinate — the blackboard they all read from and write to without speaking directly.

## The Scene

Form8, version three. I had four n8n nodes in a market-research pipeline: Scanner, Profiler, Gap Analyzer, Strategy Writer. Each node passed its full output to the next. By node four, the Strategy Writer was drowning — it received the Scanner's raw list, the Profiler's enriched data, the Gap Analyzer's findings, *plus* all the reasoning and metadata from every upstream node. Half the context was irrelevant processing notes.

The fix was a shared state object — a JSON blob that each node read from and wrote to. Scanner wrote `competitors[]`. Profiler enriched those objects in place. Gap Analyzer wrote `gaps[]`. Strategy Writer read only `competitors[]` and `gaps[]`. The processing notes, search queries, and confidence commentary stayed in each node's local output, never polluting the shared state. Context shrank by 60%. Output quality went up because the Writer saw only the curated findings, not the sausage-making.

## What This Actually Is

Shared state is the data structure — JSON object, database, file, in-memory store — that holds a pipeline's accumulated results and makes them available to any agent that needs them. It solves the fundamental coordination problem: how does Agent B know what Agent A found?

The concept maps directly to the **blackboard architecture** from AI research (HEARSAY-II, 1980): independent knowledge sources read from and write to a shared data structure, with no direct inter-agent communication. The critical design decision is access control. Unrestricted access creates context bloat and state corruption. Scoped access — each agent reads its relevant slice, writes to its designated section — keeps state clean. Shared state also enables resumability: if a pipeline fails mid-run, it restarts from the last good state instead of from zero.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| (pipe full output between agents) | "Write your findings to state.research.findings. Do not modify other state keys" | Scoped writes prevent state corruption |
| "Here's everything from the previous agent" | "Your read access: task.question, research.findings, config.output_format" | Explicit reads keep each agent's context lean |
| "Pass the results forward" | Define a JSON schema with typed fields per agent | Schema makes the state machine-legible and debuggable |
| "Remember what happened" | "Pipeline state tracks: completed_agents[], current_agent, errors[]" | Metadata enables resumability and audit |
| "Share the data" | "Research Agent: reads task.*, writes research.*. Analysis Agent: reads research.findings, writes analysis.*" | Access-control matrix prevents cross-contamination |

## Before → After

**Before:**
```
Agent 2, here is everything Agent 1 produced:
[Agent 1's full 1,200-word output including reasoning,
search strategy notes, rejected sources, and findings]

Now analyze the findings.
```

**After:**
```
You are Agent 2 (Analysis). Here is your slice of
pipeline state:

{
  "task": { "question": "What drove Q4 revenue decline?" },
  "research": {
    "findings": [
      {"claim": "APAC revenue dropped 18%",
       "source": "10-K p.23", "confidence": "high"},
      {"claim": "Two major contracts deferred to Q1",
       "source": "call transcript", "confidence": "medium"}
    ]
  }
}

Analyze the findings. Write your output to:
- analysis.conclusions (array of conclusion objects)
- analysis.confidence (overall confidence: high/medium/low)
- analysis.gaps (information gaps you identified)

Do not modify any other state keys.
```

## Try This Now

```
I'll describe a three-agent pipeline. Your job: design
the shared state schema.

Pipeline:
- Agent A: Collects customer feedback from three sources
- Agent B: Identifies the top 5 themes across all feedback
- Agent C: Writes a summary report for the product team

For each agent, define:
1. What state keys it reads
2. What state keys it writes
3. What data type each key holds

Then answer: what happens if Agent B runs before Agent A
has finished? How does the schema prevent stale reads?
```

## When It Breaks

- **State explosion** — Every agent appends its full output without pruning. By agent ten, the state is 50K tokens. Fix: the orchestrator must actively summarize or prune state after each agent, keeping only what downstream agents need.
- **Write conflicts** — Two parallel agents write to the same key, overwriting each other. Fix: scoped write access. Each agent writes to its own section. Parallel agents that contribute to the same result use append (add to a list), not overwrite.
- **Stale reads** — Agent B reads state before Agent A has written to it, getting defaults or outdated values. Fix: enforce dependency ordering. Agent B doesn't start until Agent A's write is confirmed.

## Quick Reference

- **Family:** Agent workflow
- **Adjacent:** → handoff (the event that reads/writes shared state), → orchestration (manages flow over the state), → pipeline (the sequence of steps state connects), → context windowing (determines how much of shared state each agent sees)
- **Model fit:** Shared state is implemented in code, not prompts — but the model's ability to work with it varies. Frontier models reliably read structured state and write to designated keys. Midsize models handle simple schemas but may violate write-access boundaries. Small models need state presented as flat key-value pairs, not nested objects.
