# analyze

> Break something apart to see how the pieces relate — the decomposition verb that comes before judgment.

## The Scene

You're on the OpsPilot project, and the planning agent just handed your analysis agent a 3,000-word competitor product launch brief. The agent's prompt says "analyze this." So it produces... a book report. Three paragraphs of paraphrase that could have come from the press release. The problem isn't the model. It's the instruction. "Analyze" without axes is "look at this" with a fancier hat.

You rewrite: "Analyze along four dimensions: feature overlap with our product, pricing position relative to market segments, target audience overlap, and six-month threat level." Same model, same input. Now it produces a structured brief your strategy team can act on.

## What This Actually Is

Analysis is structured disassembly. You take a whole and pull it into parts so you can see relationships that were invisible in the original. The word gets used loosely — people write "analyze this" the way they'd say "look at this" in conversation. But real analysis has a shape: identify components, examine relationships, surface implications.

The key: always specify the *axis*. Financial analysis looks for cost structures and risk. Literary analysis looks for theme and voice. Competitive analysis looks for positioning and vulnerability. Same verb, completely different lens.

Analysis also has a natural position in a chain. It follows retrieval and precedes synthesis. Skip it, and you get conclusions without foundations.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Analyze this document" | "Analyze this document along three axes: financial viability, technical feasibility, organizational readiness" | Axes turn vague attention into structured decomposition |
| "Look at this data" | "Identify the three strongest patterns in this dataset and the evidence for each" | Forces the model to commit to specific observations |
| "What do you think?" | "For each dimension, provide 2-3 observations with supporting evidence and a confidence level" | Structures the output so downstream steps can parse it |
| "Analyze and summarize" | "First analyze (decompose into parts), then summarize (compress the key findings)" | These are different operations — sequence them explicitly |
| "Do a deep analysis" | "Analyze at three levels: surface metrics, underlying drivers, second-order implications" | Defines what "deep" actually means |

## Before → After

**Before:**
```
Analyze this customer review.
```

**After:**
```
Analyze this customer review along three dimensions:
1. Product satisfaction (what they liked/disliked about the product itself)
2. Service experience (interactions with support or delivery)
3. Purchase intent (likelihood of repurchase or recommendation)

For each dimension, quote the relevant sentence from the review.
```

**What changed:** The model now has a structure to fill rather than a void to improvise in. Three dimensions, evidence required. The quality difference is dramatic and consistent across model families.

## Try This Now

Paste into ChatGPT:

```
Here is a short product description:

"Our project management tool helps teams stay organized with
kanban boards, time tracking, and automated reporting. Trusted
by 10,000+ teams worldwide. Start free, upgrade anytime."

Analyze this along exactly these axes:
1. Claims that are verifiable vs. claims that are vague
2. What the description assumes about the reader
3. What a competitor could copy in a week vs. what would take months

Format as a table with one row per axis.
```

Notice how specifying axes produces analysis that's actually *useful* instead of a restated summary.

## When It Breaks

- **Dimension-free analysis** → "Analyze this" with no axes. You get a book report. Always specify 2-5 dimensions.
- **Analysis-as-summary** → The model compresses instead of decomposes. Fix by requesting structured output with named categories or a table.
- **Infinite recursion** → In agent loops, analysis triggers re-analysis of its own output when the stopping condition is vague. Define what "done" looks like.

## Quick Reference

- Family: instructional action
- Adjacent: → contrast (differences between items), → evaluate (adds judgment), → critique (analysis with a normative frame)
- Model fit: All current-gen models handle dimensional analysis well when given explicit axes. Smaller models benefit from few-shot examples of the desired decomposition format.
