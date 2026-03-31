# rubric

> If you can't define "good," the model can't produce it.

## The Scene

ResumeForge had a generation problem and an evaluation problem. The generation problem — hallucinated credentials, inflated metrics — got solved with → constraints and → grounding. But then I had a new question: how do I know if a rewrite is actually *good*?

"Good" meant different things depending on who you asked. To the candidate, good meant "I sound impressive." To an ATS parser, good meant "keywords from the JD appear in the right density." To me as the builder, good meant "truthful, well-targeted, and not going to get someone fired when their employer checks." These aren't the same thing, and the model couldn't optimize for all three without knowing which mattered and how much.

So I built a rubric. Five criteria, each with a weight and a pass/fail definition:

```
RESUME REWRITE SCORING RUBRIC

1. Truthfulness (30%) — PASS: every claim traceable to source
   resume. FAIL: any fabricated credential, metric, or employer.

2. JD Alignment (25%) — PASS: 3+ key requirements from the JD
   addressed with evidence. PARTIAL: 1-2 addressed. FAIL: none.

3. ATS Compatibility (20%) — PASS: critical JD keywords appear
   naturally. FAIL: keyword-stuffed or zero keyword overlap.

4. Specificity (15%) — PASS: bullets include concrete outcomes
   (numbers, scope, or named tools). FAIL: vague, generic phrasing.

5. Voice Preservation (10%) — PASS: candidate's original
   communication style is recognizable. FAIL: rewrite sounds like
   a completely different person.
```

I used this rubric in two ways. First, I embedded it in the generation prompt so the model *knew* what it was being scored on. Second, I fed the output + rubric to a separate evaluator model that scored each criterion. The rubric turned "is this resume good?" from a vibes question into a measurable one.

## What This Actually Is

A rubric is an explicit list of what "good" means, written before you see the output. It's the checklist the verifier uses, the scorecard the evaluator applies, and the specification the generator targets — often all in the same document.

Without a rubric, evaluation is: read it, feel something, decide. That works for one output. It doesn't work for a hundred, or for a pipeline that runs while you sleep, or for an agent that needs to decide whether to ship or revise. Rubrics convert intuition into criteria. The criteria don't have to be perfect. They have to be *explicit* — because explicit criteria can be debated, improved, and automated, and implicit ones can't.

Three uses, each essential. **Design guidance:** writing the rubric before the prompt forces you to decide what you actually want. Most prompt failures trace back to never having answered this question. **Automated evaluation:** feed the output + rubric to a separate model (LLM-as-judge), get a score. Now you can run A/B tests on prompts, detect regressions, and monitor quality at scale. **Verification criteria:** in a → verification loop, the rubric is what the verifier checks. Without it, the verifier has no standard. With it, the verifier has a job.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Is this good?" | "Score this output on: accuracy (1-5), completeness (1-5), clarity (1-5). For each, give one sentence of evidence" | Turns a feeling into a measurement |
| "Needs improvement" | "Fails criterion 3: no source citations found. Revise to include [source_id] for each factual claim" | Points to the specific criterion and the specific fix |
| "Review this" | "Apply the evaluation rubric below. For each criterion, mark PASS/PARTIAL/FAIL with a one-sentence justification" | Makes the review structured and auditable |
| "Make it better" | "Target score: 4+ on every criterion. Current weakest: specificity (2). Revise to add concrete metrics or scope markers to each bullet" | Ties revision to the specific dimension that's lagging |
| "Check quality" | "Gate: output must score PASS on all weighted criteria before advancing to the next agent" | Makes the rubric a hard gate in the pipeline |

**Power verbs for rubric use:** score, evaluate against, gate on, weight, calibrate, benchmark, audit.

## Before → After

From ResumeForge — using the rubric both to generate and to evaluate:

> **Before (rubric-less generation)**
> ```
> Rewrite this resume bullet to be more impactful for the job
> description. Make it strong and quantified.
> ```
> *Result: model optimizes for "impact" — the vaguest possible target. Output varies wildly between runs.*
>
> **After (rubric-informed generation + evaluation)**
>
> *Generation prompt (rubric embedded):*
> ```
> Rewrite this resume bullet for the target JD. Your output will
> be scored on:
> 1. Truthfulness — is every claim in the source resume?
> 2. JD Alignment — does it address a key requirement from the JD?
> 3. Specificity — does it include a concrete outcome?
> 4. Voice — does it sound like the original candidate?
>
> Optimize for all four. If they conflict, prioritize truthfulness.
> ```
>
> *Evaluation prompt (separate model):*
> ```
> You are a resume quality evaluator. Score the following rewrite
> against this rubric:
>
> | # | Criterion    | Weight | PASS                      | FAIL                    |
> |---|-------------|--------|---------------------------|-------------------------|
> | 1 | Truthfulness | 30%    | All claims in source      | Any fabrication         |
> | 2 | JD Alignment | 25%    | 3+ JD requirements mapped | Fewer than 1            |
> | 3 | ATS Keywords | 20%    | Critical keywords present | Zero keyword overlap    |
> | 4 | Specificity  | 15%    | Concrete outcomes cited   | Vague, generic phrasing |
> | 5 | Voice        | 10%    | Original style preserved  | Unrecognizable voice    |
>
> Source resume: [attached]
> Rewrite: [attached]
> JD: [attached]
>
> Return: JSON with score per criterion + weighted total + SHIP/REVISE/REJECT.
> ```
>
> **What changed:** "Make it good" became a 5-criterion rubric. The generator knows what it's being scored on. The evaluator applies the same scorecard independently. Quality is now measurable, repeatable, and debuggable.

## Try This Now

Take the last prompt you wrote that produced "okay but not great" output. Paste it with this wrapper:

```
I have a prompt that produces mediocre output. Before I fix the
prompt, I need to define what "good" actually means.

Help me build a rubric. For this prompt, define:
- 4-5 criteria that distinguish great output from mediocre output
- For each criterion: a PASS definition and a FAIL definition
- A weight (should sum to 100%)
- Which criterion to prioritize when they conflict

Then rewrite the prompt to include the rubric as explicit
success criteria.

Here's my prompt:
[paste your prompt here]
```

The rubric is usually more valuable than the prompt fix. Once you have the rubric, the fix is often obvious.

## From the Lab

We tested how verb choice in critique and evaluation prompts affected rubric application quality. The right verbs produced more discriminating, more actionable evaluations:

![Critique Verbs Word Choice](../art/figures/exp_critique_verbs_word_choice.png)

**Key finding:** Evaluation prompts using verbs like "assess," "diagnose," and "score against" produced sharper, more discriminating rubric scores than those using "review" or "check." The more specific the evaluation verb, the less the model rubber-stamped. "Rate each criterion 1-5 and cite specific evidence" outperformed "tell me if this is good" by a wide margin on inter-rater agreement with human evaluators.

## When It Breaks

- **Rubric bloat** → 20 criteria, half redundant, the evaluator loses focus and checks trivial things while missing important ones. Fix: 5-8 criteria max. If two criteria always pass or fail together, merge them. Each criterion should be independently meaningful.
- **Rubric without teeth** → The rubric exists in a planning doc but isn't actually applied to outputs. Nobody feeds it to the verifier. Nobody uses it to gate the pipeline. A rubric that isn't executed is documentation, not quality control.
- **Rubric-prompt mismatch** → The prompt says "summarize this article." The rubric checks for "actionable recommendations." The model fails the rubric not because it performed poorly but because the rubric and prompt were designed by different people who never talked. Fix: derive the prompt *from* the rubric. Every criterion should map to an explicit instruction.

## Quick Reference

- **Family:** Quality control
- **Adjacent:** → verification loop (the process that applies the rubric), → constrain (limits the model during generation; rubrics evaluate after), → test harness (the infrastructure that runs rubric-based evaluations at scale), → regression check (uses rubric scores to detect quality degradation)
- **Model fit:** LLM-as-judge evaluation works best with frontier models, which show high agreement with human evaluators on well-defined rubrics. Mid-tier models evaluate binary criteria (PASS/FAIL) reliably but struggle with graded scales. Strategy: use a frontier model for rubric evaluation and a lighter model for generation. Calibrate against human-evaluated samples before deploying at scale.
- **Sources:** Zheng et al. (2023) MT-Bench, Schulhoff et al. (2025) Prompt Report, ResumeForge scoring criteria
