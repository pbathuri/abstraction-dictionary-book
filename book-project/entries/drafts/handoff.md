---
headword: "handoff"
slug: "handoff"
family: "agent_workflow"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# Handoff

**Elevator definition** The transfer of control, context, and responsibility from one agent to another at a defined boundary in a multi-agent workflow.

## What it is

A handoff is the moment one agent stops working and another begins. It is not a suggestion, not a CC, not a shared workspace where two agents happen to overlap. It is a discrete transfer: Agent A relinquishes control, Agent B assumes it, and a packet of context crosses the boundary between them.

The concept borrows from shift changes in hospitals, relay races, and air traffic control — domains where a sloppy transfer kills. In each case, the outgoing party must communicate not just "what happened" but "what matters next." A nurse doesn't hand off a patient by reciting the entire medical history. She says: allergies to penicillin, blood pressure trending down, the IV in the left arm is positional. The incoming nurse now has what she needs to act, not merely to know.

In agentic systems, a handoff has three structural components. First, the **trigger**: a condition or completion state that tells Agent A its work is done. Second, the **context packet**: the structured information Agent B needs — not the full conversation history, not a raw dump of everything that happened, but a curated summary of state, decisions made, open questions, and constraints. Third, the **acceptance**: Agent B's acknowledgment that it has received sufficient context to proceed. Without all three, you don't have a handoff. You have a hope.

Handoffs can be synchronous (Agent A waits for Agent B to accept before releasing) or asynchronous (Agent A deposits context and exits). Synchronous handoffs are safer. Asynchronous handoffs are faster. Most production systems use a hybrid: synchronous for critical path transitions, asynchronous for parallel branches.

The failure mode unique to handoffs is **context loss at the boundary**. Every time information crosses from one agent to another, some of it degrades. Structured handoff protocols — explicit schemas for what must be passed — reduce this loss. Unstructured handoffs ("here's the conversation so far") guarantee it.

A handoff is not delegation. Delegation says "do this task and report back." Handoff says "I'm done; you're in charge now." The delegating agent retains authority. The handing-off agent surrenders it. This distinction matters because it determines who owns the outcome. In delegation, the delegator owns it. In handoff, the receiving agent does.

## Why it matters in prompting

When you write a prompt that will feed into another prompt — a chain, a pipeline, a multi-step workflow — you are designing a handoff whether you know it or not. The output of Prompt A becomes the input of Prompt B, and every piece of ambiguity or missing context in that output is a fault line.

Prompt engineers who think about handoffs structure their outputs differently. They don't just ask for "a summary." They ask for a summary that includes specific fields the downstream prompt expects. They name variables. They enforce output schemas. They build the bridge before the traffic arrives.

Ignoring handoff design is the single most common source of failures in multi-step prompt chains. The individual prompts work fine in isolation. Stitched together, they produce nonsense — because nobody designed the seams.

## Why it matters in agentic workflows

In agentic architectures — tool-using agents, multi-agent pipelines, orchestrated swarms — handoffs are load-bearing joints. An orchestrator delegates a research task to Agent A, which hands off its findings to Agent B for synthesis, which hands off a draft to Agent C for critique. Each transition is a handoff, and each handoff is a potential point of failure.

The difference between a fragile demo and a reliable system often comes down to handoff engineering. Systems that define explicit handoff contracts — what fields must be present, what format they take, what constitutes a valid state — survive edge cases. Systems that pass raw context and hope for the best collapse under real-world variance.

Handoff design also determines latency. A well-designed context packet is small and targeted. A lazy one dumps the full conversation, forcing the receiving agent to parse irrelevant information and burning tokens on context that doesn't aid the task.

## What it changes in model behavior

When a model receives a clean handoff — structured context, clear task framing, explicit constraints — it behaves as if it's starting fresh with strong priors. It doesn't hallucinate missing context because the context isn't missing. It doesn't drift from the original goal because the goal is restated at the boundary. Clean handoffs reset the model's attention to what matters.

## Use it when

- Control must shift from one agent (or prompt stage) to another with no shared memory
- The receiving agent needs curated context, not raw history
- You are building a pipeline where each stage has a different role or capability
- Error handling requires clear ownership — you need to know which agent is responsible at any given moment
- A human-in-the-loop checkpoint separates two automated stages
- You are debugging a multi-agent system and need to inspect what crossed each boundary

## Do not use it when

- A single agent can complete the entire task — handoffs add overhead and risk
- Two agents need to collaborate interactively (use shared workspace or dialogue patterns instead)
- The "receiving agent" is just the same model in a new turn with full conversation history (that's continuation, not handoff)

## Contrast set

- **Delegation** — Delegation assigns a subtask and expects a return. Handoff transfers full control with no expectation of return. The delegator remains the authority; the handing-off agent exits.
- **Orchestration** — Orchestration manages the entire flow, including handoffs. A handoff is one event within an orchestrated system. Orchestration is the control plane; handoff is a specific operation on it.
- **Escalation** — Escalation moves a problem upward to a more capable or more authorized agent. Handoff moves work laterally or forward in a sequence. Escalation implies "I can't handle this." Handoff implies "My part is done."
- **Context window** — The context window is the technical constraint that makes handoff design necessary. If models had infinite context with perfect attention, you could skip handoffs entirely and keep everything in one thread. They don't. So you can't.

## Common failure modes

- **Context starvation** — The handing-off agent passes too little context. The receiving agent lacks critical information and either hallucinates it or produces generic output. Fix: define a handoff schema with required fields and validate before transfer.
- **Context flooding** — The handing-off agent passes everything. The receiving agent drowns in irrelevant detail, and its attention dilutes across noise. Fix: curate the context packet. Pass what the next agent needs to act, not what the previous agent happened to see.
- **Orphaned handoffs** — Agent A hands off, but Agent B never picks up. The task stalls silently. Fix: implement acceptance confirmation and timeout-based alerts.

## Prompt examples

Minimal (no handoff design — the failure case):

```
Summarize this article. Then write a blog post based on the summary.
```

Strong (explicit handoff structure):

```
Step 1: Summarize the following article in exactly 5 bullet points. Each bullet must include: the key claim, the supporting evidence, and the source paragraph number.

Step 2: Using ONLY the bullet points from Step 1 (not the original article), write a 300-word blog post for a technical audience. If any bullet point is unclear, flag it rather than guessing.
```

Agentic workflow (formal handoff contract):

```yaml
handoff:
  from: research_agent
  to: synthesis_agent
  context_packet:
    task: "Synthesize findings into executive brief"
    findings:
      - claim: "<string>"
        confidence: "<high|medium|low>"
        source: "<citation>"
    constraints:
      max_length: 500
      audience: "C-suite, non-technical"
      tone: "direct, no hedging"
    open_questions:
      - "<any unresolved issues the research agent surfaced>"
  acceptance_criteria:
    required_fields: ["findings", "constraints"]
    min_findings: 3
```

## Model-fit note

All frontier models (GPT-4-class, Claude 3+, Gemini Ultra) handle structured handoffs well when the context packet is explicit and schema-conformant. Smaller models (7B-13B parameter range) struggle with implicit handoff cues — they need heavier scaffolding, stricter schemas, and shorter context packets. For open-source deployments, validate handoff fidelity at every boundary.

## Evidence and provenance

The handoff pattern is formalized in OpenAI's multi-agent cookbook (2025) and Anthropic's agent design documentation. The term itself migrates from operations research and healthcare shift-change protocols, where structured handoff checklists (SBAR: Situation, Background, Assessment, Recommendation) reduced error rates by 23% in clinical settings (Haig et al., 2006).

## Related entries

- **delegation**
- **orchestration**
- **pipeline**
- **context window**
- **escalation**
