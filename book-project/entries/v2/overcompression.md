# overcompression

> You asked for brevity the content couldn't survive. Now the summary is technically correct and practically useless.

## The Scene

Form8's market research pipeline compresses a 10,000-word competitive analysis through four stages. The web search node returns raw data. The profiler node produces 2,000-word competitor breakdowns. The gap analyzer condenses to 800 words. The strategy writer compresses to a 300-word brief. Each stage's compression seemed reasonable — 50% here, 60% there.

The final brief said: "Competitor X has strong market share in the mid-market segment." That's technically true. What got compressed away: "Competitor X's share is concentrated in three verticals (healthcare, fintech, logistics), their growth is decelerating at 8% QoQ versus 22% last year, and their enterprise push is failing — two Fortune 500 deals fell through in Q3." The skeleton survived. The insight died. Each stage trimmed "a little," and the cumulative result was a brief that said nothing a stakeholder couldn't have guessed.

## What This Actually Is

Overcompression is what happens when you demand brevity that the content cannot survive. Not because the model can't write short, but because the subject matter can't *be* short without becoming false or trivially obvious. The mechanism is systematic: under tight length constraints, the model preserves high-frequency, high-salience content (headline facts) and drops low-frequency, high-importance content (caveats, conditions, context). "Revenue up 12%" survives. "Driven by a one-time contract, not repeatable growth" doesn't.

Three species: **length-forced** (word count too small), **scope-forced** (too many topics in too little space), and **accumulated** (each pipeline stage compresses slightly, and the cumulative loss exceeds tolerance).

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Summarize in 2 sentences" (for a 50-page report) | "Executive headline: 1 sentence, the most important finding. Key findings: 4-6 bullets. Critical caveats: 2-3 bullets noting limitations that affect decisions" | Structured compression preserves nuance in layers |
| "Keep it brief" | "Summarize in 300-500 words. Prioritize non-obvious findings over those that confirm existing assumptions" | Calibrated length + content guidance prevents trivial output |
| "One paragraph comparing five vendors" | "One paragraph per vendor (5 total). Each paragraph: positioning, key differentiator, one weakness" | Give the content the space it needs — expand the container |
| "Analyze the merger implications in 100 words" | "Describe the merger in 100 words. Then analyze three key implications in 300 words each" | Separate description (compresses well) from analysis (doesn't) |
| Trusting each pipeline stage to compress responsibly | Set a per-stage compression ratio cap (max 50%) and a cumulative floor (final must retain ≥15% of source information density) | Compression math should be visible in the design, not discovered in debugging |

## Before → After

From Form8 — fixing the pipeline compression cascade:

> **Before (unchecked compression)**
> ```
> Stage 1: Raw search results (10,000 words)
> Stage 2: Competitor profiles (2,000 words)
> Stage 3: Gap analysis (800 words)
> Stage 4: Strategy brief (300 words)
>
> Result: "Competitor X has strong market share." (true, useless)
> ```
>
> **After (compression budget)**
> ```
> COMPRESSION POLICY:
> No single stage may compress by more than 50%.
> Final output must be at minimum 500 words.
>
> Stage 4 instructions:
> Produce a strategy brief (500-750 words). Structure:
> - Headline finding: 1 sentence (the non-obvious takeaway)
> - Key findings: 4-6 bullets, each 1-2 sentences
> - Critical caveats: 2-3 bullets noting limitations
> - Oversimplification flag: if any finding cannot be
>   represented accurately in this space, note it and direct
>   the reader to the full gap analysis
>
> Prioritize: findings that would change a decision over
> findings that confirm what the reader already believes.
> ```
>
> **What changed:** The brief went from 300 words of obvious observations to 600 words with actual strategic insight. The "oversimplification flag" gave the model permission to say "this is too complex for a summary" instead of silently mangling it.

## Try This Now

Find any summary you've asked a model to produce. Now ask:

```
Compare this summary against the source material. For each
claim in the summary:
1. Is it accurate? (yes/no)
2. Is it misleading due to missing context? (yes/no)
3. What caveat or qualification was dropped in compression?

Rate the summary: FAITHFUL (accurate and fair), LOSSY
(accurate but missing important context), or DISTORTED
(technically true but would lead to wrong conclusions).
```

Most summaries land on LOSSY. The question is whether the loss matters for the reader's purpose.

## When It Breaks

- **The stakeholder squeeze** — "Give me the one-pager." The model produces one page. It omits the three caveats that would change the decision. Fix: include a "key caveats" section even in compressed output, and flag when the compression ratio risks distortion.
- **Compression cascading** — Four pipeline stages each compress 50%. The final output contains 6.25% of the original information. That math should be visible at design time. Fix: set per-stage limits and monitor cumulative compression.
- **False precision** — Overcompressed output keeps specific numbers ("revenue up 12%") while dropping context ("driven by a one-time contract"). Numbers create an illusion of precision that masks lost context. Fix: instruct the model to prioritize context over numbers when space is tight.

## Quick Reference

- **Family:** Failure mode
- **Adjacent:** → decomposition (often the fix — break the task into parts and give each adequate space), → progressive disclosure (staged information delivery avoids the need for aggressive compression), → precision (overcompression is the enemy of precision)
- **Model fit:** All models overcompress when constraints are too tight — this is mathematical, not a flaw. Stronger models make better triage decisions about what to keep. The key variable is whether the model can *flag* when compression is lossy. Claude and GPT-4 can be prompted to note when a summary omits important material; smaller models compress silently.
