---
headword: "pipeline"
slug: "pipeline"
family: "agent_workflow"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# Pipeline

**Elevator definition** A fixed sequence of processing stages where each stage's output becomes the next stage's input, turning a complex task into a repeatable assembly line.

## What it is

A pipeline is decomposition made permanent. Where ad hoc task breakdown happens once and is forgotten, a pipeline encodes that breakdown into architecture — a sequence of stages that runs the same way every time, with defined inputs, defined outputs, and defined handoffs between them.

The metaphor comes from plumbing, and the fit is exact. Water enters one end, passes through a series of connected pipes, and exits the other end transformed. No pipe needs to understand the full journey. Each pipe does one thing: filter, heat, pressurize, redirect. The system's power comes from the composition, not from any individual component.

In LLM systems, a pipeline typically looks like this: raw input enters Stage 1 (classification, parsing, or preprocessing), the output feeds Stage 2 (retrieval, analysis, or transformation), that output feeds Stage 3 (generation, synthesis, or formatting), and the final output exits Stage N (validation, post-processing, or delivery). Each stage can be a different prompt, a different model, a different tool call, or even a non-LLM function. The pipeline doesn't care what's inside the box — only that the interface between boxes is respected.

Pipelines come in several structural variants. **Linear pipelines** are the simplest: A → B → C → D, no branching. **Branching pipelines** include conditional routing: A → (if X, then B; if Y, then C) → D. **Fan-out/fan-in pipelines** split work across parallel stages and recombine: A → [B, C, D] → E. **Iterative pipelines** include feedback loops: A → B → C → (if quality check fails, back to B).

The defining characteristic that separates a pipeline from a one-off chain is **reusability and persistence**. A chain is a sequence you execute once. A pipeline is a sequence you deploy. Chains are scripts; pipelines are infrastructure. This distinction matters because pipelines justify engineering investment — monitoring, error handling, retry logic, logging, versioning — that one-off chains do not.

Pipelines also enforce **interface contracts**. Each stage has an expected input format and a promised output format. When Stage A's output doesn't match Stage B's expected input, the pipeline breaks loudly — which is far better than the silent degradation you get when raw prompts feed unstructured output into each other. Interface contracts are the immune system of a pipeline. They catch disease at the boundary rather than letting it spread.

The tension in pipeline design is between **rigidity and adaptability**. Pipelines are powerful because they're fixed — you can optimize, monitor, and debug each stage independently. But that fixedness means they can't adapt to inputs that don't fit the expected pattern. A customer support query that doesn't match any classification bucket, a document in an unexpected format, an edge case that no stage was designed to handle. Production pipelines need escape hatches: fallback stages, escalation paths, and default behaviors for unrecognized inputs.

The economic argument for pipelines is strong. Each stage can use the cheapest model that handles its specific task. Classification might need a tiny model. Retrieval might need no model at all. Generation might need a frontier model. Post-processing might need a rule-based system. By decomposing into stages, you decompose cost — and the total is usually less than throwing a single powerful model at the entire task.

## Why it matters in prompting

Every multi-step prompt is a proto-pipeline. "First classify this text, then extract entities, then generate a summary" is three pipeline stages crammed into one prompt. The problem with cramming them is that the model must hold all three tasks in working memory simultaneously, and each task's constraints compete for attention.

Separating the stages into distinct prompts — each with its own clear instruction, input format, and output format — produces better results at every stage. The classification prompt can be tuned for classification. The extraction prompt can be tuned for extraction. Neither is diluted by the other's requirements.

Prompt engineers who think in pipelines also think about **intermediate representations** — the data format that flows between stages. Is the output of Stage 1 a JSON object? A numbered list? Free text? The choice of intermediate representation determines how cleanly stages compose. Structured formats (JSON, YAML, tables) compose better than free text because they're parseable and validatable.

## Why it matters in agentic workflows

Multi-agent pipelines are the workhorse of production AI systems. Document processing pipelines (ingest → parse → classify → extract → validate → store). Content generation pipelines (research → outline → draft → edit → format → publish). Data analysis pipelines (collect → clean → analyze → visualize → narrate). Each stage is handled by a specialized agent with specific tools, specific prompts, and specific quality criteria.

Pipelines give agentic systems two things that ad hoc agent collaboration doesn't: **predictability** (you know the execution order in advance) and **debuggability** (when something breaks, you know which stage broke it). In a free-form multi-agent conversation, tracing the source of an error requires reading the full interaction log. In a pipeline, you inspect the stage boundary where the output went wrong.

Agent frameworks (LangGraph, Prefect, Dagster) provide pipeline primitives natively: stage definitions, inter-stage data passing, retry logic, parallel execution, and monitoring dashboards. These are not luxuries — they are prerequisites for running LLM pipelines in production.

## What it changes in model behavior

Each model call in a pipeline operates in a narrower context than a monolithic call. Narrower context means sharper attention, fewer competing instructions, and more consistent output. A model asked to "classify, extract, and summarize" will do all three adequately. A model asked only to "classify" will do classification well. The pipeline trades call volume for call quality — more calls, each one better.

## Use it when

- The task has a natural sequence of distinct processing stages
- Each stage requires different capabilities, tools, or model strengths
- Reproducibility matters — you need the same process to run identically on different inputs
- Cost optimization requires stage-specific model selection
- Monitoring and debugging require per-stage visibility
- The system will process high volumes of similar inputs

## Do not use it when

- The task is inherently non-sequential or exploratory
- Each input requires a unique processing path (use dynamic orchestration instead)
- The overhead of managing inter-stage data exceeds the benefit of decomposition
- You're prototyping and the pipeline structure isn't yet known

## Contrast set

- **Decomposition** — Decomposition is the cognitive act of breaking a task into parts. A pipeline is the architectural reification of a specific decomposition. Decomposition is the analysis; the pipeline is the build.
- **Chain-of-thought** — Chain-of-thought is a single model reasoning through steps sequentially within one call. A pipeline distributes those steps across multiple calls (or agents). Chain-of-thought is a model thinking aloud. A pipeline is an assembly line.
- **Orchestration** — Orchestration is the control layer that manages a pipeline (and potentially much more: branching, error handling, dynamic routing). A pipeline is one pattern that an orchestrator can run. Orchestration is the operating system; the pipeline is one process.
- **DAG (Directed Acyclic Graph)** — A DAG generalizes a pipeline by allowing branching and parallelism while prohibiting cycles. A linear pipeline is a degenerate DAG with no branches. Most production "pipelines" are actually DAGs.
- **Handoff** — A handoff is a single transfer between two stages. A pipeline is a sequence of handoffs. The pipeline defines the architecture; each handoff is an event within it.

## Common failure modes

- **Stage coupling** — Stages become implicitly dependent on upstream implementation details. Stage B expects Stage A's output to include a field that isn't in the contract. When Stage A changes, Stage B breaks. Fix: enforce explicit interface schemas and validate at every boundary.
- **Error propagation** — A failure in Stage 2 produces garbage output that Stage 3 processes as if it were valid, producing confidently wrong final output. The pipeline converts a local error into a systemic one. Fix: validate stage outputs and halt or branch on validation failure.
- **Brittleness to input variance** — The pipeline handles the expected case beautifully but collapses on unexpected input. A document in a language the pipeline wasn't designed for. A query that doesn't match any classification bucket. Fix: include a default/catch-all path and monitoring for unclassified inputs.

## Prompt examples

Minimal (no pipeline — monolithic prompt):

```
Take this customer email and classify the issue, extract the key details, draft a response, and check it for policy compliance.
```

Strong (explicit pipeline stages with interface contracts):

```
STAGE 1 — CLASSIFICATION
Input: raw customer email (plain text)
Task: Classify the email into exactly one category: [billing, technical, shipping, general]
Output format: {"category": "<string>", "confidence": <float>}

STAGE 2 — EXTRACTION
Input: original email + classification from Stage 1
Task: Extract: customer_name, order_number (if mentioned), issue_summary (one sentence), urgency (low/medium/high)
Output format: {"customer_name": "...", "order_number": "...", "issue_summary": "...", "urgency": "..."}

STAGE 3 — RESPONSE DRAFTING
Input: extracted fields from Stage 2
Task: Draft a response email. Tone: professional, empathetic. Length: 80-150 words. Address the specific issue.
Output format: plain text email

STAGE 4 — COMPLIANCE CHECK
Input: draft response from Stage 3
Task: Check against policy rules: no promises of specific timelines, no admission of liability, refund offers must cite policy section.
Output format: {"compliant": true/false, "issues": ["..."], "revised_response": "..." (if non-compliant)}
```

Agentic workflow (pipeline with framework orchestration):

```yaml
pipeline:
  name: "customer_email_processor"
  stages:
    - id: classify
      agent: "classifier"
      model: "haiku"
      input: "$raw_email"
      output_schema:
        category: {type: "enum", values: ["billing", "technical", "shipping", "general"]}
        confidence: {type: "float", min: 0, max: 1}
      on_failure: {action: "default", value: {category: "general", confidence: 0.0}}

    - id: extract
      agent: "extractor"
      model: "sonnet"
      input: {email: "$raw_email", classification: "$classify.output"}
      output_schema:
        customer_name: {type: "string"}
        order_number: {type: "string", nullable: true}
        issue_summary: {type: "string", max_length: 200}
        urgency: {type: "enum", values: ["low", "medium", "high"]}

    - id: draft
      agent: "writer"
      model: "sonnet"
      input: "$extract.output"
      output_schema:
        response: {type: "string", min_length: 80, max_length: 250}

    - id: compliance
      agent: "compliance_checker"
      model: "haiku"
      input: "$draft.output"
      output_schema:
        compliant: {type: "boolean"}
        issues: {type: "array", items: "string"}
      on_non_compliant:
        action: "loop_to"
        target: "draft"
        max_retries: 2
        feedback: "$compliance.output.issues"
```

## Model-fit note

Pipelines are model-agnostic by design — that's the point. Each stage can use whatever model (or non-model tool) is best suited to its task. Classification stages work well with small, fast models. Generation stages benefit from larger models. Validation stages can often use rule-based systems with no model at all. The pipeline pattern is how you turn model diversity from a management headache into a cost optimization strategy.

## Evidence and provenance

Pipeline architecture in computing predates LLMs by decades — Unix pipes (1973), ETL pipelines in data engineering, and CI/CD pipelines in DevOps all share the pattern. In LLM contexts, the LCEL (LangChain Expression Language) pipeline abstraction (2023), Haystack's pipeline API (2023), and DSPy's modular pipeline design (Khattab et al., 2023) formalize the pattern for language model chains. Multi-agent pipeline benchmarks show 15-30% cost reduction versus monolithic single-call approaches at equivalent quality (Databricks, 2025).

## Related entries

- **decomposition**
- **orchestration**
- **handoff**
- **planner-executor split**
- **chain-of-thought**
