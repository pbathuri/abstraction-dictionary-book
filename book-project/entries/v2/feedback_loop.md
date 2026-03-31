# feedback loop

> A cycle where output evaluation feeds back into improvement — the system watching itself and getting better from what it sees.

## The Scene

Your ResumeForge pipeline has been running for a month. Support tickets mention the same problem: cover letters sound generic, with boilerplate opening lines. But nobody has changed the prompts since launch. The system produces the same mediocre quality forever because there's no mechanism for the problem to feed back into the prompt.

You build one. Every generated cover letter gets scored on four dimensions (specificity, tone match, achievement alignment, opening hook). Weekly, you aggregate scores, cluster the low-scoring outputs by failure type, pull representative examples, draft a prompt revision, A/B test it for 48 hours, and adopt it if results improve. Two weeks later, the opening hook scores jump 40%.

That's not a prompt tweak. That's a feedback loop.

## What This Actually Is

A feedback loop is a cycle: produce, evaluate, change how you produce next time. Two fundamentally different types:

**Inner loops** operate within a single run. Generate a draft, score it, revise based on the score — all in one session. Immediate, tactical, bounded. They improve *this* output.

**Outer loops** operate across runs. Analyze logs from many executions, identify patterns, modify prompts or pipeline logic. Slow, strategic, compounding. They improve *the system*.

Both require three components:
- **Sensor**: something that evaluates (a separate model, a rule-based check, human feedback)
- **Signal**: the evaluation result in actionable form (scores, error list, critique)
- **Actuator**: a mechanism that changes behavior (prompt revision, parameter change, pipeline restructure)

A feedback loop missing any component isn't a loop — it's a dead end. Most teams log outputs but don't evaluate them. Evaluate but don't trace failures to causes. Identify causes but never change the prompts. Each of those is monitoring, not a feedback loop.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "We'll keep an eye on quality" | "If accuracy drops below 85% for a week, review and revise the retrieval prompt" | Trigger condition + response action = actual loop |
| "We should iterate" | "Inner loop: generate → score → revise (max 2 cycles). Outer loop: weekly aggregate analysis → A/B test prompt changes." | Names the loop types and their cadence |
| "Let's improve the prompts" | "Pull 5 representative low-scoring outputs, identify the shared failure pattern, draft a revision, test it" | Actionable improvement protocol, not a vague intention |
| "Users say it's not great" | "Score every output on [criteria]. Cluster failures by type. Act on any cluster exceeding 10%." | Turns anecdotal feedback into systematic signals |

## Before → After

**Before:**
```
Write a one-paragraph summary of the attached article.
```

**After:**
```
Write a one-paragraph summary of the attached article.

Then evaluate your summary:
- Does it capture the main argument? (yes/no)
- Does it include the key evidence? (yes/no)
- Is it under 100 words? (yes/no)

If any answer is "no," revise to address the gap.
Present only the final version.
```

**What changed:** The prompt now contains an inner feedback loop — generate, evaluate, revise. One cycle. The model's second look at its output catches errors the first pass missed.

## Try This Now

```
You'll write a technical explanation and then improve it
through one feedback cycle.

PASS 1 — Draft:
Explain how database connection pooling works. Target: 150 words,
for a junior developer, one concrete example.

PASS 2 — Self-evaluate and revise:
Score your draft 1-5 on:
1. Accuracy: all technical claims correct?
2. Clarity: would a junior developer understand every sentence?
3. Concreteness: does the example illustrate the concept?
4. Conciseness: is every sentence load-bearing?

For any criterion below 4, explain what's wrong and revise.
Present the revised version with before/after scores.
```

Notice how the evaluation step forces genuine improvement, not cosmetic rewriting.

## When It Breaks

- **Open loop** → Evaluation without action. You score outputs, build dashboards, track metrics, but never change the prompts based on what you learn. That's monitoring, not a loop. Fix: define a response action for every trigger condition.
- **Overcorrection** → One bad output triggers a prompt rewrite that fixes that case but breaks ten others. Fix: require a minimum sample size before acting. A/B test changes before adopting.
- **Stale feedback** → Evaluation criteria that don't evolve. You built the rubric six months ago but the input distribution shifted. The loop optimizes for yesterday's definition of quality. Fix: review criteria on a regular cadence.

## Quick Reference

- Family: quality control
- Adjacent: → checkpoint (provides evaluation points that generate signals), → audit_trail (data source for outer loops), → critique (the inner-loop mechanism that drives revision)
- Model fit: Inner loops (self-critique + revision) work reliably with large models. Smaller models tend to agree with their own output — use a separate, stronger model as evaluator, or rely on rule-based evaluation.
