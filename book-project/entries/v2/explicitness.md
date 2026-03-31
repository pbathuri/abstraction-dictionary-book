# explicitness

> State what you mean fully — the antidote to the model filling in blanks you didn't know existed.

## The Scene

"Write a product description."

What's implicit? The product (maybe provided). The audience (consumers? investors?). The tone (playful? authoritative?). The length (a tweet? a page?). The purpose (sell? inform?). The format (prose? bullets?). Every unstated dimension is a gap the model fills with its best guess — a guess drawn from the statistical center of its training data, which is nowhere near your intent.

You're talking to the model as if it were a colleague who shares your context, industry knowledge, aesthetic preferences, and definition of success. It shares none of these. It has statistical approximations of all of them. Explicitness is what bridges the gap.

## What This Actually Is

Explicitness is the discipline of closing accidental gaps. Every prompt has them — gaps between what you meant and what you said. Some are deliberate (you want the model to exercise judgment). Most are accidental (you assumed shared context).

Five categories of implicitness to watch:
- **Audience**: Who is this for? What do they know?
- **Quality criteria**: What does "good" mean here?
- **Scope boundaries**: What's in bounds? What's out?
- **Format**: What shape should the output take?
- **Epistemic standards**: How confident? How should uncertainty be expressed?

Explicitness is not verbosity. A prompt can be explicit in 30 words if those words nail the key specifications. It can be verbose in 300 words and still leave critical dimensions unstated.

This is the single highest-leverage prompt improvement technique. Making implicit requirements explicit produces larger quality gains than any other modification. Every explicit specification narrows the output distribution toward your target. Every implicit gap widens it toward the mean.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Write a product description" | "Audience: Etsy shoppers, 25-35. Tone: warm, slightly witty. Length: 50 words. Must mention: handmade, dishwasher-safe, 12oz." | Five dimensions made explicit in one block |
| "Give me a good analysis" | "Identify the 3 most significant trends. For each: headline, 2-3 sentence explanation, one data point. Label as DATA-SUPPORTED or INFERENCE." | Defines "good" with measurable criteria |
| "Write formally" | "Write for a regulatory affairs specialist reviewing an IND submission" | Audience implies the right formality without vague adjectives |
| "Be comprehensive" | "Cover all five dimensions listed below. If a dimension has no relevant data, state 'No data in provided sources.'" | "Comprehensive" means something specific and testable |
| "Improve this" | "Refactor for readability: shorten functions over 20 lines, rename unclear variables, add type hints where missing" | Turns a vague wish into a specific checklist |

## Before → After

**Before:**
```
Analyze the quarterly earnings report.
```

**After:**
```
Analyze the attached quarterly earnings report.

Audience: the CFO, who has read the raw numbers but needs
interpretive context
Purpose: identify the 3 most significant trends and their
implications for next quarter
Format: numbered findings, each with headline + 2-3 sentence
explanation + one data point
Tone: direct, confident assertions with stated evidence
Length: 300-400 words
Epistemic standard: label each finding as DATA-SUPPORTED
or INFERENCE

Do not summarize generally. Do not restate numbers without
interpretation.
```

**What changed:** Six dimensions made explicit — audience, purpose, format, tone, length, epistemic standard — plus two exclusions. The model has almost no room to guess wrong.

## Try This Now

```
Here's a deliberately underspecified prompt:

"Write something about our new feature."

Your job: list every implicit dimension — every question this
prompt leaves unanswered that the model will have to guess at.

Aim for at least 8 dimensions. For each, explain what the
model would default to and why that default probably isn't
what the prompter wanted.

Then rewrite the prompt with all 8 dimensions made explicit,
in under 100 words.
```

## When It Breaks

- **Specifying the wrong dimensions** → Explicit about word count but implicit about audience. The output is exactly 500 words of wrong tone for the wrong reader. Fix: prioritize the dimensions that most affect output quality for this task.
- **Pseudo-explicitness** → "Write a good, comprehensive analysis." Feels specific, tells the model nothing. Replace every adjective with a measurable criterion.
- **Specification overload** → Twenty requirements competing. The model satisfies some, violates others. Fix: state which specs are hard requirements vs. soft preferences. Give the model room to trade off the less important dimensions.

## Quick Reference

- Family: core abstraction
- Adjacent: → anchoring (one mechanism for making implicit reference points explicit), → clarity (removes structural ambiguity; explicitness removes assumption gaps), → constraint (constraints are a form of explicitness)
- Model fit: Explicitness benefits all models. The marginal gain is largest for mid-range models that have broad capability but weak defaults. No model is good enough to make explicitness unnecessary.
