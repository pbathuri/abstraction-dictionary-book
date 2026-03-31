# tool selection

> How an agent chooses which tool to call — the decision that connects reasoning to action in the world.

## The Scene

Clap/OpsPilot, the customer-support agent, had five tools: `search_kb`, `lookup_account`, `check_order`, `create_ticket`, `calculate_refund`. A user asked: "How much would my refund be if I cancel mid-cycle?" The agent called `search_kb("refund policy")` — reasonable — read the policy, then called `calculate_refund(account_id=user.id, cancel_date=today)`. Correct tool, correct parameters, correct sequence. The answer came back with the exact dollar amount. Clean.

Then a different user asked: "What's 15% of $230?" The agent called `calculate_refund(amount=230, percentage=15)`. Wrong tool. `calculate_refund` requires an account ID and hits the billing system. The agent used a domain-specific tool for a general arithmetic question it could have answered without any tool call at all.

The fix had two parts. First, I added to each tool description: "Do NOT use for: [specific misuse cases]." Second, I added a routing instruction: "If you can answer from general knowledge or simple math, answer directly without calling any tool." The unnecessary tool calls dropped by half. The wrong-tool calls dropped by 80%.

## What This Actually Is

An agent receives a task and a list of tools — each with a name, description, and parameter schema. The agent reads the task, considers the tools, and decides: for this task, I need tool X with parameters Y. The decision is generated as structured output (JSON), which the runtime executes.

The quality depends almost entirely on **tool descriptions** — the description is the tool's resume, and if it's vague, the model makes bad hiring decisions. Selection accuracy degrades with tool count. An agent with 3 tools evaluates all options. An agent with 30 plays favorites. Production systems manage this through **tool scoping**: showing each agent only the tools relevant to its current task.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "search: searches things" | "search_kb(query: str): Searches internal docs. Use for product features, pricing, compatibility. NOT for customer-specific data" | Specific scope + negative scope in every description |
| "Use the right tool" | "If question mentions a specific customer → lookup_account. If general knowledge → search_kb. If answer is in context → no tool" | Decision tree beats open-ended choice |
| (show all 15 tools) | Show only the 3-4 tools relevant to the current task | Tool scoping reduces the decision space |
| (no reasoning required) | "Before calling a tool, state: REASONING: what I need, why this tool provides it, why not the others" | Forced reasoning catches bad selections before execution |
| "You have access to tools" | Include one example of a correct tool call AND one example where no tool is needed | Few-shot examples of correct selection > paragraphs of description |

## Before → After

**Before:**
```
You have these tools: search, lookup, calculate, create.
Answer the user's question.
```

**After:**
```
Tools (select ONLY when the task requires it):

1. search_kb(query: str)
   What it does: Searches product docs, policies, how-to guides.
   Use when: product features, pricing, setup questions.
   Don't use for: account-specific or order-specific questions.

2. lookup_account(email: str)
   What it does: Retrieves account details.
   Use when: billing, subscription, account settings.
   Requires: user's email. If not provided, ask first.

3. check_order(order_id: str)
   What it does: Returns order status and details.
   Use when: user provides an order number.
   Don't use for: general product questions.

Decision rules:
- Try search_kb first for information questions.
- Try lookup_account for account-specific questions.
- If you can answer from general knowledge → don't call any tool.
- If unsure which tool → state your uncertainty, don't guess.
```

## Try This Now

```
I'll give you an agent with 4 tools and 5 user questions.
For each question, decide: (a) which tool to call, or
(b) answer directly with no tool.

Tools:
- web_search(query) — public internet search
- db_query(sql) — read-only SQL against customer database
- calculate(expression) — evaluates math expressions
- send_email(to, subject, body) — sends an email

Questions:
1. "What's the capital of France?"
2. "How many orders did customer #4521 place last month?"
3. "What's 847 * 0.085?"
4. "Send a follow-up email to the customer about their ticket"
5. "What's the current stock price of AAPL?"

For each: state your tool choice (or "no tool"), your
reasoning, and one thing that could go wrong with that
choice. For question 4, explain why this requires extra
caution.
```

## When It Breaks

- **Tool-happy agents** — The model calls tools for every query, including "What is the capital of France?" Fix: explicitly instruct when NOT to call tools. "If the question can be answered from general knowledge, answer directly."
- **Description-driven hallucination** — Vague descriptions let the model infer capabilities the tool doesn't have. It calls "search" expecting internet results but the tool only searches a local database. Fix: state what the tool does AND what it does not do. Specify the scope of its data.
- **Favorite-tool bias** — With many tools available, the model over-uses the 2-3 it's most familiar with and neglects others. Fix: scope tools per task (show only relevant tools) or add routing rules that explicitly mention less-common tools.

## Quick Reference

- **Family:** Agent workflow
- **Adjacent:** → routing (system-level dispatch; tool selection is agent-level dispatch), → tool misfire (what happens when selection goes wrong), → delegation (inter-agent assignment; tool selection is agent-to-tool invocation), → orchestration (the broader coordination that includes tool-using agents)
- **Model fit:** Frontier models correctly select from 10+ tools with clear descriptions. Midsize models handle 3-5 reliably but struggle with larger sets. Small models are unreliable selectors — scope to 1-2 relevant tools per turn or hard-code routing that bypasses model selection. For all tiers, better descriptions improve selection more than model upgrades.
