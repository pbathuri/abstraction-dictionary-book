# terseness

> Saying only what needs saying. Not brevity for its own sake — economy: the ratio of meaning to words.

## The Scene

Clap/OpsPilot, the incident-response pipeline. The Log Analyst agent returned 800 words per incident. Reading one took three minutes. During an outage, reading three took nine minutes — nine minutes where the on-call engineer was reading instead of fixing. I opened the outputs: 300 words of findings, 200 words of reasoning notes, 150 words of hedging ("it's worth noting," "it could potentially be the case that"), and 150 words of preamble ("I've analyzed the logs and here is what I found").

New system prompt for the Log Analyst: "Each finding is one sentence. Format: [TIMESTAMP] [SEVERITY] [FINDING]. No prose. No transitions. No context-setting. Findings only." The 800-word output became 120 words. Same information. Thirteen minutes of reading saved across three incidents. During an outage, that's the difference between diagnosis and downtime.

The next agent, Root Cause Identifier, got: "Identify the most probable root cause in one paragraph, 60 words maximum. State the cause, the evidence, and your confidence level. Nothing else." Sixty words. Every one carrying weight.

## What This Actually Is

Models are verbose by default. Their training objective rewards plausible continuation, and the most probable continuation of a sentence is another sentence. Without a terseness instruction, the model doesn't know you wanted it to stop three paragraphs ago. It explains, re-explains, summarizes the explanation, then offers a caveat about the summary.

Terseness is the corrective. Not "be brief" (the model trims 15% and calls it a day) but "every sentence must carry its own weight." Preambles ("That's a great question!"), throat-clearing ("When it comes to..."), false hedges ("It's worth noting that..."), redundant summaries ("In conclusion...") — these patterns are deeply embedded in training data. The model isn't padding on purpose. It's reproducing the padding it learned was normal.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Be concise" | "Answer in under 50 words" | Hard limit beats vague instruction |
| "Keep it short" | "One paragraph. No preamble. No summary" | Names the specific waste to cut |
| "Be brief" | "Three sentences: one per point. No transitions between them" | Structural constraint forces density |
| "Get to the point" | "Reply as if every word costs a dollar" | Memorable frame that sticks during generation |
| (no terseness instruction) | "Do not write 'it's worth noting,' 'in other words,' or 'as mentioned.' If you're about to, stop" | Explicitly bans the most common filler patterns |

## From the Lab

We tested the same content prompt at different register settings — from maximally formal to maximally terse. Verbosity correlated with register but also with information density in the opposite direction:

![Register and Verbosity](../art/figures/exp_same_content_different_register_register.png)

**Key finding:** Terse outputs consistently scored higher on information density (unique facts per 100 words) than verbose outputs at the same content level. The terse register didn't lose information — it shed the packaging around the information.

## Before → After

**Before:**
```
What is the CAP theorem? Explain it thoroughly so I
understand it well.
```

**After:**
```
What is the CAP theorem?

Answer in exactly three sentences: one per letter
(C, A, P). No preamble. No closing summary.
```

## Try This Now

```
I'll give you a verbose paragraph. Rewrite it to say
the same thing in half the words or fewer.

Rules:
- Preserve all factual claims
- Remove every sentence that restates something already said
- Remove every phrase that adds no information
- Do not add new content
- Do not summarize — rewrite

"When it comes to database indexing, it's important to
understand that there are several different types of
indexes that can be used, and each type has its own set
of advantages and disadvantages. B-tree indexes are
perhaps the most commonly used type of index, and they
work well for a wide range of query patterns. However,
it's worth noting that for certain specific use cases,
such as full-text search or geospatial queries,
specialized index types like GIN or GiST indexes may be
more appropriate and can offer significantly better
performance characteristics."

After rewriting, count the words in both versions and
report the compression ratio.
```

## When It Breaks

- **Terseness as rudeness** — The model strips padding AND the minimal courtesies that make output readable. "Mutex: sync primitive. One thread. Lock/unlock." Fine for machine consumption. Hostile in a customer response. Fix: "Be concise but not curt. Write for a colleague, not a parser."
- **False terseness** — The model uses shorter words but the same number of them, or adds "I'll keep this brief" before a non-brief response. Fix: specify a hard word or sentence limit, not just "concise."
- **Terseness that omits necessary qualification** — In domains where precision requires hedge language (medicine, law), forced terseness strips qualifiers that make the output professionally responsible. Fix: "Be terse in expression but complete in qualification."

## Quick Reference

- **Family:** Tone / style
- **Adjacent:** → specificity (controls topic scope; terseness controls word budget — they compound well), → authority (terse output reads as more authoritative), → register (terseness is one dimension of register), → narrative glue (the opposite force — adds connective tissue that terseness strips)
- **Model fit:** All tiers respond to hard length constraints (word counts, sentence limits). Frontier models also respond to subtler cues ("write like a senior engineer"). Midsize models sometimes cut information to meet length limits. Small models interpret "concise" as "short" — producing brief but not dense output. For small models, structural constraints ("3 sentences, one per point") outperform stylistic instructions ("be terse").
