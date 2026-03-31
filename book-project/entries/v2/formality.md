# formality

> The distance between "Hey, this thing broke" and "We have identified a service degradation" — and why the model needs you to pick one.

## The Scene

I was building the AI Ethics Coach Chrome extension and needed it to produce two types of output from the same ethical analysis: one for the developer using the tool (direct, casual, "here's what to watch for") and one for the compliance report the developer could hand to their manager (no contractions, third person, hedged claims). Same facts. Same structure. Completely different clothes.

The first version had one prompt for both. The output landed in a no-man's-land — too stiff for the developer, too casual for the report. I split it into two prompts with explicit formality markers: the developer version said "use contractions, address as 'you,' keep sentences under 20 words." The report version said "no contractions, third person, define all terms on first use." Same analysis engine, two register settings. Both felt right for their audience.

## What This Actually Is

Formality is where your language sits on the spectrum from boardroom to group chat. Models have a default — boringly middle-of-the-road, slightly hedged, slightly impersonal. It's the linguistic equivalent of hotel art: acceptable everywhere, perfect nowhere. Without explicit formality cues, every output sounds like it was written by the same cautious middle manager.

The fix is cheap and high-leverage. Adding 3-5 specific formality markers shifts output dramatically. Not the word "formal" — that's too broad. Academic formal, legal formal, corporate formal, and Japanese business formal are radically different registers that one label doesn't distinguish.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Write formally" | "No contractions. Third person. Sentences average 20-25 words. Hedge uncertain claims with 'suggests' or 'indicates'" | Markers, not a label |
| "Keep it casual" | "Use contractions. Address the reader as 'you.' One idea per sentence. Concrete examples over abstract principles" | Specific informality the model can execute |
| "Professional tone" | "Like a well-written Slack post in a professional channel — direct, no throat-clearing, lead with what changed" | An anchoring reference the model can match |
| "Make it friendly" | "First person plural ('we'). Conversational, as if explaining to a technically literate friend. Enthusiasm OK but don't oversell" | Friendly with guardrails |
| "Academic style" | "Passive voice for methods. Active for results. Define terms on first use. Cite parenthetically. No rhetorical questions" | Domain-specific formality checklist |

## Before → After

From the AI Ethics Coach — the actual prompt split:

> **Before (one-size-fits-none)**
> ```
> Analyze this code snippet for ethical concerns. Provide
> findings in a professional manner suitable for developers
> and management.
> ```
>
> **After (developer version)**
> ```
> You're reviewing code for ethical red flags. Talk to the
> developer directly:
> - Use "you" and "your code"
> - Contractions are fine
> - Lead each finding with what to fix, then why it matters
> - Skip preambles. First sentence = first finding
> ```
>
> **After (compliance report version)**
> ```
> Produce a compliance-ready ethics assessment:
> - No contractions
> - Third person ("the application" not "your app")
> - Each finding: description, risk level, remediation,
>   regulatory reference
> - Hedging: "may indicate" for uncertain, "demonstrates"
>   for confirmed
> ```
>
> **What changed:** The developer version reads like a senior teammate's code review. The compliance version reads like something legal can file. Same facts, different formality — and the audience trusts both.

## From the Lab

We tested the same factual content delivered through different register settings and measured how evaluators perceived quality:

![Same Content, Different Register](../art/figures/exp_same_content_different_register_register.png)

**Key finding:** Formality-matched output was rated 25-40% higher in quality assessments even when the factual content was identical to mismatched output. The strongest effect was when formal content was presented casually — evaluators perceived it as less credible. The lesson: formality isn't cosmetic. It's a trust signal.

## Try This Now

Take any recent LLM output that felt "off" but was factually fine. Paste it with this:

```
This text has the right content but the wrong formality for
its audience. The audience is: [describe them].

Rewrite it with these formality markers:
- Contractions: [yes/no]
- Person: [first/second/third]
- Sentence length: [range]
- Hedging: [when to hedge, when to assert]

Don't change the facts. Only change the register.
```

You'll see how much of "it doesn't sound right" is a formality problem, not a content problem.

## When It Breaks

- **Label without markers** — "Write formally" means nothing specific. The model's idea of formal may not match yours. Always describe formality through 3-5 linguistic features: contractions, sentence length, vocabulary level, voice, hedging behavior.
- **Register drift in long outputs** — The intro is formal, the middle relaxes, the conclusion stiffens again. Reinforce formality markers at section boundaries, or run a post-generation consistency check.
- **Formality fighting content** — Highly technical content forced into extreme casualness sounds condescending. Casual content in legal register sounds absurd. Let formality serve the content, not the other way around.

## Quick Reference

- **Family:** Tone and style
- **Adjacent:** → register (formality is one axis of register), → perspective (shapes what to say; formality shapes how to say it), → audience specification (the audience determines the right formality level)
- **Model fit:** All models respond to formality instructions. Frontier models handle subtle gradations ("board presentation formal" vs. "technical documentation formal"). Smaller models handle broad strokes (formal vs. informal). For any model, 3-5 specific markers beat a single-word label.
