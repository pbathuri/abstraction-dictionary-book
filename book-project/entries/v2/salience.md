# salience

> Not everything in the context window matters equally — salience is what the model treats as figure versus ground.

## The Scene

Form8, the n8n market-research workflow. I fed a competitive analysis agent five documents: two analyst reports, a pricing page screenshot transcript, a Reddit thread, and a 40-page industry whitepaper. The agent produced a summary that devoted three paragraphs to an offhand Reddit comment about a competitor's logo redesign and one sentence to the analyst's finding that the market had contracted 12%.

The Reddit comment was 200 words long, vivid, and positioned near the middle of the context. The market contraction finding was one sentence buried on page 31 of the whitepaper. The model didn't evaluate importance. It evaluated *token proximity and density*. The loud, nearby, verbose thing won. The quiet, distant, crucial thing lost.

I fixed it by restructuring the input. The contraction finding went first, labeled "PRIORITY 1." The Reddit thread went last, labeled "BACKGROUND — low weight." Same data. Radically different output.

## What This Actually Is

Salience is the relative importance of information within a context, and models are bad at judging it without help. A human reader skims for what matters based on task understanding. A model distributes attention based on position, token density, and statistical patterns — not task relevance. The "lost in the middle" phenomenon is a salience failure: information at the beginning and end of the context gets attention; the middle gets ghosted.

You manage salience through positioning (important stuff first), explicit markers ("PRIORITY 1"), structural separation (headers, tiers), and pruning (remove the irrelevant entirely). Every low-salience token you include dilutes attention on the high-salience tokens.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| (dump all docs in a flat list) | "PRIORITY 1 — must address: [data]. PRIORITY 2 — address if relevant: [data]. BACKGROUND: [data]" | Explicit tiers tell the model where to spend attention |
| "Here are some documents" | "The most important data point is the revenue miss on page 3. Everything else is supporting context" | Points a spotlight at the signal |
| "Consider all factors" | "Spend 70% of your analysis on the two metrics flagged HIGH. Mention the rest only if they connect" | Allocates word budget proportionally to importance |
| "Analyze this report" | "The key finding is in paragraph 4. The rest is methodology and background" | Prevents the model from summarizing boilerplate |
| "Review everything" | "Focus on sections 2 and 5. Sections 1, 3, 4 are context only — do not analyze them" | Negative scope raises salience of what remains |

## Before → After

**Before:**
```
Here are five documents about the competitive landscape.
Analyze them and tell me what matters.

[doc1] [doc2] [doc3] [doc4] [doc5]
```

**After:**
```
You are analyzing the competitive landscape. I'm providing
data in priority order.

PRIORITY 1 — Must address:
- Market contraction: 12% YoY decline (source: Gartner, p.31)
- Competitor X acquired Vendor Y (source: analyst report, p.3)

PRIORITY 2 — Address if connected to Priority 1:
- Pricing changes across top 3 competitors (source: pricing pages)

BACKGROUND — Do not analyze separately:
- Community sentiment (source: Reddit thread)
- Industry whitepaper methodology sections

Write a 300-word analysis. Spend at least 60% on Priority 1.
Mention Priority 2 only where it connects. Ignore Background
unless it directly contradicts a Priority 1 finding.
```

## Try This Now

```
I'll give you a block of text with mixed importance.
Your job: read it, then tell me which THREE facts are
most important for making a hiring decision — and which
three are noise.

"Alex has 8 years of Python experience, enjoys rock
climbing, graduated summa cum laude from MIT, once met
Guido van Rossum at a conference, reduced API latency
by 40% at their last company, has a golden retriever
named Byte, holds two patents in distributed systems,
prefers dark mode, and led a team of 12 engineers
through a successful SOC 2 audit."

After sorting signal from noise, rewrite the paragraph
with only the signal. How much shorter is it?
```

## When It Breaks

- **Flat context** — All information presented at the same level with no hierarchy. The model spreads attention evenly and produces shallow coverage of everything. Fix: tier the input explicitly.
- **Inverted salience** — Background context at the top, critical data at the bottom. The model's strongest attention hits the least important material. Fix: put the task and critical data before the context.
- **Salience by volume** — A 500-word description of a minor issue drowns a 50-word description of a major one. The model treats word count as an importance signal. Fix: normalize length to reflect actual priority, or add explicit labels.

## Quick Reference

- **Family:** Context architecture
- **Adjacent:** → signal-to-noise ratio (the aggregate measure salience produces), → context budget (salience determines how to spend it), → progressive disclosure (a technique for managing salience across stages), → scope (limits territory; salience prioritizes within it)
- **Model fit:** All models benefit from salience management. Small models benefit most — they treat everything in context equally, making explicit signals and aggressive pruning essential. Frontier models tolerate moderate noise but still measurably improve with clear hierarchy. Positioning critical information at the start outperforms burying it in the middle, always.
