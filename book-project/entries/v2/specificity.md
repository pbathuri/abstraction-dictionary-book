# specificity

> The degree to which your prompt narrows the space of acceptable answers by naming exactly what you want.

## The Scene

Last year I was building ResumeForge — a tool that tailors resumes to job descriptions using a local LLM. The first prompt I wrote for the rewrite engine looked like this:

```
Improve this resume bullet point for the given job description.
```

The model returned a bullet point that was, technically, "improved." It was also completely fabricated. It added a certification the candidate didn't have, inflated a team size from 3 to 15, and swapped "contributed to" with "led the transformation of." The resume was now a fiction.

The problem wasn't the model. The problem was the prompt. I had told it *what to do* (improve) without telling it *what improvement means* (truthful, ATS-safe, evidence-backed). I had left every important decision to the model, and the model made them all wrong.

The fix took thirty seconds:

```
Rewrite this resume bullet for the target JD. Constraints:
- Never fabricate employers, titles, dates, or certifications
- Never inflate team size, scope, or metrics
- If a claim needs evidence the candidate hasn't provided, flag it
  as evidence_required=true instead of inventing support
- Preserve the candidate's actual verb ("contributed to" stays, not "led")
```

Same model. Same resume. Completely different output. The only variable that changed was specificity.

## What This Actually Is

Specificity is choosing not to say "analyze this" when you mean "identify the three metrics that changed most quarter-over-quarter." It is the single largest lever in prompt engineering, and the one most consistently underused.

It works along five axes: **content** (what to address), **format** (how to structure it), **scope** (how much to cover), **criteria** (what counts as good), and **audience** (who reads it). Most weak prompts fail on at least three of these. Most strong prompts nail at least three.

One counterintuitive finding: more specific is not always better. Schreiter (2024) tested word-level specificity across four LLMs and three domains, and found an optimal range — a sweet spot where the model performs best. Push verb specificity past that ceiling and reasoning performance actually *drops* [src_paper_schreiter2024]. Specificity is a tuning knob, not a volume dial.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Analyze this data" | "Identify the 3 largest cost drivers in Q3" | Names the operation, count, and scope |
| "Summarize the document" | "Extract the 5 key decisions from this meeting" | Specifies what to extract and how many |
| "Help me write an email" | "Write a 150-word email to enterprise buyers emphasizing time-to-value" | Adds length, audience, and angle |
| "Review this code" | "Check this function for unhandled edge cases in the error path" | Targets the review to a specific concern |
| "Make this better" | "Tighten the prose: cut filler words, vary sentence length, keep under 200 words" | Defines what "better" means in concrete terms |
| "Give me feedback" | "Score this draft 1-5 on clarity, completeness, and tone, with one fix per category" | Turns vague feedback into a structured rubric |

**Power verbs for specificity:** identify, extract, list (with count), compare (with named items), flag, score, classify, rank, distinguish, isolate.

**Danger verbs** (too vague alone): analyze, explore, discuss, address, consider, review.

## Before → After

From my Clap/OpsPilot project — an agent instruction for architecture reconciliation:

> **Before**
> ```
> Review the codebase and suggest improvements.
> ```
>
> **After** (from the actual SHOT_1 prompt)
> ```
> You are working inside the workflow-llm-dataset project.
> Do not treat this as a cold start.
>
> Read these files for grounding:
> - agent_os_pack/01_product_north_star.md
> - agent_os_pack/02_control_model.md
>
> Required outputs:
> 1. REPO_REALITY.md — what the code actually does today
> 2. REFERENCE_FRAMEWORK_MAPPING.md — how our code maps to framework concepts
>
> Rules:
> - Do not rewrite the whole repo in this shot
> - Inspect actual code, not just documentation
> - Verify code, not reports
> ```
>
> **What changed:** Five specificity axes covered — scope (this project, these files), format (named deliverables), criteria (verify code not reports), constraint (don't rewrite everything), grounding (read these files first).

## Try This Now

Open your favorite LLM chat and paste this:

```
I'm going to give you a vague prompt, and I want you to rewrite it
as a specific one by adding: a count, a format, an audience, a scope
limit, and one exclusion.

Vague prompt: "Tell me about cloud computing."

Rewrite it now. Then explain what each addition does.
```

Notice how the model's rewrite is immediately more useful than the original? That's specificity at work. Now try it with a prompt from your own work.

## From the Lab

We tested 10 analysis verbs across 2,000 prompt variations on four model families (GPT-4o, Claude 3.5 Sonnet, Llama 3.1 70B, Mistral Large). The results:

![Word Choice Impact: Analysis Verbs](../art/figures/exp_analysis_verbs_word_choice.png)

**Key finding:** "Investigate" and "dissect" consistently outperformed the generic "analyze" — more specific verbs activated more structured, detail-oriented outputs. The effect was strongest on smaller models, where vague verbs produced the most variance.

## When It Breaks

- **Format-only specificity** → You asked for JSON with five fields but didn't say *what content* goes in them. Perfect structure, wrong answer.
- **Specificity without grounding** → "List the exact revenue figures for Q3" without providing the data. You just turned specificity into → hallucination bait.
- **Specificity past the ceiling** → Schreiter found that over-specific verbs in reasoning tasks *hurt* performance. If you're micromanaging the model's word choice, you've gone too far.

## Quick Reference

- **Family:** Core abstraction
- **Adjacent:** → precision (accuracy of wording), → constraint (mechanism for adding specificity), → vagueness (the absence of it), → grounding (specificity about sources)
- **Model fit:** Benefits all tiers; most critical for small open models. Frontier models tolerate vagueness better but still improve measurably with specific prompts.
- **Sources:** [src_paper_schreiter2024], [src_paper_schulhoff2025]
