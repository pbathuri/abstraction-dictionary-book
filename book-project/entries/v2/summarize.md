# summarize

> Lossy compression applied to language — keeping what matters, dropping what doesn't, and the most carelessly used instruction in all of prompting.

## The Scene

Clap/OpsPilot, the support-automation system. I needed a node that compressed 5,000-word research outputs into 500-word briefings for the Decision Agent downstream. First prompt: "Summarize the research findings." The model returned 800 words — 60% as long as the original. It reproduced the structure paragraph by paragraph, rephrasing slightly. No compression happened. It was paraphrase wearing a summary costume.

Second attempt: "Summarize for a product manager who needs to decide whether to prioritize this bug fix. 4 bullets maximum. Include any quantitative findings with exact numbers. Skip methodology — I've already read it." Output: four sharp bullets, 120 words, every one of them decision-relevant. The model didn't produce a shorter version of everything. It produced the version that mattered for the person reading it.

The delta between those two prompts is twenty words. The delta between the outputs is the difference between information and insight.

## What This Actually Is

Summarization requires four operations: comprehend the full input, identify what's essential, discard what isn't, and reconstruct the essential material in a standalone form. Each step involves judgment. What's "essential" depends on audience, purpose, and downstream use. A summary of a medical study for a physician emphasizes methodology. For a patient, outcomes and risks. For a policymaker, population impact. Same source, three different compressions, all correct.

"Summarize this" is a function call with no arguments. You get the default behavior, and the default is generic compression for no one. The three parameters that transform it: **audience** (who reads this), **length** (how compressed), and **purpose** (what will the reader do with it). Any one helps. All three together change everything.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Summarize this" | "Summarize in 4 bullets for a CFO, emphasizing anything that deviates from forecast by >10%" | Three parameters: length, audience, purpose |
| "Give me the highlights" | "Extract the 3 decisions made and 2 open action items. Skip discussion that led to decisions" | Specifies what to keep and what to cut |
| "Make it shorter" | "Compress to 150 words. If a metric is mentioned, keep the number and direction (up/down vs. prior quarter)" | Tells the model what survives compression |
| "Summarize the meeting" | "Summarize for the project sponsor who wasn't there. Focus on what changed, not what was discussed" | Audience + purpose in one sentence |
| "TL;DR" | "One sentence: the single most important takeaway for someone deciding whether to read the full document" | Forces ruthless prioritization |

## Before → After

**Before:**
```
Summarize the attached quarterly engineering report.
```

**After:**
```
Summarize the attached quarterly engineering report.

Audience: VP of Engineering, 3 minutes before an
executive review meeting.

Format:
1. "Headlines" — 3 bullets, 1 sentence each.
   The 3 most important things to know.
2. "Concerns" — 2 bullets. What should she ask about?
   Flag anything behind schedule or over budget.
3. "Good news" — 1 bullet. What exceeded expectations?

Constraints:
- Under 200 words total
- No jargon requiring engineering context
- Every metric includes the number and direction
- No padding ("overall solid progress" = delete)
```

## Try This Now

```
I'll give you the same paragraph twice. Summarize it
differently each time based on the audience.

Paragraph: "The new caching layer reduced p99 API
latency from 450ms to 120ms, a 73% improvement. However,
cache invalidation bugs caused 3 incidents in the first
week, each lasting 15-30 minutes. The team patched the
invalidation logic and has seen zero incidents in the
14 days since."

Summary 1: For a CTO deciding whether to ship it to
production. 2 sentences max.

Summary 2: For an engineer joining the on-call rotation.
3 bullets max.

After both: explain how the audience changed what you
kept and what you cut.
```

## When It Breaks

- **Summarize without audience** — The model doesn't know who's reading and defaults to generic compression that serves no one. Always specify the reader and what they'll do with the summary.
- **Primacy bias** — The model over-represents early content and under-represents late content. This is a known attention pattern. Fix: "Ensure all sections are represented proportionally" or summarize in two passes — key points from each section first, then compress those.
- **Summarize as paraphrase** — The model rewrites at roughly the same length in slightly different words. No compression occurred. Fix: enforce a compression ratio. "This 2,000-word document → exactly 5 bullet points."

## Quick Reference

- **Family:** Instructional action
- **Adjacent:** → synthesize (integrates multiple sources; summarize compresses one), → elaborate (the opposite direction — expansion vs. compression), → constrain (length limits are constraints), → framing (every summary implicitly frames what matters through what it keeps)
- **Model fit:** Short-input summarization works across all tiers. Long documents (50K+ tokens) are handled well by frontier models but show increasing primacy bias in smaller models beyond 8K tokens. For long documents with small models, chunk-then-summarize: summarize each section independently, then summarize the summaries. All tiers benefit enormously from audience + length + purpose parameters.
