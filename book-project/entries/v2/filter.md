# filter

> Remove what doesn't belong so what remains is worth using.

## The Scene

Form8, my n8n market-research workflow, had a retrieval problem. The web-search node returned twenty results for every competitor query. Most were irrelevant — press releases from unrelated companies, LinkedIn posts, outdated blog entries. I was feeding all twenty into the analysis node and wondering why the competitive profiles read like they were written by someone who'd Googled the wrong company.

The fix wasn't a better search query. It was a filter node between search and analysis. Three criteria: must mention the company by name, must be dated within 18 months, must contain at least one of five target keywords (pricing, features, market share, funding, customers). Twenty results became five. The analysis node stopped hallucinating competitor details because it stopped receiving garbage to hallucinate from.

## What This Actually Is

Filtering is selection by exclusion. You start with a set — search results, candidate sentences, data rows, generated options — and you remove everything that fails your criteria. What survives is smaller, cleaner, and actually usable.

The key distinction: a constraint prevents bad output from being *generated*. A filter removes bad output *after* generation. Constraints shape the mold. Filters trim the casting. In practice, you need both. Constraints get the model into the right neighborhood. Filters evict the stragglers. The generate-then-filter pattern often outperforms heavy up-front constraining because it preserves creative breadth while still delivering a focused result.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Show me the relevant ones" | "Remove any result not published after January 2024" | Testable criterion, not a vibe |
| "Keep the good ones" | "Pass only items scoring above 7/10 on the rubric" | Quantitative threshold the model can apply |
| "Filter out the noise" | "Exclude items that don't mention at least two of these keywords: [list]" | Turns an abstraction into a checklist |
| "Only include what matters" | "For each item, verdict: PASS or FAIL. If FAIL, cite the criterion number it violated" | Forces the model to show its filtering work |
| "Clean up this list" | "Remove duplicates, then remove any item where company revenue is under $10M" | Two specific, ordered filter operations |

**Power verbs for filtering:** exclude, remove, discard, retain (only), pass, reject, screen, winnow, cull, sieve.

## Before → After

From Form8's competitor research pipeline — the actual node-level change:

> **Before**
> ```
> Here are 20 search results about competitors in the CRM
> space. Analyze each competitor's positioning and pricing.
> ```
>
> **After**
> ```
> FILTER NODE (runs before analysis):
> Input: 20 search results
> Criteria — pass all three or discard:
> 1. Mentions competitor by exact company name (not just industry)
> 2. Published after July 2024
> 3. Contains at least one of: pricing, features, market share,
>    funding round, customer count
>
> Output per result:
> - URL, title, date
> - Verdict: PASS / FAIL
> - If FAIL: which criterion was not met
>
> Pass only PASS results to the analysis node.
> If fewer than 3 results pass, relax criterion 2 to "after
> January 2024" and re-run.
> ```
>
> **What changed:** The analysis node went from processing twenty results (most noise) to processing five (mostly signal). Competitor profiles stopped including phantom companies because the phantom results never reached the analyst.

## Try This Now

Take any list-producing prompt you've used recently — search results, brainstormed ideas, candidate solutions. Now write a filter prompt for the output:

```
I'll give you a list of [N] items. Apply these filter criteria
to each:
1. [your first testable criterion]
2. [your second testable criterion]

For each item, output:
- Item title or summary
- PASS or FAIL
- If FAIL: which criterion it violated

After filtering, report: X of N passed. Most common failure
reason: [criterion number].
```

The report at the end is the real value — it tells you whether your filter criteria are too strict, too loose, or just right.

## When It Breaks

- **Criterion creep** — You specified eight filter conditions and the model applies some while silently ignoring others. Limit filters to 3-5 clear conditions. If you need more, chain two filter steps with distinct criteria at each.
- **Over-filtering** — Your criteria are valid but too strict for this input set. Everything fails. Fix: rank items by degree of match rather than binary pass/fail, and return the top N.
- **Subjective criteria masquerading as filters** — "Remove anything not useful" removes nothing because the model can justify the usefulness of anything. Swap qualitative words for quantitative or categorical ones. "Published after 2023" is enforceable. "Useful" is not.

## Quick Reference

- **Family:** Instructional action
- **Adjacent:** → constrain (preventive where filter is corrective), → evaluate (scores items; filter acts on those scores), → rank (orders by quality; filter sets a pass/fail threshold)
- **Model fit:** Clear categorical criteria work across all sizes — even small models can check "contains keyword X." Judgment-based filtering (relevance, quality) needs larger models. For production pipelines, use small models for hard-criteria filtering and large models only for soft-criteria ranking.
