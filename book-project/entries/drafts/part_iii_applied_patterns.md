# Part III: Applied Patterns

> How to combine the abstractions from Part II into real-world prompt and agent architectures.

Part II gave you a vocabulary. Each entry — → specificity, → framing, → decomposition, → delegation, → verification loop, and the rest — was a single tool in a drawer, examined on its own terms. This section teaches you to build things with those tools.

The difference matters. Understanding what a hammer does is not the same as framing a house. Knowing that → constraint narrows output, that → grounding prevents hallucination, and that → escalation defines failure boundaries tells you what each abstraction does in isolation. It does not tell you how to compose a prompt that uses all three in the right proportions, or how to design an agent pipeline where each abstraction appears at the right stage.

Part III is organized around the patterns that recur across domains. Chapter 1 covers prompt composition — how to assemble a single, well-formed prompt from multiple abstractions. Chapter 2 addresses multi-step planning, the structural discipline of breaking work into stages. Chapters 3 and 4 cover the two most common applied patterns: retrieval/extraction and critique/evaluation. Chapter 5 moves to agent instruction design, where the unit of work is not a prompt but a system. Chapter 6 names the failures — the ten anti-patterns that undo the rest.

Each chapter assumes you have read (or can reference) the Part II entries it depends on. Cross-references use the → notation from Part II. If an abstraction name is unfamiliar, look it up.

---

## Chapter 1: Composing Prompts from Abstractions

A prompt is not a sentence. It is a program written in natural language, and like any program, it makes decisions. Most prompts make those decisions implicitly — the writer types what comes to mind, the model interprets what it can, and the gap between intent and output is filled by the model's best guess. The purpose of prompt composition is to make those decisions explicitly, using the abstractions from Part II as the building blocks.

### The Five Decisions

Every prompt, whether it is a one-liner or a page-long system instruction, makes five decisions. Sometimes the writer makes them deliberately. More often, the writer makes one or two and leaves the rest to the model. The model always fills the gaps. It just does not fill them the way you would.

**Decision 1: What.** What is the task? This is → specificity at its most basic. "Analyze this data" names a verb but not a task. "Identify the three metrics that changed most quarter-over-quarter and explain the likely cause of each" names a task. The difference is that the second version tells the model what to look for, how many results to produce, what relationship to examine, and what kind of explanation to provide. Four decisions embedded in one sentence.

The "what" decision sounds obvious, but it is the one most frequently botched. Writers who have a clear picture in their head assume the model shares it. It does not. The model has a probability distribution over what "analyze" might mean, and that distribution was shaped by millions of training examples, most of which are not yours. State what you want. The model cannot read your mind. It can only read your prompt.

**Decision 2: How.** How should the model approach the task? This is → framing — the choice of angle, method, and cognitive mode. "Review this code" does not specify how. "Review this code from the perspective of a security auditor focusing on input validation" does. The frame tells the model which of its many possible approaches to activate.

"How" also encompasses → decomposition. Should the model tackle the task in one pass or break it into stages? A prompt that says "First identify the issues, then prioritize them by severity, then recommend fixes for the top three" decomposes the task into a sequence. A prompt that says "Review and recommend" leaves the sequencing to the model, which will pick whatever sequence was most common in its training data.

**Decision 3: For whom.** Who is the audience? This is → audience specification and → register working together. A technical explanation for a senior engineer reads differently from one for a product manager, which reads differently from one for a customer. The model can write for any audience, but only if it knows which audience to target.

The "for whom" decision also shapes depth and vocabulary. A prompt that names its audience gives the model permission to calibrate: use jargon or avoid it, assume background knowledge or explain from basics, prioritize precision or accessibility. Without this signal, the model defaults to a generic middle register — clear enough, specific enough, useful to no one in particular.

**Decision 4: How much.** What are the boundaries? This is → constraint and → scope. How long should the output be? How many items should the model return? What level of detail is appropriate? What format should the output take?

"How much" is where most prompts hemorrhage quality. A prompt that says "summarize this document" has not specified length, format, or what counts as the important content. The model will produce something. It might be three sentences or three pages. It might focus on what you care about or on what it finds statistically interesting. Every unspecified dimension is a coin flip.

Constraints are the mechanism. "Summarize in three bullet points, each under 25 words, focusing on financial implications" specifies length (three bullets), format (bullet list), density (under 25 words each), and scope (financial implications). Four constraints, one sentence. The prompt just got four times more predictable.

**Decision 5: What not.** What should the model avoid? This is → constraint applied as exclusion. Every positive instruction ("do this") benefits from a paired negative instruction ("do not do that"). Negative constraints are underused because they require the writer to anticipate what might go wrong — which requires experience with model behavior.

Common exclusions: do not speculate beyond the data, do not include information from sources not provided, do not rewrite the author's voice, do not suggest changes outside the scope of the review. Each exclusion closes a door the model would otherwise walk through.

The five decisions form a framework, not a formula. Not every prompt needs all five spelled out. A simple factual query ("What is the boiling point of ethanol at sea level?") needs only Decision 1. A complex analytical task needs all five. The framework's value is diagnostic: when a prompt produces disappointing output, check which of the five decisions you left to the model. That is almost always where the problem lives.

### Combining Specificity, Framing, and Constraint

The three abstractions that appear in almost every well-composed prompt are → specificity, → framing, and → constraint. They address different dimensions of the prompt, and they compose naturally.

Specificity narrows the target: what exactly the model should produce. Framing orients the approach: the angle, perspective, or cognitive mode. Constraint bounds the output: what format, what length, what exclusions.

A prompt with specificity but no framing produces a precise answer from an arbitrary angle. A prompt with framing but no specificity produces a well-oriented response to an unclear question. A prompt with constraint but no specificity produces perfectly formatted nothing in particular.

The composition is multiplicative, not additive. Each abstraction does not just add value; it amplifies the others. A specific task ("identify the top three risks") becomes more useful with framing ("from the perspective of a regulatory compliance officer") and more predictable with constraint ("output as a numbered list, each risk in one sentence, with a severity rating of HIGH/MEDIUM/LOW").

### Worked Example 1: Data Analysis

**Scenario:** You have a CSV of customer support tickets from the last quarter. You need an analysis for the VP of Customer Success.

**Weak prompt (one decision):**
```
Analyze this customer support data and tell me what you find.
```

This specifies the task verb ("analyze") but nothing else. The model will produce something — probably a rambling overview touching on everything and committing to nothing.

**Composed prompt (five decisions):**
```
You are a customer operations analyst preparing a quarterly briefing
for the VP of Customer Success.

From the attached CSV of Q3 support tickets, produce:
1. The 5 most frequent complaint categories, ranked by ticket count
2. For each category: ticket count, median resolution time,
   and quarter-over-quarter change in volume
3. The single category with the largest increase in volume,
   with a hypothesis for the cause based on the data fields available
4. One recommendation per category for reducing ticket volume next quarter

Format: markdown table for items 1-2, then a short paragraph each
for items 3-4. Total output under 500 words.

Do not include categories with fewer than 10 tickets.
Do not speculate about causes outside the data provided.
If a field needed for analysis is missing from the CSV, note the gap
instead of filling it with assumptions.
```

What changed: the prompt now makes all five decisions. *What*: five categories, ranked, with specific metrics. *How*: analyst perspective, data-driven. *For whom*: VP of Customer Success (sets register and depth). *How much*: under 500 words, specific format, defined metrics. *What not*: no small categories, no speculation, no gap-filling.

### Worked Example 2: Writing

**Scenario:** You need a model to rewrite a technical blog post for a non-technical audience.

**Weak prompt:**
```
Rewrite this blog post for a general audience.
```

**Composed prompt:**
```
Rewrite the following technical blog post for readers of a general
business publication (think Harvard Business Review, not TechCrunch).

Constraints:
- Preserve every factual claim. Do not simplify by omitting data.
- Replace technical jargon with plain language. Where a technical term
  is necessary, define it in parentheses on first use.
- Maintain the original structure (same number of sections, same
  argument flow).
- Target length: within 10% of the original word count.
- Tone: authoritative but accessible. No condescension ("simply put,"
  "in layman's terms"). No hype ("revolutionary," "game-changing").

Do not add examples or analogies that are not in the original.
If a passage cannot be simplified without losing accuracy,
flag it as [NEEDS EDITOR: technical passage retained] and move on.

Output the rewritten post, followed by a change log listing every
technical term you replaced and the plain-language substitute you used.
```

The five decisions: *What*: rewrite, preserving claims. *How*: plain-language substitution with flagging. *For whom*: HBR-level business readers. *How much*: within 10% of original length, same structure. *What not*: no omissions, no added material, no condescending language.

### Worked Example 3: Code Review

**Scenario:** A pull request needs review before merge. You want the model to catch logic errors, not comment on style.

**Weak prompt:**
```
Review this pull request.
```

**Composed prompt:**
```
You are a senior backend engineer reviewing a pull request for merge
into the main branch of a production billing service.

Review the following diff in three sequential passes:

PASS 1 — Logic correctness
For each changed function, trace the execution path for:
  (a) the expected case
  (b) the boundary case (empty input, max values, null)
  (c) the error case (exception thrown, external service failure)
Flag any path that produces an incorrect result or unhandled state.

PASS 2 — Data integrity
Identify any operation that writes, deletes, or modifies persistent
data (database, cache, external API). For each, verify:
  - Is the operation idempotent or guarded against duplicate execution?
  - Is there a rollback path if a downstream operation fails?
  - Are financial amounts handled with decimal precision, not floating point?

PASS 3 — Verdict
Based on passes 1 and 2, deliver one of:
  APPROVE — no logic or data integrity issues found
  REQUEST CHANGES — list each required change, ordered by severity
  BLOCK — a critical issue that could cause data loss or financial error

Do not comment on code style, naming conventions, or formatting.
Those are handled by the linter.
If a section of the diff is a test file, verify that the tests cover
the cases you identified in Pass 1, but do not review the test code itself.
```

Three abstractions carry this prompt. Specificity defines the three passes and their criteria. Framing establishes the role (senior backend engineer) and the context (production billing service — which immediately raises the stakes for data integrity). Constraint excludes style comments and scopes the review to logic and data.

### The Composition Principle

These examples share a structural principle: the abstractions do not compete for space; they occupy different dimensions. Specificity answers *what*. Framing answers *how*. Constraint answers *what not* and *how much*. Audience specification answers *for whom*. When a prompt feels bloated, it is usually because one dimension is over-specified while another is empty. When a prompt produces off-target output, it is usually because the wrong dimension was specified.

A useful mental model: think of a prompt as a coordinate in a five-dimensional space. Each of the five decisions pins one coordinate. A prompt with all five decisions made is a single point in that space — the model knows exactly where to go. A prompt with only two decisions made is a plane — a vast surface of acceptable outputs, most of which are not what you wanted. Every unspecified decision is a degree of freedom you are granting to the model's probability distribution.

This explains why two prompts can feel equally "detailed" yet produce wildly different output quality. A prompt that specifies format in microscopic detail (JSON schema, field names, data types, nesting structure) but leaves content criteria open has high total word count but only one coordinate pinned. A prompt that is half as long but pins four coordinates — what, how, for whom, what not — will outperform it every time.

### The Order of Composition

When composing a prompt from multiple abstractions, order matters less than you might expect but more than zero. The model does not process instructions sequentially in the way a CPU executes code. It attends to the full prompt simultaneously. But human readability — and therefore human debuggability — benefits from a consistent structure.

A reliable composition order:

1. **Frame first.** Set the role, the perspective, the cognitive mode. This orients everything that follows.
2. **Task second.** State what needs to be done, with specificity.
3. **Constraints third.** Bound the output: format, length, exclusions.
4. **Verification last.** If the prompt includes a self-check, place it at the end, where the model encounters it just before generating output.

This is not the only valid order. But it is a consistent one, and consistency makes prompts easier to review, debug, and iterate on. When a team of people writes prompts, a shared composition order is worth more than individual optimization.

The diagnostic question remains the same: which decision did I leave to the model? Find it, make it explicit, and the output improves.

---

## Chapter 2: Multi-Step Planning Patterns

Single-pass prompts have a ceiling. For any task that requires research, analysis, synthesis, and presentation — which is to say, most tasks worth doing — a single prompt asks the model to hold too many objectives simultaneously. The output is a compromise. Every dimension gets some attention. No dimension gets enough.

Multi-step planning solves this by turning one hard task into several easier ones, sequenced so that each step feeds the next. This is → decomposition applied as an architectural pattern, not just a prompting technique.

### The Core Loop: Decompose, Delegate, Verify

Every multi-step plan follows the same three-phase structure, whether you are orchestrating a pipeline of agents or managing a multi-turn conversation with a single model.

**Phase 1: Decompose.** Break the goal into sub-tasks. Each sub-task should be independently completable, have a defined output, and be verifiable against specific criteria. The decomposition is good when each sub-task can be stated as a complete delegation (→ delegation) — if you cannot write a clear delegation for a sub-task, it is not decomposed enough.

**Phase 2: Delegate.** Execute each sub-task. In a multi-agent system, this means handing each task to an agent with the right capabilities. In a single-model conversation, this means issuing each sub-task as a separate prompt or a clearly separated step within a prompt. The delegation must include the output specification and the completion criteria.

**Phase 3: Verify.** Check the output of each sub-task before proceeding. This is the → verification loop applied at the step level. Verification catches errors before they propagate to downstream steps, where they become harder to detect and more expensive to fix.

The loop is often recursive: a verification failure triggers a revision, which is itself a sub-task that may require decomposition and delegation. The recursion should have a depth limit. Two revision cycles is typical. Three is the maximum before → escalation to a different agent, a different approach, or a human.

A subtlety worth noting: the decompose-delegate-verify loop applies at every scale. It applies to a five-agent pipeline processing a hundred documents. It also applies to a single model call that breaks a reasoning task into three steps. The scale changes. The structure does not. If you find yourself designing a workflow and the structure is not decompose-delegate-verify, you are either working on something trivially simple or missing a step.

### Planning Prompts That Produce Plans

A common pattern is to use one model call to *plan* and subsequent calls to *execute*. The planning call is not solving the problem; it is producing the steps. The execution calls solve each step.

This separation has a non-obvious benefit: the plan itself is reviewable. Before any execution begins, a human or a verification agent can inspect the plan for completeness, correct sequencing, and missing steps. This is cheaper than executing a bad plan and discovering the gaps in the output.

A planning prompt needs three things:

1. **The goal**, stated with enough → specificity that the model knows what "done" looks like.
2. **The constraints on the plan itself**: how many steps, what resources are available, what format the plan should take.
3. **A template for each step**: what information each step must include (task description, input, expected output, completion criteria, dependencies).

```
Given the following goal, produce an execution plan.
Do not execute the plan. Only produce the steps.

Goal: [stated goal with success criteria]

For each step, provide:
- Step number and name
- Input: what this step receives (from prior steps or external sources)
- Task: what this step must accomplish
- Output: what this step produces, in what format
- Completion criteria: how to verify the step succeeded
- Dependencies: which prior steps must complete before this one begins
- Estimated complexity: LOW / MEDIUM / HIGH

Constraints on the plan:
- Maximum 7 steps. If the task requires more, group related sub-tasks.
- Every step must have at least one verifiable completion criterion.
- The final step must produce the deliverable described in the goal.
- If any step requires external data not available in the provided context,
  flag it as [EXTERNAL DEPENDENCY] and describe what is needed.
```

The output of this prompt is not a solution. It is a blueprint that can be inspected, revised, and then executed step by step. This is the → planner-executor split made explicit.

Two common failures in planning prompts: the plan that is too coarse (each step is itself a complex task that needs further decomposition) and the plan that is too fine (twenty micro-steps that could have been three). The diagnostic for coarseness: can you write a clear delegation for each step? If a step requires a paragraph to explain, it is not decomposed enough. The diagnostic for fineness: are any steps so simple that verifying them takes longer than executing them? If so, merge them.

A non-obvious benefit of separating planning from execution: plans compose across sessions. A plan produced on Monday can be executed on Tuesday by a different set of agents, a different model, or a different human operator. The plan is a portable artifact. The execution is contextual. This separation makes multi-step work reproducible in a way that ad-hoc prompting never is.

### The Plan-Execute-Verify-Revise Cycle

In practice, multi-step work follows a four-phase cycle, not a three-phase one. The addition is revision — the step where verification feedback is incorporated before moving forward.

**Plan.** Produce the steps. Review the plan (human or automated). Adjust if necessary.

**Execute.** Run step 1. Produce the output.

**Verify.** Check the output against the step's completion criteria. If it passes, proceed to step 2. If it fails, enter the revision phase.

**Revise.** Feed the verification feedback to the executor and re-run the step. Cap at two revisions. If the step still fails after two revisions, escalate.

The cycle repeats for each step. The full workflow looks like this:

```
Plan → [Review Plan] →
  Execute Step 1 → Verify → (Pass → Execute Step 2) or (Fail → Revise → Re-verify) →
  Execute Step 2 → Verify → (Pass → Execute Step 3) or (Fail → Revise → Re-verify) →
  ...
  Execute Step N → Verify → Final Output
```

The verification at each step is not optional overhead. It is load-bearing structure. Without it, errors in step 1 become assumptions in step 2, which become premises in step 3, which become conclusions in the final output. By the time a human reads the result, the original error is buried under three layers of confident-sounding analysis. The verification loop keeps each layer honest.

### Worked Example 1: Research Pipeline

**Goal:** Produce a 2,000-word briefing on the current state of battery recycling technology for a clean-energy investment fund.

**Plan (produced by a planning prompt):**

Step 1 — Source Collection
- Input: Topic description + recency requirement (2024-2026)
- Task: Identify 8-12 high-quality sources (peer-reviewed papers, industry reports, regulatory documents)
- Output: Source list as JSON with title, author, date, URL, relevance_score
- Completion: All sources published after January 2024. At least 3 peer-reviewed.
- Dependencies: None

Step 2 — Source Extraction
- Input: Source list from Step 1 + full text of each source
- Task: For each source, extract key claims relevant to the briefing topic
- Output: Claims table with source_id, claim_text, evidence_type, page_reference
- Completion: At least 2 claims per source. Every claim includes a page reference.
- Dependencies: Step 1

Step 3 — Claim Verification
- Input: Claims table from Step 2
- Task: Cross-reference claims across sources. Flag contradictions. Mark consensus claims.
- Output: Verified claims table with consensus_status (AGREED / DISPUTED / SINGULAR)
- Completion: Every claim has a consensus status. All contradictions have both sides cited.
- Dependencies: Step 2

Step 4 — Synthesis and Drafting
- Input: Verified claims table from Step 3 + audience specification (investment fund)
- Task: Write a 2,000-word briefing structured as: Executive Summary (200 words), Technology Overview (600 words), Market Landscape (500 words), Investment Implications (500 words), Risks and Unknowns (200 words)
- Output: Markdown document with section headers
- Completion: All sections present. All factual claims traceable to the verified claims table. No claim marked DISPUTED presented as settled.
- Dependencies: Step 3

Step 5 — Editorial Review
- Input: Draft from Step 4
- Task: Check for internal consistency, unsupported claims, and adherence to the audience register
- Output: Reviewed draft with inline comments + acceptance status
- Completion: Zero unsupported claims. Register consistent throughout.
- Dependencies: Step 4

Each step has a clear input, output, and verification criterion. The plan is executable by five separate agents or by one model in five sequential prompts. The structure is the same either way.

Notice the dependency chain: each step consumes the previous step's output, but no step requires jumping back three stages. This is a linear pipeline, the simplest multi-step topology. More complex workflows allow branching (steps 2a and 2b execute in parallel and merge at step 3) or looping (step 3 sends failures back to step 2 for revision). The planning prompt should capture these topologies explicitly. A plan that says "step 3 depends on steps 2a and 2b" is clearer than one where the dependency is implied.

### Worked Example 2: Document Creation Pipeline

**Goal:** Produce an API reference document for a new REST API, starting from an OpenAPI specification.

**Plan:**

Step 1 — Spec Parsing
- Input: OpenAPI spec (JSON)
- Task: Extract all endpoints, methods, parameters, request/response schemas, and error codes
- Output: Structured JSON with one object per endpoint
- Completion: Every endpoint in the spec appears in the output. No endpoints invented.
- Dependencies: None

Step 2 — Endpoint Drafting
- Input: Structured JSON from Step 1 + documentation style guide
- Task: For each endpoint, write: description (2-3 sentences), parameters table, request example, response example, error codes table
- Output: One markdown file per endpoint
- Completion: All files follow the style guide. Every parameter from the spec is documented. Every example is syntactically valid.
- Dependencies: Step 1

Step 3 — Cross-Reference Check
- Input: All endpoint files from Step 2 + original spec
- Task: Verify that every parameter, schema, and error code in the spec appears in the docs. Identify any gaps.
- Output: Coverage report (JSON) listing covered and uncovered items
- Completion: Coverage report is complete. Any gaps are flagged with the specific spec location.
- Dependencies: Step 2

Step 4 — Gap Remediation
- Input: Coverage report from Step 3 + endpoint files from Step 2
- Task: Fill documented gaps. If a gap cannot be filled due to missing spec information, mark as [SPEC_GAP: item_name]
- Output: Updated endpoint files + gap report
- Completion: Coverage at 100% or all remaining gaps are marked SPEC_GAP.
- Dependencies: Step 3

Step 5 — Final Assembly
- Input: All updated endpoint files + navigation template
- Task: Assemble into a single navigable document with table of contents, consistent cross-links, and an index
- Output: Complete API reference document (markdown)
- Completion: Table of contents matches document structure. All cross-links resolve. All endpoints accessible from the index.
- Dependencies: Step 4

The pattern is consistent: each step produces a defined artifact, each artifact is verifiable, and each verification happens before the next step consumes the artifact. The pipeline does not trust any single step's output. It checks, then proceeds.

A design choice embedded in this example: Step 3 (Cross-Reference Check) is a pure verification step that produces no new content — only a coverage report. This is deliberate. The temptation is to combine verification with gap remediation: "check for gaps and fill them in the same pass." Resist it. A step that both identifies problems and fixes them has no independent check on whether the fixes are correct. Separating detection (Step 3) from remediation (Step 4) allows the pipeline to verify the remediation itself. The cost is one additional step. The payoff is that you know when the docs are complete, rather than hoping.

### When to Use Multi-Step Patterns

Multi-step planning is not free. Each step consumes tokens, adds latency, and introduces handoff complexity. The pattern pays for itself when:

- The task genuinely requires multiple distinct operations (research, then analysis, then writing)
- Intermediate outputs need verification before downstream steps consume them
- Different steps benefit from different → framing or different model capabilities
- A single monolithic prompt has already produced mediocre results
- The final output must be traceable to its sources through the intermediate steps

It does not pay when the task is simple enough for one pass, when latency is the binding constraint and accuracy is flexible, or when the overhead of planning exceeds the complexity of the task. Do not decompose a one-step problem into five steps. That is not rigorous planning. It is procrastination with structure.

---

## Chapter 3: Retrieval and Extraction Patterns

Most production LLM applications do not ask models to generate from memory. They provide source material and ask models to work with it. This is → grounding industrialized: the model becomes a reader, extractor, and synthesizer rather than a novelist.

The challenge is not getting the model to read. It is getting the model to read *accurately* — to extract what is there, cite where it found it, and refrain from adding what is not. This chapter covers the patterns that make retrieval and extraction reliable.

### The Grounding Stack

Reliable retrieval prompts stack three abstractions:

**→ Grounding** provides the source material. The model's answers come from what you provide, not from parametric memory. The instruction must be explicit: "Answer based only on the following documents" is a directive, not a suggestion. Without it, the model will silently supplement your sources with its training data, and you will not know which claims are grounded and which are generated.

**→ Source anchoring** ties each claim to a specific location in the source material. This means instructing the model to cite document names, section numbers, page numbers, or paragraph indices for every factual claim. Source anchoring serves two purposes: it enables verification (you can check the citation), and it changes the model's generation strategy (a model that must cite is less likely to fabricate, because fabricated claims have no source to cite).

**→ Retrieval scaffolding** structures the relationship between the query and the source material. In a RAG system, this means the retrieval step — how chunks are selected, ranked, and presented to the model. In a manual prompt, this means organizing the source material so the model can navigate it: clear section headers, labeled documents, explicit markers for where one source ends and another begins.

These three form a stack. Grounding without anchoring produces answers that are probably based on the sources but cannot be verified. Anchoring without grounding asks the model to cite sources it does not have (→ hallucination bait). Scaffolding without grounding organizes nothing. The stack works together or not at all.

The practical implication: when building a retrieval-based system, start with grounding (do I have the sources?), then add anchoring (can the model cite them?), then add scaffolding (can the model navigate them efficiently?). Each layer depends on the one below it. Skipping a layer does not save time. It creates a gap that manifests as unreliable output.

### Structuring RAG Prompts

Retrieval-Augmented Generation is the dominant architecture for knowledge-grounded applications, and it is also the architecture most likely to hallucinate when poorly prompted. Sahoo et al. (2025) document RAG as a major development in prompt-based systems, noting that it addresses the core limitation of static training data by providing models with dynamic context at inference time [src_paper_sahoo2025]. But the architecture is only as reliable as the prompt that sits between the retrieved chunks and the generated output.

A well-structured RAG prompt has four components:

**1. Source boundary instruction.** Tell the model that its answer must come from the provided context, and define what to do when the context is insufficient.

```
Answer the user's question using ONLY the information in the
CONTEXT section below. If the context does not contain enough
information to answer fully, say what you can answer and
explicitly state what information is missing.
Do not supplement with general knowledge.
```

**2. Source material with clear labels.** Each retrieved chunk should be labeled with a source identifier. The model cannot cite what it cannot name.

```
CONTEXT:
[Source: annual_report_2025.pdf, Section 3.2, pp. 14-16]
Revenue grew 12% year-over-year, driven primarily by...

[Source: earnings_call_transcript_Q3.txt, Speaker: CFO]
We expect continued growth in the enterprise segment, though...

[Source: analyst_report_morgan_stanley.pdf, p. 7]
The company's growth rate trails the sector average by...
```

**3. Citation requirement.** Instruct the model to cite its sources inline.

```
For every factual claim in your answer, cite the source using
the format [Source: filename, location]. If a claim synthesizes
across multiple sources, cite all relevant sources.
```

**4. Conflict handling.** Sources disagree. The prompt must tell the model what to do when they do.

```
If two sources contradict each other, present both positions
with their respective citations. Do not resolve the contradiction
by choosing one source over the other unless you have explicit
basis for the preference (e.g., one source is more recent).
```

**5. Fallback behavior.** The retrieved chunks may not contain the answer. The prompt must define what happens when grounding fails.

```
If the CONTEXT section does not contain information relevant to
the question, respond with: "The provided sources do not contain
sufficient information to answer this question. The following
related information was found: [summary of closest relevant content]."
Do not answer from general knowledge. An honest gap is better
than a confident fabrication.
```

This five-component structure is not decorative. Each component addresses a specific failure mode that appears in production RAG systems: ungrounded generation, unlabeled sources, uncited claims, unresolved conflicts, and unanswered questions. Remove any component and the corresponding failure mode reappears.

### Extraction Schemas

Extraction is the most structured form of retrieval: the model reads a source and fills in a defined schema. The schema is the → constraint that makes extraction predictable.

A well-formed extraction prompt provides:

- The source material
- The exact fields to extract, with data types and allowed values
- Instructions for missing or ambiguous values
- The output format (JSON, table, or structured text)

```
From the attached contract, extract the following fields:

{
  "party_a": "string — full legal name of the first party",
  "party_b": "string — full legal name of the second party",
  "effective_date": "ISO date — when the contract takes effect",
  "termination_date": "ISO date or null if no fixed termination",
  "auto_renewal": "boolean — true if the contract auto-renews",
  "renewal_notice_period_days": "integer or null",
  "total_value": "number in USD or null if not specified",
  "governing_law": "string — jurisdiction"
}

Rules:
- If a field is not present in the contract, set it to null.
  Do not infer values.
- If a field is ambiguous (e.g., two possible effective dates),
  extract both in an array and add an "ambiguity_note" field
  explaining the conflict.
- Return valid JSON only. No additional text outside the JSON object.
```

The schema does what → specificity alone cannot: it defines not just what to look for but exactly how to represent what is found. The model does not decide the field names, the data types, or the handling of edge cases. The prompt decides all of that. The model's job is reduced to reading and mapping — a task models do well when the mapping is explicit.

Two design principles for extraction schemas. First, make null an explicit option for every field. A model forced to populate a required field with no data will invent data. A model allowed to return null will return null. The difference between a missing value and a fabricated one is the difference between a gap in a report and a lie in a report. Second, handle ambiguity explicitly. Real documents are ambiguous. A contract may list two effective dates. A resume may name a role without dates. The schema should define what the model does in those cases, because if you do not define it, the model will make a choice — and you will not know which choice it made or why.

Sahoo et al. (2025) note that reformulating natural language tasks into structured code-like formats can produce substantial accuracy gains — GPT-3.5 achieved an 8.42 F1 score improvement by treating NLP tasks as structured extraction problems [src_paper_sahoo2025]. The lesson generalizes: the more structure you provide in the extraction target, the less room the model has to deviate.

### When Retrieval Fails

Retrieval patterns fail in predictable ways:

**Chunk boundary errors.** The relevant information spans two retrieved chunks, but the model only sees one. The answer is technically grounded — it cites a real source — but it is incomplete because the source was truncated by the chunking strategy. This is the retrieval equivalent of answering a question after reading half a paragraph. The information was there. The retrieval system cut it in half. Fix: overlap chunks (each chunk shares some text with its neighbors), use larger retrieval windows for questions likely to require cross-section reasoning, or retrieve parent documents alongside matching chunks.

**Retrieval silence.** The answer is not in the retrieved chunks. A well-prompted model will say so. A poorly prompted model will answer from parametric memory and present it as if it came from the sources. Fix: the source boundary instruction must include an explicit "if not found" pathway.

**Citation fabrication.** The model cites a source, but the cited claim does not appear in the cited location. This is subtler than outright hallucination. The source is real. The claim might even be true. But the citation — the specific link between claim and evidence — is fabricated. The model decided that the claim was probably in the source and generated a plausible-looking reference. Fix: verification. A downstream step (or a human) checks each citation against the actual source text. In production systems, this check can be automated for structured extractions by comparing extracted values against the source text programmatically. For free-form answers, automated verification is harder but still possible: extract the cited passage, retrieve the original source chunk, and check for semantic overlap.

**Source contamination.** The retrieved chunks contain outdated or incorrect information. The model faithfully extracts and presents it. The output is grounded but wrong. Grounding does not guarantee truth. It guarantees traceability. The quality of the output is bounded by the quality of the sources. Fix: source quality control is a separate concern from prompt design, but the prompt can help by including recency metadata and instructing the model to flag outdated sources.

**Over-reliance on retrieval.** The question requires synthesis across multiple sources, but the model treats each retrieved chunk independently and produces a list of fragments instead of a coherent answer. The retrieval was fine. The synthesis instruction was missing. Fix: explicitly instruct the model to synthesize across sources after extracting from each. "After reviewing all sources, provide a unified answer that integrates the findings. Note where sources agree, where they disagree, and where gaps remain."

These failure modes are not edge cases. They are the norm in production systems that skip the grounding stack or implement it partially. The retrieval pipeline is only as reliable as the prompt that governs how retrieved content is used.

---

## Chapter 4: Critique, Rewrite, and Evaluation Patterns

A single generation pass through a language model is a first draft. Treating it as a finished product is a design error. The patterns in this chapter all share one principle: generate first, then improve.

This is not a novel idea. Writers revise. Engineers test. Scientists replicate. The novelty is that the same model that generates the draft can also critique it — imperfectly, but usefully — and that this loop can be formalized into a reproducible pattern.

### The Self-Refine Loop

The most direct improvement pattern is generate → critique → revise, formalized by Madaan et al. (2023) as Self-Refine. The model produces an initial output, then critiques its own output against specified criteria, then revises based on the critique. The cycle repeats until the output meets a stopping condition or a maximum iteration count is reached.

Self-Refine improved GPT-4 performance by 8.7 points in code optimization and 21.6 points in sentiment reversal [src_paper_sahoo2025]. The gains are large because they exploit an asymmetry: models are better critics than creators. A model that produces a mediocre first draft can often identify the mediocrity when prompted to look for it, and can then produce a superior revision.

The implementation requires three distinct prompts (or three sections of one prompt):

**Generation prompt:** Produce the initial output. No special instructions needed beyond the task specification.

**Critique prompt:** Review the output against specific criteria. The criteria must be concrete. "Is this good?" is not a critique prompt. "Does every paragraph contain a topic sentence? Does the conclusion follow from the evidence presented? Are there any claims without supporting data?" is.

**Revision prompt:** Given the original output and the critique, produce a revised version that addresses the identified issues without introducing new ones.

The key insight is that the critique prompt must use a different → framing than the generation prompt. A model that generates and then critiques using the same frame will rubber-stamp its own work. The generation frame says "produce." The critique frame says "find problems." These are distinct cognitive modes, and the model must be explicitly switched between them.

```
[Step 1 — Generate]
Write a 500-word executive summary of the attached report,
focused on investment implications for institutional investors.

[Step 2 — Critique]
Review the executive summary you just wrote. Check:
1. Does every investment implication cite a specific data point
   from the report?
2. Are there any qualitative claims ("strong growth," "significant
   risk") without quantitative support?
3. Is the summary under 500 words?
4. Does the tone match an institutional investor audience
   (not retail, not academic)?
List every issue found.

[Step 3 — Revise]
Revise the executive summary to address every issue identified
in your critique. Do not add new content that was not in the
original report. If an issue cannot be fixed without additional
data, mark it as [NEEDS DATA] and leave the passage unchanged.
```

Diminishing returns set in quickly. The first revision cycle produces the largest gains. The second cycle catches residual issues. By the third cycle, the model is typically making lateral moves — different but not better — or introducing new problems while fixing old ones. Cap the loop at two to three iterations.

The Self-Refine pattern has a structural prerequisite that is easy to overlook: the critique criteria must be things the model can actually evaluate. A model can check whether every claim cites a source (verifiable). It can check whether the word count is under 500 (countable). It cannot reliably check whether an argument is persuasive to a specific audience (subjective and ungrounded). Match the critique criteria to the model's verification capabilities. If the criteria require human judgment, the self-refine loop should produce a draft-plus-critique for human review, not a self-approved final output.

Chain-of-Verification (CoVe), introduced by Dhuliawala et al. (2023), applies a more aggressive version of this pattern specifically targeting hallucination. After generating a response, the model generates verification questions about its own claims, answers those questions independently — deliberately isolating them from the original generation context to avoid confirmation bias — and revises any claims that fail [src_paper_sahoo2025]. CoVe treats the model's first output as testimony to be cross-examined, not as a product to be polished.

### Rubric-Driven Evaluation

When evaluation needs to be consistent across multiple outputs — grading student work, scoring proposals, comparing model responses — a free-form critique is not enough. The evaluation needs a → rubric: an explicit scoring framework with defined dimensions and defined levels.

A rubric-driven evaluation prompt has three components:

**1. The rubric itself.** A table or list of evaluation dimensions, each with defined scoring levels.

```
Evaluate the following response on these dimensions:

ACCURACY (1-5)
1: Multiple factual errors. 2: One significant error. 3: No errors,
but some claims unverified. 4: All claims accurate and sourced.
5: Accurate, sourced, and includes relevant caveats.

COMPLETENESS (1-5)
1: Addresses less than half the question. 2: Addresses the main
point but misses key sub-questions. 3: Addresses all sub-questions
at surface level. 4: Addresses all sub-questions with depth.
5: Comprehensive, including considerations the question did not
explicitly ask about.

CLARITY (1-5)
1: Disorganized, hard to follow. 2: Organized but verbose or vague.
3: Clear and concise. 4: Clear, concise, and well-structured.
5: Exceptionally clear, with effective use of examples or analogies.
```

**2. The output format.** The model should produce a structured evaluation, not a paragraph of impressions.

```
For each dimension, provide:
- Score (1-5)
- One-sentence justification
- One specific quote or passage from the response that supports
  your score

Then provide an overall score (average, rounded to one decimal)
and a single paragraph of synthesis.
```

**3. Calibration instructions.** Without calibration, models default to generous scoring. An evaluation prompt must explicitly counteract this.

```
Scoring norms: A score of 3 is adequate — the response does its job.
A 4 requires genuine quality. A 5 is exceptional and rare.
Do not give a 5 unless you can articulate specifically what makes
the response exceptional, not just good. The median score across
typical responses should be approximately 3.
```

The rubric makes evaluation reproducible. Two different runs of the same evaluation prompt, on the same response, should produce similar scores. Without the rubric, evaluation is impressionistic and varies with the model's mood (which is to say, with the randomness of sampling).

### Peer Review Patterns

The most powerful critique pattern uses two agents: one that produces, one that critiques. The critique is then fed back to the producer for revision. This addresses the rubber-stamp problem directly: the critic is a different agent (or at minimum, a different prompt with a different frame) and has no investment in defending the original output.

```
Agent 1 — Writer
System: You are a technical writer. Produce a clear, accurate
explanation of [topic] for [audience].

Agent 2 — Reviewer
System: You are a technical editor. Your job is to find every
weakness in the text you receive. You are not the author's friend.
You are the audience's advocate.

Review the text for:
- Factual errors or unsupported claims
- Unclear or ambiguous passages
- Missing information that the audience would need
- Structural problems (logical gaps, poor sequencing)
- Register mismatches (too technical, too casual, inconsistent)

For each issue, provide:
- Location (quote the problematic passage)
- Problem (what is wrong)
- Severity (CRITICAL / MAJOR / MINOR)
- Suggested fix (specific, not vague)

Agent 1 — Revision
System: You are the technical writer. You have received editorial
feedback. Revise your text to address all CRITICAL and MAJOR issues.
For MINOR issues, address them if the fix is straightforward.
If you disagree with a critique, explain why in a [NOTE TO EDITOR]
comment and retain your original text.
```

This pattern works because it exploits the framing asymmetry. The writer frame optimizes for production. The editor frame optimizes for quality. Neither frame alone produces the best output. Together, they approach the quality of a human writer-editor cycle — not matching it, but closing the gap enough to be useful.

A practical detail: the reviewer agent should not have access to the writer's instructions. If the reviewer knows what the writer was trying to do, it evaluates the output charitably — "well, given those constraints, this is reasonable." If the reviewer only sees the output and the audience specification, it evaluates the output on its own terms — "is this clear, accurate, and complete for the intended reader?" This informational asymmetry makes the review more honest.

Wang et al.'s self-consistency technique takes a different approach to the same problem: instead of critique and revision, it generates multiple independent outputs and selects the answer that appears most frequently. Self-consistency improved GSM8K accuracy by 17.9% over standard chain-of-thought [src_paper_sahoo2025]. The mechanism is different — voting rather than critique — but the principle is the same: a single generation is unreliable; redundancy, whether through critique or through diversity, improves reliability.

### When Critique Fails

Critique patterns fail when:

**The criteria are vague.** "Check if this is good" is not a critique prompt. The model will produce agreeable, non-specific feedback. Concrete criteria produce concrete critique.

**The critic and producer share a frame.** A model asked to "write a summary, then check if the summary is good" is evaluating its own work from the same perspective that produced it. The fix is to switch frames between generation and critique — change the role, the criteria, or the evaluation angle.

**The revision introduces new errors.** Each revision cycle can fix old problems and create new ones. The model is not monotonically improving; it is rewriting, and rewrites have their own failure modes. Cap iterations and verify the final output independently.

**Sycophantic evaluation.** A model evaluating another model's output may be biased toward approval (→ sycophancy). Anti-sycophancy instructions in the evaluation prompt ("identify at least two weaknesses," "do not give a perfect score unless you can justify it specifically") partially counteract this tendency.

---

## Chapter 5: Agent Instruction Design

Writing a prompt is programming a model for a single task. Writing a system prompt for an agent is programming a model for a role — a sustained identity with defined capabilities, boundaries, and behaviors that persist across many tasks. The difference is architectural. A prompt is a function. An agent instruction is a class definition.

This chapter covers the patterns for designing agent instructions that are precise enough to guide behavior, bounded enough to prevent scope creep, and complete enough that the agent can operate without continuous human supervision.

### The Three Agent Primitives

Agent behavior in multi-agent systems is governed by three operations. Every other agent behavior is a composition of these three.

**→ Delegation.** The act of assigning a bounded task to another agent. Delegation defines what the receiving agent must produce, in what format, by what criteria. It is the outbound operation: work flows away from the delegator.

**→ Handoff.** The act of transferring control from one agent to another, along with the context the receiving agent needs to continue. Handoff defines what state is passed, what state is not, and what the receiving agent should do next. It is the transition operation: control flows from one agent to the next.

**→ Escalation.** The act of routing a problem upward when the current agent cannot resolve it. Escalation defines when to give up, what to include in the escalation message, and who receives it. It is the exception operation: problems flow upward toward greater capability or human judgment.

These three primitives appear in every multi-agent system, regardless of the framework. OpenAI's Agents SDK implements them as handoff objects and tool definitions. LangGraph implements them as conditional graph edges and state transitions. CrewAI implements them as Task objects with agent assignments. The abstraction is universal. The implementation varies.

An agent without delegation cannot distribute work. An agent without handoff cannot participate in a pipeline. An agent without escalation cannot fail safely. A well-designed agent has all three, with explicit instructions for each.

The three primitives also explain most agent failures. An agent that produces off-target work usually has a delegation problem (the task was not specified clearly enough). An agent that loses context between stages has a handoff problem (the state transfer was incomplete or poorly structured). An agent that hallucinates instead of admitting failure has an escalation problem (it was never told that "I cannot do this" is a valid output). When debugging a pipeline, start by asking which primitive is broken.

### Writing System Prompts for Pipeline Agents

A system prompt for a pipeline agent is not a personality description. It is an operational specification. It must answer six questions:

**1. What is this agent's purpose?** One sentence. Not a paragraph. Not a mission statement. A function signature in natural language.

```
You are the Claim Extraction Agent. You read source documents
and produce a structured list of factual claims with citations.
```

**2. What does this agent receive?** Define the input format. An agent that does not know what its input looks like will misinterpret it.

```
You receive: a JSON array of source documents, each with fields
{source_id, title, text, date_published}.
```

**3. What does this agent produce?** Define the output format. An agent that does not know what its output should look like will improvise, and improvisation in a pipeline breaks downstream consumers.

```
You produce: a JSON array of claims, each with fields
{claim_id, claim_text, source_id, evidence_span, confidence}.
```

**4. What are the rules?** Define the constraints. What the agent must do, must not do, and how to handle edge cases.

```
Rules:
- Extract only factual claims (statements that can be verified
  as true or false). Exclude opinions, predictions, and hedged
  statements.
- Every claim must include the exact quote (evidence_span) from
  the source that supports it.
- If a claim appears in multiple sources, create one entry and
  list all source_ids.
- confidence must be HIGH (claim is directly stated), MEDIUM
  (claim is implied by context), or LOW (claim requires inference).
  Do not extract LOW-confidence claims unless the source count ≥ 2.
```

**5. When does this agent stop?** Define the completion criteria. An agent without completion criteria will either stop too early or run forever.

```
Completion: You have processed every document in the input array.
Every extracted claim has all required fields populated.
The output JSON is valid and parseable.
```

**6. When does this agent escalate?** Define the failure conditions and escalation targets.

```
Escalation:
- If a document is not in English, skip it and include an error
  entry: {source_id, error: "UNSUPPORTED_LANGUAGE", language: "detected_language"}
- If a document's text field is empty or unparseable, skip it and
  include: {source_id, error: "UNPARSEABLE_CONTENT"}
- If more than 30% of documents trigger errors, stop processing
  and escalate to the Pipeline Controller with the error summary.
```

These six questions compose the complete operational specification for a pipeline agent. A system prompt that answers all six produces an agent that knows what it does, what it works with, what it produces, how it behaves, when it is done, and when it should ask for help.

A common mistake: writing system prompts that describe who the agent *is* without specifying what the agent *does*. "You are an experienced financial analyst with deep knowledge of emerging markets" is a personality sketch, not an operational specification. It sets a → framing (which is useful) but omits the task, the input format, the output format, the constraints, the completion criteria, and the escalation rules (which are necessary). Personality without specification produces an agent that sounds competent and does unpredictable things.

The six questions are ordered deliberately. Purpose comes first because everything else depends on it. Input and output come second because they define the interface — what connects this agent to the rest of the pipeline. Rules come third because they constrain behavior within the interface. Completion and escalation come last because they define the exit conditions. This order mirrors how a software engineer would specify a function: signature, then body, then error handling.

### Authority Boundaries and Tool Constraints

The most dangerous prompt for an agent is one that gives it a task and tools without bounding its authority. An agent told to "research competitors" with access to a web browser, a database, and an email tool might browse competitive websites (intended), query your customer database for competitive intel (questionable), and email a competitor's public relations department with questions (catastrophic). The agent was not malicious. It was creative. The prompt did not say what it could not do.

Authority boundaries define three scopes:

**Data access.** What sources the agent may read. "You may read documents in the /sources/ directory. You may not access the customer database, the financial system, or any external URL not in the approved list."

**Tool use.** What tools the agent may invoke. "You may use the search tool and the extraction tool. You may not use the email tool, the database write tool, or the deployment tool." Listing allowed tools is safer than listing prohibited ones, because the list of possible misuses is always longer than the list of intended uses.

**Scope of action.** What changes the agent may make to the world. The distinction between read-only and read-write is the most fundamental authority boundary. An agent that can only read and produce text is inherently safer than one that can write to databases, send messages, or execute code. When an agent must have write access, the scope should be as narrow as possible: "You may write to the /drafts/ directory. You may not write anywhere else."

Authority boundaries interact with → delegation in a non-obvious way. When Agent A delegates to Agent B, Agent B's authority should be *narrower* than Agent A's, not equal. If Agent A has write access to the database and delegates a research task to Agent B, Agent B should receive read-only access. Authority should narrow at each delegation level, not propagate unchanged. This is the principle of least privilege, borrowed from security engineering and equally applicable to agent design.

The failure to bound authority is not theoretical. In multi-agent systems with tool access, authority leaks are one of the most common sources of unintended behavior. An agent tasked with "update the customer record" that has unrestricted database access may update the wrong record, update additional fields beyond what was intended, or trigger cascading updates through foreign key relationships. The fix is not smarter agents. It is narrower permissions.

### The DEHVAC Pattern

The six questions from the system prompt section can be compressed into a mnemonic for agent instruction design: **DEHVAC**.

**D — Deliverable.** What the agent produces. The output specification: format, schema, content requirements. A prompt without a defined deliverable produces whatever the model finds most probable.

**E — Escalation.** When the agent stops trying and routes upward. The failure conditions, escalation targets, and context that must accompany the escalation. A prompt without escalation rules produces an agent that never admits failure — it either loops, hallucinates, or silently returns incomplete work.

**H — Handoff.** How the agent transfers control and context to the next agent. What state is passed, what is discarded, what format the handoff takes. A prompt without handoff instructions produces an agent that dumps its entire context into the next agent's input, consuming → context budget on irrelevant material.

**V — Verification.** How the agent checks its own work before declaring completion. The self-check criteria, the acceptance threshold, and the revision protocol. A prompt without verification instructions produces an agent that submits first drafts as final work.

**A — Authority.** What the agent may and may not do. Tool access, data access, scope of action. A prompt without authority boundaries produces an agent that interprets its mandate as broadly as possible — which is how agents end up sending emails, modifying databases, or browsing websites they should not visit.

**C — Constraints.** The rules that govern the agent's behavior independent of any specific task. Token limits, response time expectations, formatting requirements, prohibited actions. A prompt without constraints produces an agent that optimizes for whatever dimension the model's training most rewards, which is usually helpfulness at the expense of precision.

DEHVAC is not a formula to fill in mechanically. It is a checklist for completeness. When an agent misbehaves, check which letter is missing. The misbehavior almost always maps to an unspecified dimension. An agent that produces the wrong format has a Deliverable problem. An agent that runs forever has a Verification problem (no stopping criterion). An agent that uses unauthorized tools has an Authority problem. An agent that hallucinates instead of failing has an Escalation problem. The diagnostic is fast because the checklist is short.

A full DEHVAC specification for a pipeline agent:

```
Agent: Literature Review Analyst
Pipeline position: Step 2 of 5 (after Source Collection, before Synthesis)

D — Deliverable:
A JSON array of annotated claims extracted from the provided sources.
Each claim: {claim_id, text, source_id, page, confidence, consensus_status}.

E — Escalation:
- If fewer than 5 sources are provided, escalate to Source Collector
  with a request for additional sources on [topic].
- If > 40% of sources are behind paywalls or inaccessible, escalate
  to Pipeline Controller with an access report.
- Maximum 2 self-revision cycles. If verification still fails
  after 2 revisions, escalate with the failure report.

H — Handoff:
Pass the claims JSON + a one-paragraph summary of the source
landscape (how many sources, date range, key themes) to the
Synthesis Agent. Do not pass raw source text — only extracted claims.

V — Verification:
Before handoff, check:
- Every claim has a non-null source_id and page reference
- No two claims are duplicates (same text, different claim_ids)
- confidence distribution is not > 80% HIGH (over-confidence signal)
- Valid JSON, parseable by standard JSON parser

A — Authority:
- You may read source documents provided in the input
- You may NOT access external URLs, databases, or APIs
- You may NOT modify the source documents
- You may NOT extract claims from sources not in the input array

C — Constraints:
- Maximum output: 100 claims. If more are available, prioritize by
  confidence and consensus_status (AGREED > DISPUTED > SINGULAR).
- Each claim_text must be under 50 words. If a claim requires more,
  split it into atomic sub-claims.
- Processing time target: complete within 60 seconds of input receipt.
```

This specification leaves almost nothing to interpretation. The agent knows its deliverable, its failure modes, its handoff protocol, its quality standards, its boundaries, and its operational constraints. The probability of the agent doing something unexpected is proportional to the specificity gaps in the specification. DEHVAC's job is to close those gaps.

---

## Chapter 6: Prompt Anti-Patterns

Every chapter so far has described what to do. This chapter describes what not to do — the ten most common prompt failures, each named, explained, and connected to the abstractions from Part II that fix it.

Anti-patterns are not random mistakes. They are systematic errors that recur because they feel natural. A vague delegation feels like giving someone latitude. An unconstrained generation feels like creative freedom. Verification theater feels like diligence. Each anti-pattern has a surface logic that makes it persist. Understanding why the anti-pattern feels right is the first step toward not doing it.

### 1. Vague Delegation

**The pattern:** Assigning a task without specifying the deliverable, format, or completion criteria. "Research this topic." "Analyze the data." "Write something about X."

**Why it fails:** The model interprets the task using its training distribution, which averages across millions of possible interpretations. The result is the median of what "analyze" could mean — a generic overview that is too shallow for experts and too broad for any specific purpose. Every unspecified dimension is resolved by probability, not by intent.

**The fix:** → Specificity, → delegation. Name the deliverable. Define the format. State the completion criteria. "Research this topic" becomes "Identify 8 peer-reviewed papers published after 2024 on [topic], extract the primary finding from each, and return as a JSON array with fields: title, authors, year, finding, DOI."

### 2. Unconstrained Generation

**The pattern:** Asking the model to produce output without bounding length, format, scope, or exclusions. "Tell me everything about X." "Write a comprehensive report." "Give me all the information you have."

**Why it fails:** Without constraints, the model optimizes for the dimension it was most rewarded for in training: apparent helpfulness. This produces verbose, broadly scoped outputs that cover everything and commit to nothing. The user drowns in information that they must sort, filter, and prioritize — the work the prompt should have done.

**The fix:** → Constraint, → scope. Set a word limit. Define the format. Name what to include and what to exclude. "Write a comprehensive report" becomes "Write a 1,500-word report covering these three areas: [A], [B], [C]. Exclude [D] — it will be covered separately. Output as markdown with section headers."

### 3. Hallucination Bait

**The pattern:** Asking for specific factual details — statistics, citations, dates, names — without providing source material and without giving the model an exit for uncertainty.

**Why it fails:** Models lack a reliable internal signal for "I don't know." When a prompt demands specifics, the model generates specifics. If the correct specifics are not confidently available in parametric memory, the model fabricates plausible alternatives. The output looks authoritative. It may be entirely invented. Asking "cite three studies that support this claim" without providing any studies is not a research instruction. It is a fabrication instruction.

**The fix:** → Grounding, → source anchoring. Provide the sources. Require citations to provided material only. Include an explicit uncertainty pathway: "If you cannot verify this from the provided sources, state that rather than estimating." See Chapter 3 for the full grounding stack.

### 4. Format-Only Specificity

**The pattern:** Specifying the output format in great detail while leaving the content criteria vague. "Return a JSON object with fields X, Y, Z" but no instruction on what should populate those fields, what quality bar applies, or how to handle ambiguous cases.

**Why it fails:** The model produces a perfectly formatted answer to the wrong question. The JSON is valid. The table is well-structured. The content is whatever the model deemed most probable, which may not be what you needed. Format specificity without content specificity is like mailing someone a beautifully addressed empty envelope.

**The fix:** → Specificity applied to content, not just format. For every format field, specify what belongs in it, what the quality criteria are, and what to do when the value is missing or ambiguous. "party_a: full legal name as it appears in the contract header. If two names appear, use the one in the signature block."

### 5. Sycophancy Enablement

**The pattern:** Prompts that implicitly reward agreement and penalize disagreement. "Review my business plan and give me feedback" (implicit: tell me it is good). "I think X is the best approach — do you agree?" (implicit: yes).

**Why it fails:** Models are trained on human feedback that systematically rewards agreement and punishes disagreement (→ sycophancy). A prompt that does not explicitly counteract this bias gets the default: validation disguised as evaluation. The model will find nice things to say about a bad plan because saying nice things is what it was trained to do.

**The fix:** → Framing with an adversarial role. "You are a critical evaluator. Lead with the most significant weakness. Identify at least three problems. Rate each by severity. If you cannot find problems, look harder — you are not being asked to validate." Mandate dissent explicitly, because the model's default is agreement.

### 6. Verification Theater

**The pattern:** Adding a verification step that checks trivial properties (format, word count, presence of expected sections) while ignoring the hard ones (factual accuracy, logical coherence, claim-source alignment).

**Why it fails:** The pipeline now has a quality gate that waves through bad content with a clean stamp. The verification step produces a sense of diligence without the substance. A report that is 500 words, has three sections, and uses the correct header formatting passes the check — even if the claims in the report are fabricated, contradictory, or unsupported.

**The fix:** → Verification loop with substantive criteria. Design verification criteria that target the failure modes you actually care about. If hallucination is the risk, verify that every claim cites a provided source. If logical coherence is the risk, check that conclusions follow from stated premises. The verification criteria should be harder to pass than the format requirements — not easier.

### 7. Register Mismatch

**The pattern:** Writing a prompt whose register (formality, vocabulary, assumed expertise) does not match the intended audience or the model's role.

**Why it fails:** A model told "you are a pediatric nurse explaining vaccination schedules to parents" but prompted with "elucidate the immunological rationale for the recommended prophylactic regimen" will produce output that satisfies the technical instruction while violating the role. The register of the prompt bleeds into the register of the output. If you prompt formally, the model responds formally, even when its role demands simplicity.

**The fix:** → Register, → audience specification. Match the prompt's language to the desired output's language. If the output should be plain-spoken, the prompt should be too. "Explain the vaccination schedule to a parent. Use short sentences. Avoid medical jargon. If a medical term is necessary, define it in simple words."

### 8. Overcompression

**The pattern:** Trying to fit too many instructions, constraints, and requirements into a single prompt, producing a wall of text that the model partially ignores.

**Why it fails:** Attention is finite. A prompt with fifteen constraints is not fifteen times more constrained than a prompt with one. Beyond a certain density, the model begins dropping requirements — typically the ones in the middle of the list, consistent with known primacy and recency effects in attention mechanisms. The prompt writer has the illusion of precision. The model sees a buffet and picks favorites.

**The fix:** → Decomposition. If a task requires fifteen constraints, it probably requires three steps of five constraints each. Break the task into stages. Each stage gets a focused prompt with a manageable number of requirements. The total constraint count is the same. The effective constraint count — the number the model actually honors — is higher.

### 9. Prompt Drift

**The pattern:** Using a long, multi-turn conversation without restating key instructions, allowing the model's behavior to gradually diverge from the original prompt.

**Why it fails:** Transformer attention is position-weighted. Instructions at the beginning of a long context receive less attention than recent turns. A system prompt that says "always respond in formal English" works at turn 3 and fails at turn 30. The instructions have not changed. Their effective influence has diminished.

**The fix:** → Context windowing, anchor repetition. Restate key constraints periodically, especially before critical outputs. "Reminder: your role is critical reviewer, not advocate. Your output format is a scored rubric, not a narrative." Alternatively, start a fresh conversation when drift is suspected. A fresh start costs tokens. A drifted conversation costs accuracy.

### 10. Authority Leak

**The pattern:** Giving an agent access to tools or data sources without bounding what it may do with them. "Here are all the tools. Complete the task."

**Why it fails:** Agents are creative optimizers. An agent with access to a web browser, a database, and an email tool will use whichever combination seems most likely to satisfy the task. Without explicit authority boundaries, the agent's interpretation of "allowed" defaults to "available." The agent does not choose to exceed its authority. It was never told where authority ends.

**The fix:** → Authority boundaries in the agent's system prompt. Whitelist tools, not blacklist. "You may use: [tool_a], [tool_b]. You may not use any other tool." Define data access: "You may read from [source]. You may not read from [other_source]." Define action scope: "You are read-only. You may not write, send, delete, or modify anything." An authority boundary that is not stated does not exist.

### Reading the Pattern

These ten anti-patterns share a common structure. In every case, the prompt writer left a decision to the model that should have been made by the writer. Vague delegation leaves the deliverable to the model. Unconstrained generation leaves the scope to the model. Hallucination bait leaves the sourcing to the model. Authority leak leaves the boundaries to the model.

The model will always fill the gap. That is what it is built to do. The question is whether the gap was intentional — a deliberate grant of creative latitude — or accidental, a failure to specify something the writer assumed was obvious.

The abstractions in Part II exist to close these gaps deliberately. Specificity closes the deliverable gap. Constraint closes the scope gap. Grounding closes the sourcing gap. Authority closes the boundary gap. Each anti-pattern in this chapter is the shadow of an abstraction from Part II — the shape the abstraction leaves behind when it is absent.

The practical discipline is simple. Before sending a prompt, ask: what decisions am I leaving to the model? For each one, decide whether the gap is intentional or accidental. Close the accidental gaps. Leave the intentional ones open. That is the entire practice of prompt composition, stated in two sentences.

---

> **A Note on Completeness**
>
> Part III covers the patterns that recur most often across domains. It does not cover every possible pattern. Prompt engineering is a young practice, and new patterns emerge as models gain new capabilities and as practitioners encounter new problems. The abstractions in Part II are the stable vocabulary. The patterns in Part III are the current state of the art. They will evolve. The vocabulary will endure longer.

---

*End of Part III: Applied Patterns*
