# underspecification

> The prompt has shape but missing pieces — specific enough to look complete, but missing the data, constraints, or criteria the model needs, so it fills the gaps with assumptions you never approved.

## The Scene

ResumeForge, a client complaint. "The resume rewrite changed my job title." I checked the prompt: "Rewrite this resume to be competitive for the target role." Clear goal. Clear format. Clear audience. Missing: an explicit rule about not altering job titles, company names, dates, or certifications. The prompt was specific in some dimensions and had a hole in one critical dimension. The model saw the hole, walked through it, and upgraded "Junior Analyst" to "Data Analyst" because it made the resume more competitive — exactly as instructed.

The fix was one constraint: "Preserve all job titles, employer names, dates, and certifications exactly as written in the source." That constraint filled the hole. But here's the thing — I only added it because a user reported the failure. Before the report, the output *looked correct*. The model's assumptions happened to match mine on the first fifty resumes. On the fifty-first, they didn't. That's the trap: underspecification produces output that looks right until it isn't.

## What This Actually Is

Underspecification is the failure of missing pieces. Unlike vagueness (too broad), underspecification leaves holes in an otherwise clear instruction. The prompt has a goal, a format, maybe an audience — but it's missing the data, constraints, context, or criteria the model needs. The model doesn't pause. It fills the gap with plausible assumptions.

Five categories of what can be missing: **input data** (referencing information not provided), **constraints** (no bounds on what's allowed), **criteria** (asking for judgment without defining "good"), **context** (assuming the model knows your situation), and **examples** (no demonstration of what success looks like). The danger scales with model capability: weaker models produce visibly incomplete output when information is missing. Stronger models produce smooth, convincing output that papers over the gaps. GPT-4 is *worse* for underspecification than GPT-3.5 — not as a model, but as a confabulator.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Summarize this report" | "Summarize for investors, 3 bullets, focus on revenue deviation from forecast" | Adds audience, length, and focus — three common missing pieces |
| "Is this a good strategy?" | "Evaluate this strategy against three criteria: market fit, execution risk, and 18-month ROI" | Defines what "good" means |
| "Write a product comparison" | "Compare on these dimensions: price, integrations, uptime SLA, support response time" | Named dimensions prevent the model from choosing its own |
| "Update the deployment process" | "The current process is [X]. The problem is [Y]. Constraints: [Z]. Rewrite step 3 only" | Fills in the context the model can't infer |
| (no examples provided) | Include one example of correct output with annotation: "Note: this format, this depth, this tone" | For subjective quality, examples ARE specification |

## Before → After

**Before:**
```
Summarize this article.
```

**After:**
```
Summarize this article for a product designer evaluating
whether the research findings apply to our mobile
checkout flow.

- Length: 3-4 bullets, each 1-2 sentences
- Focus: product implications only (ignore methodology,
  background, author credentials)
- Include: any quantitative findings with exact numbers
- Exclude: speculation, opinions, and recommendations
  from the original author
- If the article contains no quantitative findings,
  state that explicitly.
```

**What changed:** Five specification gaps filled — audience, length, focus, inclusion criteria, and handling of a specific edge case. The model now knows what to do when it encounters a missing element.

## Try This Now

```
I'll give you a prompt. Your job: find every
underspecification — every place where the model would
have to make an assumption to complete the task.

Prompt: "Analyze our Q1 performance and recommend
next steps."

For each underspecification you find:
1. Name it (what's missing?)
2. What assumption would the model make?
3. Write the one sentence that fills the gap

After listing all gaps, rewrite the full prompt
with every gap filled. How many words did you add?
How many assumptions did you eliminate?
```

## When It Breaks

- **The invisible assumption** — The model makes a reasonable but wrong assumption, and the output looks correct until you compare it to your actual intent. Fix: before running any important prompt, read it from the model's perspective and ask "what would I assume?"
- **Specification drift across turns** — In multi-turn conversations, early constraints get buried as context grows. What was specified becomes, through attention decay, effectively unspecified. Fix: re-state critical constraints in later turns.
- **Platform-dependent underspecification** — A prompt that works on GPT-4 (which infers intent from subtle cues) may be underspecified on a smaller model. Fix: test on the deployment model, not the prototyping model.

## Quick Reference

- **Family:** Failure mode
- **Adjacent:** → vagueness (too broad; underspecification has specific missing pieces — a wide lens vs. a missing puzzle piece), → specificity (the antidote), → constrain (adding constraints fills specification gaps), → hallucination bait (underspecification creates the conditions for fabrication)
- **Model fit:** Frontier models are both best and worst at handling underspecification. Best because they sometimes infer missing pieces from subtle cues. Worst because they fill gaps so smoothly you never notice. Smaller models produce obviously bad output when information is missing — which is arguably better, because the failure is visible. Test for underspecification explicitly; don't trust output quality as a proxy.
