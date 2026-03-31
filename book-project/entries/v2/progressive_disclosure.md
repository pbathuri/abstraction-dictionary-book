# progressive disclosure

> Don't dump everything into the context and hope the model sorts it out. Give it what it needs, when it needs it.

## The Scene

Form8's competitor research pipeline originally front-loaded everything. The analysis node received: the raw search results (20 items), the product description, the target market spec, the output format requirements, three example competitor profiles, and a 200-word rubric. The model was supposed to find what it needed in that wall of context. It reliably buried the rubric under the weight of the examples and produced profiles that matched the examples' structure but ignored the rubric's criteria.

I restructured into three stages. Stage 1: receives raw search results + filter criteria only. Task: filter to the 5 most relevant results. Stage 2: receives the 5 filtered results + the product description. Task: extract competitor profiles with specific fields. Stage 3: receives the profiles + the rubric. Task: score and rank. At no point does any stage see information meant for a different stage. The rubric doesn't compete with examples for attention because they never appear in the same context.

## What This Actually Is

Progressive disclosure is revealing information to a model in stages rather than all at once. Borrowed from UI design (show only the controls a user needs at each step), it translates directly to prompt architecture. Instead of a monolithic context, each stage receives only the information relevant to its task.

Two constraints drive this. The hard constraint: context windows are finite, and stuffing them with irrelevant material pushes out what matters. The soft constraint: even within the window, attention isn't uniform. The "lost in the middle" effect means information buried in a long context gets underweighted. Progressive disclosure sidesteps both by keeping the context small and focused at every step.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| One prompt with all context front-loaded | Break into 3 stages: each receives only the information for its task | Smaller context = higher signal-to-noise ratio at every step |
| Passing a 10-page document for a question about page 7 | Stage 1: "Identify which sections are relevant to [question]." Stage 2: provide only those sections + the question | The model does retrieval OR reasoning — don't make it do both |
| Including all reference materials "just in case" | Conditional disclosure: provide regulatory text only if the initial analysis flags a compliance risk | Prevents irrelevant material from biasing the analysis |
| Forwarding full Stage 1 output to Stage 2 | Stage 1 produces a structured output. Stage 2 receives only that structured output, not Stage 1's raw inputs | Intermediate representations prevent context bloat |
| "Here's everything, figure out what's relevant" | "You will receive information for this stage only. Previous stage outputs have been summarized. Source documents are not included — work with the findings provided" | Explicit scoping tells the model its world is intentionally limited |

## Before → After

From Form8 — staged information delivery:

> **Before (everything at once)**
> ```
> Here are 20 search results, a product description, a target
> market spec, 3 example competitor profiles, and a scoring
> rubric. Produce ranked competitor profiles.
> ```
> (Rubric ignored — lost in the middle of a 3,000-token context)
>
> **After (progressive disclosure)**
> ```
> STAGE 1 — Filter
> Input: 20 search results + 3 filter criteria
> Task: Return the 5 most relevant results. Output: JSON array
> with URL, title, relevance score.
> (Stage 1 sees: search results + criteria. Nothing else.)
>
> STAGE 2 — Profile
> Input: 5 filtered results + product description
> Task: For each competitor, extract: name, positioning,
> pricing tier, key features, target segment.
> Output: structured competitor profiles (JSON).
> (Stage 2 sees: filtered results + product desc. No rubric,
> no examples, no raw search results.)
>
> STAGE 3 — Score
> Input: 5 competitor profiles + scoring rubric
> Task: Score each profile against the rubric. Rank by total
> score. Flag any profile with incomplete data.
> (Stage 3 sees: profiles + rubric. No search results, no
> product description, no filter criteria.)
> ```
>
> **What changed:** The rubric finally got used — because in Stage 3, it's 20% of the context instead of 5%. Each stage has a signal-to-noise ratio close to 1.0 because irrelevant material is never present.

## Try This Now

Take any long prompt (200+ words). Highlight each piece of information and label it by which stage of the task actually uses it. Then restructure:

```
For your longest prompt, identify:
1. What information does the model need to UNDERSTAND the task?
2. What information does it need to EXECUTE the task?
3. What information does it need to FORMAT the output?

Now run them as three separate stages:
- Stage 1 gets only understanding context
- Stage 2 gets Stage 1's output + execution data
- Stage 3 gets Stage 2's output + format requirements
```

Compare against the single-prompt version. The staged version will follow formatting instructions more consistently because they're not competing with task content for attention.

## When It Breaks

- **Under-disclosure** — Withholding information a stage genuinely needs. The model produces confidently wrong output because it lacked critical context. Fix: for each stage, explicitly list what the model needs and verify it's present before running.
- **Disclosure leakage** — Passing forward the full context from the previous stage instead of just the intermediate result. You've recreated the monolithic context across steps. Fix: each stage should produce structured output that the next stage consumes. Raw inputs should not propagate forward.
- **Premature synthesis** — Asking the model to draw conclusions at an early stage when it only has partial information. Those conclusions anchor everything downstream. Fix: early stages should report findings, not conclusions. Conclusions belong in the final stage.

## Quick Reference

- **Family:** Context architecture
- **Adjacent:** → decomposition (breaks the task into stages; progressive disclosure breaks the context into stage-appropriate portions), → information routing (decides what data each agent receives — progressive disclosure applied to pipelines), → overcompression (staged disclosure avoids the need for aggressive compression)
- **Model fit:** Benefits all tiers but most critical for smaller models with limited context or weaker long-context retrieval. Frontier models with 128K+ windows tolerate monolithic prompts better but still produce higher-quality output with staged disclosure. The overhead of managing stages is always repaid in output quality.
