# retrieval scaffolding

> The structure you impose on retrieved information before the model sees it — because RAG without organization is just fancy copy-paste.

## The Scene

Form8's market-research workflow has a retrieval step that pulls competitor data from multiple sources. Early version: dump ten document chunks into the prompt, no labels, no ordering. The model received a wall of text fragments — some from Gartner (authoritative), some from Reddit (not), some from 2024 (stale), some from last week (fresh). It treated them all equally, citing a Reddit rumor with the same confidence as a Gartner Magic Quadrant finding.

The fix wasn't better retrieval. It was better *presentation*. I added three things: source labels ("[Source: Gartner 2025, Trust: T1]"), date stamps, and a usage instruction ("Prefer T1 sources. Use T3 only if no alternative exists, and flag as LOW CONFIDENCE"). Same chunks. Same retrieval. Completely different output — the model now cited Gartner for market share numbers, flagged the Reddit post as unverified, and noted when sources conflicted instead of silently picking one.

## What This Actually Is

Retrieval scaffolding is the organizational layer between your retrieval system and the model. It adds metadata (source name, date, trust tier), imposes structure (grouping by source, sorting by relevance), provides usage instructions ("prefer T1 over T2"), and marks boundaries ("after reviewing these excerpts, synthesize in your own words").

Without scaffolding, the model treats all retrieved chunks equally — an official product spec and a three-year-old blog post get the same weight. Scaffolding tells the model what each chunk *is* so it can use them intelligently.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Here are some relevant docs" | "Below are 4 excerpts, each labeled [Source], [Date], [Trust Tier: T1/T2/T3]" | Model knows what each chunk is |
| "Answer from these" | "Use ONLY these excerpts. Prefer T1. If using T3, flag as LOW CONFIDENCE" | Priority rules prevent equal-weight treatment |
| "Search results:" | "Retrieved excerpts, sorted by relevance score. Top result is most relevant" | Ordering signals priority |
| "[chunk1][chunk2][chunk3]" | Group chunks by source. If two chunks share a source, merge with "[...continued]" | Grouping preserves argument structure |
| "Here's context" | "--- RETRIEVED CONTEXT --- [excerpts] --- END RETRIEVED CONTEXT --- Below this line, reason in your own words" | Boundary marker separates retrieval from generation |

## Before → After

**Before (naked chunks):**
```
Here are some documents about the competitor landscape.
Answer the user's question.
[chunk1] [chunk2] [chunk3] [chunk4]
```

**After (scaffolded):**
```
Below are excerpts retrieved from our research corpus.

[Source: Gartner Magic Quadrant 2025, Date: 2025-09, Trust: T1]
"Vendor X holds 23% market share in enterprise..."

[Source: TechCrunch Analysis, Date: 2026-02, Trust: T2]
"Vendor X reportedly lost several large accounts..."

[Source: Reddit r/enterprise_tech, Date: 2026-01, Trust: T3]
"Heard from a friend at Vendor X they're pivoting..."

Rules:
- Prefer T1 sources. Use T3 only if no T1/T2 alternative
  exists, and flag the claim as LOW CONFIDENCE.
- When sources conflict, report both and note the conflict.
- For date-sensitive facts, always note the source date.
- Do not supplement with your own knowledge.
```

## Try This Now

```
I'll give you the same three facts presented two ways.
Answer a question from each version, then compare.

VERSION A (unscaffolded):
The company had 500 employees. The company is hiring 200
people. The company laid off 50 people last quarter.

VERSION B (scaffolded):
[Source: Annual Report 2025, Date: 2025-12, Trust: T1]
"Headcount stood at 500 as of December 2025."
[Source: Job Board Listings, Date: 2026-03, Trust: T2]
"200 open positions currently listed."
[Source: Anonymous Glassdoor Review, Date: 2026-01, Trust: T3]
"50 people were let go last quarter."

Question: Is this company growing or shrinking?

Which version lets you give a more nuanced, trustworthy
answer? What can you say with Version B that you can't
with Version A?
```

## When It Breaks

- **Metadata overload** — So many labels per chunk (source, date, author, department, retrieval score, chunk ID, embedding distance) that metadata tokens crowd out the actual content. Include only metadata the model will act on.
- **Scaffolding-instruction mismatch** — You tell the model to "prioritize recent sources" but don't include dates in the labels. Or "cite by source name" but label chunks with numeric IDs only. Instructions and metadata must match.
- **Flat-list presentation** — All chunks in a flat list when the task needs hierarchy. Chunks from a primary source and secondary commentary appear interleaved with no distinction. Group by source, separate primary from secondary.

## Quick Reference

- **Family:** Context architecture
- **Adjacent:** → scaffolding (the general concept; retrieval scaffolding is the RAG-specific application), → context windowing (decides how much enters context; scaffolding decides how it's organized), → source anchoring (tying claims to sources, enabled by scaffolding's labels), → grounding (the broader goal scaffolding serves)
- **Model fit:** Frontier models handle multi-dimensional scaffolding (trust tiers + dates + conflict rules) reliably. Mid-tier models follow two-dimensional scaffolding (source + date) but may ignore priority instructions. Small models benefit most from simple labeled chunks in relevance order — push complexity upstream into the scaffolding agent.
