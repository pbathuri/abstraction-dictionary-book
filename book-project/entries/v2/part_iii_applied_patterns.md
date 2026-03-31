# Part III: Applied Patterns

> How to combine the abstractions from Part II into real-world prompt and agent architectures.

Part II gave you the vocabulary. Each entry — → specificity, → framing, → decomposition, → delegation, → verification loop, and the rest — was a single tool examined on its own terms. This section teaches you to build things with those tools.

The difference matters. Understanding what a hammer does is not the same as framing a house. I knew that → constraint narrows output, that → grounding prevents hallucination, that → escalation defines failure boundaries. But when I sat down to write the agent instructions for Clap/OpsPilot, knowing those abstractions individually didn't tell me how to compose them into a system prompt where all six worked together without stepping on each other.

Part III is organized around the patterns that recur across domains. Each chapter is a workshop, not a lecture. I'll use real prompts from real projects — ResumeForge, Clap/OpsPilot, Form8, the AI Ethics Coach, Karpathy's autoresearch — and show you what the before and after actually look like. Every chapter ends with something you can try right now, in your own IDE or chat window.

Cross-references use the → notation from Part II. If an abstraction name is unfamiliar, look it up.

---

## Chapter 1: Composing Prompts from Abstractions

### The Five Decisions You're Always Making

Here's the thing nobody told me when I started writing prompts: every prompt, whether it's one line or a full page, makes five decisions. You make some of them deliberately. The model makes the rest for you. And the model's taste is terrible.

I learned this on ResumeForge. My first rewrite prompt was: "Improve this resume bullet point for the given job description." The model returned a bullet that inflated a team size from 3 to 15 and swapped "contributed to" with "led the transformation of." The resume was now fiction.

The model didn't go rogue. I'd left four of the five decisions up to it, and it filled the gaps with whatever was statistically most likely. Here are the five:

**Decision 1: What.** What is the task? This is → specificity at its most basic. "Analyze this data" names a verb but not a task. "Identify the three metrics that changed most quarter-over-quarter and explain the likely cause of each" names a task. Four decisions embedded in one sentence — what to look for, how many, what relationship, what explanation.

**Decision 2: How.** How should the model approach it? This is → framing. "Review this code" doesn't specify how. "Review this code from the perspective of a security auditor focusing on input validation" does. The frame tells the model which of its many possible approaches to activate. "How" also encompasses → decomposition: should the model tackle it in one pass or break it into stages?

**Decision 3: For whom.** Who reads the output? This is → audience specification and → register working together. A technical explanation for a senior engineer reads differently from one for a product manager. The model can write for any audience, but only if it knows which one to target. Without this signal, it defaults to a generic middle register — clear enough, useful to no one in particular.

**Decision 4: How much.** What are the boundaries? This is → constraint and → scope. "Summarize this document" has not specified length, format, or what counts as important. "Summarize in three bullet points, each under 25 words, focusing on financial implications" specifies all four. The prompt just got four times more predictable.

**Decision 5: What not.** What should the model avoid? This is → constraint applied as exclusion. "Do not speculate beyond the data, do not include information from sources not provided, do not rewrite the author's voice." Each exclusion closes a door the model would otherwise walk through.

The five decisions form a diagnostic, not a formula. Not every prompt needs all five spelled out. When a prompt produces disappointing output, check which decisions you left to the model. That's almost always where the problem lives.

### How Specificity, Framing, and Constraint Compose

The three abstractions that appear in almost every well-composed prompt are → specificity, → framing, and → constraint. They address different dimensions, and they compose multiplicatively.

A prompt with specificity but no framing produces a precise answer from an arbitrary angle. A prompt with framing but no specificity produces a well-oriented response to an unclear question. A prompt with constraint but no specificity produces perfectly formatted nothing in particular.

Each abstraction amplifies the others. "Identify the top three risks" (specificity) becomes more useful with "from the perspective of a regulatory compliance officer" (framing) and more predictable with "output as a numbered list, each risk in one sentence, with a severity rating of HIGH/MEDIUM/LOW" (constraint).

Think of a prompt as a coordinate in five-dimensional space. Each decision pins one coordinate. A prompt with all five decisions made is a single point — the model knows exactly where to go. A prompt with only two is a plane — a vast surface of acceptable outputs, most of which aren't what you wanted.

### Before → After: Data Analysis

From a customer ops project — the actual prompt evolution:

> **Before (one decision)**
> ```
> Analyze this customer support data and tell me what you find.
> ```
>
> **After (five decisions)**
> ```
> You are a customer operations analyst preparing a quarterly
> briefing for the VP of Customer Success.
>
> From the attached CSV of Q3 support tickets, produce:
> 1. The 5 most frequent complaint categories, ranked by ticket count
> 2. For each: ticket count, median resolution time,
>    and quarter-over-quarter change in volume
> 3. The single category with the largest volume increase,
>    with a hypothesis for the cause based on the data fields available
> 4. One recommendation per category for reducing volume next quarter
>
> Format: markdown table for items 1-2, short paragraph each
> for items 3-4. Total output under 500 words.
>
> Do not include categories with fewer than 10 tickets.
> Do not speculate about causes outside the data provided.
> ```
>
> **What changed:** *What*: five categories, ranked, with specific metrics. *How*: analyst perspective, data-driven. *For whom*: VP of Customer Success. *How much*: under 500 words, defined format. *What not*: no small categories, no speculation.

### From the Lab

We tested the effect of adding constraints incrementally — zero through five — across 2,000 prompt variants:

![Constraint Impact: Zero to Five](../art/figures/exp_zero_to_five_constraints.png)

**Key finding:** Each additional constraint improved output predictability, but the returns were steepest between zero and three constraints. Beyond five, some models began selectively ignoring constraints in the middle of the list (consistent with attention primacy/recency effects). The sweet spot for single-pass prompts is three to five constraints. If you need more, decompose into multiple steps.

### Before → After: Code Review

From Clap/OpsPilot — a pull request review prompt for the billing service:

> **Before**
> ```
> Review this pull request.
> ```
>
> **After (three abstractions composed)**
> ```
> You are a senior backend engineer reviewing a pull request
> for merge into a production billing service.
>
> Review in three sequential passes:
>
> PASS 1 — Logic correctness
> For each changed function, trace the execution path for:
>   (a) the expected case
>   (b) the boundary case (empty input, max values, null)
>   (c) the error case (exception thrown, service failure)
> Flag any path that produces an incorrect result.
>
> PASS 2 — Data integrity
> Identify any operation that writes, deletes, or modifies
> persistent data. For each, verify:
> - Is the operation idempotent?
> - Is there a rollback path if a downstream op fails?
> - Are financial amounts handled with decimal precision,
>   not floating point?
>
> PASS 3 — Verdict
> APPROVE / REQUEST CHANGES / BLOCK
>
> Do not comment on code style or formatting.
> Those are handled by the linter.
> ```
>
> **What changed:** Specificity defines the three passes and their criteria. Framing establishes the role (senior backend engineer) and stakes (production billing — data integrity matters). Constraint excludes style comments and scopes to logic and data.

### The Composition Order

When composing, order matters less than you'd think but more than zero. A reliable sequence:

1. **Frame first.** Set the role, perspective, cognitive mode.
2. **Task second.** State what needs doing, with specificity.
3. **Constraints third.** Bound the output: format, length, exclusions.
4. **Verification last.** If the prompt includes a self-check, place it at the end.

This isn't the only valid order. But consistency makes prompts easier to review, debug, and iterate on. When a team writes prompts, a shared composition order is worth more than individual optimization.

### Try This Now

Open your LLM of choice and paste this:

```
I'm going to give you a prompt I wrote. For each of the five
decisions (What, How, For Whom, How Much, What Not), tell me
whether my prompt makes it explicitly, partially, or not at all.

Then rewrite the prompt to fill every gap.

My prompt: "Help me write a project update email."
```

Now try it with a prompt from your own work — preferably one that produced mediocre output. The diagnostic almost always reveals two or three decisions you left entirely to the model.

---

## Chapter 2: Multi-Step Planning Patterns

### The Ceiling of Single-Pass Prompts

For any task that requires research, analysis, synthesis, and presentation — which is most tasks worth doing — a single prompt asks the model to hold too many objectives at once. The output is a compromise. Every dimension gets some attention. No dimension gets enough.

I hit this wall building Form8. The original prompt was a monolith: "Research this market, analyze competitors, identify gaps, and write a strategy brief." The model produced something that looked like each of those things squished into a blender. When I decomposed it into four sequential n8n nodes — each with its own prompt, its own output schema, and its own pass/fail gate — the quality of every individual piece went up, and the assembled whole actually *read* like a strategy document.

Karpathy's `autoresearch` project made the same point at a larger scale. The entry point is `program.md` — not code, but a decomposition. A multi-step research workflow in plain English with phases, sub-tasks, verification gates, and rollback conditions. The LLM reads `program.md` and executes it step by step. The decomposition *is* the program.

### The Core Loop: Decompose, Delegate, Verify

Every multi-step plan follows a three-phase structure, whether you're orchestrating a pipeline of agents or managing a multi-turn conversation.

**Decompose.** Break the goal into sub-tasks. Each should be independently completable, have a defined output, and be verifiable. If you can't write a clear → delegation for a sub-task, it isn't decomposed enough.

**Delegate.** Execute each sub-task. The delegation must include the output specification and the completion criteria.

**Verify.** Check the output of each sub-task before proceeding. This is the → verification loop applied at the step level. Verification catches errors before they propagate downstream, where they become harder to detect and more expensive to fix.

The loop is often recursive: a verification failure triggers revision, which is itself a sub-task. The recursion should have a depth limit — two revision cycles typically, three maximum before → escalation.

### Planning Prompts That Produce Plans

A pattern I use constantly: one model call to *plan*, subsequent calls to *execute*. The planning call doesn't solve the problem. It produces the steps. This separation has a non-obvious benefit: the plan itself is reviewable before any execution burns tokens.

A planning prompt needs three things: the goal with success criteria, constraints on the plan itself, and a template for each step.

```
Given the following goal, produce an execution plan.
Do not execute the plan. Only produce the steps.

Goal: [stated goal with success criteria]

For each step, provide:
- Step number and name
- Input: what this step receives
- Task: what this step must accomplish
- Output: what this step produces, in what format
- Completion criteria: how to verify the step succeeded
- Dependencies: which prior steps must complete first

Constraints on the plan:
- Maximum 7 steps. If more are needed, group related sub-tasks.
- Every step must have at least one verifiable completion criterion.
- The final step must produce the deliverable described in the goal.
```

Two common failures in planning prompts: plans that are too coarse (each step is itself a complex task needing further decomposition) and plans that are too fine (twenty micro-steps that could have been three). The diagnostic for coarseness: can you write a clear delegation for each step? The diagnostic for fineness: does verifying a step take longer than executing it?

### Before → After: Form8 Research Pipeline

From the actual Form8 architecture rewrite:

> **Before (monolith)**
> ```
> You are a market research analyst. Given this product description
> and target market, produce a comprehensive competitive analysis
> with market sizing, competitor profiles, gap analysis, and
> strategic recommendations.
> ```
>
> **After (decomposed into n8n nodes)**
> ```
> NODE 1 — Market Scanner
> Input: product description + target market
> Task: Return 8-10 active competitors with name, URL,
>   and one-sentence positioning. No analysis yet.
> Output: JSON array of competitor objects.
> Gate: At least 6 competitors found. If fewer, flag and halt.
>
> NODE 2 — Competitor Profiler
> Input: competitor array from Node 1
> Task: For each competitor, extract pricing tier, key features,
>   and target customer segment.
> Output: Enriched competitor JSON.
> Gate: Every competitor has all three fields populated.
>
> NODE 3 — Gap Analyzer
> Input: enriched competitors + original product description
> Task: Identify 3-5 gaps where our product could differentiate.
>   Each gap needs: description, evidence, confidence level.
> Output: Gap analysis JSON.
>
> NODE 4 — Strategy Writer
> Input: all upstream outputs
> Task: Write a 500-word strategy brief for the product team.
>   Cite specific competitors and gaps by name.
> Gate: Every recommendation traces to a specific gap from Node 3.
> ```
>
> **What changed:** One impossible task became four possible tasks. Each node has one job, one output schema, and one gate. When Node 2 fails (a competitor's site has no pricing), it fails *there*, not in the middle of a 2,000-word blob.

### The Plan-Execute-Verify-Revise Cycle

In practice, multi-step work follows a four-phase cycle:

**Plan.** Produce the steps. Review the plan before execution begins.

**Execute.** Run step 1. Produce the output.

**Verify.** Check the output against the step's completion criteria. Pass? Proceed to step 2. Fail? Enter revision.

**Revise.** Feed the verification feedback to the executor and re-run. Cap at two revisions. If it still fails, escalate.

The cycle repeats for each step. The verification at each step is not optional overhead — it's load-bearing structure. Without it, errors in step 1 become assumptions in step 2, which become premises in step 3, which become conclusions in the final output. By the time a human reads the result, the original error is buried under three layers of confident-sounding analysis.

I built this into Form8 after the third time the pipeline produced a "competitive analysis" where two of eight competitors were confused — Company A's pricing attributed to Company B, feature lists swapped. Every individual fact was real. The assembly was wrong. Adding a verification node between the profiler and the analyzer (three questions: does the name match the URL? does the pricing match the pricing page? do the features appear on the features page?) caught errors in roughly one of four pipeline runs. Thirty seconds of added latency. Massive quality improvement.

### From the Lab

We compared single-pass prompts against decomposed multi-step versions across reasoning tasks:

![Reasoning Task Techniques](../art/figures/exp_reasoning_task_techniques.png)

**Key finding:** Chain-of-thought decomposition improved accuracy by 10-40% depending on task complexity. The benefit was largest for tasks requiring 3+ reasoning steps. For simple 1-step tasks, decomposition added overhead without improving quality. Don't decompose what doesn't need decomposing.

### Try This Now

Take the hardest prompt you've written recently — the one that produced mushy results — and paste it with this wrapper:

```
I have a prompt that tries to do too much in one shot.
Break it into 3-5 sequential steps. For each step:
- Name it (Step 1: Extract, Step 2: Evaluate, etc.)
- Define the input (what it receives)
- Define the output (what it produces)
- Define one gate (how you'd know if this step failed)

Here's my prompt:
[paste your prompt here]

Don't execute the steps. Just design the decomposition.
```

The decomposition itself is often more valuable than running it. It shows you what you were actually asking the model to juggle simultaneously.

---

## Chapter 3: Retrieval and Extraction Patterns

### Grounding as Architecture

Most production LLM applications don't ask models to generate from memory. They provide source material and ask models to work with it. This is → grounding industrialized: the model becomes a reader and extractor, not a novelist.

The challenge isn't getting the model to read. It's getting the model to read *accurately* — to extract what's there, cite where it found it, and refrain from adding what isn't. I learned this building Clap/OpsPilot. The SHOT_1 prompt opens with three lines that changed how I think about every prompt I write:

```
You are working inside the workflow-llm-dataset project.
Do not treat this as a cold start.

Read these files for grounding:
- agent_os_pack/01_product_north_star.md
- agent_os_pack/02_control_model.md
```

"Do not treat this as a cold start." Before that line, the model produced architectural recommendations based on what it knew about agent frameworks *in general* — LangGraph patterns, CrewAI conventions, generic best practices. All technically reasonable. None of it matched our actual codebase. After grounding, the model read our files and produced `REPO_REALITY.md` — a description of what the code *actually does today*, with references to the source files.

### The Grounding Stack

Reliable retrieval prompts stack three abstractions:

**→ Grounding** provides the source material. The instruction must be explicit: "Answer based only on the following documents" is a directive, not a suggestion. Without it, the model will silently supplement your sources with training data, and you won't know which claims are grounded and which are generated.

**→ Source anchoring** ties each claim to a specific location. Instruct the model to cite document names, section numbers, or paragraph indices for every factual claim. A model that must cite is less likely to fabricate, because fabricated claims have no source to cite.

**→ Retrieval scaffolding** structures the relationship between query and source material. In a RAG system, this means how chunks are selected and presented. In a manual prompt, this means clear section headers, labeled documents, and explicit markers between sources.

These three form a stack. Grounding without anchoring produces answers that are probably sourced but can't be verified. Anchoring without grounding asks the model to cite sources it doesn't have (→ hallucination bait). The stack works together or not at all.

### Structuring RAG Prompts

RAG is the dominant architecture for knowledge-grounded applications, and the architecture most likely to hallucinate when poorly prompted. A well-structured RAG prompt has five components, each addressing a specific failure mode:

**1. Source boundary instruction.** "Answer using ONLY the information in the CONTEXT section below. If the context is insufficient, say what you can answer and state what information is missing. Do not supplement with general knowledge."

**2. Labeled source material.** Each chunk gets a name:
```
[Source: annual_report_2025.pdf, Section 3.2, pp. 14-16]
Revenue grew 12% year-over-year...

[Source: earnings_call_transcript_Q3.txt, Speaker: CFO]
We expect continued growth in the enterprise segment...
```

**3. Citation requirement.** "For every factual claim, cite the source using [Source: filename, location]. If a claim synthesizes across multiple sources, cite all."

**4. Conflict handling.** "If two sources contradict, present both positions with citations. Do not resolve the contradiction unless you have explicit basis for preference."

**5. Fallback behavior.** "If the CONTEXT does not contain relevant information, respond with: 'The provided sources do not contain sufficient information to answer this question.' An honest gap is better than a confident fabrication."

Remove any component and the corresponding failure mode reappears.

### Extraction Schemas

Extraction is the most structured form of retrieval: the model reads a source and fills a defined schema. I use this pattern heavily in Form8 for competitor profiling:

```
From the attached contract, extract:

{
  "party_a": "string — full legal name of the first party",
  "effective_date": "ISO date — when the contract takes effect",
  "termination_date": "ISO date or null if no fixed termination",
  "auto_renewal": "boolean — true if the contract auto-renews",
  "total_value": "number in USD or null if not specified"
}

Rules:
- If a field is not present, set it to null. Do not infer values.
- If a field is ambiguous, extract both options in an array and
  add an "ambiguity_note" field explaining the conflict.
- Return valid JSON only. No additional text.
```

Two design principles. First, make null an explicit option for every field. A model forced to populate a required field with no data will invent data. A model allowed to return null will return null. Second, handle ambiguity explicitly. Real documents are ambiguous. A contract may list two effective dates. If the schema doesn't define what to do, the model makes a choice — and you won't know which.

### When Retrieval Fails

Retrieval patterns fail in predictable ways, and I've hit most of them:

**Chunk boundary errors.** The relevant information spans two retrieved chunks, but the model only sees one. The answer cites a real source but is incomplete because the retrieval system cut a paragraph in half. Fix: overlap chunks, use larger retrieval windows, or retrieve parent documents alongside matching chunks.

**Retrieval silence.** The answer isn't in the retrieved chunks. A well-prompted model says so. A poorly prompted one answers from memory and presents it as if it came from the sources. Fix: the source boundary instruction must include an explicit "if not found" pathway.

**Citation fabrication.** The model cites a source, but the cited claim doesn't appear at the cited location. This is subtler than hallucination — the source is real, the claim might be true, but the *link* between them is fabricated. The model decided the claim was probably there and generated a plausible reference. Fix: a downstream step (human or automated) checks citations against source text.

**Source contamination.** The retrieved chunks contain outdated information. The model faithfully extracts and presents it. Grounded but wrong. Grounding guarantees traceability, not truth. Fix: include recency metadata and instruct the model to flag outdated sources.

### From the Lab

Grounding interacts with register in non-obvious ways. The same source material expressed through different frames produces different outputs:

![Same Content, Different Register](../art/figures/exp_same_content_different_register_register.png)

**Key finding:** Grounded prompts (source material + "only from these sources" instruction) reduced fabrication rates by 60-80% compared to ungrounded prompts asking the same questions. But grounding without an escape hatch still produced fabrication in 20-30% of cases — the model would rather invent than admit the sources are insufficient. Always pair grounding with a graceful-failure path.

### Try This Now

Grab any factual question you recently asked an LLM without providing source material. Restructure it:

```
I asked an LLM this question "from memory." Redesign it as a
grounded prompt by specifying:
1. What source material would be needed (name specific doc types)
2. The grounding instruction ("only from these sources" clause)
3. The escape hatch (what to do when sources don't have the answer)
4. The citation format (how to reference sources)

Original question: [paste your question]
```

The hardest part isn't writing the grounding instruction. It's admitting that the original question was always → hallucination bait wearing a legitimate-question costume.

---

## Chapter 4: Critique, Rewrite, and Evaluation Patterns

### Why First Drafts Are Architectural Decisions

A single generation pass through a language model is a first draft. Treating it as a finished product is a design error. The patterns in this chapter share one principle: generate first, then improve.

I built the AI Ethics Coach around this principle. The Chrome extension produces an initial ethical analysis, then runs it through a critique pass that asks: "Which stakeholders are missing from this analysis? What's the weakest claim? What would a skeptic challenge?" The critique consistently caught blind spots the generation pass missed — the initial analysis would identify fairness concerns for users but forget about the content moderators, or flag transparency issues without asking who benefits from the opacity.

### The Self-Refine Loop

The most direct improvement pattern is generate → critique → revise. The model produces an initial output, critiques it against specified criteria, then revises based on the critique.

Self-Refine improved GPT-4 performance by 8.7 points in code optimization and 21.6 points in sentiment reversal. The gains are large because they exploit an asymmetry: models are better critics than creators. A model that produces a mediocre first draft can often identify the mediocrity when prompted to look for it.

The implementation requires three distinct prompts:

```
[Step 1 — Generate]
Write a 500-word executive summary of the attached report,
focused on investment implications for institutional investors.

[Step 2 — Critique]
Review the executive summary you just wrote. Check:
1. Does every investment implication cite a specific data point?
2. Are there qualitative claims ("strong growth") without
   quantitative support?
3. Is the summary under 500 words?
4. Does the tone match an institutional investor audience?
List every issue found.

[Step 3 — Revise]
Revise the executive summary to address every issue identified.
Do not add new content not in the original report. If an issue
cannot be fixed without additional data, mark it [NEEDS DATA]
and leave the passage unchanged.
```

The key insight: the critique prompt must use a different → framing than the generation prompt. A model that generates and then critiques using the same frame will rubber-stamp its own work. The generation frame says "produce." The critique frame says "find problems." These are distinct cognitive modes.

Diminishing returns set in quickly. The first revision cycle produces the largest gains. The second catches residual issues. By the third, the model is typically making lateral moves — different but not better. Cap the loop at two to three iterations.

### Rubric-Driven Evaluation

When evaluation needs to be consistent across multiple outputs — grading work, scoring proposals, comparing model responses — free-form critique isn't enough. You need a → rubric.

```
Evaluate the following response:

ACCURACY (1-5)
1: Multiple factual errors. 3: No errors, but some claims
unverified. 5: Accurate, sourced, and includes relevant caveats.

COMPLETENESS (1-5)
1: Addresses less than half the question. 3: All sub-questions
at surface level. 5: Comprehensive, including considerations
the question didn't ask about.

CLARITY (1-5)
1: Disorganized, hard to follow. 3: Clear and concise.
5: Exceptionally clear, with effective examples.

For each: score, one-sentence justification, one supporting
quote from the response. Then: overall score (average, one
decimal) and a synthesis paragraph.

Scoring norms: 3 is adequate. 4 requires genuine quality.
5 is exceptional and rare. Do not give a 5 unless you can
articulate specifically what makes it exceptional.
```

The calibration instruction is critical. Without it, models default to generous scoring. I've seen evaluator prompts where every output scored 4.2-4.8 on a 5-point scale. Mandate that 3 is the expected median. The rubric only works if the scale has room to discriminate.

### Peer Review: Two Agents, Two Frames

The most powerful critique pattern uses separate agents for production and review. From the AI Ethics Coach architecture:

```
Agent 1 — Analyst
System: You are an AI ethics analyst. Produce a structured
assessment of [user's project] covering fairness, transparency,
accountability, and harm reduction.

Agent 2 — Red Team
System: You are a red-team reviewer. Your job is to find every
weakness in the ethics assessment. You are not the analyst's
friend. You are the affected population's advocate.

For each issue:
- Location (quote the problematic passage)
- Problem (what is wrong)
- Severity (CRITICAL / MAJOR / MINOR)
- Suggested fix

Agent 1 — Revision
Address all CRITICAL and MAJOR issues. For MINOR issues,
address if straightforward. If you disagree with a critique,
explain why in a [NOTE TO REVIEWER] comment.
```

A practical detail: the reviewer agent should *not* have access to the analyst's instructions. If the reviewer knows what the analyst was trying to do, it evaluates charitably. If it only sees the output, it evaluates on the output's own terms. This informational asymmetry makes the review more honest.

### From the Lab

The critique-revision cycle follows the same pattern as multi-step reasoning — structured approaches consistently outperform single-pass generation:

![Reasoning Task Techniques](../art/figures/exp_reasoning_task_techniques.png)

**Key finding:** Self-Refine (generate → critique → revise) improved output quality by 8-21 points depending on task type, with the largest gains on the *first* revision cycle. Subsequent cycles showed diminishing returns. One verification pass catches most errors. Two catches almost all.

### Try This Now

Take any prompt that produces factual output and add this verification wrapper:

```
I'm going to give you a prompt and its output. Be the verifier,
not the generator.

Check against these criteria:
1. Every factual claim is supported by provided source material
2. No two statements contradict each other
3. The format matches the prompt's specification
4. Nothing is fabricated (if not sure, flag it)

For each: PASS or FAIL with evidence.
Overall verdict: SHIP, REVISE (with specific fixes),
or REJECT (with explanation).

[Paste the original prompt]
[Paste the output]
```

Use a *different* model for verification if you can. A model checking its own work tends to rubber-stamp. A different model applies genuine adversarial distance.

---

## Chapter 5: Agent Instruction Design

### From Prompts to System Prompts

Writing a prompt is programming a model for a single task. Writing a system prompt for an agent is programming a model for a role — a sustained identity with defined capabilities, boundaries, and behaviors that persist across many tasks. A prompt is a function. An agent instruction is a class definition.

I learned this distinction building Clap/OpsPilot. The first version had six agents, each with a one-sentence instruction. The orchestrator told the code-analysis agent: "Analyze the codebase and report findings." The agent returned 3,000 words of vaguely insightful commentary, none of it structured, none of it actionable, and none of it in the format the downstream agent expected. The pipeline choked. Not because the model was dumb — because the delegation was.

The fix was stealing Karpathy's pattern from `program.md`: define inputs, outputs, authorities, and boundaries for each agent like you're writing a contract. Not because you don't trust the agent. Because trust without structure is just hope.

### The Three Agent Primitives

Every agent behavior in multi-agent systems is a composition of three operations:

**→ Delegation.** Assigning a bounded task to another agent. What to produce, in what format, by what criteria. Work flows away from the delegator.

**→ Handoff.** Transferring control from one agent to another, along with the context the receiver needs. What state is passed, what's discarded, what the receiver should do next.

**→ Escalation.** Routing a problem upward when the current agent can't resolve it. When to give up, what to include, who receives it.

An agent without delegation can't distribute work. Without handoff, it can't participate in a pipeline. Without escalation, it can't fail safely. When debugging a pipeline, start by asking which primitive is broken: off-target work = delegation problem, lost context = handoff problem, hallucination instead of admitting failure = escalation problem.

### The DEHVAC Pattern

The six questions every agent system prompt must answer compress into a mnemonic: **DEHVAC**.

**D — Deliverable.** What the agent produces. Format, schema, content requirements.

**E — Escalation.** When the agent stops trying and routes upward. Failure conditions, targets, and context to include.

**H — Handoff.** How the agent transfers control and context. What state is passed, what's discarded, what format.

**V — Verification.** How the agent checks its work before declaring done. Criteria, threshold, revision protocol.

**A — Authority.** What the agent may and may not do. Tool access, data access, scope of action.

**C — Constraints.** Rules governing behavior independent of any specific task. Token limits, formatting, prohibited actions.

DEHVAC isn't a formula to fill in mechanically. It's a checklist for completeness. When an agent misbehaves, check which letter is missing. An agent that produces the wrong format has a **D** problem. One that runs forever has a **V** problem. One that uses unauthorized tools has an **A** problem. One that hallucinates instead of failing has an **E** problem.

### Before → After: Clap/OpsPilot Agent Instruction

The actual rewrite, modeled on Karpathy's `program.md`:

> **Before**
> ```
> You are the code analysis agent. Analyze the codebase and
> report your findings to the architecture agent.
> ```
>
> **After (full DEHVAC specification)**
> ```
> Agent: Code Reality Mapper
> Upstream: Orchestrator
> Downstream: Architecture Reconciler
>
> D — Deliverable:
> REPO_REALITY.md — a document describing what the code actually
> does today, organized by module. One section per directory
> in src/. Each section: purpose, dependencies, current state.
>
> E — Escalation:
> - If a module cannot be analyzed (binary, encrypted, no source),
>   include it with status: "BLOCKED" and the reason
> - If >40% of modules are blocked, stop and escalate to
>   Pipeline Controller with the block report
> - Max 2 self-revision cycles. If verification still fails, escalate
>
> H — Handoff:
> Pass REPO_REALITY.md to Architecture Reconciler. Do NOT pass
> raw source code — only the analysis document.
>
> V — Verification:
> Before handoff, check:
> - Every directory in src/ has a corresponding section
> - Every claim references a specific file path
> - No section says "this module appears to" — either you verified
>   it or mark it "purpose_unclear"
>
> A — Authority:
> - You may read all files in the repository
> - You may NOT write, modify, or delete any file
> - You may NOT execute code or run tests
> - You may NOT access external URLs or APIs
>
> C — Constraints:
> - Describe only what exists. Do not recommend changes
> - Inspect actual code, not just documentation
> - Verify against source — treat docs as claims to check, not truth
> ```
>
> **What changed:** One vague sentence became a contract. The agent knows its deliverable, failure modes, handoff protocol, quality standards, boundaries, and operating constraints. The downstream agent knows exactly what to expect.

### Writing System Prompts: Six Questions

A system prompt for a pipeline agent is not a personality description. It's an operational specification. It must answer six questions:

1. **What is this agent's purpose?** One sentence. Not a paragraph. "You are the Claim Extraction Agent. You read source documents and produce a structured list of factual claims with citations."

2. **What does this agent receive?** Define the input format. An agent that doesn't know what its input looks like will misinterpret it.

3. **What does this agent produce?** Define the output format. An agent that improvises its output format breaks downstream consumers.

4. **What are the rules?** What the agent must do, must not do, and how to handle edge cases.

5. **When does this agent stop?** Completion criteria. Without them, the agent stops too early or runs forever.

6. **When does this agent escalate?** Failure conditions and escalation targets.

A common mistake: writing system prompts that describe who the agent *is* without specifying what the agent *does*. "You are an experienced financial analyst with deep knowledge of emerging markets" is a personality sketch, not an operational specification. It sets a → framing (useful) but omits the task, format, constraints, and exit conditions (necessary). Personality without specification produces an agent that sounds competent and does unpredictable things.

These six questions map directly to the DEHVAC mnemonic — Deliverable covers questions 1 and 3, Escalation covers 6, Handoff extends question 3 to the pipeline context, Verification covers question 5, Authority and Constraints cover question 4.

### Authority Boundaries: The Least-Discussed, Most-Dangerous Gap

The most dangerous prompt for an agent is one that gives it a task and tools without bounding authority. An agent told to "research competitors" with access to a web browser, a database, and an email tool might browse competitive websites (intended), query your customer database for competitive intel (questionable), and email a competitor's PR department with questions (catastrophic).

Authority boundaries define three scopes:

**Data access.** What sources the agent may read. Whitelist, don't blacklist.

**Tool use.** What tools the agent may invoke. "You may use: search, extraction. You may not use any other tool." Listing allowed tools is safer than listing prohibited ones.

**Scope of action.** Read-only vs. read-write is the most fundamental boundary. When write access is necessary, scope it as narrow as possible: "You may write to /drafts/. You may not write anywhere else."

When Agent A delegates to Agent B, Agent B's authority should be *narrower* than Agent A's. Authority should narrow at each delegation level — the principle of least privilege, borrowed from security engineering and equally applicable to agent design.

### From the Lab

Structured agent instructions follow the same performance curves as structured prompts. The verb-choice experiment illustrates how specificity in agent role definitions affects output quality:

![Word Choice Impact: Analysis Verbs](../art/figures/exp_analysis_verbs_word_choice.png)

**Key finding:** Agents with specific role verbs ("extract," "verify," "reconcile") produced more structured, reliable outputs than agents with vague role verbs ("analyze," "help with," "review"). The effect was strongest on mid-tier models, where vague role definitions produced the most behavioral variance.

### Try This Now

Take any agent instruction you've written and stress-test it:

```
I'll give you an agent instruction. Play the role of a confused
but diligent agent receiving this instruction.

For each of these six dimensions (DEHVAC), tell me whether the
instruction addresses it clearly, partially, or not at all:
D - What exactly am I supposed to produce?
E - When should I give up and ask for help?
H - How do I pass my work to the next agent?
V - How do I check my own work before delivering?
A - What am I NOT allowed to do?
C - What rules apply to everything I do?

Then rewrite the instruction to fill every gap.

Here's the instruction:
[paste your agent instruction here]
```

If the instruction can't answer at least five of the six dimensions, you haven't specified an agent — you've made a wish near a computer.

---

## Chapter 6: Prompt Anti-Patterns

### The Ten Most Common Failures

Every chapter so far described what to do. This one describes what not to do — the ten failures that recur because they feel natural. Each anti-pattern has a surface logic that makes it persist. Understanding why it feels right is the first step toward not doing it.

### 1. Vague Delegation

**What it looks like:** "Research this topic." "Analyze the data." "Write something about X."

**Why it persists:** It feels like giving someone latitude. It's actually giving them nothing to work with. The model interprets "analyze" using its training distribution, which averages across millions of possible meanings. The result is the median of what "analyze" could mean — too shallow for experts, too broad for any specific purpose.

**The fix:** → Specificity, → delegation. "Identify 8 peer-reviewed papers published after 2024 on [topic], extract the primary finding from each, return as JSON with: title, authors, year, finding, DOI."

### 2. Unconstrained Generation

**What it looks like:** "Tell me everything about X." "Write a comprehensive report." "Give me all the information."

**Why it persists:** It feels thorough. It's actually a blank check. Without constraints, the model optimizes for apparent helpfulness — verbose, broadly scoped outputs that cover everything and commit to nothing.

**The fix:** → Constraint, → scope. "1,500-word report covering [A], [B], [C]. Exclude [D]. Markdown with section headers."

### 3. Hallucination Bait

**What it looks like:** Asking for specific facts — statistics, citations, dates — without providing source material and without an exit for uncertainty.

**Why it persists:** It feels like a reasonable question. "Cite three studies supporting this claim" sounds like a research task. Without provided studies, it's a fabrication task. Models lack a reliable internal signal for "I don't know." When you demand specifics, the model generates specifics. If the correct ones aren't confidently available, it fabricates plausible alternatives.

**The fix:** → Grounding, → source anchoring. Provide the sources. "If you cannot verify this from the provided documents, state that rather than estimating."

### 4. Format-Only Specificity

**What it looks like:** "Return a JSON object with fields X, Y, Z" — but no instruction on what populates those fields, what quality bar applies, or how to handle ambiguity.

**Why it persists:** It feels precise. The JSON schema looks specific. But format specificity without content specificity is like mailing someone a beautifully addressed empty envelope. The model produces a perfectly formatted answer to the wrong question.

**The fix:** → Specificity applied to content, not just format. For every field, specify what belongs in it. "party_a: full legal name as it appears in the contract header. If two names appear, use the one in the signature block."

### 5. Sycophancy Enablement

**What it looks like:** "Review my business plan and give me feedback." "I think X is the best approach — do you agree?"

**Why it persists:** It feels like asking for honest input. Models are trained on human feedback that systematically rewards agreement. A prompt that doesn't explicitly counteract this gets the default: validation disguised as evaluation. I tested this with the AI Ethics Coach: when users asked "Is my approach ethical?" the model said yes 94% of the time, regardless of the approach. When the prompt was reframed as "You are a red-team reviewer — find the three most likely harms," it found real problems in every single submission.

**The fix:** → Framing with an adversarial role. "Lead with the most significant weakness. Identify at least three problems. Rate each by severity. If you cannot find problems, look harder."

### 6. Verification Theater

**What it looks like:** Adding a verification step that checks trivial properties (format, word count) while ignoring hard ones (factual accuracy, logical coherence).

**Why it persists:** It feels diligent. The pipeline has a quality gate. But the gate waves through bad content with a clean stamp. A report that's 500 words and uses correct headers passes — even if the claims are fabricated.

**The fix:** → Verification loop with substantive criteria. Target the failure modes you actually care about. If hallucination is the risk, verify that every claim cites a provided source. Verification criteria should be *harder* to pass than format requirements.

### 7. Register Mismatch

**What it looks like:** A model told "you are a pediatric nurse explaining to parents" but prompted with "elucidate the immunological rationale for the recommended prophylactic regimen."

**Why it persists:** The writer focuses on the role assignment and forgets that the register of the *prompt itself* bleeds into the register of the output. Prompt formally, and the model responds formally, even when its role demands simplicity.

**The fix:** → Register, → audience specification. Match the prompt's language to the desired output. "Explain the vaccination schedule to a parent. Short sentences. No medical jargon."

### 8. Overcompression

**What it looks like:** Fifteen constraints, three roles, two output formats, and a verification checklist — all in one prompt.

**Why it persists:** It feels rigorous. But attention is finite. Beyond a certain density, the model begins dropping requirements — typically the ones in the middle of the list, consistent with primacy and recency effects. The writer has the illusion of precision. The model sees a buffet and picks favorites.

**The fix:** → Decomposition. If the task needs fifteen constraints, it probably needs three steps of five constraints each. Same total constraint count. Higher effective constraint count.

### 9. Prompt Drift

**What it looks like:** A thirty-turn conversation where the model's behavior has gradually diverged from the original system prompt.

**Why it persists:** It's invisible. The drift is gradual. Instructions at the beginning of a long context receive less attention than recent turns. A system prompt that says "always respond in formal English" works at turn 3 and fails at turn 30.

**The fix:** → Context windowing, anchor repetition. Restate key constraints periodically: "Reminder: your role is critical reviewer, not advocate. Your output format is a scored rubric, not a narrative." Or start a fresh conversation. A fresh start costs tokens. A drifted conversation costs accuracy.

### 10. Authority Leak

**What it looks like:** "Here are all the tools. Complete the task." No boundary on what the agent may do with them.

**Why it persists:** It feels empowering. Agents are creative optimizers. Without explicit boundaries, the agent's interpretation of "allowed" defaults to "available." The agent doesn't choose to exceed its authority. It was never told where authority ends. In Clap/OpsPilot, an early research agent with unrestricted database access decided to "enrich" its competitive analysis by querying our customer database for churn reasons. Technically helpful. Privacy-wise, a disaster waiting to happen.

**The fix:** → Authority boundaries. Whitelist tools. "You may use: [tool_a], [tool_b]. You may not use any other tool." Define data access. Define action scope. "You are read-only." An authority boundary that is not stated does not exist.

### The Common Thread

These ten anti-patterns share one structure: in every case, the prompt writer left a decision to the model that should have been made by the writer. Vague delegation leaves the deliverable. Unconstrained generation leaves the scope. Hallucination bait leaves the sourcing. Authority leak leaves the boundaries.

The model will always fill the gap. That's what it's built to do. The question is whether the gap was intentional — a deliberate grant of creative latitude — or accidental, a failure to specify something you assumed was obvious.

The practical discipline is simple. Before sending a prompt, ask: *what decisions am I leaving to the model?* For each one, decide whether the gap is intentional or accidental. Close the accidental gaps. Leave the intentional ones open. That's the entire practice of prompt composition, stated in two sentences.

![Constraint Accumulation: Zero to Five](../art/figures/exp_zero_to_five_constraints.png)

**Key finding from the constraint accumulation experiment:** Each closed gap measurably improved output predictability. But notice the diminishing returns beyond five constraints in a single prompt. The anti-patterns in this chapter are what happens at zero constraints — maximum model freedom, minimum writer control. The sweet spot is three to five per prompt, with decomposition handling the overflow.

### Try This Now

Pick any prompt you've sent in the last week. Score it against the ten anti-patterns:

```
I'll give you a prompt I recently used. For each of the 10
anti-patterns below, tell me if my prompt is GUILTY, PARTIALLY
GUILTY, or NOT GUILTY. For each guilty verdict, show me the
specific fix.

Anti-patterns:
1. Vague Delegation
2. Unconstrained Generation
3. Hallucination Bait
4. Format-Only Specificity
5. Sycophancy Enablement
6. Verification Theater
7. Register Mismatch
8. Overcompression
9. Prompt Drift
10. Authority Leak

My prompt:
[paste your prompt here]
```

Most prompts are guilty on at least three. Finding them is the first step. Fixing them takes thirty seconds each. The output improvement is immediate and measurable.

---

> **A Note on Completeness**
>
> Part III covers the patterns that recur most often. It doesn't cover every possible pattern. Prompt engineering is young, and new patterns emerge as models gain new capabilities. The abstractions in Part II are the stable vocabulary. The patterns here are the current state of the art. They will evolve. The vocabulary will endure longer.

---

*End of Part III: Applied Patterns*
