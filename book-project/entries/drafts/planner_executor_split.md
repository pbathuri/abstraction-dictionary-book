---
headword: "planner-executor split"
slug: "planner-executor-split"
family: "agent_workflow"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# Planner-Executor Split

**Elevator definition** An architecture that separates the agent that decides what to do from the agent that does it, so that reasoning and action don't contaminate each other.

## What it is

The planner-executor split is a division of labor inside an agentic system. One agent — the planner — analyzes the task, breaks it into steps, sequences those steps, and produces a plan. A different agent — the executor — takes that plan and carries it out, one step at a time, without re-reasoning about why these steps were chosen or whether different steps would be better.

This is not a new idea. It is the command structure of every military, the relationship between an architect and a general contractor, the distinction between a screenplay and its production. What makes it newly relevant is that language models are bad at doing both things simultaneously. When a single model plans and executes in the same context, it frequently abandons its own plan mid-execution, gets distracted by details, or loses track of which step it's on. Splitting the roles externalizes the plan as an artifact — a written document the executor can reference — and that externalization is what makes complex tasks reliable.

The planner's job is decomposition: take a complex goal and produce an ordered list of concrete, actionable steps. Good plans are specific enough that the executor doesn't need to interpret them. "Research the market" is a planner failure. "Search for the five largest competitors in the North American SaaS CRM market by 2025 revenue, and for each competitor extract: company name, annual revenue, primary product, and market share percentage" is a plan the executor can follow without guessing.

The executor's job is compliance: follow the plan faithfully, report results, and flag any step it cannot complete. The executor should not freelance. If the plan says "extract these four fields," the executor extracts those four fields — not six fields it thinks might also be useful. Executor creativity is a bug, not a feature. The moment the executor starts re-planning, you've collapsed back to a single-agent architecture with extra overhead.

The split can be implemented in several ways. In the simplest version, the planner runs first and produces a plan as structured text, which is then fed to the executor as its system prompt or task description. In more sophisticated versions, an orchestrator mediates: it sends the task to the planner, receives the plan, validates it, and then dispatches steps to the executor one at a time, collecting results and handling failures. The orchestrator can also send executor results back to the planner for mid-course correction — a feedback loop that is powerful but expensive.

The quality ceiling of a planner-executor system is set by the plan. A brilliant executor cannot salvage a bad plan. A mediocre executor can often succeed with a great one. This asymmetry means you should invest more design effort in the planner prompt than in the executor prompt. The planner prompt needs examples of good plans, explicit decomposition strategies, and constraints on granularity. The executor prompt needs clear instructions on compliance, output formatting, and error reporting.

## Why it matters in prompting

Every multi-step prompt is an implicit planner-executor split. When you write "First do X, then do Y, then do Z," you are both planner and executor designer. The quality of your decomposition — how well X, Y, and Z are scoped, how clearly their boundaries are defined, how explicitly their outputs are specified — determines whether the model executes faithfully or drifts.

Making the split explicit improves results. Instead of embedding both roles in a single prompt, write two prompts: one that generates the plan, another that executes it. This lets you inspect the plan before execution, catch decomposition errors early, and iterate on the planning logic without re-running the entire task. It also lets you use different models for each role — a reasoning-heavy model for planning, a faster model for execution.

## Why it matters in agentic workflows

The planner-executor split is the backbone of most production agent architectures. Frameworks like LangGraph, CrewAI, and AutoGen implement it explicitly, with planner agents that decompose tasks and executor agents that carry out individual steps. The pattern scales: a planner can decompose a task into subtasks, each of which is handled by a specialized executor, and each executor can itself be a planner-executor pair for its own sub-problem.

The split also enables **observability**. When planning and execution are separate, you can log the plan independently, compare it to execution results, and identify where failures originate. Did the planner produce a bad decomposition? Or did the executor fail to follow a good one? Without the split, debugging is archaeology. With it, debugging is bookkeeping.

## What it changes in model behavior

A model operating as a pure executor — given an explicit plan to follow — produces more consistent, more predictable output than the same model asked to plan and execute simultaneously. The plan acts as an external scaffold that compensates for the model's tendency to lose track of multi-step reasoning. It reduces hallucination of intermediate goals and prevents the model from conflating "what should I do" with "what am I doing."

## Use it when

- The task requires more than three sequential steps
- Steps have different skill requirements (research, analysis, writing, code generation)
- You need to inspect or approve the plan before execution begins
- Reproducibility matters — you want to re-run the same plan with different executors or parameters
- Debugging requires isolating planning failures from execution failures
- You are operating under token budgets and want to use a cheaper model for execution

## Do not use it when

- The task is simple enough that a single prompt handles it reliably
- The task is inherently exploratory and cannot be planned in advance (use iterative refinement instead)
- Latency is critical and the overhead of a planning step is unacceptable
- The planner has no way to validate its plan against the executor's actual capabilities

## Contrast set

- **Chain-of-thought** — Chain-of-thought keeps reasoning and action in the same agent, interleaved. The planner-executor split externalizes reasoning into a separate artifact. Chain-of-thought is thinking aloud while working. Planner-executor is writing the blueprint, then handing it to the builder.
- **Decomposition** — Decomposition is the act of breaking a task into parts. The planner-executor split is an architecture that assigns decomposition to one agent and execution to another. Decomposition is the skill; the split is the org chart.
- **Orchestration** — Orchestration manages the flow between planner and executor (and potentially many executors). The planner-executor split defines roles; orchestration coordinates them.
- **ReAct (Reason + Act)** — ReAct interleaves reasoning and action within a single agent loop. The planner-executor split separates them into distinct phases. ReAct is flexible but hard to control. The split is rigid but auditable.

## Common failure modes

- **Over-granular planning** — The planner decomposes the task into 47 micro-steps, each so trivial that the overhead of managing them exceeds the complexity of the original task. The executor spends more time reading the plan than doing the work. Fix: constrain the planner to produce 3-8 steps, and define a minimum step complexity.
- **Plan-executor mismatch** — The planner assumes capabilities the executor doesn't have. It writes "query the database for recent transactions" when the executor has no database access. Fix: include the executor's available tools and capabilities in the planner's context.
- **Frozen plans** — The plan doesn't adapt when early steps produce unexpected results. The executor follows the plan into a wall because no feedback loop exists. Fix: implement checkpoints where executor results are reviewed (by the planner or an orchestrator) and the plan is revised if needed.

## Prompt examples

Minimal (single prompt, implicit split):

```
Analyze the sales data and write a report with recommendations.
```

Strong (explicit two-stage split):

```
STAGE 1 — PLANNING
You are a task planner. Given the goal below, produce a numbered plan of 4-6 steps.
Each step must specify: the action, the input it requires, and the output it produces.
Do not execute any steps. Only produce the plan.

Goal: Analyze Q4 sales data to identify underperforming regions and recommend resource reallocation.

STAGE 2 — EXECUTION
You are a task executor. Follow the plan below exactly. For each step:
1. Perform the specified action using the specified input.
2. Produce the specified output.
3. If you cannot complete a step, report what is missing and stop.
Do not add steps. Do not skip steps. Do not reinterpret the plan.

Plan:
[insert output from Stage 1]
```

Agentic workflow (orchestrated planner-executor with feedback):

```yaml
workflow:
  planner:
    model: "claude-3-opus"
    prompt: |
      Decompose this task into 4-6 steps. For each step, specify:
      - action: what to do
      - tool: which tool to use (from: [web_search, code_exec, doc_reader, calculator])
      - input: what data the step needs
      - output_schema: what the step must produce
      - success_criteria: how to know the step succeeded
    task: "Research and compare the pricing models of the top 5 cloud GPU providers."

  executor:
    model: "claude-3-haiku"
    for_each_step: true
    prompt: |
      Execute this step exactly as specified. Use the designated tool.
      Return output matching the output_schema. Report failures immediately.

  checkpoint:
    after_step: [2, 4]
    action: "Send executor results to planner for plan revision if needed."
```

## Model-fit note

Strong reasoning models (GPT-4o, Claude Opus, Gemini Pro) make the best planners — they produce coherent decompositions and anticipate executor constraints. Executor roles can often be handled by faster, cheaper models (Haiku, GPT-4o-mini, Gemini Flash) since the plan provides sufficient scaffolding. This asymmetric model allocation is one of the split's main economic advantages.

## Evidence and provenance

The planner-executor architecture appears in robotics planning literature (STRIPS, 1971; PDDL, 1998) and was adapted for LLM agents in the "Plan-and-Solve" prompting paper (Wang et al., 2023). LangChain's Plan-and-Execute agent module (2023) and Microsoft's AutoGen framework both implement the pattern explicitly. Empirical results from Wang et al. show that plan-then-execute outperforms single-pass chain-of-thought on multi-step reasoning benchmarks by 5-12%.

## Related entries

- **decomposition**
- **orchestration**
- **chain-of-thought**
- **handoff**
- **delegation**
