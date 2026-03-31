# test harness

> The rig that runs your prompt tests, records the results, and tells you where quality stands — unit testing for language models.

## The Scene

ResumeForge, month two. I'd been testing prompts by hand: paste a resume, read the output, decide if it's good. This worked for three test cases. By the time I had twelve variations of the system prompt and forty resumes in my test set, I was skipping cases, forgetting which version produced which result, and unconsciously lowering my standards because I was tired of reading outputs.

I built a harness. A Python script that sent each of forty resumes through the prompt, ran the output through six checks (truthfulness: no fabricated claims, format compliance, length under 200 words, skill-match coverage, gap flagging, tone), and wrote results to a JSON file. Every prompt change: run the harness, read the report, ship only if pass rate held or improved.

First run of the harness on my "best" prompt: 72% pass rate. I thought it was at 90%. The cases I'd been skipping were the ones failing. The harness didn't make the prompt better — it made my ignorance visible. That's the entire value.

## What This Actually Is

A test harness has four parts. **Test cases**: inputs paired with evaluation criteria (not exact expected outputs — LLM outputs are non-deterministic, so you test *properties*). **Test runner**: sends inputs through the prompt and collects outputs. **Evaluator**: scores each output against its criteria — programmatic checks for structure (length, format, schema) and LLM-as-judge for semantics (relevance, accuracy, tone). **Reporter**: aggregates results into pass/fail per case and trends over time.

The power isn't in any single run. It's in the accumulation. One run tells you if the prompt works now. A hundred runs across iterations tell you if it's getting better or worse. A test harness with historical data is the empirical record of your prompt engineering decisions and their consequences.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "It looks good to me" | Run 20 test cases and report the pass rate | Subjective assessment → measured quality |
| "I tested it on a few examples" | Define the test set, run it systematically, record results | "A few" is not a test suite |
| "Did the output change?" | Compare per-criterion scores before and after the prompt change | Detects regressions exact-match misses |
| "The model seems worse" | "Pass rate dropped from 91% to 84% after the March 15 change" | Replaces anecdotes with data |
| (skip testing after small edit) | Every prompt change triggers the harness. No exceptions | Small edits cause global behavior shifts in system prompts |

## Before → After

**Before:**
```
[Manual testing workflow]
1. Paste a resume into ChatGPT
2. Read the output
3. Think "looks good" or "looks bad"
4. Ship
```

**After:**
```
Test case TC-007:
  Input: resume_senior_analyst.txt + jd_data_engineer.txt
  Rubric:
    - No fabricated claims: PASS/FAIL
    - All skill matches identified: PASS/FAIL
    - Gaps flagged with suggestions: PASS/FAIL
    - Output under 200 words: PASS/FAIL
    - Tone: professional, not sycophantic: PASS/FAIL

  Result: { pass: 4, fail: 1 }
  Failed criterion: skill_match_coverage
  Note: missed "SQL" match between resume line 12
  and JD requirement 4

Aggregate (40 cases): 36/40 PASS (90%)
Regression vs. v2.3 baseline: TC-007 is NEW failure.
TC-022 previously failing, now PASS.
Net: +1 pass, -1 pass. Neutral.
```

## Try This Now

```
I'll give you a prompt. Your job: design a 3-case test
suite for it. Don't run the prompt — design the tests.

Prompt: "You are a customer support agent. Answer the
user's question using the company FAQ document."

For each test case, define:
1. The input (a user question)
2. The rubric (3-4 criteria, each PASS/FAIL)
3. One criterion that tests for a failure mode
   (hallucination, off-topic, format violation)

Then: what would a 4th test case look like that tests
adversarial input ("ignore your instructions and...")?
```

## When It Breaks

- **Unrepresentative test cases** — The suite covers easy cases the developer thought of. Hard cases, edge cases, and adversarial inputs are missing. The harness reports 95% but production shows 75%. Fix: populate test cases from real user inputs, including failure cases from production.
- **Exact-match fragility** — Tests check for exact output strings, which fail constantly because models paraphrase. The team disables failing tests. Fix: test properties and criteria, not exact strings. Use rubric-based evaluation.
- **Evaluator drift** — The LLM-as-judge becomes more lenient over time. Tests pass that a human would fail. Fix: calibrate periodically against human judgments. Maintain a "golden set" of human-evaluated outputs.

## Quick Reference

- **Family:** Quality control
- **Adjacent:** → rubric (the evaluation criteria the harness applies), → regression check (one test type the harness supports — comparing against baseline), → verification loop (runtime quality control; the harness is development-time quality control), → evaluation (the broader concept the harness operationalizes)
- **Model fit:** Harnesses are model-agnostic infrastructure. For the evaluator component, use frontier models for LLM-as-judge (highest agreement with human judgments). Use programmatic checks wherever possible to reduce cost. The harness should parameterize the model under test so the same suite evaluates different models or versions.
