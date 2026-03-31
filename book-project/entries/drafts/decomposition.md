---
headword: "decomposition"
slug: "decomposition"
family: "core_abstraction"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["hierarchy", "modularity", "specificity", "chunking", "overcompression", "planner-executor split", "pipeline"]
cross_links: ["hierarchy", "modularity", "specificity", "constraint", "planner-executor split", "overcompression", "context windowing"]
tags: ["core", "prompting-fundamental", "reasoning", "agent-architecture"]
has_note_box: true
note_box_type: "workflow_note"
---

# decomposition

## One-Sentence Elevator Definition

Decomposition is the act of breaking a complex task into smaller, individually solvable sub-tasks before asking a model to execute.

## Expanded Definition

Decomposition is the structural discipline of not asking a model to do too much at once. When a task involves multiple reasoning steps, multiple output types, or multiple evaluation criteria, a single monolithic prompt forces the model to juggle all of them simultaneously. The result is usually mediocre on every dimension. Decomposition solves this by turning one hard problem into several easier ones.

In software engineering, decomposition is a foundational principle: functions do one thing, modules encapsulate one concern, services own one domain. The same logic applies to language-as-programming. A decomposed prompt assigns one job per step, one evaluation criterion per pass, one reasoning chain per sub-task.

The technique has formal backing. Chain-of-thought prompting, introduced by Wei et al. (2022), is decomposition applied to reasoning: instead of asking the model to jump to an answer, you ask it to work through intermediate steps [src_decomposition_001]. Least-to-most prompting extends this by explicitly ordering sub-problems from simple to complex [src_decomposition_002]. Both techniques produce measurably better performance on tasks that require multi-step reasoning.

Decomposition is not just a prompting technique. It is an architectural principle. In → planner-executor split workflows, decomposition is the planner's primary job: take a goal and break it into a sequence of delegatable tasks. The quality of the decomposition determines the quality of the entire workflow.

## Why This Matters for LLM Prompting

Language models process prompts sequentially, and attention has limits. A prompt that bundles analysis, evaluation, formatting, and recommendation into a single instruction forces the model to allocate attention across competing demands. The typical result: shallow analysis, generic evaluation, correct formatting, and a recommendation that does not follow from the evidence.

Decomposition lets you serialize these demands. Step 1: analyze the data. Step 2: evaluate the findings against criteria. Step 3: format the evaluation. Step 4: recommend based on the evaluation. Each step gets full attention. Each step can be checked before proceeding. The compound quality improvement is significant.

## Why This Matters for Agentic Workflows

Decomposition is the bridge between a high-level goal and a set of agent tasks. A well-decomposed plan maps directly to agent assignments: each sub-task becomes a delegation with a clear input, output, and completion criterion.

Poorly decomposed plans create two problems. Under-decomposition produces tasks too broad for any single agent to execute reliably, leading to vague outputs and scope creep. Over-decomposition fragments the work into pieces so small that the overhead of → handoff and → context passing exceeds the value of each piece.

## What It Does to Model Behavior

When you decompose a task explicitly in a prompt (or across a multi-turn interaction), models produce more structured, step-wise reasoning. Research shows that chain-of-thought decomposition improves accuracy on arithmetic, commonsense reasoning, and symbolic manipulation tasks by 10-40% compared to direct prompting, depending on model size and task complexity [src_decomposition_001]. The benefit is largest for tasks that genuinely require multi-step inference.

## When to Use It

- When a task requires more than two distinct reasoning steps
- When the output needs to satisfy multiple, potentially competing criteria
- When a previous monolithic prompt produced shallow or inconsistent results
- When you need to verify intermediate work before proceeding
- When delegating across multiple agents in a workflow
- When the task spans multiple knowledge domains

## When NOT to Use It

- When the task is genuinely simple and a single prompt handles it cleanly
- When decomposition would fragment a naturally cohesive thought process
- When the sub-tasks are so interdependent that separating them loses necessary context
- When you are optimizing for speed and the overhead of multi-step execution is not justified
- When working within tight token budgets where each step consumes scarce → context budget

## Strong Alternatives / Adjacent Abstractions / Contrast Set

| Term | Relationship | Key Difference |
|------|-------------|----------------|
| → hierarchy | overlaps | Hierarchy organizes levels of abstraction; decomposition breaks tasks into steps |
| → modularity | overlaps | Modularity encapsulates components; decomposition sequences sub-tasks |
| → specificity | complementary | Specificity narrows what to do; decomposition structures how to do it |
| → chunking | child | Chunking is decomposition applied to information segments |
| → overcompression | contrast | Overcompression is the failure of insufficient decomposition |
| → planner-executor split | application | The planner's job is decomposition; the executor handles individual pieces |
| → pipeline | application | A pipeline is decomposition made into a persistent architecture |

## Failure Modes / Misuse Patterns

1. **Over-decomposition.** Breaking a task into sub-tasks so fine-grained that each one is trivial but the reassembly is harder than the original problem. Symptoms: outputs that are locally correct but globally incoherent, and excessive context-passing overhead.

2. **Decomposition without dependency mapping.** Splitting a task into parallel sub-tasks when they actually depend on each other sequentially. The result: sub-tasks produce inconsistent outputs because they lacked information from prior steps.

3. **Decomposition as procrastination.** Endlessly planning sub-tasks instead of executing them. In agent workflows, this manifests as planner agents that produce increasingly detailed task breakdowns without ever triggering execution.

## Minimal Prompt Example

```
I need to evaluate whether our customer support team should adopt a new ticketing tool.

Step 1: List the top 5 features our team uses most in the current tool.
Step 2: For each feature, rate the new tool's equivalent on a 1-5 scale.
Step 3: Identify any features the new tool offers that we don't currently have.
Step 4: Based on steps 1-3, give a recommendation with your confidence level.

Start with Step 1.
```

## Strong Prompt Example

```
You are a senior code reviewer. I will give you a pull request diff.
Your review should proceed in three passes:

PASS 1 — Structural Review
- Does the PR do one thing? If it bundles unrelated changes, flag them.
- Are new functions/methods appropriately scoped?
- Are there any obvious architectural concerns?
Output: a bullet list of structural observations.

PASS 2 — Correctness Review
- For each changed function, trace the logic path.
- Identify edge cases that are not handled.
- Flag any assumptions that are not validated.
Output: a numbered list of potential bugs or logic gaps, with file and line references.

PASS 3 — Recommendation
- Based on passes 1 and 2, give one of: APPROVE, REQUEST CHANGES, or NEEDS DISCUSSION.
- If REQUEST CHANGES, list the specific changes required, ordered by severity.
- If NEEDS DISCUSSION, state the open question that blocks approval.

Complete all three passes. Do not skip ahead.
```

## Agent Workflow Example

```
Agent: Project Planner
Goal: Produce a competitive analysis report for {product}

Decomposition:
1. RESEARCH phase (→ Research Analyst agent)
   - Input: product name, market category
   - Task: identify 5 competitors, collect feature lists and pricing
   - Output: structured competitor data as JSON
   - Completion: data for all 5 competitors, each with ≥3 verified sources

2. ANALYSIS phase (→ Strategy Analyst agent)
   - Input: competitor JSON from step 1
   - Task: compare features, identify gaps, rank competitive threats
   - Output: comparison matrix + threat ranking
   - Completion: matrix covers all feature categories, ranking justified

3. SYNTHESIS phase (→ Report Writer agent)
   - Input: comparison matrix + threat ranking from step 2
   - Task: write executive summary (max 500 words) + detailed report
   - Output: markdown document with sections
   - Completion: summary addresses top 3 threats, recommendations included

4. REVIEW phase (→ Consistency Editor agent)
   - Input: final report
   - Task: verify all claims trace to source data, check for contradictions
   - Output: reviewed report + list of any unresolved issues
   - Completion: zero unresolved factual issues

Each phase must complete before the next begins.
Escalation: if any phase cannot complete, return to the Planner with a gap analysis.
```

## Model-Fit Note

Decomposition is beneficial across all model tiers but critical for different reasons. Smaller open models benefit because they have limited capacity for simultaneous multi-step reasoning; decomposition turns what they cannot do in one pass into what they can do in several. Frontier models benefit because decomposition allows verification at each step, catching errors before they propagate. Reasoning-specialized models like o1/o3 perform internal decomposition, but explicit decomposition in the prompt still helps by structuring the verification surface.

## Evidence / Provenance Note

Chain-of-thought prompting (Wei et al., 2022) and least-to-most prompting (Zhou et al., 2022) provide the primary evidence base for decomposition's effectiveness [src_decomposition_001, src_decomposition_002]. The interaction with model size is documented in the original chain-of-thought paper, which showed that benefits scale with model capability [src_decomposition_003]. Over-decomposition patterns are documented in agent workflow literature and prompt engineering community practice [src_decomposition_004, src_decomposition_005].

## Related Entries

- **→ hierarchy** — decomposition produces hierarchy; hierarchy informs decomposition
- **→ planner-executor split** — the agent architecture that operationalizes decomposition
- **→ specificity** — decomposition makes each sub-task more specific
- **→ pipeline** — a pipeline is decomposition hardened into a repeatable workflow
- **→ overcompression** — what happens when you don't decompose enough
- **→ context windowing** — decomposition interacts with context limits (each step consumes tokens)

---

> **Workflow Note**
>
> When decomposing for an agent pipeline, number your steps and name your agents. "Step 3 (Strategy Analyst)" is easier to debug than an unnamed handoff. If step N fails, you know exactly where to look. If the decomposition changes, the numbered structure makes the diff clear.
