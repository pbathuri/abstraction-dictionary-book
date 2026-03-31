# perspective

> Where the model stands determines what it sees. Move the viewpoint and the analysis changes — not the tone, the substance.

## The Scene

Clap/OpsPilot's architectural review needed to be useful to two audiences: the engineering team (who cares about implementation gaps) and the product lead (who cares about user-facing impact). The first version had one agent producing one review. It was evenhanded and useless to both — too strategic for the engineers, too technical for the product lead.

The fix was perspective splitting. I created two parallel agents powered by the same model. Agent A's system prompt: "You are a senior backend engineer reviewing this codebase for technical debt, missing error handling, and scalability bottlenecks." Agent B: "You are a product manager reviewing this codebase for features that are half-built, user flows that dead-end, and gaps between what the product promises and what the code delivers." Same codebase. Same model. The engineering agent flagged missing retry logic. The product agent flagged that the onboarding flow had no error state. Neither agent saw what the other saw, because where you stand determines what you look for.

## What This Actually Is

Perspective is the viewpoint from which a model considers information — the cognitive position that shapes what it notices, prioritizes, and concludes. It's not tone (how it says things) or scope (how much it covers). It's *substance* — what the model chooses to say in the first place.

When you set a perspective, you shift the model's attention allocation. A security auditor perspective treats a missing input validation as critical. A performance engineer perspective treats the same code as irrelevant. Neither is wrong — they're standing in different places. The richest analyses combine multiple perspectives and then synthesize across them.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Analyze this business plan" | "Analyze from the perspective of a VC evaluating for Series A. Focus on: market size, unit economics, founder-market fit" | Named perspective with specific attention targets |
| "Review this code" | "Review as a security auditor. Treat every user input as hostile. Flag injection points, auth gaps, and data exposure" | Perspective + threat model = focused review |
| "You are an expert" (generic) | "You are a structural engineer with 20 years of seismic retrofitting experience, working under California building codes" | Grounded perspective activates domain reasoning, not just vocabulary |
| One agent producing a balanced review | Two agents with contrasting perspectives + a third synthesis agent that reconciles their findings | Multi-perspective architecture surfaces blind spots |
| "What do you think about this proposal?" | "Analyze from three perspectives: (1) the CFO — cash flow risk, (2) the CTO — technical feasibility, (3) the customer — usability impact. Then synthesize where they agree and conflict" | Structured multi-perspective in a single prompt |

## Before → After

From Clap/OpsPilot — perspective-split architectural review:

> **Before (generic single perspective)**
> ```
> Review this codebase and identify architectural issues.
> Consider both technical and product implications.
> ```
>
> **After (parallel perspectives)**
> ```
> AGENT A — Engineering Perspective
> System: You are a senior backend engineer. Review this
> codebase for: technical debt, missing error handling,
> scalability bottlenecks, test coverage gaps. Every finding
> must reference a specific file and line range.
>
> AGENT B — Product Perspective
> System: You are a product manager. Review this codebase for:
> half-built features, user flows that dead-end, mismatches
> between product promises and code reality. Every finding
> must map to a user-facing impact.
>
> AGENT C — Synthesis
> System: You receive two reviews of the same codebase from
> different perspectives. Produce a unified priority list
> where each item notes whether it was flagged by engineering,
> product, or both. Items flagged by both go to the top.
> ```
>
> **What changed:** The review surfaced findings that a single-perspective agent missed entirely. The missing retry logic (engineering concern) and the dead-end onboarding flow (product concern) both made it to the priority list. A balanced single agent would have produced a mediocre version of both.

## Try This Now

Take any analysis prompt you've written recently. Run it as-is. Then prepend a specific perspective and run again:

```
Before answering, adopt this perspective: you are a
[specific role] with [specific experience] whose primary
concern is [specific priority].

Now analyze: [your original question]
```

Compare the two outputs. Count the claims that appear in one but not the other. Those exclusive claims are the perspective's contribution — what it sees that the default viewpoint misses.

## When It Breaks

- **Shallow perspective** — "You are an expert" activates surface patterns (bigger words) but not domain-specific reasoning. Fix: ground the perspective with specifics — years of experience, specialization, regulatory context, typical concerns.
- **Perspective collapse** — You assign a perspective but then ask a question incompatible with it. "You are a constitutional lawyer. Write a poem about sunsets." The task overrides the perspective. Fix: ensure the task matches the perspective.
- **Perspective-fact confusion** — Treating one perspective's conclusions as ground truth. A bullish investor perspective will find reasons to invest — that's the perspective working correctly, not evidence the investment is sound. Fix: multi-perspective analysis requires a synthesis step that weighs viewpoints, not selects one.

## Quick Reference

- **Family:** Core abstraction
- **Adjacent:** → framing (the act of choosing a perspective; perspective is the state after the choice), → audience specification (who the output is *for*; perspective is who it's *from*), → register (the tonal consequence of perspective choices)
- **Model fit:** Frontier models maintain complex perspectives across long outputs and switch between perspectives within a single response. Midsize models hold simple perspectives but may flatten nuance — "expert" becomes "uses big words" rather than "reasons with domain frameworks." Small models need periodic perspective reinforcement.
