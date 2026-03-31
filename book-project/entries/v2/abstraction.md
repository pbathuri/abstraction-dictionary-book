# abstraction

> A named, reusable pattern that lets you work at the level of intent instead of mechanism.

## The Scene

You're building ResumeForge, and the third time you copy-paste the same block of instructions — "list pros and cons, weigh them, state a recommendation with confidence" — you stop. You give it a name: `weighted_tradeoff_analysis`. Now when any agent in the pipeline needs a decision, it invokes the name, not the paragraph. The name becomes a handle you can test, swap, and teach to new teammates. You just went from writing instructions to designing a toolkit.

## What This Actually Is

Abstraction is drawing a boundary around messy details and slapping a name on the outside. Inside: the gears. Outside: a clean grip.

In software, this gave us functions and APIs. In prompt engineering, it gives us reusable instruction blocks, named agent skills, and the shared vocabulary that makes this dictionary possible. Every entry here *is* an abstraction — a named pattern pulled from the chaos of how models actually respond to structured input.

The risk is naming too early, before you understand the boundary. The reward is leverage: once named correctly, a pattern can be taught, tested, reused, and improved without rebuilding from scratch.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "List pros and cons, weigh them, then recommend..." (every time) | `Apply weighted_tradeoff_analysis to:` | Invokable, testable, portable across prompts |
| "You are a helper that checks facts" | `You operate as a fact_checker agent. Contract: accepts a claim list, returns verdict + source per claim.` | The contract makes the abstraction debuggable |
| "Do the research thing" | `Execute the research_and_summarize skill` | Named skills compose; vague gestures don't |
| "Analyze this like before" | `Apply the same 4-axis competitive analysis from the Q3 template` | Repeatable reference beats shared memory |

## Before → After

**Before:**
```
List the strengths and weaknesses of this proposal. Then compare them.
Then give me a recommendation. Be specific about confidence.
```

**After:**
```
You operate as a tradeoff_analyzer. This abstraction encapsulates:
1. Identify the decision and its options
2. List benefits and costs for each option
3. Weight factors by the user's stated priorities
4. Produce a ranked recommendation with confidence level

Apply this to the following decision: {user_input}
```

**What changed:** The second prompt is a *tool definition*, not a one-time instruction. It has a name, a contract, a sequence. You can reuse it, test it against edge cases, and hand it to another agent.

## Try This Now

Paste this into ChatGPT:

```
I keep giving you the same kind of instruction over and over.
Here are three examples of tasks I've asked for recently:

1. "Review this code for bugs, style issues, and performance, then prioritize fixes"
2. "Read this essay for logic gaps, unsupported claims, and unclear writing, then prioritize fixes"
3. "Audit this project plan for risks, missing steps, and unclear ownership, then prioritize fixes"

Name this pattern. Give it a one-sentence contract (what it accepts,
what it returns). Then apply it to: "my weekly team standup notes."
```

You'll see the model extract the recurring structure and give it a reusable name. That's abstraction in action.

## When It Breaks

- **Premature naming** → You name `research_and_summarize` after two uses, but different contexts need different research depths. The abstraction cracks because you drew the boundary too early. Wait for stability.
- **Leaky abstraction** → Your "analyze" tool requires callers to know about internal token limits and retry logic. The whole point was hiding complexity — now it's bleeding through the interface.
- **Abstraction worship** → The team debates whether it's "synthesis" or "integration" while the actual prompt sits broken. The map is not the territory.

## Quick Reference

- Family: core abstraction
- Adjacent: → compose, → explicitness, → checkpoint
- Model fit: All major models respond to named abstractions. Larger models adopt contracts reliably; smaller models need the name *and* the expansion.
