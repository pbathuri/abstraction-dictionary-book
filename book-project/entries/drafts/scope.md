---
headword: "scope"
slug: "scope"
family: "core_abstraction"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# scope

**Elevator definition**
Scope defines the boundaries of what a prompt addresses — what is included, what is excluded, and where the model should stop — functioning as the fence around the model's attention.

## What it is

Every prompt defines a territory. Scope is the act of drawing the border. What is inside the border gets attention, reasoning, and output. What is outside gets ignored. The problem is that if you do not draw the border yourself, the model draws one for you — and the model's default border is "everything I can think of that might be relevant," which is almost always too much.

Consider the instruction "Analyze this company's performance." That prompt has no scope. The model must decide: Performance over what time period? Financial performance, operational performance, market performance? Compared to what — its own history, competitors, industry benchmarks? The model will make reasonable choices, but they will be its choices, not yours. Scope is how you make those choices explicit.

Scope operates on multiple dimensions simultaneously. **Temporal scope** bounds the time period: "Q3 2025" versus "the last five years" versus "since the acquisition." **Domain scope** bounds the subject area: "focus on supply chain operations, not marketing" versus "consider only the regulatory implications." **Depth scope** bounds how far the model should go: "provide a high-level overview" versus "conduct a detailed analysis with specific metrics." **Coverage scope** bounds what entities are included: "compare these three competitors only" versus "survey the full competitive landscape."

What makes scope distinct from → specificity is that specificity narrows what the model *does*, while scope limits what the model *considers*. A specific prompt says "identify the top three risks." A scoped prompt says "considering only the financial data from Q3, identify the top three risks." Specificity without scope is focused action on an unbounded field. Scope without specificity is a bounded field with no clear action. You need both, but they do different work.

Scope is also distinct from → framing. Framing orients *how* the model interprets material — the angle, the lens, the perspective. Scope determines *what material* the model interprets. A financial analyst frame with no scope produces financial analysis of everything. A narrow scope with no frame produces bounded but undirected output. The two are complementary: scope selects the material, framing determines the approach.

## Why it matters in prompting

Unscoped prompts produce three predictable problems. First, the output is too broad — the model tries to address everything and addresses nothing deeply. Second, the output contains irrelevant material that the user must filter manually, which defeats the purpose of using a model. Third, the model burns tokens on material outside the user's interest, reducing the quality of attention available for the material that matters.

Explicit scope statements are cheap and effective. Adding a single sentence — "Focus exclusively on the European market" or "Consider only the period from January to June 2025" or "Exclude pricing strategy; that is handled separately" — can transform a rambling, diffuse output into a focused one. Negative scope (stating what to exclude) is particularly powerful because models are biased toward inclusion. Left to their own devices, they will address adjacent topics, provide caveats, and hedge with context. Telling them what to leave out is often more effective than telling them what to include.

The hardest part of scope is knowing what to exclude. This requires the human to have already thought about the problem deeply enough to know its boundaries. Scope failures are often thinking failures: the prompt is unscoped because the user has not yet decided what they actually want.

## Why it matters in agentic workflows

In multi-agent pipelines, scope leakage is a primary source of waste and error. When a planner agent delegates a task with insufficient scope, the executor agent either over-delivers (spending tokens on unnecessary analysis) or addresses the wrong aspect (interpreting scope by default rather than by instruction).

Each agent in a pipeline should receive an explicit scope statement that bounds its work. This is more than a task description — it is a declaration of territory. "You are responsible for financial risk analysis of the attached contract. Operational risks, legal risks, and reputational risks are handled by other agents. Do not address them. If you encounter something that falls outside your scope, note it briefly and pass it to the Router Agent for reassignment."

Scope also governs context passing between agents. When Agent A hands off to Agent B, the handoff should include only the information within Agent B's scope, plus a minimal orientation summary. Passing everything creates noise. Passing too little creates gaps. Scope statements at each boundary define what crosses and what stays.

## What it changes in model behavior

Explicit scope constraints reduce output length, increase relevance density, and decrease the frequency of tangential content. When a model knows what is out of scope, it does not need to hedge against the possibility that you wanted it addressed. This produces more confident, more direct output. It also reduces the "everything-but-the-answer" pattern where the model provides extensive context and setup before delivering the actual analysis, because it knows the context outside its scope is not its responsibility.

## Use it when

- When the subject matter is broad and the model could reasonably address many aspects
- When previous prompts produced output that was technically correct but included irrelevant material
- When working in multi-agent pipelines where each agent has a defined territory
- When token budget is limited and you need the model to focus its attention
- When the task is one part of a larger project and you need to prevent overlap with other parts
- When the output will be combined with outputs from other prompts or agents that cover adjacent scope

## Do not use it when

- When you genuinely want an open-ended exploration and do not know the boundaries yet
- When the task is narrow enough that scope is self-evident ("Translate this sentence to Spanish")
- When premature scoping might cause the model to miss something important that you had not anticipated

## Contrast set

- → framing — framing determines the angle of analysis; scope determines the territory of analysis. Scope is what you look at. Framing is how you look at it.
- → specificity — specificity narrows the action (what to do and how much detail); scope limits the domain (what material to consider). A specific prompt on an unscoped domain produces detailed analysis of the wrong thing.
- → constrain — constraints limit the model's output (format, length, style); scope limits the model's input consideration. Constraints shape the response. Scope shapes the attention.

## Common failure modes

- **Implicit scope** → Assuming the model will intuit the boundaries from context. "Analyze the Q3 report" seems scoped, but the model may address financial metrics, operational highlights, forward guidance, risk factors, and management commentary. If you only want financial metrics, say so.
- **Scope creep via helpfulness** → Models are trained to be helpful, which often means providing more than asked for. A model asked to "summarize the marketing section" may also summarize the sales section because it seems related. Negative scope ("do not address sales, operations, or finance") prevents this.
- **Scope too narrow for the question** → Scoping so tightly that the model cannot produce a useful answer. "Based only on paragraph 3, explain the company's overall strategy" asks the model to derive a broad conclusion from insufficient scope. Scope should match the question's requirements.

## Prompt examples

### Minimal example

```text
Review the attached performance report.
Focus exclusively on customer retention metrics.
Do not address acquisition, revenue, or product metrics —
those are covered in separate analyses.
Identify the three retention metrics that changed most
quarter-over-quarter.
```

### Strong example

```text
You are a cybersecurity analyst reviewing a penetration test report.

Scope:
- IN SCOPE: findings related to network infrastructure
  (firewalls, routers, switches, VPN endpoints)
- OUT OF SCOPE: application-layer vulnerabilities (these are
  handled by the AppSec team), social engineering findings,
  and physical security findings
- TIME PERIOD: findings from the March 2026 test only;
  ignore references to historical findings from prior tests

For each in-scope finding:
1. State the affected asset (hostname or IP)
2. Classify severity as CRITICAL, HIGH, MEDIUM, or LOW
   using CVSS 3.1 base score ranges
3. State the recommended remediation in one sentence
4. Estimate remediation effort as: hours, days, or weeks

If a finding spans your scope and another team's scope
(e.g., a network misconfiguration that enables an application
vulnerability), include it but flag it as CROSS-SCOPE and
note which other team should be consulted.
```

### Agentic workflow example

```text
Pipeline: Quarterly Business Review Generator

Scope Assignments:

Agent: Financial Analyst
Scope: Revenue, costs, margins, cash flow from the Q1 2026
financial statements. Exclude non-financial metrics.
If you encounter operational or market data, ignore it —
other agents cover those areas.

Agent: Operations Analyst
Scope: Supply chain efficiency, fulfillment rates, production
metrics from the Q1 2026 operations dashboard. Exclude
financial data (costs, revenue) — even if you see it in your
source material, do not analyze it.

Agent: Market Analyst
Scope: Market share, competitive positioning, customer
sentiment from the Q1 2026 market research report. Exclude
internal operational and financial data.

Agent: Synthesis Agent
Scope: All outputs from the three analysts above. Your job
is to identify where financial, operational, and market
findings intersect or conflict. Do not re-analyze the source
data — work only from the analyst outputs. If an analyst's
output seems incomplete, flag the gap rather than filling it.
```

## Model-fit note

Scope compliance is generally strong across model tiers for simple boundary conditions ("only discuss X"). It weakens for negative scope ("do not discuss Y") in smaller models, which are more prone to mentioning excluded topics briefly before moving on. Frontier models handle complex, multi-dimensional scope well. For all tiers, explicit scope at the beginning of the prompt is more effective than scope buried in the middle, because early tokens set the attention frame for everything that follows.

## Evidence and provenance

The Prompt Report discusses scope-related prompt components under task specification and output formatting [src_paper_schulhoff2025]. The interaction between scope and model attention is related to research on "lost in the middle" effects in long-context models. Sahoo et al. (2025) address scope implicitly in their discussion of task-specific prompting strategies [src_paper_sahoo2025].

## Related entries

- → framing — scope selects what the model considers; framing determines how it considers it. Both are needed for focused output.
- → specificity — specificity narrows what the model does; scope narrows what the model considers. They operate on different dimensions of the same prompt.
- → constrain — constraints limit output; scope limits input attention. A scoped, constrained prompt is tightly controlled on both sides.
