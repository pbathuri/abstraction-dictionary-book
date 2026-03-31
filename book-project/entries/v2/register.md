# register

> Same facts, different voice. The voice decides who listens.

## The Scene

Form8 — my n8n market research workflow — had just finished a competitive analysis of a productivity SaaS tool. Good data: 8 competitors profiled, pricing tiers mapped, feature gaps identified, three strategic opportunities ranked. One problem: the output had to go to three different people.

The **VP of Strategy** needed a 200-word brief focused on positioning and differentiation. Board-meeting voice. No jargon, no feature lists, just "here's where we win and why."

The **lead investor** in our next round needed a one-pager focused on market size, competitive moat, and revenue potential. Formal, forward-looking, the kind of prose that belongs in a quarterly letter. Numbers first, narrative second.

The **ops team** needed the full breakdown: competitor-by-competitor feature tables, pricing grids, integration compatibility matrices. Technical, dense, organized for reference, not for reading.

Same data. Same analysis. Three registers. I wrote three prompt variants that differed in exactly one dimension: how the model was told to *talk*. The strategist version said "Write for a senior executive making allocation decisions. Lead with the insight, not the evidence." The investor version said "Formal, measured, forward-looking. Emphasize defensibility and TAM. Suitable for inclusion in a fundraising deck." The ops version said "Technical reference format. Tables over prose. Assume the reader will ctrl-F, not read sequentially."

The data was identical in all three outputs. The voice made each one useful to exactly one audience and useless to the other two. That's register.

## What This Actually Is

Register is the constellation of word choice, sentence structure, formality, and assumed familiarity that signals "this was written for someone like you." It's not tone — tone is one ingredient. Register is the whole recipe: vocabulary level, sentence complexity, hedging frequency, directness, use of jargon, assumed context.

A Kubernetes explanation for a developer who's used Docker has a different register than the same explanation for a CTO evaluating infrastructure costs. The developer version uses terms like "pod," "container runtime," and "kubectl" without defining them. The CTO version says "workload isolation" and "infrastructure abstraction" and never mentions a command line. Both are correct. Both are professional. They're written for different brains.

Here's the trap: "Write in a professional tone" is the most common register instruction and the least useful. A lawyer's brief is professional. So is a Slack message from a senior engineer. So is a kindergarten teacher's parent conference note. All professional. None interchangeable. Name the register you actually want: "clinical and precise," "warm but authoritative," "technically dense, no hand-holding."

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Professional tone" | "Write as a senior analyst briefing the board. No jargon, no hedging, lead with the conclusion" | Names the role, audience, and stylistic constraints |
| "Keep it simple" | "Write for a reader who understands the business but not the technology. Define any acronym on first use" | Specifies what "simple" means for this audience |
| "Formal" | "Formal and measured. No contractions. No first person. Suitable for a regulatory filing" | Defines what formal *looks like* in context |
| "Casual" | "Internal Slack voice: short paragraphs, contractions fine, assume the reader knows the codebase" | Specifies the *channel*, not just the vibe |
| "Technical" | "Write for a backend engineer debugging in production. Include error codes, stack references, and exact CLI commands" | Defines the reader's situation, not just their expertise |
| "Friendly" | "Warm and direct. Use 'you' and 'your.' Imagine the reader just signed up and is slightly confused" | Turns a mood into a reader persona |

**Power verbs for register:** calibrate, pitch (to audience), voice (as), adapt, mirror, sustain.

## Before → After

From Form8 — the same competitive data rendered in three registers:

> **Strategic register (for VP of Strategy)**
> ```
> Write a 200-word executive brief on competitive positioning.
> Register: Senior executive making portfolio decisions.
> - Lead with the strategic insight, not the supporting data
> - One paragraph on where we're differentiated, one on the
>   biggest competitive threat, one on recommended action
> - No feature names. No pricing figures. Implications only.
> - Tone: confident, direct, forward-looking
> ```
>
> **Investor register**
> ```
> Write a one-page market summary suitable for a fundraising deck.
> Register: Institutional investor evaluating the opportunity.
> - Open with TAM and growth rate
> - Frame competitive landscape as moat evidence
> - End with revenue trajectory framing
> - Tone: formal, measured, no superlatives. Let numbers carry weight.
> - No exclamation marks. No "exciting." No "revolutionary."
> ```
>
> **Ops register**
> ```
> Produce a technical reference document for the ops team.
> Register: Engineers who will ctrl-F, not read sequentially.
> - Use tables for competitor features, pricing, integrations
> - Include API compatibility notes where available
> - Dense, organized, no narrative padding
> - If data is missing for a competitor, mark the cell as "—"
>   rather than writing around it
> ```
>
> **Same data. Three registers. Three useful documents instead of one mediocre compromise.**

## Try This Now

Paste this into ChatGPT:

```
Take this sentence and rewrite it in 4 different registers.
Keep the facts identical. Change ONLY the voice.

Original: "We reduced API response time by 40% by migrating
from REST to gRPC and implementing connection pooling."

Register 1: Internal Slack message to the eng team
Register 2: Quarterly investor update paragraph
Register 3: Technical blog post for developer audience
Register 4: Product changelog entry for customers

After all four, highlight which words changed between each
version and explain what signal each word choice sends.
```

Notice how "reduced" might become "knocked down" (Slack), "improved" (investor), "optimized" (blog), or "faster" (changelog). Same fact. Four signals.

## From the Lab

We tested how register instructions affected output characteristics across seven dimensions (formality, technicality, hedging, directness, sentence length, vocabulary level, jargon density):

![Same Content, Different Register](../art/figures/exp_same_content_different_register_register.png)

**Key finding:** Explicit register instructions changed output measurably along all seven dimensions. But the effect was asymmetric: it was easier to push a model toward *more* formal or *more* technical registers than toward casual or accessible ones. Models trained on professional text have a gravitational pull toward mid-formal. If you want genuinely casual output, you need to be explicit about what casual means — contractions, short sentences, direct address, incomplete sentences okay.

## When It Breaks

- **Register drift in long outputs** → The model starts in the specified register, then gradually relaxes toward its default mid-formal voice. Especially common in small models and outputs over 500 words. Fix: reinforce the register at section breaks ("Continue in the same direct, technical voice").
- **Register without substance** → You specified "write like a brilliant Harvard professor" so the model produces prose that *performs* intelligence — long words, nested clauses, hedged conclusions — without conveying any. Register instructions should complement content instructions, not replace them.
- **Register conflict** → "Write formally but keep it casual and fun." The model oscillates between registers, producing text that reads as uncertain. If you want a blend, describe it precisely: "Write with the vocabulary of a technical paper but the sentence rhythm of a blog post."

## Quick Reference

- **Family:** Tone / style
- **Adjacent:** → framing (orients interpretation; register orients voice), → formality (one axis of register), → authority (the expertise dimension of register), → audience specification (choosing the audience determines the register)
- **Model fit:** Frontier models sustain register across long outputs and switch registers on command. Mid-tier models follow explicit register instructions but drift in 500+ word outputs. Small models have limited register range — they do formal and casual but struggle with nuanced registers like "experienced engineer explaining to a junior colleague."
- **Sources:** Schulhoff et al. (2025), Halliday (1978) sociolinguistic register theory
