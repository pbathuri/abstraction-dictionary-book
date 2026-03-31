---
headword: "feedback_loop"
slug: "feedback_loop"
family: "quality_control"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# Feedback Loop

**Elevator definition** A mechanism where output evaluation feeds back into prompt or agent improvement — the system watching itself and getting better from what it sees.

## What it is

A feedback loop is a cycle: produce output, evaluate that output, and use the evaluation to change how you produce the next output. The concept is borrowed from control theory, where feedback loops are the basis of all self-correcting systems — thermostats, cruise control, biological homeostasis. In LLM work, feedback loops are what separate systems that stay broken from systems that learn.

There are two fundamentally different types of feedback loops in prompt engineering. **Inner loops** operate within a single conversation or pipeline run. The model generates a draft, an evaluator scores it, and the model revises based on the score — all in one session. Inner loops are immediate, tactical, and bounded. They improve a specific output. **Outer loops** operate across runs. You analyze logs from many pipeline executions, identify systematic failures, and modify the prompt, the pipeline structure, or the evaluation criteria. Outer loops are slow, strategic, and compounding. They improve the system.

Both types require the same three components: a sensor (something that evaluates the output), a signal (the evaluation result, in a form the system can act on), and an actuator (a mechanism that changes behavior based on the signal). In LLM systems, the sensor might be a separate evaluator model, a rule-based check, or human feedback. The signal is a score, a list of errors, or a qualitative critique. The actuator is a prompt revision, a parameter change, or a pipeline restructure.

The most common inner feedback loop is generate-then-critique. The model produces a draft, then a second prompt (or a second model) evaluates it against specified criteria, and the original model revises. This simple pattern — one loop iteration — improves quality measurably. Two iterations improve it more. Three rarely add value and sometimes degrade quality as the model over-corrects.

Outer feedback loops are more powerful but harder to implement. They require logging (what happened), evaluation (was it good), attribution (why was it good or bad), and action (what to change). Most teams skip one or more of these steps. They log outputs but don't evaluate them. They evaluate but don't trace failures to root causes. They identify root causes but don't actually change the prompts. A feedback loop that's missing any component isn't a loop — it's a dead end.

The key insight is that feedback loops must be designed, not discovered. LLM systems don't self-improve by default. You must build the evaluation, build the signal pathway, and build the revision mechanism. Left to themselves, LLM pipelines produce the same quality forever — or degrade as input distributions shift.

## Why it matters in prompting

In single-prompt work, the feedback loop is you. You write a prompt, read the output, judge its quality, and revise the prompt. This is effective but slow and doesn't scale. Making this loop explicit — writing down the evaluation criteria, scoring outputs systematically, tracking which prompt changes produced which quality changes — turns prompt iteration from art into engineering.

The most impactful inner-loop technique for individual prompts is self-critique: asking the model to evaluate its own output against stated criteria before finalizing. This adds one extra step but consistently improves output quality because it forces the model to shift from generation mode to evaluation mode — different cognitive operations that catch different errors.

## Why it matters in agentic workflows

Agent systems without feedback loops are systems that fail the same way forever. A retrieval agent that returns irrelevant documents will continue returning irrelevant documents until someone analyzes the failure pattern and adjusts the retrieval prompt, the search parameters, or the relevance filter.

Designed feedback loops in agent systems take several forms. **Per-run loops**: the output of a quality-check agent feeds back to the generation agent for revision within a single pipeline execution. **Cross-run loops**: aggregated quality metrics trigger prompt revisions when performance drops below a threshold. **Human-in-the-loop**: human evaluators score a sample of outputs, and their feedback informs systematic prompt or pipeline changes.

The most sophisticated agent systems implement all three, creating a layered feedback architecture: fast inner loops for immediate quality, periodic cross-run analysis for trend detection, and occasional human review for calibration and edge-case handling.

## What it changes in model behavior

Within a single run, feedback loops enable iterative refinement — the model produces output, receives structured critique, and generates improved output that addresses the critique. Across runs, feedback loops don't change the model itself but change the prompts, tools, and routing logic that shape the model's behavior — an indirect but powerful form of system-level learning.

## Use it when

- Output quality must improve over time, not just stay constant
- The same pipeline runs repeatedly and you can aggregate quality signals
- The task is complex enough that first-pass output is reliably improvable
- You have or can build an evaluation mechanism — automated scoring, human review, or user feedback
- Failures are patterned and diagnosable, not random and irreducible

## Do not use it when

- The task is one-shot with no iteration opportunity (single query, single response)
- The cost of evaluation exceeds the benefit of improvement (cheap, low-stakes outputs)
- You lack a meaningful quality signal (no evaluation criteria, no ground truth, no user feedback)
- The system is already at the quality ceiling for the model and the task

## Contrast set

- **Checkpoint** → A checkpoint verifies quality at a point in time; a feedback loop uses quality signals to improve future performance. Checkpoints are gates. Feedback loops are cycles.
- **Audit trail** → An audit trail records what happened; a feedback loop acts on what happened to change what happens next. Trails are passive. Loops are active.
- **Contradiction detection** → Contradiction detection is one sensor in a feedback loop — it detects a type of error. The feedback loop is the full cycle from detection through correction.
- **Evaluation** → Evaluation produces a quality signal; a feedback loop is the full circuit that includes evaluation and uses the signal to drive change.

## Common failure modes

- **Open loop → evaluation without action.** You score outputs, build dashboards, track metrics — but never change the prompts or pipeline based on what you learn. This is monitoring, not a feedback loop. Fix: for every metric you track, define a trigger condition and a response action. "If accuracy drops below 85% for a week, review and revise the retrieval prompt."
- **Overcorrection → revising too aggressively in response to individual failures.** One bad output causes a prompt rewrite that fixes that case but breaks ten others. Fix: base prompt revisions on patterns, not incidents. Require a minimum sample size before acting. Use A/B testing to validate that changes improve aggregate quality, not just the triggering case.
- **Stale feedback → evaluation criteria that don't evolve with the system.** You built the feedback loop six months ago. The input distribution has shifted, user expectations have changed, but the evaluation rubric is the same. The loop is optimizing for yesterday's quality definition. Fix: review and update evaluation criteria on a regular cadence, informed by user feedback and changing requirements.

## Prompt examples

### Minimal example

```
Write a one-paragraph summary of the attached article.

Then evaluate your summary:
- Does it capture the main argument? (yes/no)
- Does it include the key evidence? (yes/no)
- Is it under 100 words? (yes/no)

If any answer is "no," revise the summary to address the gap.
Present only the final version.
```

### Strong example

```
You will write and then improve a technical explanation in two passes.

PASS 1 — Draft:
Explain how database indexing works to a junior developer.
Target: 200-250 words, no jargon without definition, one concrete example.

PASS 2 — Self-critique and revise:
Evaluate your draft against these criteria (score 1-5 each):
  1. Accuracy: are all technical claims correct?
  2. Clarity: would a junior developer understand every sentence?
  3. Completeness: are the key concepts (B-trees, query plans, tradeoffs) covered?
  4. Concreteness: does the example illustrate the concept effectively?

For any criterion scored below 4, explain what's wrong and revise that
portion of the draft. Present the revised explanation as your final output.
Include the scores (before and after) at the end.
```

### Agentic workflow example

```
pipeline: support_response_optimization
feedback_architecture:
  inner_loop (per-run):
    - drafter generates response
    - quality_checker evaluates: empathy (1-5), accuracy (1-5),
      resolution_completeness (1-5), tone_match (1-5)
    - if any score < 3: return to drafter with specific feedback
    - max 2 revision cycles, then deliver with quality scores attached

  outer_loop (weekly):
    - aggregate quality scores across all runs
    - cluster low-scoring responses by failure type:
        [inaccurate, tone_mismatch, incomplete_resolution, too_long]
    - for each cluster exceeding 10% of total:
        - pull 5 representative examples
        - generate prompt revision proposal
        - A/B test revised prompt against current for 48 hours
        - adopt if statistically significant improvement (p < 0.05)

  human_loop (monthly):
    - sample 50 responses stratified by quality score
    - human evaluators rate and annotate
    - calibrate automated quality_checker against human ratings
    - adjust scoring thresholds if drift detected
```

## Model-fit note

Inner feedback loops (self-critique and revision) work reliably with GPT-4-class and Claude 3.5+ models. Smaller models tend to agree with their own output rather than genuinely critiquing it, making the loop ineffective. For smaller models, use a separate, stronger model as the evaluator in the feedback loop, or rely on rule-based evaluation rather than LLM-based self-critique.

## Evidence and provenance

Feedback loops in control theory date to Wiener's cybernetics (1948). In LLM systems, inner-loop self-critique is documented in "Self-Refine" (Madaan et al., 2023) and constitutional AI (Bai et al., 2022). Outer-loop prompt optimization is the subject of DSPy (Khattab et al., 2023) and related automatic prompt tuning research. The layered feedback architecture pattern is emerging from production agent system design (LangSmith, Braintrust, 2024).

## Related entries

- → **checkpoint** — Checkpoints provide evaluation points that generate signals for feedback loops.
- → **audit_trail** — The audit trail is the data source for outer feedback loops.
- → **contradiction_detection** — One type of sensor that can be embedded in a feedback loop's evaluation step.
- → **falsifiability** — Falsifiable claims make evaluation possible; unfalsifiable claims cannot participate in meaningful feedback loops.
