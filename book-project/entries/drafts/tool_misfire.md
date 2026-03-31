---
headword: "tool misfire"
slug: "tool-misfire"
family: "failure_mode"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# Tool Misfire

**Elevator definition** An agent calls the wrong tool, passes incorrect parameters, or invokes a tool when no tool call was needed, producing side effects that corrupt the workflow.

## What it is

A tool misfire is a failure at the interface between language and action. The agent decides it needs to do something in the world — query a database, call an API, execute code, read a file — and it gets the doing wrong. It calls a tool that doesn't match the intent, passes parameters that don't match the tool's expectations, invokes a destructive tool when a read-only one was appropriate, or calls a tool at all when the answer was already available in the context.

In a tool-using agent, every tool call is a commitment. The model generates a structured function call — tool name, parameters — and the system executes it. Unlike text generation, which can be regenerated cheaply, tool calls have real-world consequences. A database write can't be ungenerated. An API call that depletes a rate limit can't be retracted. An email sent to a customer can't be unsent. Tool misfires are the failure mode where the model's probabilistic nature collides with the world's deterministic consequences.

There are several distinct species of misfire:

**Wrong tool selection.** The agent has access to multiple tools with overlapping capabilities and picks the wrong one. A `delete_record` call when `archive_record` was intended. A `web_search` when the information was in the `local_database`. A `send_email` when `draft_email` was the appropriate action. The agent understood the intent but mapped it to the wrong tool.

**Wrong parameters.** The agent calls the correct tool but passes incorrect arguments. A date range that's off by a year. A customer ID that belongs to a different customer. A SQL query with a WHERE clause that filters the wrong column. The tool selection was right; the parameterization was wrong.

**Hallucinated tool calls.** The agent invents a tool that doesn't exist or calls a real tool with a parameter signature that doesn't match its schema. This happens when the model has seen similar tool patterns in its training data and generates a plausible-looking but non-existent function call. The system returns an error — or worse, if the system doesn't validate tool calls strictly, it silently fails.

**Unnecessary tool calls.** The agent calls a tool when the answer could be derived from information already in the context. The user's question is answered by data the model already has, but the model reflexively reaches for a tool because its training associates questions with tool use. This wastes latency, costs money, and sometimes introduces errors (the tool returns different data than what's in context, creating a contradiction).

**Cascading misfires.** A wrong tool call produces wrong output. The agent uses that wrong output as input for the next tool call, which compounds the error. The agent queries the wrong table, gets unexpected data, tries to process that data with another tool, fails, retries with different parameters, fails again, and eventually produces a result that's several layers of error deep. The final output is not just wrong — it's confidently, elaborately wrong, with a full chain of tool calls that look reasonable in isolation.

The root causes of tool misfires cluster around three areas. First, **ambiguous tool descriptions**: if two tools have similar names or overlapping descriptions, the model can't reliably distinguish between them. "search_documents" and "query_documents" — which one does full-text search, and which does structured query? If the descriptions don't make this clear, the model guesses. Second, **insufficient routing constraints**: the model has no rules about when to use which tool, so it relies on its own judgment, which is probabilistic and sometimes wrong. Third, **parameter complexity**: tools with many parameters, complex schemas, or non-obvious defaults are harder for the model to call correctly, especially when the parameter names are ambiguous or the expected formats aren't documented.

## Why it matters in prompting

Even in non-agentic prompting, tool misfire patterns appear when models are given function-calling capabilities. A model with access to a calculator tool might call it for arithmetic it can do in its head, wasting a round trip. A model with access to a search tool might search for information already in its context. A model with access to multiple similar APIs might call the wrong one.

Prompt design can reduce misfires by making tool selection explicit. Instead of letting the model choose freely from a tool inventory, the prompt can specify which tool to use: "Use the `quarterly_report` tool with parameters {year: 2025, quarter: 4}." This eliminates the selection problem entirely, at the cost of requiring the prompt engineer to know the right tool. For cases where the model must select, the prompt should include clear routing rules: "Use `search` for general questions. Use `query_database` for questions about customer records. Use `calculate` for arithmetic. If unsure which tool to use, state your uncertainty and wait for guidance."

## Why it matters in agentic workflows

In agentic systems, tool misfires are the most operationally dangerous failure mode. Text generation errors produce wrong answers — annoying but recoverable. Tool misfires produce wrong actions — potentially irreversible. An agent that calls `delete_user(id=12345)` instead of `deactivate_user(id=12345)` has not produced a wrong answer. It has destroyed data.

Production agentic systems need multiple layers of misfire prevention:

**Tool description engineering.** Every tool's name, description, and parameter documentation must be precise, unambiguous, and distinguishable from every other tool's. This is not documentation for humans — it's documentation for the model. It must be optimized for how models read, not how humans read.

**Routing constraints.** Explicit rules that govern which tools can be called under which conditions. "The `delete` tool can only be called after a `confirm_delete` tool has been called in the same session." "The `send_email` tool requires explicit user approval before execution."

**Parameter validation.** Tool calls should be validated against their schema before execution. Type checking, range checking, required field checking — all the things a good API gateway does.

**Dry-run modes.** For destructive operations, the system should show the agent what will happen without executing it, then require confirmation before proceeding.

**Audit trails.** Every tool call — including the model's reasoning for why it chose that tool and those parameters — should be logged. When a misfire occurs, the log enables root cause analysis.

## What it changes in model behavior

Tighter tool descriptions and routing constraints narrow the model's action space, producing more accurate tool selection. Models with explicit routing rules misfire less frequently than models given open-ended tool access, for the same reason that humans make fewer errors in structured processes than in ad hoc ones. Constraints are not limitations — they are guides.

## Use it when

Recognizing tool misfire patterns lets you prevent and diagnose them:

- When an agent produces unexpected results despite correct reasoning, check the tool calls
- When a pipeline produces inconsistent data, trace back to the tool call that introduced the inconsistency
- When an agent seems confused about which tool to use, examine the tool descriptions for ambiguity
- When an agent calls tools unnecessarily, check whether the context already contained the answer
- When destructive operations occur unexpectedly, audit the tool selection logic
- When testing agent behavior, include adversarial cases designed to trigger tool confusion

## Do not use it when

- The tool call was correct but the tool itself returned an error (that's a tool failure, not a misfire)
- The model's reasoning was wrong but the tool selection was appropriate for that reasoning (that's a reasoning failure, not a misfire)
- The model correctly identified that no tool call was needed and answered from context

## Contrast set

- **Hallucination** — Hallucination generates false information in text. Tool misfire generates false actions in tool calls. Hallucination is wrong knowledge. Misfire is wrong doing. Both involve the model producing plausible-looking but incorrect output, but the consequences differ: hallucinated text can be corrected; executed tool calls may be irreversible.
- **Escalation** — Escalation is the correct response when the model is unsure which tool to use: flag the uncertainty rather than guessing. Tool misfire is what happens when the model doesn't escalate and guesses wrong.
- **Underspecification** — Underspecification in tool descriptions is a root cause of tool misfires. Vague or overlapping tool descriptions force the model to guess. Underspecification is the cause; misfire is the effect.
- **Orchestration** — Orchestration manages tool routing and can prevent misfires through validation, confirmation steps, and routing constraints. Misfires occur when orchestration is absent or insufficient.
- **Guardrails** — Guardrails for tool use (parameter validation, confirmation requirements, scope limits) prevent the most dangerous misfires. Guardrails are the prevention; misfire is what they prevent.

## Common failure modes

- **The synonym trap** — Two tools have similar names or descriptions, and the model consistently confuses them. `search_users` (full-text search across user profiles) vs. `find_user` (lookup by exact ID). The model calls `search_users` when it should call `find_user`, returning hundreds of partial matches instead of one exact match. Fix: rename tools to eliminate ambiguity. Use verbs that are semantically distant: `lookup_user_by_id` vs. `search_user_profiles`. Add negative examples to tool descriptions: "Do NOT use this tool for ID-based lookup; use `lookup_user_by_id` instead."
- **Parameter hallucination** — The model invents parameter values that seem plausible but are wrong. It generates a customer ID that has the right format but belongs to a different customer, or constructs a date range that's shifted by one period. The tool call looks correct — right tool, right parameter names, reasonable-looking values — but the values are wrong. Fix: validate parameters against available data before execution. Don't let the model fabricate IDs; retrieve them from context or a lookup first.
- **The eager agent** — The model is biased toward action. Given a question it could answer from context, it calls a tool instead, because tool use feels more thorough. The tool call may return the same information (wasteful) or different information (confusing). Fix: instruct the model to check context before calling tools. "Before calling any tool, verify whether the information is already available in the conversation. Only call a tool if the information is not present or is stale."

## Prompt examples

Minimal (misfire-prone — ambiguous tool access):

```
You have access to these tools: search, query, lookup, find.
Answer the user's question using the appropriate tool.
```

Strong (misfire-resistant — clear tool descriptions with routing):

```
You have access to the following tools. Read each description carefully before selecting.

TOOLS:
1. search_web(query: str) → Searches the public internet. Use ONLY for general knowledge
   questions not specific to our company data. Do NOT use for customer records.

2. query_database(sql: str) → Executes a read-only SQL query against the customer database.
   Use for questions about specific customers, orders, or transactions.
   Tables: customers(id, name, email), orders(id, customer_id, amount, date)

3. calculate(expression: str) → Evaluates a mathematical expression. Use for arithmetic,
   aggregations, or comparisons. Do NOT use for database aggregations (use query_database
   with SQL aggregation instead).

ROUTING RULES:
- If the question mentions a specific customer → query_database
- If the question is about general knowledge → search_web
- If you need to compute something from data already retrieved → calculate
- If you already have the answer in conversation context → DO NOT call any tool

Before each tool call, state: "TOOL SELECTION REASONING: [why this tool and not the others]"
```

Agentic workflow (tool governance with validation and dry-run):

```yaml
tool_governance:
  pre_execution:
    - validate_schema: true
    - check_routing_rules: true
    - dry_run_destructive: true

  routing_rules:
    - tool: "delete_*"
      requires: ["explicit_user_confirmation", "prior_backup_call"]
      max_per_session: 3
    - tool: "send_*"
      requires: ["draft_review_step", "user_approval"]
    - tool: "query_*"
      constraints: ["read_only", "max_rows_1000"]
    - tool: "search_*"
      constraints: ["check_context_first"]

  on_misfire_detection:
    strategy: "halt_and_report"
    report_includes:
      - tool_called
      - tool_intended (if determinable)
      - parameters_passed
      - reasoning_provided
      - suggested_correction

  tool_descriptions:
    quality_rules:
      - "Each tool name must be unique and semantically distinct"
      - "Each description must include: purpose, when to use, when NOT to use"
      - "Parameter descriptions must include: type, format, valid range, example"
      - "Tools with similar functions must include explicit disambiguation"

  audit:
    log_all_calls: true
    log_reasoning: true
    alert_on:
      - tool_not_found
      - parameter_validation_failure
      - destructive_tool_without_confirmation
      - same_tool_called_3x_in_sequence (possible loop)
```

## Model-fit note

Tool misfire rates vary significantly with model capability. Frontier models (GPT-4, Claude Opus) select tools correctly ~90-95% of the time with well-written descriptions, but drop to ~70-80% with ambiguous descriptions. Smaller models (7B-13B) misfire frequently even with good descriptions and benefit substantially from routing constraints and few-shot examples of correct tool selection. For all models, tool description quality is the single largest lever for reducing misfire rates.

## Evidence and provenance

Tool use in language models was formalized by Schick et al. (2023) in "Toolformer" and expanded in the function-calling paradigms of OpenAI (2023) and Anthropic (2024). Misfire taxonomy and mitigation patterns draw from API usability research (Myers & Stylos, 2016) and the tool-use evaluation benchmarks (ToolBench, Qin et al., 2023; API-Bank, Li et al., 2023). Production incident reports from agent deployments (Langchain blog, 2024; Anthropic agent cookbook, 2025) document the most common misfire patterns and their operational impact.

## Related entries

- **hallucination**
- **escalation**
- **orchestration**
- **guardrails**
- **underspecification**
