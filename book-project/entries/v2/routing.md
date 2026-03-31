# routing

> The traffic-cop decision — which agent, model, or processing path handles this input — made before any actual work begins.

## The Scene

Clap/OpsPilot handles support messages for a workflow-automation product. Early architecture: every message went to the same model with the same system prompt. "I want to cancel my subscription" got the same treatment as "ERR-4502 when running the sync node." The billing question got a technically flavored response. The bug report got an empathetic one. Both wrong.

The fix was a three-layer router. Layer 1: keyword rules. Contains "cancel" or "unsubscribe"? Route to the retention agent. Contains an error code pattern (ERR-\d+)? Route to the technical agent. Layer 2: a small fine-tuned classifier for messages the rules miss. Confidence above 0.85? Route to the selected agent. Below 0.85? Pass to Layer 3 — a frontier model that reads the message carefully, considers whether parallel routing to multiple agents is needed, and flags messages that need human clarification.

Result: 80% of messages handled by Layer 1 (fast, free). 15% by Layer 2 (fast, cheap). 5% by Layer 3 (slower, expensive, but only for genuinely ambiguous inputs). Average latency dropped. Accuracy went up. Cost per message went down.

## What This Actually Is

Routing decides where work goes. It's the first decision in any non-trivial pipeline, and often the most consequential. A brilliant analysis agent can't compensate for being routed the wrong task. Routing can be rule-based (fast, brittle), classifier-based (handles paraphrases, needs training data), or LLM-based (most flexible, most expensive). Production systems layer all three.

Model routing is the cost-optimization variant: simple greeting goes to a cheap model, complex legal analysis goes to a frontier model. At 100K queries/day, routing 70% to the cheap tier saves thousands daily.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Handle this message" | "Classify into: billing, technical, retention, feedback, other. Return only the category" | Explicit categories make routing deterministic |
| "Figure out what they need" | "Select the best-fit agent. If ambiguous, select 'triage' for human review" | Triage path prevents confident misroutes |
| "Use the right tool" | "If question mentions a customer → query_database. If general knowledge → search_web" | Decision tree beats open-ended selection |
| "Route to the best model" | "Simple greetings → small model. Multi-step reasoning → frontier model. Math → reasoning model" | Model routing by task type optimizes cost |
| "If unclear, just try" | "If confidence is 'low,' always select 'triage' regardless of your best guess" | Low-confidence default to human prevents errors |

## Before → After

**Before:**
```
You are a customer support agent. Help the user with
whatever they need.
```

**After:**
```
You are a routing classifier. Read the user message and
select the best-fit agent:

- billing_agent: payment issues, refunds, pricing
- technical_agent: bugs, errors, integration help
- retention_agent: cancellation, downgrade, dissatisfaction
- feedback_agent: feature requests, compliments
- triage: ambiguous or multi-topic messages

Output JSON:
{
  "selected_agent": "agent_name",
  "confidence": "high | medium | low",
  "reasoning": "one sentence"
}

If confidence is "low", always select "triage."
```

## Try This Now

```
I'll give you 5 customer messages. For each, decide:
which specialist should handle it? Pick from:
billing, technical, retention, or triage (ambiguous).

Also rate your confidence (high/medium/low).

1. "My credit card was charged twice this month"
2. "The API returns a 500 error on POST /webhooks"
3. "I love the product but I'm thinking of switching
   to a competitor because the price went up"
4. "Can you help me?"
5. "I need to downgrade my plan and also fix a bug
   in the export feature"

For message 5, explain why single-category routing
fails and what a multi-route solution looks like.
```

## When It Breaks

- **Misroute to confidence** — Router sends an ambiguous message to a specialist that handles it confidently but incorrectly. "Interest rates" routes to banking when the user meant "topics of interest." Include a triage path for ambiguous inputs.
- **Router as bottleneck** — An LLM router processing every input at frontier cost, even trivially classifiable ones. Tier the routing: rules first, classifier second, LLM only for the genuinely hard cases.
- **Static routing, dynamic inputs** — Rules designed for the original input distribution. New input types appear and get force-fit into old categories. Monitor routing accuracy and update when performance degrades.

## Quick Reference

- **Family:** Agent workflow
- **Adjacent:** → orchestration (the full management system; routing is one function within it), → tool selection (routing within an agent — which tool to call), → delegation (the assignment that routing targets)
- **Model fit:** Routing classifiers should use the smallest model that achieves acceptable accuracy. Fine-tuned small models typically outperform prompted large models on well-defined routing and cost 10-100x less per decision. Reserve LLM routing for genuinely ambiguous cases.
