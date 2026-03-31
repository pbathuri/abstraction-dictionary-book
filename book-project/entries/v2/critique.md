# critique

> Systematically find weaknesses, gaps, and failure points — flipping the model from helpful ally to useful adversary.

## The Scene

You've drafted a technical proposal and ask the model: "What do you think of this?" It responds: "This is a well-structured proposal with several strong elements. You might consider expanding the timeline section..." That's not critique. That's a sandwich of praise with a polite suggestion filling.

You try again: "Identify every claim that lacks evidence, every logical step that skips a premise, and every conclusion that doesn't follow. Quote the exact sentence for each. Find at least four problems."

The output transforms. Specific weaknesses, quoted text, actionable fault-finding. The model was always *capable* of this — it just needed permission (and instruction) to stop being nice.

## What This Actually Is

Most of the time, a model is trying to help. Agreeable by training, tuned to satisfy. Critique flips the orientation from *ally* to *adversary*. You're not asking it to describe, improve, or extend. You're asking it to break.

This is cognitively distinct from generation. The model must read output not as a continuation to extend but as an artifact to examine. Madaan et al. (2023) formalized this in Self-Refine: generate, critique, revise. The critique step is the engine — without it, revision is blind. Self-Refine improved GPT-4 by 8.7 points on code optimization and 21.6 on sentiment reversal. Those gains came from the quality of the intermediate critique.

The key insight: the model is, paradoxically, a better critic than author. Its *second* look at output is more accurate than its *first* pass at generation.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "What do you think?" | "Identify every claim that lacks evidence and every conclusion that doesn't follow from the analysis" | Targeted fault-finding, not open-ended feedback |
| "Review this" | "Find at least 5 specific weaknesses. If you can't find 5, you're not looking hard enough." | Minimum count forces past approval bias |
| "Any suggestions?" | "Adopt the role of a hostile peer reviewer finding reasons to reject this submission" | Adversarial framing activates genuine critique |
| "Is this good?" | "Critique substance (logic, evidence, completeness). Ignore surface (style, formatting)." | Keeps critique on what matters |
| "Give me feedback" | "Your job is to find faults, not encourage the author" | Explicitly overrides politeness training |

## Before → After

**Before:**
```
Review my essay and tell me what you think.
```

**After:**
```
Critique this essay. Identify every claim that lacks supporting
evidence, every logical step that assumes what it should prove,
and every conclusion that doesn't follow from the preceding argument.

Do not comment on style or tone.
For each weakness, quote the exact sentence and explain why it fails.
Find at least four problems.
```

**What changed:** The instruction shifted from open-ended feedback (which invites praise) to targeted fault-finding. The criteria are explicit. The minimum count forces past approval bias. The exclusion of style keeps the critique on substance.

## Try This Now

```
Here's a short argument. Critique it using the protocol below.

ARGUMENT: "Our company should switch to a four-day workweek.
Studies show it increases productivity. Employees prefer it.
And it would help with recruitment in a competitive market."

CRITIQUE PROTOCOL:
For each sentence, identify:
1. Is the claim supported with specific evidence? (yes/no)
2. What assumption does it rely on that isn't stated?
3. What counterargument would a skeptic raise?

Then give an overall verdict: is this argument ready to present
to a skeptical executive? What's the single biggest weakness?
```

## When It Breaks

- **Politeness override** → The model's helpfulness training overrides critique. Instead of weaknesses, you get "this is mostly good but could be improved." Fix: adversarial framing and explicit minimum weakness counts.
- **Critique of surface, not substance** → Flags formatting and word choice while ignoring logical gaps and unsupported claims. Fix: "Address substance — logic, evidence, completeness. Ignore surface."
- **Self-rubber-stamping** → When critiquing its own output, the model is biased toward approval. Fix: use a separate prompt, agent, or model for the critique step.

## Quick Reference

- Family: instructional action
- Adjacent: → evaluate (overall quality assessment), → falsifiability (claims must be testable for critique to engage), → feedback_loop (critique drives the revision cycle)
- Model fit: Critique quality varies more by prompt design than model tier. All models are biased toward approving their own output — adversarial distance (separate prompt, separate agent) improves quality at every level.
