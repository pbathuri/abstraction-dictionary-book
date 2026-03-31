# evaluate

> Assess quality against defined criteria, producing a judgment — not a description, not a summary, a verdict.

## The Scene

You ask the model: "Is this a good cover letter?" It says yes. Of course it says yes. Helpfulness bias means models are terrible at honest evaluation when the criteria are vague. "Good" could mean anything, so it means nothing, and the model defaults to approval.

You try again: "Evaluate this cover letter on four criteria: (1) Demonstrates specific knowledge of the company's recent work. (2) Connects the applicant's experience to the job's top three requirements. (3) Under 350 words. (4) Ends with a specific, non-generic call to action. Score each 1-5 where 1 = not addressed, 3 = partially addressed, 5 = fully addressed."

Now you get a real assessment. Scores of 5, 2, 4, 1. The call to action is "I look forward to hearing from you" — generic, scored accordingly. *That's* evaluation.

## What This Actually Is

Evaluation is judgment under rules. It takes something — an argument, a plan, some code — and measures it against a standard. The standard might be explicit (a rubric) or implicit (the model's trained sense of "good"). But make no mistake: the standard is always there. When you don't specify it, the model fills it in, and you lose control of the judgment.

Compare asks "how do these differ?" Critique asks "what's wrong?" Evaluate asks "how good is this?" — and that question requires both a definition of "good" and a method for measuring it.

The LLM-as-judge pattern is real: models evaluating other models' output is now standard in training, benchmarking, and production QA. The reliability depends almost entirely on the evaluation prompt. Vague criteria produce inconsistent scores. Specific criteria produce reproducible ones. Even minor phrasing changes can shift scores 10-15% on the same output.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Is this good?" | "Evaluate on these criteria: [list]. Score 1-5 each." | Decomposes "good" into measurable dimensions |
| "Rate this 1-10" | "Rate 1-5 where 1 = fails to address, 3 = adequate with gaps, 5 = thorough with examples" | Anchored scales prevent clustering at 7-8 |
| "Tell me if it works" | "Does it meet spec? Check each requirement: COVERED, PARTIALLY, or MISSING" | Binary-ish checks are more reliable than gradient scores |
| "Review this" | "Use the full range of the scale. A 5 should be rare and earned." | Counteracts positive bias — models default to generous |
| "Evaluate and suggest improvements" | "First evaluate (score each criterion). Then critique (identify specific weaknesses). These are separate steps." | Separates judgment from prescription |

## Before → After

**Before:**
```
Is this a good cover letter?
```

**After:**
```
Evaluate this cover letter on four criteria:

1. COMPANY KNOWLEDGE (1-5): Does it reference specific recent
   work, products, or initiatives by the company?
2. REQUIREMENT MATCH (1-5): Does it connect the applicant's
   experience to the job's stated requirements?
3. CONCISENESS (1-5): Is it under 350 words with no filler?
4. CALL TO ACTION (1-5): Does it end with a specific,
   non-generic next step?

For each, provide the score and one sentence of justification.
If any criterion scores 2 or below, flag as NEEDS_REVISION.
```

**What changed:** "Good" was decomposed into four falsifiable criteria with an anchored scale. The model evaluates against a rubric instead of returning "yes, this is a good cover letter."

## Try This Now

```
Evaluate the following prompt on three criteria:

PROMPT: "Write me a blog post about AI."

CRITERIA:
1. SPECIFICITY (1-5): How narrowly does it define the topic?
   1 = completely open-ended, 5 = precise enough for consistent output
2. AUDIENCE CLARITY (1-5): How well does it define the reader?
   1 = no audience specified, 5 = reader profile with domain + role + context
3. OUTPUT SPECIFICATION (1-5): How clearly does it define format,
   length, and structure?
   1 = no specs, 5 = fully constrained

Score each, justify in one sentence, then write an improved
version of the prompt that would score 4+ on all three criteria.
```

## When It Breaks

- **Evaluation without rubric** → The model produces vague, generally positive assessments because its training bias is toward helpfulness. Fix: always specify criteria. Even two are better than none.
- **Positive bias** → Models rate generous — 4/5 when a human would give 3/5. Fix: "Use the full range. A score of 5 should be rare and earned." Or require finding at least one weakness before scoring.
- **Criterion drift** → When evaluating multiple items sequentially, the model's standards shift. Fix: evaluate each item in a separate prompt, or include calibration examples.

## Quick Reference

- Family: instructional action
- Adjacent: → critique (targeted fault-finding feeds evaluation), → compare (maps differences; evaluation maps quality), → falsifiability (evaluation criteria should be testable)
- Model fit: Frontier models apply nuanced rubrics consistently and use the full scale. Midsize models compress toward the middle (everything gets 3/5). Small models are unreliable beyond binary pass/fail. For all tiers: anchored scales with concrete examples substantially improve consistency.
