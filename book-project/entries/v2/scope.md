# scope

> The fence around the model's attention — what's included, what's excluded, and where to stop.

## The Scene

AI Ethics Coach, the project that reviews corporate AI policies. I asked the model: "Analyze this company's AI governance." The response was 1,400 words covering data privacy, algorithmic bias, model transparency, employee surveillance, customer consent, regulatory compliance, international law, and the EU AI Act. Comprehensive. Useless. The stakeholder needed only the gap between the company's current policy and the EU AI Act requirements. Everything else was noise.

The fix was one sentence: "Focus exclusively on gaps between the attached company policy and EU AI Act requirements. Do not address privacy, bias, surveillance, or any other governance topic — those are handled in separate reviews." Output dropped to 400 focused words. Every sentence mapped a specific policy clause to a specific regulation. The model didn't get better. It got boundaries.

## What This Actually Is

Scope defines the territory. What's inside gets attention and output. What's outside gets ignored. If you don't draw the border, the model draws one for you — and the model's default border is "everything I can plausibly connect to this topic," which is always too much.

Scope operates on four axes: **temporal** (Q3 2025 vs. last five years), **domain** (supply chain only, not marketing), **depth** (high-level overview vs. granular metrics), and **coverage** (these three competitors vs. the full landscape). Scope is distinct from specificity — specificity narrows what the model *does*, while scope limits what it *considers*. And distinct from framing — framing shapes *how* the model interprets, scope determines *what* it interprets. Negative scope (stating what to exclude) is particularly powerful because models default toward inclusion.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Analyze the company's performance" | "Analyze Q4 2025 financial performance only. Exclude operations, marketing, and HR" | Draws hard borders on four sides |
| "Review the report" | "Review sections 3-5 only. Sections 1-2 are background. Section 6 is handled separately" | Prevents the model from summarizing everything |
| "What are the risks?" | "What are the cybersecurity risks to network infrastructure? Exclude application-layer, social engineering, and physical security risks" | Negative scope stops the model from being "helpful" beyond the territory |
| "Tell me about the market" | "Focus on the European market for enterprise SaaS, 2024-2026. Ignore consumer, SMB, and non-European segments" | Four-axis scope: domain, geography, time, segment |
| "Summarize the findings" | "Summarize only findings that deviate from the forecast by more than 10%. Skip anything within forecast range" | Threshold-based scope cuts the unremarkable |

## Before → After

**Before:**
```
Review the attached penetration test report and
summarize the findings.
```

**After:**
```
Review the attached penetration test report.

Scope:
- IN SCOPE: Network infrastructure findings (firewalls,
  routers, VPN, switches)
- OUT OF SCOPE: Application-layer vulnerabilities,
  social engineering, physical security
- TIME PERIOD: March 2026 test only. Ignore references
  to historical findings from prior tests.

For each in-scope finding:
1. Affected asset (hostname or IP)
2. Severity: CRITICAL / HIGH / MEDIUM / LOW
3. Recommended remediation (one sentence)
4. Estimated effort: hours / days / weeks

If a finding spans your scope and another team's,
include it but flag as CROSS-SCOPE.
```

## Try This Now

```
Here's a deliberately unscoped prompt. Your job is to
add scope constraints — not answer the prompt, but
tighten its boundaries.

Original: "Analyze our Q1 performance and give me
your thoughts."

Add scope on all four dimensions:
- Temporal: What time period exactly?
- Domain: Which aspect of performance?
- Depth: Overview or deep-dive?
- Coverage: Which products, regions, or teams?

Also add one negative scope statement (something
to explicitly exclude). Show the scoped version and
explain what each scope boundary prevents.
```

## When It Breaks

- **Implicit scope** — Assuming the model intuits the boundary. "Analyze the Q3 report" feels scoped, but the model may address financials, operations, guidance, risk, and management commentary. If you only want financials, say so.
- **Scope creep via helpfulness** — The model provides more than asked. "Summarize the marketing section" yields a bonus summary of sales because it seemed related. Fix: negative scope ("do not address sales, operations, or finance").
- **Scope too narrow for the question** — "Based only on paragraph 3, explain the company's overall strategy." Paragraph 3 can't support that conclusion. Match the scope to what the question actually requires.

## Quick Reference

- **Family:** Core abstraction
- **Adjacent:** → framing (scope selects what to look at; framing determines how to look at it), → specificity (specificity narrows action; scope narrows territory), → constrain (constraints limit output; scope limits input consideration)
- **Model fit:** Simple scope ("only discuss X") is respected across all tiers. Negative scope ("do not discuss Y") weakens in smaller models, which tend to mention excluded topics briefly before moving on. For all models, scope placed at the start of the prompt outperforms scope buried in the middle.
