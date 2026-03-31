---
headword: "information routing"
slug: "information_routing"
family: "context_architecture"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# information routing

**Elevator definition**
Information routing is the practice of directing the right information to the right agent or prompt stage at the right time — the postal system of a pipeline's context.

## What it is

In a multi-stage system, information exists in many places: source documents, user inputs, intermediate agent outputs, tool results, shared state. Not all of this information is relevant to every stage. The Research Agent does not need the Writing Agent's style guide. The Verification Agent does not need the Planner's internal reasoning notes. The Synthesis Agent does not need the raw source documents if it has the extracted findings. Information routing is the discipline of ensuring each component receives precisely the information it needs — no more, no less.

The concept is distinct from → routing (which decides where *work* goes) and from → progressive disclosure (which decides *when* information is revealed). Information routing decides *what information* accompanies the work at each stage. It is the addressing system on the envelope: the letter (the task) has been routed to the correct mailbox (the agent). Information routing determines which documents are stuffed inside the envelope.

The need for information routing arises from a fundamental tension in multi-agent architectures. On one hand, agents need context to do their work. On the other hand, excessive context degrades performance. The → signal-to-noise ratio entry documents this in detail: irrelevant information dilutes attention and reduces output quality. Information routing resolves the tension by curating each agent's context to maximize relevance and minimize noise.

Information routing operates through several mechanisms:

**Context assembly** — For each agent invocation, the orchestrator assembles a context package from available information: the agent's system prompt, the relevant portion of → shared state, any reference documents the agent needs, and the specific sub-task description. This assembly is an active design decision, not a passive dump. The orchestrator must decide: which shared state fields does this agent need to read? Which source documents are relevant to this sub-task? Should intermediate results from previous agents be included in full or summarized?

**Filtering** — Removing information that is irrelevant to the current agent's task. When the Research Agent produces a 1,500-token output that includes 500 tokens of findings, 400 tokens of reasoning about search strategy, and 600 tokens of source evaluation notes, the filter strips the reasoning and evaluation notes before passing the findings to the Analysis Agent. The stripped information is not lost — it remains in shared state for debugging — but it is not included in the Analysis Agent's context.

**Transformation** — Changing the format or granularity of information to match the receiving agent's needs. A Data Extraction Agent produces findings as a JSON array with 15 fields per finding. The Synthesis Agent needs only three of those fields. Information routing includes a transformation step that extracts the relevant fields and presents them in the format the Synthesis Agent expects. This is not just filtering — it is reshaping the information for its new consumer.

**Aggregation** — Combining information from multiple sources into a single, coherent context for an agent that depends on multiple upstream outputs. The Synthesis Agent needs findings from the Research Agent, verification results from the Verification Agent, and the original user question. Information routing aggregates these three inputs into a single context, structured so the Synthesis Agent can reference each source of information without confusion.

Information routing is the operational expression of a deeper architectural principle: each component in a system should have exactly the information it needs to perform its function, and no more. In software engineering, this is known as the principle of least privilege applied to data access. In LLM systems, it has an additional motivation: attention is a finite resource, and every irrelevant token consumes some of it.

## Why it matters in prompting

Even in single-model prompt chains, information routing matters. When you take the output of Prompt A and feed it to Prompt B, you are routing information. The question is whether you route thoughtfully or reflexively. Reflexively means copy-pasting the full output of A into B. Thoughtfully means extracting the relevant findings from A's output, discarding the reasoning, and presenting only the findings — in the format B expects — as B's input.

This is especially important in retrieval-augmented systems. A RAG pipeline retrieves 10 documents and the model needs 3 of them. Information routing is the re-ranking and filtering step that selects the 3 relevant documents and discards the 7 irrelevant ones. Without this step, the model receives all 10 and its attention is diluted across irrelevant material.

## Why it matters in agentic workflows

In production multi-agent systems, information routing is what prevents the → shared state from becoming a liability. Shared state accumulates information across the entire pipeline run. Without routing, each agent receives the full accumulated state — thousands of tokens, most irrelevant to its task. With routing, each agent receives a curated slice: only the state keys it needs, only the upstream outputs relevant to its task, only the source documents pertinent to its analysis.

Information routing also enables **agent reuse**. A well-designed Verification Agent should work regardless of what it is verifying — research findings, financial calculations, code outputs. But this only works if the information routed to the Verification Agent is always in the same format: a set of claims with source references. The routing layer handles the translation from each upstream agent's output format into the Verification Agent's expected input format. The Verification Agent itself never needs to change.

## What it changes in model behavior

Proper information routing improves output quality by raising the signal-to-noise ratio of each agent's context. Agents that receive only relevant, well-structured information produce more focused, accurate, and task-appropriate outputs. Agents that receive unfiltered accumulated context produce outputs that are diluted, tangential, or contaminated by irrelevant details from earlier pipeline stages.

## Use it when

- The pipeline has three or more stages and accumulated context grows with each stage
- Different agents need different subsets of the available information
- Upstream agent outputs contain reasoning or metadata that downstream agents should not see
- The pipeline reuses agents across different sub-tasks, requiring standardized input formats
- Context window limits require that only the most relevant information reaches each agent

## Do not use it when

- The pipeline is two steps and the full output of step one is exactly what step two needs
- All agents need the same information — routing adds overhead without benefit
- The total information is small enough that every agent can receive all of it without SNR degradation

## Contrast set

- → **routing** — Routing decides where work goes (which agent handles the task). Information routing decides what information accompanies the work. Task dispatch versus context curation.
- → **progressive disclosure** — Progressive disclosure sequences *when* information appears. Information routing determines *which* information appears at each stage. Temporal versus spatial.
- → **shared state** — Shared state is the repository. Information routing is the access layer that determines what each agent reads from the repository.
- → **context windowing** — Context windowing is the capacity constraint. Information routing is the strategy for staying within that constraint while maximizing relevance.

## Common failure modes

- **Pass-through syndrome** — The orchestrator passes full upstream outputs to downstream agents without filtering. The fifth agent in the pipeline receives the accumulated outputs of four predecessors — 4,000+ tokens — when it needs only 200 tokens of relevant findings. Fix: at every handoff, explicitly filter the upstream output to include only the fields and content the downstream agent needs.

- **Information loss at handoff** — Overly aggressive filtering removes information a downstream agent turns out to need. The Analysis Agent strips source citations from findings, and the Writing Agent cannot cite sources in the final output because the citations were filtered out. Fix: define each agent's input requirements before the pipeline runs. Filter based on the downstream agent's needs, not the upstream agent's output structure.

- **Format mismatch** — Information is routed correctly but in the wrong format. The Research Agent produces findings as prose paragraphs. The Verification Agent expects a JSON array of claims. The verification fails not because of content but because the downstream agent cannot parse the upstream output. Fix: define standard interchange formats between agents. The routing layer includes a transformation step that converts upstream output into the downstream agent's expected format.

## Prompt examples

### Minimal example

```text
The Research Agent found these three key findings:

1. Market grew 12% YoY (Source: Industry Report p.14)
2. Top competitor lost 3% market share (Source: SEC Filing)
3. Regulatory changes expected in Q2 (Source: Policy Brief)

Using only these findings, write a one-paragraph market
summary for the quarterly board deck. Cite each finding
by its source.
```

### Strong example

```text
You are the Synthesis Agent. You will receive information
from two upstream agents, pre-filtered for your task.

From Research Agent (findings only, reasoning stripped):
- Finding 1: [claim] | Source: [id] | Confidence: high
- Finding 2: [claim] | Source: [id] | Confidence: high
- Finding 3: [claim] | Source: [id] | Confidence: medium

From Verification Agent (results only, process stripped):
- Finding 1: VERIFIED (evidence: [quote])
- Finding 2: VERIFIED (evidence: [quote])
- Finding 3: UNVERIFIED (no supporting evidence found)

Your task:
1. Include only VERIFIED findings in your synthesis.
2. Note that Finding 3 was unverified and state what
   additional information would be needed to verify it.
3. Write a 200-word synthesis for a non-technical audience.
4. Cite each finding by its source ID.

You do not have access to the original source documents.
Do not attempt to supplement these findings with your own
knowledge. Work only with the information provided.
```

### Agentic workflow example

```text
Pipeline: Information Routing Specification

Context Router (code layer between orchestrator and agents):

For each agent, define:
  - read_from: which shared state keys to include
  - transform: how to reshape the data
  - exclude: what to explicitly strip

Agent 1 — Research Agent
  read_from: [task.question, config.source_list]
  transform: none (first agent, receives raw input)
  exclude: [all downstream agent configs]

Agent 2 — Verification Agent
  read_from: [research.findings]
  transform:
    - Extract each finding as: { claim, source_id, page }
    - Discard: research.search_strategy, research.reasoning
    - Attach: original source documents for cited source_ids
  exclude: [task.question, config.*, analysis.*, output.*]

Agent 3 — Analysis Agent
  read_from: [research.findings (verified only),
              verification.results]
  transform:
    - Filter research.findings to include only items where
      verification.results[claim_id].status == "PASS"
    - Merge finding + verification evidence into single object
    - Discard: verification.process_logs
  exclude: [research.search_strategy, config.source_list]

Agent 4 — Writing Agent
  read_from: [analysis.conclusions, task.question,
              config.audience, config.format_template]
  transform:
    - Format conclusions as numbered list with source citations
    - Include audience specification from config
    - Discard: analysis.confidence scores (not for reader)
  exclude: [research.*, verification.*, shared_state.meta]

Each agent sees only its routed context. No agent sees
the full shared state. The context router logs what was
routed to each agent for debugging.
```

## Model-fit note

Information routing is implemented in code, not in models — the orchestrator or context router is a programmatic layer that assembles each agent's context. However, the *benefit* of information routing varies by model tier. Small models are most sensitive to irrelevant context and benefit most from aggressive routing and filtering. Frontier models tolerate noisier contexts but still produce better output with well-routed information. The routing layer's complexity should match the pipeline's complexity: a three-agent pipeline needs simple routing; a ten-agent pipeline needs a formal routing specification.

## Evidence and provenance

The principle of scoped context delivery to agents is documented in LangGraph's state management patterns and CrewAI's task context design. The concept draws from the principle of least privilege in information security (Saltzer & Schroeder, 1975) and from data flow architecture in distributed systems. The empirical finding that scoped context improves output quality is supported by the broader literature on signal-to-noise ratio effects and the "lost in the middle" phenomenon [src_paper_sahoo2025].

## Related entries

- **→ routing** — decides where work goes; information routing decides what data accompanies it
- **→ shared state** — the data repository information routing draws from
- **→ signal-to-noise ratio** — the metric information routing optimizes
- **→ progressive disclosure** — sequences when information appears; information routing selects what appears
