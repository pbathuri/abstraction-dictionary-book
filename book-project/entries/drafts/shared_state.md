---
headword: "shared state"
slug: "shared_state"
family: "agent_workflow"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# shared state

**Elevator definition**
Shared state is the information accessible to multiple agents in a pipeline — the working memory, blackboard, or common ground that allows agents to coordinate without speaking directly.

## What it is

When a single model runs a single prompt, all the information lives in one place: the context window. Nothing needs to be shared because there is only one consumer. The moment you introduce a second agent, you face a fundamental architectural question: how does Agent B know what Agent A found?

Shared state is the answer. It is the data structure — a JSON object, a database, a file system, an in-memory store — that holds the accumulated results of a pipeline's work and makes those results available to any agent that needs them. When a Research Agent extracts five findings and stores them in shared state, the Analysis Agent can read those findings without the two agents ever communicating directly. When a Verification Agent marks a claim as failed and updates shared state, the Revision Agent knows what to fix without anyone passing a message.

The concept has a direct analogy in artificial intelligence research: the **blackboard architecture**, introduced by Erman et al. (1980) for the HEARSAY-II speech understanding system. In a blackboard system, multiple independent knowledge sources (analogous to agents) read from and write to a shared data structure (the blackboard). No knowledge source communicates with any other. They all communicate through the blackboard. A controller decides which knowledge source runs next based on the current state of the blackboard. This architecture is remarkably close to how modern multi-agent LLM systems work when well-designed.

Shared state in LLM pipelines typically includes several categories of information:

**Task state** — What is the overall goal? What sub-tasks have been completed? What remains? This is the pipeline's progress tracker, equivalent to a project management board.

**Intermediate results** — The outputs of each agent, stored in a structured format. Research findings, analysis conclusions, verification results, drafts. These accumulate as the pipeline runs and form the raw material for downstream agents.

**Metadata** — Timestamps, agent IDs, confidence scores, provenance records. This supports → provenance tracking and debugging: when something goes wrong, the metadata tells you which agent did what, when, and with what confidence.

**Configuration** — Parameters that multiple agents share: the user's original question, the target audience, the output format, quality thresholds. These are set at the start and read (but not written) by every agent.

The critical design decision is access control: which agents can read which parts of the state, and which agents can write to which parts. Unrestricted access — every agent reads and writes everything — creates two problems. First, **context bloat**: later agents see an enormous accumulated state that dilutes attention on what they actually need. Second, **state corruption**: an agent writes something incorrect, and every downstream agent inherits the error. Scoped access — each agent reads only the state relevant to its task and writes only to its designated output section — mitigates both problems.

The alternative to shared state is direct message passing: Agent A's output is formatted and passed directly to Agent B as input. This works for simple, linear pipelines but breaks down when agents have non-linear dependencies (Agent C needs results from both Agent A and Agent B), when agents need to check what happened earlier in the pipeline (debugging), or when multiple agents need to coordinate around a shared resource (a document being iteratively refined). Shared state handles all these patterns naturally.

## Why it matters in prompting

Even in single-model prompt chains, shared state exists informally. When you run Prompt A, copy its output, and paste it into Prompt B, you are manually maintaining shared state. The clipboard is your state store. This works for two or three steps but does not scale — you lose track of what was produced when, the context grows with each paste, and there is no structured way to select which parts of previous outputs to include.

Formalizing shared state in prompt chains means defining a structured output format for each step (JSON, not free text), storing each step's output in a named location, and assembling the next step's input by selecting from stored outputs. This turns an ad hoc copy-paste workflow into a reproducible data pipeline.

## Why it matters in agentic workflows

Shared state is what distinguishes a collection of independent agents from a coordinated system. Without it, agents are isolated: each does its work and passes output forward, but no agent knows the broader context of the pipeline's progress. With shared state, agents can make informed decisions: "The Verification Agent already flagged three of these sources as unreliable, so I will not cite them" or "The planner marked this sub-task as high priority, so I will allocate more effort to it."

Shared state also enables **resumability**. If a pipeline fails midway — an agent crashes, a model call times out, a rate limit is hit — the pipeline can resume from the last good state rather than restarting from scratch. The state store records what has been completed and what remains. This is critical for long-running pipelines where restarting from zero wastes minutes or hours of compute.

## What it changes in model behavior

Shared state does not change how any individual model generates. It changes what each model *sees*. A well-managed shared state ensures each agent's context is populated with exactly the relevant prior results, in a structured format the agent can parse. This reduces ambiguity and improves output quality because the model is working with clean, structured inputs rather than raw, unstructured output from a previous agent.

## Use it when

- Multiple agents need to coordinate around shared information
- The pipeline has non-linear dependencies (agents that depend on multiple prior agents)
- You need resumability — the ability to restart from a midpoint after failure
- Debugging requires visibility into what each agent produced and when
- The pipeline involves iterative refinement, where agents revisit and update prior results

## Do not use it when

- The pipeline is strictly linear with only two or three steps — direct message passing is simpler
- Each agent is fully independent and needs no information from other agents
- The overhead of a state management system exceeds the complexity of the pipeline

## Contrast set

- → **handoff** — A handoff is a single transfer of work between agents. Shared state is the persistent store that handoffs read from and write to. The handoff is the event; the state is the record.
- → **context** — Context is what a single model sees in a single call. Shared state is the superset of all accumulated context across the pipeline. Each agent's context is assembled from a *subset* of shared state.
- → **orchestration** — Orchestration manages the flow of work. Shared state is the data layer orchestration operates on. The orchestrator reads shared state to decide what to do next and writes to it to record progress.
- → **pipeline** — A pipeline is a sequence of processing steps. Shared state is the data substrate that connects those steps. You can have a pipeline without explicit shared state (direct message passing), but complex pipelines need it.

## Common failure modes

- **State explosion** — Every agent appends its full output to shared state without summarization or pruning. By the tenth agent, the state object is 50,000 tokens. Later agents receive bloated context or exceed the context window. Fix: the → orchestrator must actively manage state size. After each agent, summarize or prune the state, keeping only what downstream agents need.

- **Write conflicts** — Two agents running in parallel write to the same state key, and one overwrites the other's results. Fix: use scoped write access. Each agent writes to its own output section. If parallel agents need to contribute to the same result, use a merge strategy (append to a list rather than overwriting a value).

- **Stale reads** — An agent reads from shared state before a prerequisite agent has written to it, getting default or outdated values. Fix: the orchestrator must enforce dependency ordering. Agent B should not start until Agent A has completed and its results are in the state. In concurrent architectures, use readiness signals or event-driven state access.

## Prompt examples

### Minimal example

```text
You are Agent 2 in a three-agent pipeline. Here is the
current pipeline state:

{
  "question": "What drove Q4 revenue decline?",
  "agent_1_findings": [
    {"finding": "APAC revenue dropped 18%", "source": "10-K p.23"},
    {"finding": "Two major contracts deferred to Q1", "source": "call transcript"}
  ]
}

Using agent_1_findings, identify the primary driver of the
decline. Write your analysis to the "agent_2_analysis" key.
```

### Strong example

```text
You are the Analysis Agent in a multi-agent research pipeline.

Your section of shared state:

read_access:
  - task.question: "How is AI regulation evolving in the EU?"
  - research.findings: [array of 8 sourced findings]
  - research.source_quality: [array of source trust scores]
  - config.output_format: "structured_json"
  - config.max_length: 500

write_access:
  - analysis.conclusions: [your output goes here]
  - analysis.confidence: [your confidence score]
  - analysis.gaps: [information gaps you identified]

Instructions:
1. Read research.findings and research.source_quality.
2. Prioritize findings from sources with trust score >= 0.8.
3. Produce 3-5 analytical conclusions, each citing the
   findings that support it.
4. Rate your overall confidence (high/medium/low).
5. List any information gaps that would improve the analysis.
6. Write outputs to your designated state keys only.
   Do not modify any other state keys.
```

### Agentic workflow example

```text
Pipeline: Shared State Architecture for Report Generation

State schema:
{
  "task": {
    "question": string,
    "audience": string,
    "constraints": object
  },
  "research": {
    "findings": Finding[],
    "sources": Source[],
    "status": "pending | complete | needs_revision"
  },
  "verification": {
    "results": VerificationResult[],
    "pass_rate": float,
    "status": "pending | complete"
  },
  "analysis": {
    "conclusions": Conclusion[],
    "confidence": float,
    "gaps": string[]
  },
  "output": {
    "draft": string,
    "revision_notes": string[],
    "final": string,
    "status": "pending | drafting | revising | complete"
  },
  "meta": {
    "started_at": timestamp,
    "current_agent": string,
    "completed_agents": string[],
    "errors": Error[]
  }
}

Access control:
- Research Agent: reads task.*, writes research.*
- Verification Agent: reads research.findings, writes
  verification.*
- Analysis Agent: reads research.findings (only verified),
  verification.results, writes analysis.*
- Writing Agent: reads analysis.*, task.audience, writes
  output.draft
- Editor Agent: reads output.draft, task.constraints,
  writes output.revision_notes, output.final

Orchestrator: reads/writes meta.*, reads all status fields.
Manages execution order. Prunes state before each agent
receives its context (agents see only their read_access
portion, not the full state).
```

## Model-fit note

Shared state is an architectural pattern, not a model feature — it is implemented in code (Python dicts, databases, files), not in prompts. However, the *model's ability to work with shared state* varies by tier. Frontier models reliably read structured state objects, extract relevant fields, and write to designated output keys. Midsize models handle simple state schemas but may fail to respect write-access boundaries or may attempt to modify state keys outside their scope. Small models need state presented as simple key-value pairs rather than nested objects. For all tiers, keep the state schema consistent and provide explicit field descriptions.

## Evidence and provenance

The blackboard architecture originates with the HEARSAY-II system (Erman et al., 1980) and is a recognized pattern in multi-agent AI systems. Shared state in LLM agent frameworks is implemented in LangGraph (state graphs), CrewAI (shared memory), and AutoGen (group chat state). The access control pattern for shared state draws from database permission models and microservice architecture patterns. The concept of state management in LLM pipelines is discussed in practitioner literature on production agent systems.

## Related entries

- **→ orchestration** — manages the flow of work over shared state
- **→ handoff** — the event that reads from and writes to shared state
- **→ pipeline** — the sequence of processing steps that shared state connects
- **→ context windowing** — determines how much of the shared state each agent can see
