---
headword: "delegation"
slug: "delegation"
family: "agent_workflow"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["handoff", "routing", "orchestration", "decomposition", "specificity", "verification loop", "planner-executor split", "escalation"]
cross_links: ["handoff", "routing", "orchestration", "decomposition", "specificity", "verification loop", "planner-executor split", "escalation", "context windowing", "hallucination bait", "shared state", "tool selection"]
tags: ["agent-workflow", "orchestration", "multi-agent", "architecture", "control-flow"]
has_note_box: true
note_box_type: "which_word"
---

# delegation

**Elevator definition**
Delegation is the act of assigning a bounded task to another agent with enough structure that the agent can complete it without reading your mind.

## What it is

Delegation is the primary unit of work transfer in multi-agent systems. It is the instruction that moves a task from one agent to another, along with everything the receiving agent needs to succeed: what to produce, in what form, by what criteria, and what to do when something goes wrong.

In management, delegation means handing off responsibility. In agentic workflows, it means something more precise. A delegation is a structured message that contains a task description, an expected output specification, a set of constraints, and an authority boundary. Omit any of these and you are not delegating; you are hoping.

The distinction matters because agents, unlike human reports, do not fill gaps with organizational context, shared lunch conversations, or a sense of what the boss probably meant. An agent given "research this topic" will research something. Whether it researches the right thing, to the right depth, in the right format, with the right sources, depends entirely on what the delegation specifies. The delegation *is* the program.

This makes delegation the point where → decomposition meets execution. A planner agent's job is to take a complex goal and break it into sub-tasks; delegation is how those sub-tasks become work. The quality of the decomposition determines how many delegations you need. The quality of each delegation determines whether those delegations succeed.

## Why it matters in prompting

Single-turn prompts rarely involve explicit delegation, but the concept still applies. Any prompt that sets a role ("You are a senior editor...") and then assigns a task ("Review this draft for...") is performing a delegation. The role defines the agent. The task defines the work. The implicit contract is that the model will operate within the boundaries of both.

Where this becomes operational is in multi-turn and system-prompt contexts. A system prompt that says "You are a research assistant. When the user asks a question, find relevant sources, summarize them, and flag any contradictions" is delegating three sub-tasks with no explicit completion criteria, no format specification, and no escalation path. The model will comply, but with wide variance. Add structure to the delegation and the variance narrows. This is the same principle that makes → specificity effective, applied to role-based interaction.

## Why it matters in agentic workflows

Delegation is the load-bearing joint of any multi-agent architecture. In frameworks like the OpenAI Agents SDK, delegation is implemented through handoff objects: an agent can transfer control to another agent along with a description of when and why [src_delegation_001]. In LangGraph, delegation appears as conditional graph edges where a supervisor evaluates state and routes to the appropriate sub-agent [src_delegation_003]. In CrewAI, delegation is explicit: Task objects carry a description, an expected output, an agent assignment, and a tool list [src_delegation_005].

The common thread across frameworks: delegation works when it is structured and fails when it is vague. Structured delegation means the receiving agent knows five things: what the deliverable is, what format it takes, what criteria define completion, what tools are available, and when to stop trying and escalate. Each missing element is a crack where ambiguity seeps in and compounds downstream.

One pattern deserves special attention: **delegation depth**. When agent A delegates to agent B, which delegates to agent C, the original intent degrades at each hop. Anecdotal evidence from multi-agent pipeline practitioners suggests that beyond depth 3, the final agent's understanding of the original task is substantially distorted unless each intermediate delegation restates the core objective [src_delegation_006]. This is the agentic version of the telephone game, and the fix is the same: repeat the signal at every relay.

## What it changes in model behavior

Structured delegation instructions cause agents to produce more tightly scoped outputs. When a delegation specifies the deliverable format and completion criteria, the receiving agent is less likely to over-produce (generating tangential analysis the delegator did not request) or under-produce (returning a partial result without flagging incompleteness). The effect is measurable in pipeline throughput: well-delegated tasks require fewer revision cycles before downstream agents can consume their output [src_delegation_002].

Poorly structured delegation has the opposite effect. An agent receiving "analyze this data" without further specification will produce whatever analysis is most probable given its training, which may not be what the workflow requires. This forces the next agent to interpret, filter, or request clarification, each of which adds latency and error surface.

## Use it when

- A task requires capabilities, tools, or context that the current agent does not have
- A workflow involves sequential stages where each stage's output feeds the next
- You need to parallelize independent sub-tasks across multiple agents
- A planner agent has decomposed a goal and needs to assign the pieces
- A human-in-the-loop workflow needs a clear contract for what each automated step will produce
- The current agent's → context budget is better spent on coordination than execution

## Do not use it when

- The task is simple enough for one agent to complete in a single pass without ambiguity
- Delegation overhead (context passing, format specification, verification) exceeds the cost of direct execution
- The sub-task is so tightly coupled to the delegator's state that extracting the necessary context would consume more tokens than the task itself
- You lack the ability to verify the delegated output before passing it downstream (delegation without → verification loop is a liability)

## Contrast set

**Closest adjacent abstractions**

- → handoff — A handoff transfers *control* from one agent to another; delegation transfers a *task*. You can delegate without handing off (the delegator keeps running and collects the result) or hand off without delegating (agent A simply yields the floor to agent B with no task specification).
- → routing — Routing decides *which* agent gets the task; delegation defines *what* the task is. A router picks the destination. A delegation writes the ticket.
- → orchestration — Orchestration manages the overall flow of a multi-agent system; delegation is the mechanism by which orchestration assigns individual units of work.

**Stronger / weaker / narrower / broader relatives**

- → decomposition — Broader. Decomposition produces the task breakdown; delegation operationalizes each piece.
- → planner-executor split — Broader. The architectural pattern where delegation is the interface between the two roles.
- → assignment — Narrower, more static. Assignment is delegation at configuration time; delegation can happen dynamically at runtime.
- → escalation — The inverse operation: returning a task upward when a delegation cannot be completed.

## Common failure modes

- **Vague delegation** → The delegator names the topic but not the deliverable. "Research prompt engineering" produces a grab-bag essay; "Return a JSON array of the 10 most-cited papers on prompt engineering published after 2023, each with title, authors, year, and one-sentence finding" produces something usable. Most delegation failures are → specificity failures wearing a different hat.

- **Authority leak** → The delegation does not bound what the agent may do. An agent told to "find competitor pricing" with access to a web-scraping tool, an email-sending tool, and a database-write tool may use any or all of them. Without explicit tool constraints, delegation becomes an open invitation to side effects. [src_delegation_006]

- **Telephone-game degradation** → In chains deeper than two or three hops, each re-delegation paraphrases the original goal. By the terminal agent, the task may be substantially different from what the originator intended. Mitigation: include the original objective verbatim at every level, separate from any hop-specific task instructions.

- **Delegation without verification** → The delegator accepts the result without checking it. In a pipeline, this means a fabricated output (→ hallucination bait) or a malformed result propagates to the next stage. Every delegation should have a paired verification step, even if it is lightweight.

## Prompt examples

### Minimal example

```text
You are a copy editor. I will give you a blog post draft.

Your task:
- Fix grammatical errors
- Flag sentences longer than 30 words
- Do not change the author's voice or rewrite for style
- Return the edited text with changes marked in [brackets]

If a passage is ambiguous and could be edited two ways,
flag it as [AMBIGUOUS: options] instead of choosing.
```

### Strong example

```text
You are a Legal Review Agent in a contract analysis pipeline.

Delegation from: Contract Triage Agent
Input: Sections 4 through 7 of the attached vendor agreement (plain text)

Task:
1. For each section, identify any clause that creates a financial
   obligation, a liability limitation, or an auto-renewal condition.
2. For each identified clause:
   - Quote the relevant sentence(s) verbatim
   - Classify as: FINANCIAL_OBLIGATION | LIABILITY_LIMITATION | AUTO_RENEWAL
   - Rate risk as: LOW | MEDIUM | HIGH with a one-sentence justification
3. If a section contains no relevant clauses, return:
   {"section": N, "clauses_found": 0, "note": "No relevant clauses"}

Output format: JSON array, one object per clause found.

Constraints:
- Do not interpret legal implications beyond classification and risk rating.
- If a clause is ambiguous, classify it as the higher-risk option and
  add "AMBIGUOUS" to the note field.
- Do not access external legal databases or case law.

Completion: Output covers all four sections. Every clause is classified.
If a section cannot be parsed, return an error object with the section
number and the parsing issue.
```

### Agentic workflow example

```text
System: Multi-Agent Documentation Pipeline
Delegator: Documentation Planner (agent_planner)

--- DELEGATION TO: API Reference Writer (agent_api_writer) ---

Objective: Produce reference documentation for the /users endpoint group.

Input artifacts:
- OpenAPI spec: artifacts/openapi_v3.json (sections tagged "users")
- Existing docs: artifacts/current_docs/users.md (for tone reference only)
- Style guide: artifacts/docs_style_guide.md

Deliverable:
- One markdown file per endpoint (GET, POST, PUT, DELETE)
- Each file must contain: endpoint path, method, description,
  request parameters (table), response schema (table),
  one curl example, one SDK example (Python), error codes
- Naming convention: users_{method}.md

Authority boundary:
- You may read the OpenAPI spec and existing docs
- You may NOT call the live API
- You may NOT modify the OpenAPI spec
- You may NOT write docs for endpoints outside the /users group

Completion criteria:
- All four endpoint files exist and are syntactically valid markdown
- Every request parameter in the spec appears in the docs
- Every error code in the spec appears in the docs

Escalation:
- If the OpenAPI spec is missing a description for any parameter,
  flag it as [SPEC_GAP: parameter_name] in the docs and notify
  agent_planner. Do not invent descriptions.

Handoff: When complete, pass the four files plus a coverage summary
to the Documentation Reviewer (agent_doc_reviewer) for verification.
```

## Model-fit note

Delegation quality depends on instruction-following fidelity, which varies by tier. Frontier proprietary models handle complex, multi-constraint delegations well and can maintain delegation structure across long outputs. Midsize open models follow structured delegations reliably when the format is explicit (JSON schemas, numbered steps) but may drop constraints in free-form delegation prose. Small open models often require delegations to be decomposed further before they can execute cleanly. Reasoning-specialized models can handle multi-step delegations in a single pass but benefit from explicit completion criteria to anchor their chain of thought. Code-specialized models excel at delegations that produce structured output (JSON, tables, schemas) but may struggle with delegations requiring nuanced prose.

## Evidence and provenance

The structural patterns for delegation are documented in the OpenAI Agents SDK (handoff objects, tool definitions, agent transfers) [src_delegation_001] and Anthropic's published research on multi-agent reliability [src_delegation_002]. Framework-specific delegation patterns draw from LangGraph supervisor documentation [src_delegation_003], AutoGen GroupChat patterns [src_delegation_004], and CrewAI Task object design [src_delegation_005]. The telephone-game degradation pattern and authority-leak failure mode are drawn from practitioner reports in the prompt engineering and agent-building community [src_delegation_006]. Parameter counts for these frameworks' recommended models are not disclosed for proprietary tiers; open-model recommendations are based on published instruction-following benchmarks.

## Related entries

- **→ handoff** — delegation transfers a task; handoff transfers control. They often co-occur but are separable.
- **→ decomposition** — the upstream operation that produces the tasks delegation assigns
- **→ specificity** — the quality that makes delegation instructions actionable
- **→ verification loop** — the downstream operation that checks delegation results
- **→ orchestration** — the system-level pattern that sequences delegations
- **→ planner-executor split** — the architecture where delegation is the interface between planning and execution
- **→ escalation** — what happens when a delegation cannot be completed
- **→ hallucination bait** — the risk when delegation asks for information the agent cannot verify

---

> **Which Word?**
>
> *Delegation* or *handoff*? Delegation gives an agent a job: here is what to build, in what format, by what standard. Handoff gives an agent the floor: your turn, the context is attached. A delegation can happen without a handoff (the delegator waits for the result and continues). A handoff can happen without a delegation (the next agent picks up where the last one left off, with no new task assignment). In most pipelines, you want both: delegate the task, *then* hand off control.
