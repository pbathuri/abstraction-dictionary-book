# synthesize

> Combining multiple sources into a unified whole that produces insight none of the inputs contained alone. Not summary. Not a stack of summaries. Integration.

## The Scene

Form8, the market-research workflow. Three upstream nodes fed into a final "strategy brief" node: one pulled academic literature, one scraped industry reports, and one processed expert interviews. First prompt for the brief node: "Summarize the findings from all three sources." Output: three paragraphs. Paragraph one: what the papers said. Paragraph two: what the reports said. Paragraph three: what the experts said. Organized by source. Zero integration. It was three summaries stapled together.

Second attempt: "Synthesize these three research streams into a single strategic brief. Organize by theme, not by source. Where sources agree, state the consensus. Where they contradict, flag the tension and assess which evidence is stronger. End with: what picture emerges only when you read all three together?"

The output organized around three themes that cut across all sources. It surfaced a contradiction between the quantitative projections and the expert interviews that no single source revealed. The "what emerges" paragraph identified a market timing window that only became visible at the intersection. Same data. Different instruction. Fundamentally different output.

## What This Actually Is

Summary compresses one source into a smaller version. Synthesis takes *multiple* sources and makes them *one*. The operation has three phases: comprehension (understanding each input), alignment (identifying where inputs overlap or conflict), and integration (weaving them into a coherent whole). The third phase is where the value lives. Comprehension is reading. Alignment is comparison. Integration is the thing only synthesis does.

Models default to multi-document summary when asked to "synthesize" — a paragraph per source, organized by origin. The fix is specifying the axis of integration: "organize by theme, not by source." That single instruction transforms a reading list into an insight.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Summarize all of these" | "Synthesize into a single account. Organize by theme, not by source" | Forces integration over sequential summary |
| "What do these sources say?" | "Where do these sources converge? Where do they conflict? What picture emerges from their intersection?" | Three questions that drive integrative thinking |
| "Combine the reports" | "Identify the 3-5 themes that appear across at least two sources. For each, integrate evidence from all relevant sources" | Named themes prevent source-by-source organization |
| "Give me the key takeaways" | "What conclusions can be drawn only by reading these sources together, not from any single source alone?" | Targets the unique value of synthesis |
| "Merge the findings" | "Cite each claim as [ACADEMIC], [INDUSTRY], or [EXPERT]. Flag single-source findings as lower confidence" | Cross-referencing enforces actual integration |

## Before → After

**Before:**
```
I have three research documents. Summarize the key
points from each.
```

**After:**
```
I have three documents:
1. Quantitative market analysis (data, projections)
2. Qualitative user research (interviews, themes)
3. Competitive landscape overview (positioning, features)

Synthesize into a 500-word strategic brief answering:
"Should we enter this market in the next 12 months?"

Structure around these questions:
- Is there sufficient demand? (draw on docs 1 and 2)
- Can we compete? (draw on docs 2 and 3)
- Risks of entry vs. risks of waiting? (all docs)

Where documents contradict, flag the tension and assess
which evidence is more reliable for that specific question.

Do not summarize each document. I've read them. I need
the picture that emerges from reading them together.
```

## Try This Now

```
I'll give you three brief "source" statements from
different perspectives on the same topic.

Source A (researcher): "Remote work increases individual
productivity by 13% but reduces spontaneous collaboration
by 20%."

Source B (manager): "My team ships features faster remote,
but our cross-team projects take 40% longer."

Source C (employee): "I get more deep work done at home,
but I feel disconnected from company direction."

Synthesize these into 3 sentences. Rules:
- Organize by theme, not by source
- Show where sources converge and where they diverge
- End with one insight that only emerges from reading
  all three together
```

## When It Breaks

- **Synthesis as multi-summary** — The model writes a paragraph per source and calls it synthesis. No integration occurred. Fix: explicitly instruct "organize by theme, not by source" and specify themes or ask the model to identify them first.
- **Premature consensus** — The model papers over genuine disagreements to produce a smooth, unified account. The output *looks* like good synthesis but has suppressed important tensions. Fix: require "identify and discuss any contradictions or unresolved disagreements between sources."
- **Theme invention** — The model invents organizing themes not present in the source material. The output reads well but maps poorly to the actual inputs. Fix: specify themes yourself, or add a verification step checking claims against sources.

## Quick Reference

- **Family:** Instructional action
- **Adjacent:** → summarize (compresses one source; synthesis integrates multiple), → compare (the alignment step that often precedes synthesis), → elaborate (expands a single point; synthesis converges multiple points), → decomposition (the inverse operation — breaking apart vs. building together)
- **Model fit:** Frontier models handle multi-document synthesis well, maintaining thematic coherence. Midsize models manage 2-3 short sources but revert to sequential summary as input volume rises. Small models rarely produce true synthesis — break the task into explicit phases (compare first, then integrate) using separate prompts.
