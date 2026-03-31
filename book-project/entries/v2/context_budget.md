# context budget

> Treat the context window as a finite resource — every token spent on instructions is a token not spent on content.

## The Scene

You're running a Form8 n8n pipeline on a 32K-token model. Your system prompt is 4,000 tokens. The retrieved documents need 25,000. You want structured output that'll take about 6,000 tokens. That's 35,000 tokens. You're 3,000 over budget before you even start.

Something has to go. But what? If you trim the system prompt, the model loses behavioral constraints. If you truncate documents, you lose source material. If you squeeze the output reserve, the model truncates its own response silently.

This is why you need a budget, not a dump.

## What This Actually Is

The context window has a hard ceiling. A context budget divides that ceiling into named allocations — so many tokens for instructions, so many for source material, so many for conversation history, so many reserved for output — and enforces them by design.

Think of it like a financial budget. A household that spends freely until the money runs out isn't budgeting — it's hoping. A prompt engineer who pastes documents until the window fills is doing the same thing.

Four budget categories:
- **Instruction tokens**: system prompt, behavioral directives, format specs, constraints
- **Content tokens**: documents, tables, code, retrieved passages — the actual data
- **History tokens**: prior turns, prior agent outputs
- **Output reserve**: space for the model to generate its response

The fundamental trade-off: every token on instructions is a token not on content. A 3,000-token system prompt that could be expressed in 800 wastes 2,200 tokens of content capacity. In a 32K window, that's 7%. In a 4K window, that's 55%.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| (paste everything, hope it fits) | "Budget: instructions 400 tokens, source material 3,000, output reserve 1,500" | Makes allocation explicit and auditable |
| "Here's the full conversation history" | "Summary of relevant prior turns (200 tokens)" | History compression preserves budget for current task |
| "Here are 10 examples of good output" | (Remove examples if the task is simple enough without them) | Few-shot examples are expensive — test whether they earn their tokens |
| "Very detailed system prompt" | "Audit: does each instruction measurably improve output? Remove those that don't." | Prompt creep is the #1 budget killer |

## Before → After

**Before:**
```
Here is a long document. Also here is the entire conversation
history. Also here are 10 examples of good output. Now please
summarize the key points in detail.
```

**After:**
```
Instructions (targeting 300 tokens): Summarize the document
below in 5 bullet points, each citing a page number.

Document (3,500 tokens): [trimmed to relevant sections only]

Output reserve: 500 tokens.
```

**What changed:** The prompt became a budget. Instructions are lean, the document is trimmed to relevant sections, examples are removed (task is simple enough without them), and output length is bounded. Every token the model sees is load-bearing.

## Try This Now

```
Here's a challenge. I'll give you a task and a strict token budget.

TASK: Explain how TCP's three-way handshake works.
BUDGET: Your entire response must be under 150 words.

Now do it again with a 300-word budget.

After both, note: what did you include in the 300-word version
that you cut from the 150-word version? Was the 300-word version
actually better, or did the constraint force you to be sharper?
```

This exercise demonstrates the core budget insight: constrained output is often *better* because it forces prioritization.

## When It Breaks

- **Unbounded system prompts** → Grows to 4,000 tokens because every edge case gets its own instruction. Most fire rarely or never. Audit periodically.
- **No output reserve** → The prompt fills the window, leaving no room for the response. The model compresses or silently drops requirements. Always reserve explicitly.
- **False economy** → Instructions compressed so aggressively the model misunderstands the task. Saving 200 tokens on instructions but losing thousands on a wrong output that must be regenerated.

## Quick Reference

- Family: context architecture
- Adjacent: → context_windowing (the editorial act within the budget), → explicitness (being specific costs tokens; budget determines how specific you can be), → context
- Model fit: Budgeting matters most for small/midsize models where the window is a binding constraint. Even with million-token windows, allocating tokens to relevant content improves quality — attention degrades over long, unfocused contexts regardless of capacity.
