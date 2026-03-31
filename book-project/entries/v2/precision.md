# precision

> "Analyze," "evaluate," "assess," and "review" are not synonyms. Each one runs a different program in the model's head.

## The Scene

ResumeForge's job-matching feature had a prompt that said "Review the candidate's experience against the job requirements." The output was a vague paragraph: "The candidate has relevant experience in several areas mentioned in the JD..." Useless. I changed one word. "Compare the candidate's experience against the job requirements." Same prompt, different verb. The output snapped into a structured comparison: JD requirement on the left, candidate evidence on the right, gap assessment for each.

One word. "Review" triggered a discursive, find-the-problems mode. "Compare" triggered a side-by-side analysis mode. The model isn't choosing randomly — each verb activates a different generation pattern trained on millions of documents that used that verb in a specific way. "Review" comes from contexts where people look for issues. "Compare" comes from contexts where people line things up side by side. The verb is the opcode.

## What This Actually Is

Precision is the exactness of word choice in a prompt. Not how *much* you say (that's specificity). Not whether you can be *misread* (that's clarity). Precision is whether the words you chose are the *right* words — the ones that activate the model behavior you actually want.

Schreiter (2024) tested this directly: single-word vocabulary substitutions produced statistically significant performance changes across four models and three domains. Verbs had the largest effect on reasoning tasks. The existence of an optimal precision range means precision isn't monotonic — the goal isn't the fanciest verb, but the one that most accurately describes the cognitive operation you want.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Review this code" | "Identify the three highest-severity bugs in this code" | "Review" is open-ended; "identify" targets specific output |
| "Analyze the data" | "Compare Q3 to Q4 for each metric, then rank the deltas by magnitude" | "Analyze" is generic; specific verbs (compare, rank) drive specific output |
| "Look at this proposal" | "Evaluate this proposal against three criteria: feasibility, cost, and timeline risk" | "Look at" activates browsing; "evaluate against criteria" activates judgment |
| "Give me a few examples" | "Provide exactly 3 examples, each from a different industry" | Quantitative precision: "3" beats "a few," which could mean 2 or 7 |
| "Write a fairly detailed summary" | "Write a summary of 150-200 words covering the three main findings and one limitation" | Swap qualifiers ("fairly detailed") for numbers and specifics |

## From the Lab

We tested how verb choice in instructional prompts affected output quality across models and task types:

![Instruction Verbs Word Choice](../art/figures/exp_instruction_verbs_word_choice.png)

**Key finding:** Single-word verb swaps produced 5-15% accuracy swings depending on model and domain. "Enumerate" and "list" are not synonyms to a model. "Synthesize" and "summarize" trigger different operations. Verbs had the largest effect on reasoning tasks, where the right verb primes the right cognitive mode. Interestingly, pushing verb precision beyond the optimal range degraded performance — the model spent capacity interpreting the instruction instead of executing it.

## Before → After

From ResumeForge — the verb swap that changed everything:

> **Before (imprecise verb)**
> ```
> Review the candidate's experience against the job
> requirements and provide your assessment.
> ```
> (Output: vague paragraph about "relevant experience"
> without structure or specifics)
>
> **After (precise verbs)**
> ```
> Compare the candidate's experience against each JD
> requirement. For each requirement:
> - Extract the specific JD language
> - Identify the closest matching resume evidence
> - Classify the match: STRONG (direct experience),
>   MODERATE (transferable), WEAK (tangential), or
>   NONE (no evidence found)
>
> Rank requirements by match strength, weakest first.
> ```
>
> **What changed:** "Review" + "assessment" → "Compare" + "Extract" + "Identify" + "Classify" + "Rank." Five precise verbs replaced two vague ones. Each verb maps to one cognitive operation. The model stopped interpreting and started executing.

## Try This Now

Take your most recent prompt. Circle every verb. For each one, ask: "Could I replace this with a near-synonym and get different output?" If yes, you've made a precise choice (keep it). If any synonym would work equally well, the verb isn't carrying information. Replace it with the verb that most accurately describes the operation you want:

```
Vague → Precise mapping:
- "Look at" → examine, inspect, audit, scan
- "Think about" → evaluate, weigh, assess, infer
- "Write about" → argue, explain, describe, narrate
- "Deal with" → resolve, flag, escalate, classify
- "Do something with" → transform, extract, validate, enrich
```

The precision tax is zero characters. The precision payoff is a different output.

## When It Breaks

- **Thesaurus syndrome** — Using rare vocabulary to sound precise when the model associates those terms with less common generation patterns. "Elucidate" isn't more precise than "explain" — it's rarer, and the model has seen fewer high-quality examples of its usage. Precision means the *right* word, not the *fanciest* word.
- **Qualifier fog** — "Fairly detailed," "somewhat technical," "relatively brief." Each qualifier offloads a decision to the model's default. Stack enough and the model is making all the decisions while you think you are.

## Quick Reference

- **Family:** Core abstraction
- **Adjacent:** → specificity (narrowness of scope; precision is accuracy of wording — frequently confused, fundamentally different), → clarity (ensures instructions can't be misread; precision ensures the words themselves are accurate), → register (precision in tonal vocabulary determines whether the model writes for experts or novices)
- **Model fit:** Frontier models tolerate imprecise vocabulary better — they infer intent from context. Smaller models are more literal: the verb you choose is closer to the verb they execute. Quantitative precision (numbers over qualifiers) helps uniformly across all tiers.
