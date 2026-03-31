---
headword: "test harness"
slug: "test_harness"
family: "quality_control"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# test harness

**Elevator definition**
A test harness is a reusable framework for systematically evaluating prompt or agent output — the rig that runs your tests, records the results, and tells you where quality stands.

## What it is

You can test a prompt by running it once, reading the output, and deciding if it's good. This is manual testing, and it scales to about three test cases before you start skipping, forgetting, or unconsciously lowering your standards. A test harness replaces this manual process with an automated one: a structured system that runs a set of defined inputs through a prompt or pipeline, evaluates the outputs against a → rubric, records the results, and reports pass/fail status.

The concept is borrowed directly from software engineering, where a test harness (also called a test framework or test runner) is the infrastructure that executes test cases and reports results. JUnit for Java, pytest for Python, Jest for JavaScript — these are all test harnesses. In LLM systems, the test harness serves the same function: it makes quality evaluation systematic, repeatable, and scalable.

A test harness for LLM systems has four components:

**Test cases** — A collection of inputs paired with evaluation criteria. Unlike software tests, LLM test cases rarely use exact expected outputs (because model outputs are non-deterministic). Instead, each test case defines a → rubric: properties the output must have, patterns it must avoid, and quality thresholds it must meet. A test case might be: Input: "Summarize this article." Rubric: covers the main argument; under 150 words; cites no source not in the article; written in active voice.

**Test runner** — The execution engine that sends each test case's input to the prompt or pipeline, collects the output, and passes it to the evaluator. For simple prompt testing, this is a script that calls the model API. For agent pipeline testing, this includes the full pipeline infrastructure: orchestration, tool access, shared state initialization.

**Evaluator** — The component that assesses each output against its rubric. This can be a human reviewer (accurate but slow and expensive), an LLM-as-judge (scalable and consistent but imperfect), a programmatic check (reliable for structural properties like length, format, and schema compliance), or a combination. The best test harnesses use programmatic checks for structural criteria and LLM-as-judge for semantic criteria, reducing evaluator cost while maintaining accuracy.

**Reporter** — The component that aggregates results and presents them in a usable format. At minimum: a pass/fail summary per test case. At best: trend analysis over time, failure pattern identification, per-criterion breakdown, and comparison against baseline runs for → regression checking.

The power of a test harness is not in any individual test run. It is in the *accumulation* of runs over time. A single run tells you whether the current prompt is good. A hundred runs across prompt iterations tell you whether the prompt is getting better or worse. A test harness with historical data is an empirical record of your prompt engineering decisions and their consequences.

Building a test harness requires an upfront investment that many teams skip, reasoning that they can evaluate quality manually. This is true for the first week. By the second month, the team is making prompt changes without testing, shipping regressions they don't detect, and spending hours debugging quality issues that a test harness would have caught in minutes. The investment pays for itself rapidly in any system that iterates on prompts.

## Why it matters in prompting

Prompt engineering without a test harness is guessing. You change the prompt. The output on your favorite example looks better. You ship. But you didn't test the other 47 cases. Three of them now fail. You discover this from user feedback two weeks later.

A test harness changes the workflow: change the prompt, run the suite, see the results across all test cases, ship only if overall quality improves (or at least does not regress). This is the same discipline that unit tests bring to software development, and it has the same effect: fewer regressions, faster iteration, and the confidence to make bold changes because you'll see the impact immediately.

The test harness also resolves the "one-off success" problem. A prompt that works on your test case might fail on your colleague's test case. Without shared test cases in a shared harness, every prompt engineer is evaluating against their own idiosyncratic sample. The harness provides a common evaluation surface.

## Why it matters in agentic workflows

Multi-agent pipelines are harder to test than single prompts because failures can originate at any agent and propagate downstream. A test harness for an agentic system needs to test at two levels: **agent-level tests** that evaluate each agent in isolation (given these inputs, does this agent produce output meeting its rubric?) and **pipeline-level tests** that evaluate the end-to-end system (given this user query, does the final output meet the overall rubric?).

Agent-level tests catch problems early and localize them. Pipeline-level tests catch integration problems that agent-level tests miss: format mismatches between agents, context that passes through multiple handoffs and degrades, or emergent behaviors that only appear when agents interact. Both levels are necessary. Agent-level tests without pipeline tests give false confidence. Pipeline tests without agent-level tests make debugging impossible when they fail.

## What it changes in model behavior

A test harness does not change model behavior. It changes your *knowledge* of model behavior. It converts anecdotes ("the model seems worse lately") into data ("pass rate dropped from 91% to 84% after the March 15 prompt change"). It makes quality visible, measurable, and actionable.

## Use it when

- You are iterating on a prompt or pipeline that will be used repeatedly
- Multiple people contribute to prompt development and you need a shared quality standard
- The system is in production and prompt changes carry risk
- You need to compare model versions, prompt variants, or pipeline configurations
- Quality requirements are explicit and can be expressed as evaluation criteria

## Do not use it when

- You are running a one-time, ad hoc query with no future reuse
- The task is exploratory and you do not yet know what good output looks like
- The investment in building the harness exceeds the expected lifetime value of the system (very short-lived prototypes)

## Contrast set

- → **rubric** — The rubric defines the evaluation criteria. The test harness is the infrastructure that applies those criteria across many test cases. The rubric is the standard; the harness is the system.
- → **regression check** — A regression check is one type of test a harness runs — comparing current results against a baseline. The harness supports regression checks but also supports exploration, benchmarking, and A/B comparison.
- → **verification loop** — A verification loop is runtime quality control within a single pipeline execution. A test harness is development-time quality control across many executions. One happens during generation; the other happens before deployment.
- → **evaluation** — Evaluation is the broad concept. A test harness is the engineering infrastructure that makes evaluation systematic and repeatable.

## Common failure modes

- **Unrepresentative test cases** — The test suite covers the cases the developer thought of, which are usually the easy ones. The hard cases, the edge cases, and the adversarial cases are absent. The harness reports 95% pass rate, but production shows 75% because the real distribution differs from the test distribution. Fix: populate test cases from real user inputs, including failure cases from production. Update the suite regularly.

- **Evaluator drift** — The LLM-as-judge evaluator becomes more lenient or more strict over time due to model updates, or its criteria diverge from human judgment. Tests pass that a human reviewer would fail. Fix: periodically calibrate the evaluator against human judgments. Maintain a "golden set" of human-evaluated outputs and verify that the evaluator agrees.

- **Harness maintenance neglect** — The harness is built once and never updated. The system evolves — new features, new output formats, new quality expectations — but the test cases and rubrics do not. The harness gradually becomes irrelevant, testing for properties the system no longer needs to have. Fix: treat the test suite as a living codebase. Budget time for test maintenance alongside prompt development.

## Prompt examples

### Minimal example

```text
Test case 1:
  Input: "What is our return policy for electronics?"
  Rubric: Cites policy document. Mentions 30-day window.
  Mentions restocking fee. Under 100 words.

Test case 2:
  Input: "Can I return a gift without a receipt?"
  Rubric: Cites policy document. Correctly states receipt
  requirement. Offers alternative (store credit). Under 100 words.

Run both test cases. Score each rubric criterion PASS/FAIL.
Report results.
```

### Strong example

```text
You are a test evaluator. You will receive a model output
and a rubric. Evaluate the output against each criterion.

Output to evaluate:
"""
[model output inserted here]
"""

Rubric:
| # | Criterion | Type | Threshold |
|---|-----------|------|-----------|
| 1 | Answers the user's stated question | Semantic | Must directly address the question |
| 2 | All claims cite a source from the provided documents | Structural | 100% citation rate |
| 3 | No claims contradict the source documents | Semantic | Zero contradictions |
| 4 | Response length | Structural | 100-250 words |
| 5 | Professional tone, no casualisms | Stylistic | No "hey," "sure thing," slang |
| 6 | Includes a specific next-step recommendation | Semantic | Present and actionable |

For each criterion, output:
{
  "criterion": 1,
  "score": "PASS | FAIL",
  "evidence": "specific quote or observation supporting score"
}

Then output:
{
  "pass_count": N,
  "fail_count": N,
  "overall": "PASS (all criteria met) | FAIL (any criterion failed)"
}
```

### Agentic workflow example

```text
Pipeline: Test Harness for Multi-Agent Research System

Test Suite: 25 test cases stored in test_suite/cases.json
Each case:
{
  "case_id": "TC-001",
  "input_query": "user question",
  "source_documents": ["SRC-001", "SRC-003"],
  "rubric": {
    "agent_level": {
      "research_agent": ["min 3 findings", "all sourced"],
      "verification_agent": ["catches planted error in SRC-001 p.4"],
      "synthesis_agent": ["under 300 words", "cites findings"]
    },
    "pipeline_level": [
      "final output answers the query",
      "no unsourced claims in final output",
      "format matches output_template.json"
    ]
  },
  "planted_errors": ["SRC-001 p.4 contains a deliberate
    factual error the pipeline should catch"]
}

Test Runner:
1. For each test case, initialize the pipeline with the
   input query and source documents.
2. Capture all intermediate outputs (per agent) and the
   final output.
3. Send each agent's output to the evaluator with that
   agent's rubric.
4. Send the final output to the evaluator with the
   pipeline-level rubric.
5. Record all scores.

Reporter output:
| Case ID | Research | Verification | Synthesis | Pipeline | Overall |
| TC-001  | PASS     | PASS         | PASS      | PASS     | PASS    |
| TC-002  | PASS     | FAIL         | PASS      | FAIL     | FAIL    |

Aggregate: 23/25 PASS (92%). Failures in TC-002, TC-017.
Regression vs. baseline_v2: TC-017 is new failure (REGRESSION).
TC-002 was previously failing (KNOWN ISSUE).
```

## Model-fit note

Test harnesses are model-agnostic infrastructure, but the evaluator component benefits from model selection. Use frontier models for LLM-as-judge evaluation — they show the highest agreement with human judgments and are least susceptible to position bias or verbosity bias in evaluation. Use programmatic checks wherever possible (format compliance, length, schema validation) to reduce evaluator cost. For testing across model tiers, the harness should parameterize the model under test so the same suite can evaluate different models or versions.

## Evidence and provenance

LLM evaluation frameworks (OpenAI Evals, LangSmith, Braintrust, RAGAS) implement the test harness pattern for model and prompt evaluation. The LLM-as-judge paradigm is formalized in Zheng et al. (2023) with MT-Bench. The concept of test harnesses in software engineering dates to the earliest structured testing practices (IEEE 829, 1998). Property-based testing over exact-match testing reflects the non-deterministic nature of LLM outputs, discussed across LLM evaluation literature.

## Related entries

- **→ rubric** — the evaluation criteria the harness applies
- **→ regression check** — one type of test the harness supports
- **→ verification loop** — runtime quality control; the harness is development-time quality control
- **→ evaluation** — the broader concept the harness operationalizes
