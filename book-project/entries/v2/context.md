# context

> Everything in the prompt window that isn't the model's own weights — the system prompt, conversation history, attached documents, and retrieved content that determine what the model knows right now.

## The Scene

You ask the model: "Should we proceed with the Johnson deal?" It has never heard of Johnson, doesn't know your company, and has no deal documents. It either asks for clarification or — more dangerously — fabricates a plausible-sounding analysis based on nothing. You just called a consultant, refused to give them any documents, and asked for strategic advice.

That's missing context. Now the opposite: you paste a 50-page contract into the prompt and ask about a clause on page 12. The model has the answer somewhere in there, but it's buried under 49 pages of irrelevant material competing for attention. The needle is in the haystack, and the model has to find it.

Both failures are context failures, and they're the most common source of prompt problems.

## What This Actually Is

A model has two sources of information: what it learned during training (parametric knowledge) and what you give it right now (contextual knowledge). Context is the second one. For most production work, it's the more important of the two.

Context includes: **system prompts** (behavioral baseline), **conversation history** (continuity across turns), **attached documents** (reference material), and **retrieved content** (dynamically fetched information from RAG or tools).

The critical distinction: context is *information*. Framing is *orientation*. You can have perfect context — all the right documents — and still get bad output because the model doesn't know what lens to apply. Context is the library. Framing is the research question. You need both.

Context also has a hard constraint: the window. Models attend to tokens at the beginning and end more reliably than tokens in the middle. Context isn't just what you provide — it's what you provide, where you place it, and how much the model can effectively use.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| (no context, hoping the model knows) | "Using ONLY the document provided below, answer:" | Grounds the model in evidence instead of training-data guesses |
| "Here's everything" (50-page dump) | "Here is the relevant section (pages 12-18). Based ONLY on this section, answer:" | Curated context beats comprehensive context |
| "Remember what we discussed" | [Include the specific prior exchange or its summary] | Models don't remember — they see what's in the window |
| "Use your knowledge" | "CONTEXT: [labeled documents]. TASK: Using only these documents, analyze:" | Separates information (context) from instruction (task) |
| (one big blob) | "DOC 1: [Current Policy]. DOC 2: [Proposed Amendment]. DOC 3: [Impact Assessment]." | Labeled sections help the model navigate |

## Before → After

**Before:**
```
What are the key changes in the proposed energy subsidy amendment?
```

**After:**
```
CONTEXT — Source Documents:
[DOC 1: Current Subsidy Framework] {text}
[DOC 2: Proposed Amendment] {text}

TASK: Using ONLY DOC 1 and DOC 2:
1. List every change DOC 2 makes to DOC 1
2. For each change, cite the clause number in both documents
3. Flag any area DOC 1 covers that DOC 2 does not address
```

**What changed:** The model has labeled source material, a grounding instruction (ONLY these docs), and a structured task. It won't fabricate, because the prompt tells it exactly where to look.

## Try This Now

```
I'm going to give you a paragraph of context and a question.
Answer the question using ONLY the context. If the context doesn't
contain the answer, say "Not in provided context" — do not guess.

Context: "Acme Corp reported Q3 revenue of $42M, up 15% YoY.
Operating margin improved to 18% from 14% in Q2. The company
expects Q4 revenue between $44M-$48M."

Questions:
1. What was Acme's Q3 revenue? (answerable)
2. What was their Q3 headcount? (not answerable)
3. What drove the margin improvement? (partially answerable)

For each, state whether the answer is in context, not in context,
or only partially in context — then answer accordingly.
```

## When It Breaks

- **Context overload** → So much context that attention is diluted. Fix: structure with clear sections and labels, not less context — *navigable* context.
- **Stale context** → In multi-turn conversations, early turns become outdated. The model references information that was correct five turns ago. Prune or summarize old context.
- **Context without framing** → Extensive context but no instruction about what to do with it. The model has the library but no research question.

## Quick Reference

- Family: core abstraction
- Adjacent: → context_budget (how to allocate the window), → context_windowing (what to include/exclude), → anchoring (reference points within context)
- Model fit: Frontier models with 128K+ windows handle large contexts but still degrade in the middle. Smaller models need aggressive curation. All tiers benefit from labeled, structured context over raw dumps.
