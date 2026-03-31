# handoff

> The moment one agent stops and another starts — get the transfer wrong and everything downstream breaks.

## The Scene

In Clap/OpsPilot, SHOT_1 produces `REPO_REALITY.md` — a grounded description of what the codebase actually does. SHOT_2 takes that reality document and maps it against the product north star to identify architectural gaps. The first version of this handoff was casual: SHOT_2 received the full conversational output from SHOT_1, including reasoning, false starts, and self-corrections.

The result was a mess. SHOT_2 couldn't distinguish SHOT_1's final conclusions from its exploratory thinking. It cited tentative observations as confirmed findings. It referenced abandoned analysis paths as if they were recommendations. The "handoff" was just dumping the whole conversation and hoping.

The fix: SHOT_1 was restructured to produce a clean context packet — `REPO_REALITY.md` as structured output with specific fields (module name, observed behavior, confidence level, source file). SHOT_2 received *only* this artifact, not the conversation. The entire handoff was the document. Clean input, clean output. The seam became invisible.

## What This Actually Is

A handoff is a discrete transfer of control, context, and responsibility from one agent to another. Not a shared workspace. Not a CC. A relay-race baton pass — the outgoing agent relinquishes control, the incoming agent assumes it, and a curated packet of context crosses the boundary between them.

Three structural components: the **trigger** (a condition that tells Agent A its work is done), the **context packet** (structured information Agent B needs to act, not the full history), and the **acceptance** (Agent B confirms it has enough to proceed). Without all three, you don't have a handoff. You have a hope.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Pass the results to the next step" | "Output a JSON object with fields: findings[], confidence_levels[], open_questions[]. The next agent will receive only this object" | Names the exact handoff artifact |
| "Here's the conversation so far" | "Produce a context packet: task summary (2 sentences), key decisions made, constraints still active, and one open question" | Curated transfer, not a dump |
| "Continue from where I left off" | "You are receiving a structured handoff. Read the context_packet field. Do not reference any prior conversation — this packet is your complete starting context" | Explicit fresh-start with scoped context |
| "Send it to the editor" | "Handoff to editor_agent. Required fields: draft_text, style_guide_version, sections_flagged_for_review[]. If any required field is missing, halt and report" | Acceptance criteria built into the handoff |
| "Let the next agent figure it out" | "Your output becomes the next agent's only input. Include everything it needs. Exclude your reasoning process" | Forces the sender to curate |

## Before → After

From Clap/OpsPilot — the actual SHOT_1 → SHOT_2 transition:

> **Before (unstructured handoff)**
> ```
> [Full SHOT_1 conversation output: 3,000 tokens including
> exploratory analysis, self-corrections, and final conclusions
> mixed together]
>
> SHOT_2: "Based on the above, identify architectural gaps."
> ```
>
> **After (structured context packet)**
> ```
> SHOT_1 output: REPO_REALITY.md
> Format: structured document with per-module entries:
> {
>   "module": "research_agent",
>   "observed_behavior": "Calls web_search tool, returns raw
>     results without filtering or ranking",
>   "confidence": "high",
>   "source_files": ["src/agents/research_agent.py"],
>   "gaps_noted": ["no error handling for failed searches"]
> }
>
> SHOT_2 receives: REPO_REALITY.md + product_north_star.md
> Task: For each module in REPO_REALITY, identify where
> observed behavior diverges from the north star's intended
> architecture. Map each gap to a specific north star section.
> ```
>
> **What changed:** SHOT_2 stopped citing SHOT_1's exploratory thinking as findings. Every claim in the gap analysis traced to a structured observation, not to a stray sentence from a 3,000-token conversation dump.

## Try This Now

Find any multi-step prompt chain you've built. Look at the boundary between steps. Then ask:

```
I have a two-step prompt chain. Step 1 produces output that
Step 2 consumes. Currently, Step 2 receives Step 1's full
output.

Design the handoff artifact — the structured object that
should cross the boundary:
1. What fields does Step 2 actually need?
2. What from Step 1's output is reasoning/process that
   Step 2 should NOT see?
3. What's the acceptance check — how would Step 2 know
   if the handoff packet is incomplete?

Step 1 prompt: [paste]
Step 2 prompt: [paste]
```

You'll discover that most of Step 1's output is noise for Step 2's purposes.

## When It Breaks

- **Context starvation** — The handing-off agent passes too little. The receiver hallucinates what's missing or produces generic output. Fix: define a handoff schema with required fields and validate before transfer.
- **Context flooding** — The handing-off agent passes everything. The receiver drowns in irrelevant detail and its attention dilutes across noise. Fix: curate the packet. Pass what the next agent needs to *act*, not what the previous agent happened to *see*.
- **Orphaned handoffs** — Agent A hands off, Agent B never picks up. The task stalls silently with no error. Fix: implement acceptance confirmation and timeout alerts.

## Quick Reference

- **Family:** Agent workflow
- **Adjacent:** → delegation (assigns a subtask and expects return; handoff transfers full control with no return), → orchestration (manages the system of handoffs), → pipeline (a sequence of handoffs hardened into architecture)
- **Model fit:** All frontier models handle structured handoffs well when the context packet is explicit. Smaller models need stricter schemas and shorter packets. For open-source deployments, validate handoff fidelity at every boundary.
