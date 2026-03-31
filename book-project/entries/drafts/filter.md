---
headword: "filter"
slug: "filter"
family: "instructional_action"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# Filter

**Elevator definition** Removing items from a set based on criteria — the corrective scalpel where constraint is the preventive fence.

## What it is

Filtering is selection by exclusion. You start with a set of items — search results, candidate sentences, data rows, list entries — and you remove everything that doesn't meet specified criteria. What remains is the filtered output: smaller, more relevant, more usable.

The operation is deceptively simple. In programming, a filter is a pure function: predicate in, subset out. In prompt engineering, it's messier because the "predicate" is often a natural-language criterion ("remove anything not relevant to enterprise customers") and the "items" are often unstructured text rather than typed objects. The model must interpret both the criteria and the items, then make judgment calls about borderline cases. This makes filtering one of the most common sources of surprising behavior in LLM outputs.

Filtering in LLM contexts takes several forms. **List filtering** removes items from an explicit list based on stated criteria. **Content filtering** removes passages, sentences, or claims from a larger text. **Result filtering** narrows a set of retrieved documents or search results to the most relevant subset. **Quality filtering** removes outputs that don't meet a quality threshold — a special case where the "set" is a batch of generated candidates and the filter selects the best.

The critical design decision in any filter is the criterion. Vague criteria produce vague filtering. "Remove irrelevant items" is barely a filter — it pushes the entire judgment of relevance onto the model without guidance. "Remove items where the company has fewer than 100 employees or is headquartered outside North America" is a real filter — it specifies testable conditions.

Filtering differs from constraint in timing and mechanism. A constraint prevents the model from generating certain content in the first place — it's preventive. A filter removes content after generation — it's corrective. Constraints shape the generation distribution. Filters trim the generation output. Both narrow what the user sees, but they operate at different points in the pipeline.

In practice, both are usually needed. Constraints reduce the work that filters have to do. Filters catch what constraints miss. A well-designed pipeline uses constraints to get the generation into the right neighborhood and filters to remove the remaining outliers.

## Why it matters in prompting

Filtering is how you turn a broad model response into a precise one. Ask a model to "list marketing strategies for a SaaS startup" and you'll get twenty items of varying relevance. Add a filter — "now remove any strategy that requires more than $5,000/month in ad spend" — and the list becomes actionable for a bootstrapped team.

This two-step pattern (generate broadly, then filter specifically) is often more effective than trying to constrain the generation up front. The reason is that constraints compete with each other for the model's attention, and heavily constrained generation tends to produce narrower, less creative output. Generating first and filtering second preserves the creative breadth while still delivering a focused result.

## Why it matters in agentic workflows

In agent pipelines, filter agents are gatekeepers. They sit between stages and remove items that shouldn't proceed. A retrieval agent returns twenty documents; a filter agent passes the five most relevant to the analysis stage. A generation agent produces ten candidate responses; a filter agent selects the three that meet quality criteria.

Filter agents reduce downstream cost and improve downstream quality. Every item that passes the filter is one more item that downstream agents must process. Effective filtering keeps the pipeline lean. Ineffective filtering — either too aggressive (removes good items) or too permissive (passes bad items) — either starves or floods downstream stages.

The filter agent's criteria should be explicit, testable, and documented. "Relevant" is not a criterion. "Contains at least two of the five target keywords and was published after January 2024" is a criterion. The more testable the filter criteria, the more debuggable the pipeline.

## What it changes in model behavior

When filtering is separated from generation as a distinct prompt step, the model applies a genuinely different cognitive mode — evaluative rather than generative. Each item is assessed against criteria rather than produced from imagination. This separation produces more rigorous filtering than in-generation constraints, which the model may interpret as soft preferences.

## Use it when

- You have a set of items that's too large or too noisy for downstream use
- The criteria for inclusion are clear enough to specify as testable conditions
- You want to preserve the breadth of generation while narrowing the delivery
- A pipeline step needs fewer, higher-quality inputs rather than many unvetted ones
- You're implementing quality control on a batch of generated candidates

## Do not use it when

- You can constrain generation to produce only the desired items in the first place (simpler, cheaper)
- The set is already small enough that manual review is practical
- The filter criteria are too subjective to specify reliably ("remove the boring ones")
- Removing items loses context that the remaining items need (interdependent items)

## Contrast set

- **Constraint** → A constraint prevents generation of undesired content; a filter removes it after generation. Constraint is preventive. Filter is corrective.
- **Analyze** → Analysis decomposes items to understand them; filtering selects items based on criteria. Analysis is for understanding. Filtering is for selection.
- **Evaluate** → Evaluation scores items on quality dimensions; filtering uses scores (or criteria) to include or exclude. Evaluation produces signals. Filtering acts on them.
- **Curate** → Curation is filtering with editorial judgment — selecting items based on taste, narrative fit, or audience. Filtering is criteria-based. Curation is judgment-based.

## Common failure modes

- **Criterion creep → the filter criterion is so complex that the model can't apply it consistently.** You specify twelve conditions for inclusion, some of which conflict. The model applies some and ignores others unpredictably. Fix: limit filter criteria to 3-5 clear conditions. If you need more, chain multiple filters with distinct, simple criteria.
- **Over-filtering → the filter removes too aggressively, leaving an empty or impoverished set.** Your criteria are valid but too strict for the input set. Fix: rank items by degree of criterion match rather than binary pass/fail. Return the top N rather than everything that passes.
- **Under-filtering → the filter passes almost everything because the criteria are too vague.** "Remove anything not useful" removes nothing because the model can justify the usefulness of anything. Fix: replace qualitative criteria with quantitative or categorical ones. "Published after 2023" is enforceable. "Useful" is not.

## Prompt examples

### Minimal example

```
Here is a list of 15 feature requests from users.
Filter this list to only include requests that:
1. Are technically feasible with our current stack (Python, PostgreSQL, React)
2. Would affect more than 10% of users based on the descriptions
3. Can be implemented in under 2 weeks of developer time
Return only the items that pass all three criteria.
```

### Strong example

```
You are a research assistant filtering academic papers for relevance.

Input: {list_of_paper_abstracts}

Filter criteria (all must be met):
1. Published 2022 or later
2. Addresses at least one of: prompt engineering, chain-of-thought reasoning,
   or LLM evaluation methodology
3. Reports empirical results (not purely theoretical or position papers)
4. Sample size or evaluation set exceeds 100 examples

For each paper, output:
- Title
- Verdict: PASS or FAIL
- If FAIL: which criterion was not met (cite the specific criterion number)
- If PASS: one sentence on why it's relevant to our research question

After filtering, summarize: X of Y papers passed. Distribution of failure
reasons: [criterion 1: N, criterion 2: N, ...].
```

### Agentic workflow example

```
pipeline: candidate_screening
agents:
  - sourcer:
      task: retrieve 50 candidate profiles matching job description
      output: list of profiles with structured fields

  - filter_stage_1:
      task: hard-criteria filter
      criteria:
        - minimum 3 years relevant experience
        - required skills present (Python, SQL, at minimum)
        - located in or willing to relocate to approved regions
      output: filtered list + rejection_log with reasons
      expected_pass_rate: 40-60%

  - filter_stage_2:
      task: soft-criteria ranking
      criteria:
        - project complexity score (based on described work)
        - career trajectory (growth pattern)
        - domain relevance (overlap with our industry)
      output: ranked list with scores per criterion
      action: pass top 15 to interview_scheduler

  - quality_check:
      verify: no candidate was filtered for a criterion not in the
              approved list. Check rejection_log for unauthorized reasons.
      verify: at least 10 candidates reached stage 2 (if not, relax
              stage 1 criteria and re-run)
```

## Model-fit note

Filtering with clear, categorical criteria works well across all model sizes — even small models can check "published after 2022" or "contains keyword X." Filtering with nuanced, judgment-based criteria (relevance, quality, feasibility) requires larger models. For production pipelines, consider using smaller models for hard-criteria filtering (fast, cheap) and larger models only for soft-criteria ranking (slow, expensive, higher judgment).

## Evidence and provenance

Filtering as a computational primitive has roots in relational algebra (Codd, 1970) and functional programming. In LLM contexts, filtering patterns are documented in retrieval-augmented generation research (Lewis et al., 2020, RAG) where document relevance filtering directly impacts output quality. Quality filtering of generated candidates is studied in best-of-N sampling literature (Stiennon et al., 2020).

## Related entries

- → **contrast** — Contrast reveals the differences that inform filter criteria; effective filtering often follows a contrast step that identifies what matters.
- → **analyze** — Analysis produces the understanding that informs filter design; you must understand your items before you can effectively filter them.
- → **checkpoint** — Filters often operate at checkpoints, gating what proceeds to the next pipeline stage.
- → **feedback_loop** — Filter performance (pass rates, false rejections) is a key signal in feedback loops for pipeline improvement.
