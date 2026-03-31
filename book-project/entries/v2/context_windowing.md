# context windowing

> The deliberate management of what information occupies the model's finite viewport — what gets included, excluded, summarized, or deferred.

## The Scene

A Karpathy-style autoresearch agent is seven turns deep into a literature review. The context window is stuffed: the original query, six rounds of search results, the model's running notes, and the full text of three papers. The agent starts producing summaries that miss key findings — not because the model is dumb, but because the important passages are buried in the middle of 90K tokens, where attention is weakest.

You insert a compression step between turns: extract structured findings, discard the reasoning chain and dead-end searches, and carry forward only the findings and source cards. Turn eight's context is half the size and twice as useful.

## What This Actually Is

A model doesn't remember. It sees exactly what you put in front of it. Context windowing is the editorial discipline of managing that viewport — deciding what gets a seat at the table.

Bigger windows don't solve this. They create the illusion that curation is unnecessary, which is worse. A 200K window with 150K tokens of irrelevant material performs worse on targeted tasks than a 32K window with 30K tokens of relevant material.

Three axes:
- **Selection**: Which documents, turns, and instructions enter the window at all?
- **Compression**: Full text, summary, key-value extraction, or structured digest?
- **Ordering**: Where does it sit? Models attend to the beginning and end more reliably than the middle ("lost in the middle" phenomenon).

Think like an editor, not a librarian. A librarian includes everything relevant. An editor includes only what serves the current task and arranges it for impact.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Here's the full 40-page report" | "Here is the relevant section (pages 12-18). Based ONLY on this section, answer:" | The model gets less text but the *right* text |
| (pass all prior turns to every agent) | "Compress Research Agent output: retain findings[] and source_cards[], discard reasoning_chain and dead_ends" | Inter-agent compression prevents context bloat |
| (critical info in the middle) | [Move critical information to the top or bottom of the context] | Positional attention bias is real — design for it |
| "Here's everything just in case" | "Include only material the task demonstrably requires" | Kitchen-sink prompting dilutes attention |
| (full conversation history at turn 15) | "Summary of turns 1-12 (200 tokens). Full text of turns 13-15." | Sliding window preserves recent detail, compresses old turns |

## Before → After

**Before:**
```
Here is a 50,000-word research paper. What sampling method did
the authors use?
```

**After:**
```
I'm giving you one section of a research paper, not the full paper.
This section covers the methodology (pages 12-18).

Based ONLY on this section:
What sampling method did the authors use, and what was their sample size?

Do not speculate about sections you haven't seen.

[SECTION TEXT]
```

**What changed:** Instead of making the model find a needle in a haystack, you gave it the needle's neighborhood. Less input, better output.

## Try This Now

```
Here's an exercise in context windowing. I'll give you a scenario
with TOO MUCH context, then you'll practice trimming it.

SCENARIO: A customer sent a 500-word complaint email. You need
to classify it as: billing, technical, cancellation, or general.

For classification, which of these context elements are necessary
and which are waste?
1. The customer's full email (all 500 words)
2. The customer's account history (last 12 months of tickets)
3. Your company's full product documentation
4. A one-line summary of the email
5. The customer's name and email address

Rank these from "essential" to "pure waste" for the classification
task. Then explain: what's the minimum context needed?
```

## When It Breaks

- **Kitchen-sink prompting** → Ten documents when you need two. The model can't reliably identify which passages matter. Select ruthlessly.
- **Over-compression** → Summarizing so aggressively that critical details vanish. A legal document compressed to three bullets loses the specific language a legal analysis requires. Match compression to task demands.
- **Middle blindness** → Critical info in the center of a long context, where attention is weakest. Structure like a newspaper: lead with what matters most.
- **Stale accumulation** → In multi-turn work, never evicting old turns. The context fills with archaeological layers. Implement a sliding window or explicit eviction.

## Quick Reference

- Family: context architecture
- Adjacent: → context_budget (the accounting system windowing draws against), → context (the information being windowed), → compose (benefits from windowed, structured inputs)
- Model fit: Frontier models handle longer contexts more gracefully but still exhibit middle-of-context degradation. Small models with 4K windows demand rigorous windowing. For all tiers: a well-curated short context outperforms a poorly curated long one.
