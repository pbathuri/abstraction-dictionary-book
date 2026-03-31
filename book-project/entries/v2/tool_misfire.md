# tool misfire

> The agent calls the wrong tool, passes bad parameters, or reaches for a tool when it didn't need one — and unlike a text error, a tool call has real-world consequences.

## The Scene

Clap/OpsPilot, production week one. The support agent had four tools: `search_kb`, `lookup_account`, `create_ticket`, and `escalate_to_human`. A customer wrote: "Can you delete my account?" The agent called `create_ticket(subject="Account deletion", priority="low")`. Reasonable — except the customer was asking a question about how to delete, not requesting deletion. A create_ticket call puts a task in front of a human who executes it. The customer almost lost their account because the agent mapped "can you delete" to an action instead of a knowledge-base search.

Root cause: the tool descriptions were ambiguous. `create_ticket` said "Creates a support ticket." It didn't say "Use ONLY when the issue cannot be resolved through search or lookup, OR the user explicitly requests human help." The model made a plausible choice. The description allowed it.

I rewrote every tool description to include when to use, when NOT to use, and what the consequences of calling it were. Misfires dropped 70% in the next week.

## What This Actually Is

A tool misfire happens at the interface between language and action. The model decides it needs to do something in the world — query a database, send an email, execute code — and gets the doing wrong. Unlike text generation, which can be regenerated cheaply, tool calls have consequences. A database write can't be ungenerated. An email can't be unsent.

Five species: **wrong tool** (delete instead of archive), **wrong parameters** (correct tool, wrong customer ID), **hallucinated tool** (invents a nonexistent function), **unnecessary tool** (searches when the answer is already in context), and **cascading misfires** (wrong output from call #1 compounds into call #2). Root causes: ambiguous descriptions, missing routing rules, complex schemas.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "search, query, lookup, find" (four similar tools) | Name each tool with semantically distant verbs: `search_profiles_fulltext` vs. `lookup_user_by_id` | Distinct names prevent selection confusion |
| "Searches things" | "Searches the knowledge base for product docs. Use when: product questions. Do NOT use for: account-specific questions" | When-to and when-not-to in every description |
| (let model choose freely) | "Before calling any tool, check whether the answer is already in conversation context" | Prevents unnecessary tool calls |
| (no confirmation step) | "For destructive operations (delete, send, modify), show a dry-run preview before executing" | Catches misfires before they cause damage |
| (no reasoning required) | "Before each tool call, state: TOOL REASONING: [why this tool, not the others]" | Forces deliberate selection over reflexive action |

## Before → After

**Before:**
```
You have access to these tools: search, query, lookup, find.
Answer the user's question using the appropriate tool.
```

**After:**
```
Tools (read each description carefully before selecting):

1. search_kb(query: str)
   Searches product documentation and FAQ.
   Use for: product features, pricing, setup help.
   Do NOT use for: customer-specific account data.

2. lookup_account(email: str)
   Retrieves account details for a specific user.
   Use for: billing status, plan info, account settings.
   Requires: user's email. If not provided, ASK first.

3. create_ticket(subject, priority, body)
   Creates a ticket for human review.
   Use ONLY when: search and lookup cannot resolve the issue,
   OR user explicitly requests a human.
   Consequence: a human agent will act on this ticket.

4. escalate_to_human(reason: str)
   Transfers the conversation to a human agent.
   Use when: safety concern, legal question, or the user
   is frustrated and requests a person.

Routing:
- Try search_kb first for info questions.
- Try lookup_account for account questions.
- Escalate only after attempting resolution.
- NEVER call a tool if the answer is in the conversation.
```

## Try This Now

```
I'll describe an agent with three tools. You'll get
three user messages. For each, pick the right tool
and explain your reasoning — including which tools
you ruled out and why.

Tools:
- get_weather(city: str) — returns current weather
- get_forecast(city: str, days: int) — returns N-day forecast
- search_news(query: str) — searches recent news articles

Messages:
1. "Will it rain in Seattle tomorrow?"
2. "What's the temperature in Seattle right now?"
3. "Why has Seattle been having unusual weather lately?"

For each, show your tool selection reasoning. Then:
identify which message is most likely to cause a
misfire if the tool descriptions were vaguer.
```

## When It Breaks

- **The synonym trap** — Two tools with similar names or descriptions. `search_users` (full-text search across profiles) vs. `find_user` (lookup by exact ID). The model calls the wrong one, returning hundreds of partial matches instead of one exact result. Fix: rename for maximum semantic distance. Add negative examples: "Do NOT use this for ID-based lookup."
- **The eager agent** — The model is biased toward action. Given a question it could answer from context, it calls a tool anyway because tool use feels more thorough. Fix: "Before calling any tool, verify whether the information is already in the conversation."
- **Parameter hallucination** — The model invents plausible-looking but wrong parameter values — a customer ID in the right format but for the wrong customer. Fix: validate parameters against available data before execution. Retrieve IDs from context; don't let the model fabricate them.

## Quick Reference

- **Family:** Failure mode
- **Adjacent:** → tool selection (the decision process where misfires originate), → escalation (the correct response when the model is unsure — misfire is what happens when it guesses instead), → orchestration (manages tool routing and can prevent misfires through validation)
- **Model fit:** Frontier models select correctly ~90-95% of the time with good descriptions, dropping to ~70-80% with ambiguous ones. Smaller models misfire frequently even with good descriptions — benefit from routing constraints and few-shot examples. For all models, tool description quality is the single largest lever for reducing misfires.
