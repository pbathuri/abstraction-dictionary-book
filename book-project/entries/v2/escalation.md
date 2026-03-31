# escalation

> Routing a problem upward when the current agent can't handle it — the admission of limits that prevents confident nonsense.

## The Scene

Your Clap tier-1 support agent handles FAQs and status checks on a fast, cheap model. A customer writes in about a $15,000 billing discrepancy and threatens legal action. The tier-1 agent doesn't have account access, doesn't have authority to issue credits, and definitely shouldn't be improvising policy.

Without escalation rules, the agent does what models do: generates a confident-sounding response anyway. It might hallucinate a refund policy. It might promise something your company can't deliver.

With escalation rules: the agent detects "financial amount > $10,000" and "legal threat," packages the context — what was tried, why it's escalating, the customer's sentiment — and routes it to a tier-2 agent with account access, or to a human.

The admission of limits is the feature, not the failure.

## What This Actually Is

Escalation is what happens when an agent hits a boundary it can't cross — lacking capability, authority, information, or confidence — and routes the problem upward instead of guessing.

Three components are required: a **trigger** (the agent knows *when* to escalate), a **target** (it knows *where* to send the problem), and a **context package** (it tells the receiver what happened and why). Without all three, escalation is just a transfer of ignorance.

The hardest part is the trigger. Models are bad at knowing what they don't know. "Escalate when unsure" produces either constant escalation (too cautious) or none (too confident). Effective triggers are structural, not emotional:

- "Escalate when the request requires tool access you don't have"
- "Escalate when financial amounts exceed $10,000"
- "Escalate when you can't find a source for a factual claim"
- "Escalate when the user explicitly asks for human review"

Escalation is the inverse of delegation. Delegation sends work down; escalation sends problems up. In a well-designed system, they form a cycle — tasks flow down, exceptions flow up, and the system converges on solutions.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| (no escalation path — the agent just guesses) | "If you cannot answer with confidence, respond: ESCALATE: [reason] \| Summary: [one sentence]" | Structured signal instead of confident fabrication |
| "Try your best" | "Exhaust your own capabilities first. If still unresolved, escalate with what you tried." | Prevents escalation flooding while ensuring it happens when needed |
| "Ask for help if needed" | "ESCALATION RULES: account mutations → tier-2. Confidence < 0.7 → tier-2. Legal threats → human." | Specific, structural triggers, not vibes |
| (escalation without context) | "When escalating, include: original request, actions taken, reason for escalation, customer sentiment score" | Context package prevents the receiver from starting over |

## Before → After

**Before:**
```
Answer the customer's question about their billing.
```

**After:**
```
You are a tier-1 support agent. Answer billing questions
using the knowledge base provided.

ESCALATION RULES:
- Account-level access needed (refunds, credits, plan changes):
  ESCALATE: account_access_required | Summary: [request]
- Can't find the answer after checking the knowledge base:
  ESCALATE: knowledge_gap | Attempted: [what you searched] | Summary: [question]
- Customer expresses intent to cancel or threatens legal action:
  ESCALATE: retention_risk | Urgency: high | Summary: [situation]

Do NOT guess. Do NOT make up policies. If unsure, escalate.
```

**What changed:** Three structural triggers with defined outputs. The agent knows exactly when to admit its limits and how to package the handoff.

## Try This Now

```
You are a tier-1 technical support agent. You can answer
questions about our product's features, common troubleshooting
steps, and account settings. You CANNOT access user accounts,
modify data, or make exceptions to policies.

Here are three customer messages. For each, decide: answer
directly, or escalate? If escalating, format as:
ESCALATE: [reason] | Attempted: [what you can tell them] | Summary: [request]

1. "How do I reset my password?"
2. "I was charged twice for my subscription last month."
3. "Your API keeps returning 500 errors on the /users endpoint."

After handling all three, explain your reasoning for each decision.
```

## When It Breaks

- **Escalation flooding** → Trigger is too sensitive; the agent escalates everything. The target is overwhelmed. Fix: tune thresholds, require the agent to attempt resolution first, implement escalation budgets.
- **Context-free escalation** → The agent escalates but doesn't say why. The receiver starts from scratch. Fix: require structured escalation reports.
- **Missing terminal target** → Agent A escalates to B, B escalates to C, C has nowhere to go. Fix: always designate a terminal target (typically a human or hard-coded fallback).

## Quick Reference

- Family: agent workflow
- Adjacent: → checkpoint (escalation often triggered at checkpoints), → audit_trail (escalation events should be logged), → feedback_loop (escalation patterns inform system improvement)
- Model fit: Frontier models follow explicit escalation rules reliably. Smaller models tend to over-escalate (too cautious) or under-escalate (too confident). For smaller models, use structural triggers — keyword matching, tool availability checks — rather than relying on self-assessment.
