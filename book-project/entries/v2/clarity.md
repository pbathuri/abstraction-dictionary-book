# clarity

> The property of an instruction that ensures every sentence can be interpreted in exactly one way.

## The Scene

"Summarize the key points and email them to the team lead."

Does "them" refer to the key points or the summaries? Should the model write an email, produce a summary, or both? A human guesses from context. The model picks the most probable parse and proceeds without telling you which one it chose. You won't know it misinterpreted until you read the output — and sometimes not even then, because the wrong interpretation produces plausible-looking text.

Most prompt debugging is ambiguity debugging. The user writes something, gets an unexpected output, and concludes the model is bad at the task. But usually the model did something *reasonable* — it just picked a different valid reading of the instruction.

## What This Actually Is

Ambiguity is not vagueness. Vagueness is saying too little. Ambiguity is saying something that could mean two things. Both are problems, different solutions. Clarity solves ambiguity.

Three sources to watch for:

**Referential ambiguity** — the pronoun problem. "It," "they," "this" could point at more than one thing. Fix: repeat the noun.

**Scope ambiguity** — the modifier problem. "Review the financial data from Q3 and Q4 reports" — data from Q3 *and* Q4? Or Q4 reports specifically? Restructure: "From the Q3 report and the Q4 report, review the financial data sections."

**Instructional ambiguity** — the goal problem. "Improve this code" could mean optimize speed, fix bugs, improve readability, or all of the above. The model can't ask which you meant.

The cost scales with prompt length. If three instructions each have two possible readings, the model navigates eight interpretation paths. Only one is yours.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Summarize the key points and email them" | "Summarize the key points. Then draft an email to the team lead containing that summary." | Resolves both the pronoun and the task ambiguity |
| "Improve this code" | "Refactor this code for readability: shorten functions over 20 lines, rename unclear variables, add type hints" | Defines what "improve" means for this context |
| "Review the Q3 and Q4 reports" | "From the Q3 report and the Q4 report, review the revenue figures in each" | Eliminates scope ambiguity about what's from where |
| "Fix the issue we discussed" | "Fix the null pointer exception in the `processOrder` function on line 47 of `checkout.py`" | All references resolve within the prompt |

## Before → After

**Before:**
```
Summarize and critique the methodology in sections 3 and 4.
```

**After:**
```
Task 1: Summarize the methodology described in Section 3 (2-3 sentences).
Task 2: Summarize the methodology described in Section 4 (2-3 sentences).
Task 3: Critique both methodologies — identify weaknesses, unstated
assumptions, and threats to validity.
```

**What changed:** The compound instruction was split into unambiguous sequential steps. No question about what applies to what.

## Try This Now

```
Here is an ambiguous instruction:

"Analyze the sales data from the marketing team and
the product team and highlight the key differences."

Rewrite this instruction three different ways, each resolving
a different ambiguity:
1. One version where "sales data" comes from both teams
2. One version where "from the marketing team" modifies something else
3. One version that eliminates ALL ambiguity

Then explain which ambiguity the original is most likely to trip up an LLM.
```

## When It Breaks

- **Assumed shared context** → "Fix the issue we discussed" is clear to the human who had the discussion. To the model, it's an ambiguous instruction with no referent. Every reference must resolve within the prompt or the provided context.
- **Compound instructions with unclear scope** → "Summarize and critique the methodology in sections 3 and 4." Does critique apply to both? Does methodology scope to both? Each ambiguity doubles the interpretation space. Decompose.

## Quick Reference

- Family: core abstraction
- Adjacent: → explicitness (makes hidden assumptions visible), → analyze (benefits from clear dimensional specification)
- Model fit: Clarity benefits all tiers equally. It's a structural fix to the prompt, not a capability issue in the model. The cheapest way to improve consistency is to remove ambiguity from the input.
