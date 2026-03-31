---
headword: "evaluate"
slug: "evaluate"
family: "instructional_action"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["rubric", "rank", "compare", "critique", "justify", "constrain", "verification loop"]
cross_links: ["rubric", "rank", "compare", "critique", "justify", "constrain", "verification loop", "framing", "specificity", "falsifiability"]
tags: ["instructional-action", "judgment", "assessment", "criteria-dependent", "quality-control"]
has_note_box: true
note_box_type: "upgrade_prompt"
---

# evaluate

**Elevator definition**
To evaluate is to assess the quality, correctness, or fitness of something against defined criteria, producing a judgment rather than a description.

## What it is

Evaluation is judgment under rules. It takes a thing — an argument, a plan, a piece of code, a design — and measures it against a standard. The standard might be explicit (a rubric, a specification, a set of requirements) or implicit (the model's trained sense of "good writing" or "correct code"). But make no mistake: the standard is always there. Every evaluation is evaluation *against something*. When you do not specify the something, the model fills it in, and you lose control of the judgment.

The operation sits at the intersection of analysis and decision. → Compare asks "how do these differ?" → Critique asks "what is wrong with this?" Evaluate asks "how good is this?" — a question that requires both a definition of "good" and a method for measuring it. Without the definition, evaluation collapses into impressionism. With it, evaluation becomes one of the most powerful analytical operations available in prompting.

Schulhoff et al. (2025) devoted a substantial section of The Prompt Report to LLM-based evaluation, recognizing it as both a prompting task and a meta-task — models are increasingly used to evaluate the outputs of other models [src_paper_schulhoff2025]. The paper identifies several dimensions along which LLM evaluation is studied: factual correctness, instruction following, reasoning quality, and output safety. Each dimension requires its own criteria, its own scale, and its own evidence standards. A model that is "good" at factual accuracy may be poor at instruction following. Evaluation without dimensional specificity produces a single blurred score that conceals more than it reveals.

The concept of LLM-as-judge has become a practical reality in the prompting ecosystem. Evaluation prompts — prompts that ask one model to score or grade the output of another — are now used in training, benchmarking, and production quality assurance. The reliability of these evaluations depends almost entirely on the quality of the evaluation prompt: vague criteria produce inconsistent scores, specific criteria produce reproducible ones. Sahoo et al. (2025) document that even minor changes to evaluation prompt phrasing can shift model scores by 10-15% on the same output, underscoring the need for precise, well-structured evaluation instructions [src_paper_sahoo2025].

This sensitivity is the double-edged sword of LLM evaluation. The model is a flexible evaluator — you can define any criteria you want. But that flexibility means the evaluation is only as good as the criteria you define. Garbage rubric in, garbage evaluation out.

## Why it matters in prompting

Evaluation is the instruction you use when you need a verdict, not a description. "Analyze this business plan" produces commentary. "Evaluate this business plan against the criteria of market viability, financial sustainability, and competitive differentiation" produces a judgment you can act on.

The key insight for prompt authors is that evaluation *requires a rubric*, whether you provide one or not. If you say "evaluate this essay," the model uses its training-data sense of what makes a good essay. That sense is generic, weighted toward academic conventions, and may not match your standards. If you say "evaluate this essay on three criteria: clarity of argument, quality of evidence, and practical applicability to the reader's stated problem," the model evaluates against *your* rubric, and the output is specific, auditable, and consistent across runs.

Providing a scoring scale is the second lever. "Rate on a scale of 1-5" is better than "tell me if it's good." But "rate on a scale of 1-5 where 1 = fails to address the criterion at all, 3 = addresses it adequately with some gaps, and 5 = addresses it thoroughly with specific examples" is better still. Anchored scales reduce the subjective spread of model ratings and make evaluations comparable across items and across runs.

## Why it matters in agentic workflows

In agent architectures, evaluation is the mechanism that implements quality gates. A pipeline that generates, then evaluates, then decides whether to pass forward or revise is a pipeline with standards. A pipeline that generates and passes without evaluation is a pipeline with hopes.

The Evaluator Agent pattern works like this: after a Producer Agent generates output, an Evaluator Agent scores it against a → rubric. If the scores meet a threshold, the output advances. If not, the output returns to the Producer with the evaluation scores and specific feedback for revision. This pattern is the quality-controlled version of → verification loop — verification checks structural compliance, evaluation checks substantive quality.

LLM-as-judge is the backbone of this pattern. The evaluator does not need to redo the work. It needs to read the work, apply criteria, and return a structured assessment. This is cheaper than regeneration, faster than human review, and — when the rubric is good — reliable enough for production use.

## What it changes in model behavior

The instruction "evaluate" shifts the model from generative to judgmental mode. The output contains explicit quality assessments, scored dimensions, and evidence-linked ratings rather than descriptions or extensions. The model produces more structured output — tables, score-justification pairs, pass/fail determinations — because evaluation naturally lends itself to structured formats.

More importantly, evaluation activates the model's capacity for critical distance. A model asked to "continue this story" is in generative alliance with the text. A model asked to "evaluate this story against criteria X, Y, and Z" is in analytical tension with it. This shift in stance produces qualitatively different attention patterns: the model notices gaps, inconsistencies, and weaknesses that it would gloss over in generative mode.

## Use it when

- You need a quality judgment, not just a description or analysis
- You have criteria (explicit or formulatable) against which the item should be measured
- The output of the evaluation will drive a decision: accept, reject, revise, escalate
- You are building a pipeline and need a quality gate between stages
- You want to compare multiple items not just descriptively but by quality score
- You are using one model to assess the output of another (LLM-as-judge)

## Do not use it when

- You do not have criteria and would be accepting the model's default definition of "good"
- You want to understand *how* something works, not *how good* it is — that is analysis, not evaluation
- You want only the weaknesses — that is → critique, which is targeted fault-finding without an overall judgment
- The subject is purely subjective and evaluation would manufacture false objectivity (ranking poems by "quality")
- You need the items described before they can be evaluated — describe first, then evaluate as a separate step

## Contrast set

**Closest adjacent abstractions**

- → critique — Critique identifies specific weaknesses. Evaluation assesses overall quality. Critique says "here is what is broken." Evaluation says "here is how good it is overall, considering what is broken and what works." Critique is destructive. Evaluation is measured.
- → rank — Rank is evaluation with ordering. You evaluate first, then rank by the evaluation scores. Evaluation is the prerequisite. Ranking is the sort.
- → compare — Compare maps similarities and differences. Evaluation maps quality. You can compare without evaluating (purely descriptive comparison) and evaluate without comparing (single-item assessment).

**Stronger / weaker / narrower / broader relatives**

- → rubric — The structured criteria set that evaluation applies. Evaluation without rubric is impressionism.
- → verification loop — Uses evaluation as its quality gate mechanism.
- → justify — After evaluation, justification explains *why* the score is what it is.
- → falsifiability — Evaluation criteria should be falsifiable — the item could score poorly, or the evaluation has no teeth.

## Common failure modes

- **Evaluation without rubric** → "Evaluate this proposal" with no criteria specified. The model produces a vague, generally positive assessment because its training bias is toward helpfulness. Fix: always specify criteria. Even two criteria are better than none.

- **Anchoring-free scales** → "Rate 1-10" without defining what 1 or 10 means. The model clusters everything between 6 and 8 because it has no reason to use the extremes. Fix: anchor the scale — define what a 1, a 5, and a 10 look like for this specific evaluation. Anchored scales produce a wider, more informative distribution of scores.

- **Positive bias** → The model evaluates generous. It gives 4/5 when a human would give 3/5. This is a documented LLM-as-judge effect: models trained to be helpful tend to rate content favorably [src_paper_schulhoff2025]. Fix: include the instruction "use the full range of the scale — a score of 5 should be rare and earned, not default." Alternatively, ask the model to find at least one weakness before assigning a score.

- **Criterion drift** → When evaluating multiple items sequentially, the model's interpretation of criteria shifts — it becomes more lenient or more strict as it goes. Fix: evaluate each item independently in a separate prompt, or include calibration examples ("here is an item that would score 3 on this criterion") to anchor the model's judgment across items.

## Prompt examples

### Minimal example

```text
Evaluate the following code snippet for production readiness.

Criteria:
1. Error handling — are edge cases handled?
2. Readability — could a new team member understand this?
3. Performance — are there obvious inefficiencies?

Rate each criterion 1-5 and explain in one sentence.
```

### Strong example

```text
You are evaluating customer support email drafts for quality
before they are sent.

For each email I provide, score it on the following rubric:

1. ACCURACY (1-5)
   1 = contains factual errors about our product or policies
   3 = factually correct but omits relevant information
   5 = factually complete and precise

2. EMPATHY (1-5)
   1 = dismissive or robotic tone
   3 = polite but generic
   5 = acknowledges the customer's specific frustration and
       demonstrates understanding of their situation

3. ACTIONABILITY (1-5)
   1 = customer does not know what to do next after reading
   3 = next step is mentioned but vague
   5 = clear, specific next steps with timeline

4. CONCISENESS (1-5)
   1 = more than twice the necessary length
   3 = some padding but core message is present
   5 = every sentence carries information, nothing to cut

Overall threshold: if any criterion scores 2 or below, flag
as NEEDS_REVISION with the specific criterion that failed.
If all criteria are 3+, flag as APPROVED.

For NEEDS_REVISION emails, include a specific revision
instruction addressing only the failing criterion.
```

### Agentic workflow example

```text
Agent: Quality Gate Evaluator
Pipeline position: After Generation Agent, before Delivery Agent

Input: generated_output object with { task_id, content,
original_specification, source_materials }

Task: Evaluate the generated content against the original
specification.

Evaluation rubric:
1. SPECIFICATION_COVERAGE (0-100%)
   - List each requirement from original_specification
   - Mark each as COVERED, PARTIALLY_COVERED, or MISSING
   - Score = (COVERED * 1.0 + PARTIALLY * 0.5) / total

2. FACTUAL_GROUNDING (0-100%)
   - Sample 5 factual claims from the content
   - Check each against source_materials
   - Score = verified_claims / sampled_claims

3. STRUCTURAL_COMPLIANCE
   - Does the output match the format specified? YES / NO
   - Does it meet length constraints? YES / NO

4. INTERNAL_CONSISTENCY
   - Do any claims contradict other claims in the output?
   - PASS (no contradictions found) or FAIL (list contradictions)

Decision logic:
- SPECIFICATION_COVERAGE >= 80% AND FACTUAL_GROUNDING >= 80%
  AND STRUCTURAL_COMPLIANCE = all YES
  AND INTERNAL_CONSISTENCY = PASS
  → Forward to Delivery Agent

- Any criterion below threshold
  → Return to Generation Agent with:
    { failing_criteria, specific_gaps, revision_instructions }

- Second evaluation failure on same task_id
  → Escalate to human review queue

Output: Evaluation report JSON with scores, evidence,
and routing decision.
```

## Model-fit note

Evaluation quality depends heavily on rubric quality, but model tier still matters. Frontier models apply nuanced rubrics consistently, use the full range of scoring scales, and produce well-differentiated justifications. Midsize open models follow explicit rubrics but compress toward the middle of scales (giving 3/5 to everything) and produce generic justifications. Small open models are unreliable evaluators for anything beyond binary (yes/no, pass/fail) criteria — multi-point scales produce near-random distributions. For all tiers, anchored scales with concrete examples at each level substantially improve evaluation consistency. The LLM-as-judge pattern works best when the evaluator model is at least as capable as the generator model.

## Evidence and provenance

LLM-based evaluation is extensively studied in The Prompt Report, which covers factual correctness, instruction following, and output safety as evaluation dimensions [src_paper_schulhoff2025]. Sahoo et al. (2025) document the sensitivity of evaluation scores to prompt phrasing [src_paper_sahoo2025]. Positive bias in LLM-as-judge is a known phenomenon documented across evaluation benchmarks. The rubric-dependent nature of evaluation quality is a consistent finding in the LLM evaluation literature. The Quality Gate Evaluator pattern in agentic workflows is a practitioner adaptation of the verification loop architecture applied to substantive quality rather than structural compliance.

## Related entries

- **→ rubric** — the criteria set that evaluation requires; evaluation without rubric is impressionism
- **→ rank** — evaluation with ordering; rank depends on evaluation scores
- **→ critique** — targeted fault-finding; evaluation is the holistic assessment that critique contributes to
- **→ compare** — maps differences; evaluation maps quality
- **→ justify** — explains why the evaluation score is what it is
- **→ verification loop** — the architectural pattern that uses evaluation as its quality gate
- **→ constrain** — evaluation criteria are constraints on the judgment operation

---

> **Upgrade This Prompt**
>
> Before: "Is this a good cover letter?"
>
> After: "Evaluate this cover letter on four criteria: (1) Does it demonstrate specific knowledge of the company's recent work? (2) Does it connect the applicant's experience to the job's top three requirements? (3) Is it under 350 words? (4) Does it end with a specific, non-generic call to action? Score each 1-5 where 1 = not addressed, 3 = partially addressed, 5 = fully and specifically addressed."
>
> What changed: "good" was decomposed into four falsifiable criteria with an anchored scale. The model now evaluates against a rubric instead of returning "yes, this is a good cover letter" — which is what it was going to say anyway, because helpfulness bias makes models terrible at honest evaluation when the criteria are vague.
