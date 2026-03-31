---
headword: "rubric"
slug: "rubric"
family: "quality_control"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# rubric

**Elevator definition**
A rubric is a structured set of evaluation criteria that defines what "good" looks like for a particular output — the checklist that makes quality judgments explicit and repeatable.

## What it is

Without a rubric, evaluation is vibes. Someone reads the output, thinks "this seems okay" or "this feels off," and either ships it or rewrites it. The judgment is real — experienced humans have good instincts about quality — but it is opaque, inconsistent across reviewers, and impossible to automate. A rubric makes the judgment legible.

A rubric specifies, in advance of any output being produced, the criteria against which that output will be assessed. For a customer email response, a rubric might include: Does it address the customer's specific question? Does it maintain a professional but warm tone? Does it include an action item? Is it under 200 words? Does it avoid promising anything outside policy? Each criterion is a dimension of quality, and together they define the shape of an acceptable output.

The concept is borrowed from education, where rubrics have been used for decades to standardize grading. A teacher grading 30 essays needs a rubric not because she can't recognize good writing but because she needs to apply the *same* standard to all 30 papers, and she needs to be able to explain that standard to students who ask why they got a B. The same logic applies to evaluating model output: you need a standard you can apply consistently, explain to others, and encode in a verification system.

Rubrics exist on a spectrum from informal to rigorous. An **informal rubric** is a mental checklist: "Did the model answer the question? Is it the right length? Does it sound right?" This is better than nothing but degrades with fatigue, changes with mood, and cannot be automated. A **structured rubric** enumerates criteria with defined levels — typically Pass/Fail for binary criteria or a scale (1–3 or 1–5) for graded criteria. A **weighted rubric** assigns relative importance to each criterion, so that format compliance (important but not critical) counts less than factual accuracy (critical).

In LLM systems, rubrics serve three distinct functions:

1. **Design guidance** — Writing the rubric before the prompt forces you to articulate what you actually want. Many prompts fail not because the model is incapable but because the human never defined success. Writing a rubric is an exercise in specification.

2. **Automated evaluation** — A rubric can be applied by another model (an "LLM-as-judge" pattern), converting human quality assessment into a scalable, repeatable process. Feed the output and the rubric to an evaluator model; get a score. This enables → regression checks, A/B testing, and continuous quality monitoring across thousands of outputs.

3. **Verification criteria** — In → verification loops, the rubric is what the verifier checks against. Without a rubric, the verifier has no standard. With one, it has a specific list of things to confirm before passing the output downstream.

The distinction between a rubric and a constraint is worth noting. A → constraint limits what the model may do: "Do not mention competitors." A rubric evaluates what the model did: "Did the response mention competitors? (Fail if yes.)" Constraints operate during generation. Rubrics operate after generation. You can derive constraints from a rubric (each rubric criterion implies a constraint), but the rubric is the evaluation instrument, not the control mechanism.

## Why it matters in prompting

A rubric-informed prompt produces better output because the rubric forces the prompt author to decide what matters. Consider: "Summarize this article." That is a prompt with no rubric — no definition of what a good summary looks like. Now consider the rubric behind a good summary: covers the main argument, includes the key evidence, maintains the original's conclusions, does not introduce claims not in the article, stays under 150 words, and is written for a non-specialist audience. That rubric, when translated into the prompt, produces a far more precise instruction.

Rubrics also make prompt iteration principled rather than random. Without a rubric, "improving" a prompt means tweaking it until the output feels better. With a rubric, improving a prompt means changing it until the output scores higher on specific criteria. This is the difference between wandering and navigating.

## Why it matters in agentic workflows

In multi-agent pipelines, rubrics are the quality contracts between agents. Each agent's output should be evaluated against a rubric before being passed downstream. This prevents the most common pipeline failure: bad output from one agent becoming unquestioned input for the next.

Rubrics also enable agent-level accountability. When the final output is poor, the rubric at each stage tells you where quality dropped: the Research Agent passed its rubric, the Analysis Agent failed on criterion 3. You know which agent to fix. Without rubrics, diagnosis is guesswork.

## What it changes in model behavior

When rubric criteria are included in the prompt, the model attends to those criteria during generation. A model told that its output will be evaluated on "factual accuracy, source citation, and conciseness" will produce output that is more factual, better cited, and more concise than a model given no such criteria. The rubric primes the model's attention toward the properties you care about.

## Use it when

- You need to evaluate output quality consistently across many instances
- You are building a → verification loop and need explicit criteria for the verifier
- Multiple people (or agents) will produce similar outputs and you need a shared quality standard
- You are running → regression checks and need a stable definition of "passing"
- The difference between good and great output matters and you need to specify what "great" means

## Do not use it when

- The task is exploratory and you do not yet know what good looks like — premature rubric-writing constrains creativity
- The output is a one-off with no need for repeatable evaluation
- The quality is entirely subjective and no criteria can be meaningfully standardized (rare, but possible for purely aesthetic tasks)

## Contrast set

- → **verification loop** — The verification loop is the process; the rubric is what it checks against. The loop is the mechanism; the rubric is the standard.
- → **constrain** — Constraints limit the model during generation. Rubrics evaluate the model's output after generation. They often encode the same requirements from different angles.
- → **evaluation** — Evaluation is the broad act of assessing quality. A rubric is the instrument used to make evaluation consistent and specific.
- → **test harness** — A test harness runs tests and collects results. Rubrics define the pass/fail criteria those tests apply.

## Common failure modes

- **Rubric bloat** — The rubric grows to 20+ criteria, many overlapping or trivially satisfied. The evaluator (human or model) loses focus, spending attention on low-value checks while missing high-value ones. Fix: limit rubrics to 5–8 criteria. Each criterion should represent a distinct, important dimension of quality. If two criteria always pass or fail together, merge them.

- **Rubric without teeth** — The rubric exists on paper but is not actually applied to outputs. It was written during planning and forgotten during execution. Fix: embed the rubric in the pipeline — literally pass it to the verification agent or evaluation model as input. A rubric that is not executed is documentation, not quality control.

- **Rubric-prompt mismatch** — The rubric evaluates properties the prompt never asked for. The prompt says "summarize this article." The rubric checks for "actionable recommendations." The model fails the rubric not because it performed poorly but because the rubric and prompt were designed independently. Fix: derive the prompt from the rubric. Every rubric criterion should correspond to an explicit instruction or expectation in the prompt.

## Prompt examples

### Minimal example

```text
Evaluate the following customer support response on these
criteria. Score each PASS or FAIL.

1. Addresses the customer's stated issue
2. Provides a specific next step or resolution
3. Maintains professional tone
4. Does not promise anything outside standard policy
```

### Strong example

```text
You are a quality evaluator. You will receive a research
summary and the source document it was based on.

Evaluate the summary against this rubric:

| # | Criterion | Weight | Scoring |
|---|-----------|--------|---------|
| 1 | Coverage: includes the 3 main findings from the source | 30% | PASS: all 3 present. PARTIAL: 2 of 3. FAIL: 1 or fewer. |
| 2 | Accuracy: no claims that contradict the source | 25% | PASS: zero contradictions. FAIL: any contradiction. |
| 3 | Attribution: every factual claim cites a section of the source | 20% | PASS: 100% cited. PARTIAL: 80-99%. FAIL: below 80%. |
| 4 | Conciseness: summary is 100-200 words | 15% | PASS: in range. FAIL: outside range. |
| 5 | Audience: written for a non-technical executive | 10% | PASS: no jargon without definition. FAIL: unexplained jargon. |

Output format:
{
  "scores": [
    { "criterion": 1, "score": "PASS|PARTIAL|FAIL", "evidence": "..." }
  ],
  "weighted_total": "0-100",
  "overall": "PASS (>= 75) | NEEDS_REVISION (50-74) | FAIL (< 50)"
}
```

### Agentic workflow example

```text
Pipeline: Rubric-Gated Multi-Agent Report Generation

Each agent boundary includes a Rubric Gate. Output must pass
the gate before proceeding to the next agent.

Agent 1 — Research Agent → Rubric Gate 1
Rubric:
  - Minimum 5 sourced findings: PASS/FAIL
  - Each finding includes source_id and page reference: PASS/FAIL
  - No duplicate findings: PASS/FAIL
  - All sources from approved corpus: PASS/FAIL
Action on FAIL: Return to Research Agent with specific
  criterion that failed, maximum 2 retries.

Agent 2 — Analysis Agent → Rubric Gate 2
Rubric:
  - Each finding has a significance assessment (high/med/low)
  - Analysis references at least 3 of the 5 findings
  - Conclusions are supported by cited findings, not asserted
  - No claims without provenance
Action on FAIL: Return to Analysis Agent with failed criteria.

Agent 3 — Writing Agent → Rubric Gate 3
Rubric:
  - Executive summary present and under 100 words
  - All sections follow the provided template structure
  - Every paragraph cites at least one finding by ID
  - Tone matches audience specification (board-level, formal)
  - Total length 800-1200 words
Action on FAIL: Return to Writing Agent for revision.

Final gate: All three rubric gates PASS → deliver report.
Any gate fails after 2 retries → escalate to human reviewer
with rubric scores and partial output.
```

## Model-fit note

Rubric evaluation by LLM ("LLM-as-judge") works best with frontier models, which show substantial agreement with human evaluators on well-defined rubrics. Midsize models evaluate binary criteria (PASS/FAIL) reliably but struggle with nuanced graded scales. For cost efficiency, use a frontier model for rubric evaluation and lighter models for generation — the evaluation call is typically much shorter and less frequent than the generation call. Always calibrate LLM-as-judge against a small set of human-evaluated examples to confirm alignment before deploying at scale.

## Evidence and provenance

The LLM-as-judge evaluation pattern is documented in Zheng et al. (2023) with the MT-Bench and Chatbot Arena frameworks. Rubric-based evaluation of LLM outputs is discussed across evaluation framework documentation (OpenAI Evals, LangSmith, RAGAS). The educational rubric framework has decades of pedagogical literature; its transfer to LLM evaluation is a practitioner adaptation. The Prompt Report notes that output evaluation and quality criteria are recurring components of effective prompt design [src_paper_schulhoff2025].

## Related entries

- **→ verification loop** — the process that applies rubric criteria
- **→ test harness** — the infrastructure that runs rubric-based evaluations at scale
- **→ regression check** — uses rubric scores to detect quality degradation over time
- **→ constrain** — enforces requirements during generation; rubrics evaluate after
