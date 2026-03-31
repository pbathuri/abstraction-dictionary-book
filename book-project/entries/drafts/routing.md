---
headword: "routing"
slug: "routing"
family: "agent_workflow"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# routing

**Elevator definition**
Routing is the decision of which agent, tool, model, or processing path handles a given input — the traffic direction that determines where work goes before it begins.

## What it is

Every system that can do more than one thing must decide, for each input, which thing to do. A customer writes "I want to cancel my subscription" — does this go to the billing agent, the retention agent, or the general support agent? A user uploads a document — does the pipeline send it to the summarizer, the translator, or the data extractor? A query arrives — does it get routed to the fast, cheap model or the slow, expensive one? These are routing decisions, and they happen before any actual work takes place.

Routing is the first decision in any non-trivial pipeline, and it is often the most consequential. A brilliantly designed analysis agent cannot compensate for being routed the wrong task. A carefully tuned billing response cannot help if the customer's message was misclassified and sent to the FAQ bot instead. The downstream quality ceiling is set at the routing layer: route correctly, and the pipeline has a chance. Route incorrectly, and nothing downstream can recover.

Routing can be **rule-based**, **classifier-based**, or **LLM-based**. Rule-based routing uses deterministic logic: if the input contains the word "cancel," route to billing; if it contains "bug," route to engineering. This is fast, cheap, transparent, and brittle. It breaks on paraphrases ("I'd like to stop my service"), ambiguity ("cancel the meeting" in a scheduling context), and novel phrasings the rules didn't anticipate.

Classifier-based routing uses a trained model — typically a small, fast model fine-tuned on labeled routing examples — to categorize inputs. A classifier might output `{billing: 0.85, support: 0.12, retention: 0.03}` and the system routes to the highest-confidence category. This handles paraphrases and novel phrasings better than rules, at the cost of needing training data and occasionally misclassifying edge cases. Classifier-based routing is the workhorse of production systems because it is fast (milliseconds), cheap (small model inference), and good enough for well-defined categories.

LLM-based routing uses a language model to interpret the input and decide the route. The model reads the input, considers descriptions of available agents or tools, and selects the appropriate destination. This is the most flexible approach — the LLM can handle ambiguity, interpret intent, and even route to multiple destinations when the input requires parallel processing. It is also the most expensive, the slowest, and the most opaque. When an LLM routes incorrectly, diagnosing why is harder than with a rule or classifier, because the LLM's decision is embedded in a probability distribution rather than a readable condition.

In practice, production systems layer these approaches. Fast rules handle the clear cases. A classifier handles the common cases the rules miss. An LLM handles the ambiguous cases the classifier can't resolve. This tiered architecture minimizes cost and latency for the 80% of inputs that are straightforward while preserving flexibility for the 20% that require judgment.

Routing also encompasses **model routing**: selecting which model processes a task based on its complexity, cost sensitivity, or required capability. A simple greeting routes to a small, cheap model. A complex legal analysis routes to a frontier model. A math problem routes to a reasoning-specialized model. Model routing optimizes cost-quality trade-offs across the pipeline, which matters enormously at scale. An enterprise handling 100,000 queries per day that routes 70% to a model costing $0.001/query instead of $0.03/query saves $2,000 daily without quality loss on those simple queries.

## Why it matters in prompting

Even in single-model prompt chains, routing logic exists implicitly. A prompt that says "If the user asks a factual question, cite sources. If the user asks for creative writing, do not cite sources" contains a routing decision inside the prompt. The model must classify the input before generating the output. Making this routing explicit — separating the classification step from the generation step — produces more reliable results because the model handles one task at a time.

Routing also matters when choosing *which prompt* to use. A system with five specialized prompts (one for technical questions, one for policy questions, one for complaints, one for feedback, one for small talk) needs a router that reads the incoming message and selects the appropriate prompt before generation. The router is the most important component in such a system, and it is the one most often built hastily.

## Why it matters in agentic workflows

Routing is the nervous system of a multi-agent architecture. The → orchestrator may manage the overall flow, but routing makes the individual dispatch decisions: this task goes to Agent A, that task goes to Agent B, this ambiguous task goes to a triage agent for further classification.

Routing failures in agentic workflows are particularly dangerous because they compound. An input routed to the wrong agent produces output that downstream agents treat as authoritative. The wrong agent may not fail visibly — it will simply produce an answer from the wrong domain, and that answer will be wrong in ways that are hard to detect without domain expertise.

## What it changes in model behavior

Routing does not change how any individual model behaves — it changes *which model or agent* behaves. The impact is on system-level quality: well-routed systems produce consistently better outputs because each component handles tasks it is suited for, rather than forcing a general-purpose agent to handle everything.

## Use it when

- The system handles multiple input types that require different processing
- Cost optimization is important and not all inputs require the most expensive model
- Specialized agents exist for different domains and the system must select among them
- The pipeline has conditional branches where different inputs follow different paths
- Latency matters and simple inputs should be processed faster than complex ones

## Do not use it when

- The system has a single agent handling a single task type — routing has nothing to route
- All inputs require the same processing regardless of content
- You are prototyping and the overhead of routing infrastructure exceeds its benefit
- The input space is so narrow that every input goes to the same destination

## Contrast set

- → **orchestration** — Orchestration is the full management of a pipeline: routing, sequencing, state, error handling. Routing is one function within orchestration — the dispatch decision.
- → **tool selection** — Tool selection is a routing decision made by an agent at runtime: which tool should I call? Routing typically refers to the system-level decision of which agent or model handles an input. Tool selection happens *within* a routed agent.
- → **delegation** — Delegation is assigning a task to another agent. Routing is deciding *which* agent to delegate to. Delegation is the assignment; routing is the targeting.
- → **information routing** — Information routing decides what *data* goes where. Routing (this entry) decides what *work* goes where. Related but distinct: routing dispatches tasks, information routing dispatches context.

## Common failure modes

- **Misroute to confidence** — The router assigns an input to a specialized agent that handles it confidently but incorrectly, because the input was ambiguous and the agent interprets it within its own narrow domain. A question about "interest rates" routes to a banking agent when the user meant "topics of interest." Fix: include a triage or clarification path for ambiguous inputs, and monitor routing accuracy with labeled samples.

- **Router as bottleneck** — An LLM-based router becomes the slowest and most expensive component in the pipeline, processing every input at frontier-model cost even when most inputs are trivially classifiable. Fix: tier the routing — rules first, classifier second, LLM only for genuinely ambiguous inputs.

- **Static routing for dynamic needs** — The routing rules were designed for the system's original input distribution, which has since changed. New input types are forced into old categories, producing systematic misrouting. Fix: monitor routing decisions, measure downstream quality per route, and update routing logic when accuracy degrades.

## Prompt examples

### Minimal example

```text
Classify the following user message into one of these
categories: billing, technical_support, feedback, other.

Return only the category name, nothing else.

User message: "My payment failed twice and I'm locked out"
```

### Strong example

```text
You are a routing classifier. Read the user message and
select the best-fit agent from the list below. If the
message is ambiguous, select "triage" for human review.

Available agents:
- billing_agent: subscription changes, payment issues,
  refunds, pricing questions
- technical_agent: bugs, errors, feature questions,
  integration help
- retention_agent: cancellation requests, downgrade
  requests, expressions of dissatisfaction
- feedback_agent: feature requests, compliments, surveys
- triage: ambiguous or multi-topic messages

Output format (JSON):
{
  "selected_agent": "agent_name",
  "confidence": "high | medium | low",
  "reasoning": "one sentence explanation"
}

If confidence is "low", always select "triage" regardless
of your best guess.
```

### Agentic workflow example

```text
Pipeline: Tiered Routing System

Layer 1 — Rule-Based Pre-Router (code, not LLM)
Rules:
  - Contains "cancel" or "unsubscribe" → retention_agent
  - Contains "invoice" or "payment" → billing_agent
  - Contains error code pattern (ERR-\d+) → technical_agent
  - No rule match → pass to Layer 2

Layer 2 — Classifier Router (small fine-tuned model)
Input: User message
Output: { agent: string, confidence: float }
Logic:
  - confidence >= 0.85 → route to selected agent
  - confidence < 0.85 → pass to Layer 3

Layer 3 — LLM Router (frontier model, used for <5% of inputs)
System prompt: You are a routing specialist. The classifier
was uncertain about this message. Read it carefully and
select the appropriate agent. Consider:
  - What is the user's primary intent?
  - Are there secondary intents that require parallel routing?
  - Is additional information needed before routing?
Output:
{
  "primary_agent": "agent_name",
  "secondary_agents": ["agent_name"] or [],
  "needs_clarification": true | false,
  "clarification_question": "string if needed"
}

Monitoring: Log every routing decision with layer, confidence,
and selected agent. Weekly review of Layer 3 decisions to
identify patterns that should become Layer 1 rules or Layer 2
training data.
```

## Model-fit note

Routing classifiers should use the smallest model that achieves acceptable accuracy — routing is a classification task, not a generation task, and large models are wasteful here. Fine-tuned small models (distilled classifiers) typically outperform prompted large models on well-defined routing tasks and cost 10–100x less per decision. Reserve LLM-based routing for genuinely ambiguous cases. When using an LLM router, reasoning-specialized models produce more reliable classifications because they can articulate their decision logic, making misroutes easier to diagnose.

## Evidence and provenance

Routing as a system design pattern is well-established in software architecture (API gateways, message brokers, load balancers). Its application to LLM systems is documented in agent framework literature (LangChain router chains, Semantic Router library) and practitioner guides on multi-agent system design. Model routing for cost optimization is discussed in production deployment literature. The tiered routing pattern (rules → classifier → LLM) is a practitioner convention observed across production chat and support systems.

## Related entries

- **→ orchestration** — the broader system that includes routing as one function
- **→ tool selection** — routing within an agent; choosing which tool to call
- **→ delegation** — the act of assignment that routing targets
- **→ information routing** — routing data rather than tasks
