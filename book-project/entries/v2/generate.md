# generate

> Create something that didn't exist before — the most powerful instruction and the one most likely to go wrong without guardrails.

## The Scene

ResumeForge needed to generate tailored resume bullets from raw experience descriptions. The first prompt said: "Generate an impactful resume bullet for this job description." Ollama delivered masterpieces of fiction — a junior analyst who apparently "architected an enterprise-wide data platform serving 2M daily users." The candidate had built a dashboard in Google Sheets.

The generation wasn't wrong in kind. It was wrong in degree. "Generate" without specification is an invitation for the model to draw on everything it's ever seen about resume bullets, and what it's seen is a lot of inflated LinkedIn copy. The fix was specifying the *output space* — not the output itself, but the boundaries the output should explore within: "Generate a bullet using only claims supportable by the source resume. Match the JD's language where the candidate's actual experience overlaps. Where it doesn't overlap, don't invent."

Same verb. Radically different result. Generation without specification produces the average of the training distribution. Generation with specification produces something useful.

## What This Actually Is

Generation is the instructional action you use when you want something new — not extracted, not transformed, not assembled from parts, but created from specifications. It's the widest-latitude verb in the family: you're saying "here are the parameters, now create." That latitude is the power and the danger.

The key is the specification — the set of constraints, audience markers, tone cues, and success criteria that bound the creative space without strangling it. Too few specs and you get the model's default: generic, personality-free output. Too many and you get robotic compliance. The sweet spot is specifying the *space* (topic, audience, tone, format, length) while leaving the *execution* to the model.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Generate a blog post" | "Generate a 200-word intro for backend engineers who've been burned by bad database migrations. Open with a concrete scenario. Tone: practitioner, slightly wry, zero corporate polish" | Names audience, angle, tone, length, and opening strategy |
| "Write an email" | "Generate a follow-up email. Max 100 words. One ask, stated in the first sentence. Close with a specific next step and date" | Constrains structure without scripting content |
| "Create some taglines" | "Generate 5 tagline options, each under 8 words. One playful, one authoritative, one minimal, one question-based, one metaphorical" | Diversity instruction prevents five variations of the same idea |
| "Generate a summary" | "Generate a summary for a VP who has 90 seconds. Lead with the non-obvious finding. Skip anything they'd already know" | Audience + angle + exclusion = useful generation |
| "Write test cases" | "Generate 5 edge-case test scenarios that a junior developer would miss. Each: one setup sentence, one expected behavior, one failure condition" | Specific format and difficulty target |

**Power verbs for generation:** draft, produce, compose, devise, create, formulate, design, craft.

## Before → After

From ResumeForge — the actual prompt evolution:

> **Before**
> ```
> Generate an impactful resume bullet for this job description.
> Make it quantified and results-oriented.
> ```
>
> **After**
> ```
> Generate a resume bullet for the target JD.
>
> Specification:
> - Source: only claims supportable by the candidate's actual
>   experience description (attached)
> - Language: mirror the JD's terminology where the candidate's
>   experience genuinely overlaps
> - Quantification: use the candidate's real numbers. If no
>   numbers exist, don't invent them — describe the impact
>   qualitatively
> - Gap handling: if the JD asks for experience the candidate
>   lacks, return { "gap": true, "suggestion": "how to address
>   in cover letter" } instead of fabricating the experience
> - Tone: confident but honest. "Contributed to" stays if that's
>   what happened. Don't upgrade to "led" without evidence
> ```
>
> **What changed:** The specification turned "generate" from "make something up that sounds good" into "create something new that's tethered to truth." The gap-handling rule gave the model a path to honesty instead of invention.

## Try This Now

Find the last time you typed "write me a..." or "generate a..." prompt. Paste the prompt into a new chat with this wrapper:

```
I wrote a generation prompt that produced mediocre output.
Help me add specification without over-constraining it.

For my prompt, suggest:
1. An audience specification (who reads this?)
2. An angle or hook (what makes this one different?)
3. One hard constraint (what must it NOT do?)
4. One success criterion (how would a human judge quality?)

My original prompt:
[paste here]
```

The specifications you were missing are usually the reason the output felt generic.

## When It Breaks

- **Specification vacuum** — "Generate a blog post" with no further guidance. The model produces generic content from the center of its training distribution. Specify audience, angle, tone, and what makes this piece different from every other one on the topic.
- **Over-constrained generation** — Fifteen hard rules and a rigid template. The model fills every box and produces something that reads like a compliance form. Distinguish hard constraints (must satisfy) from soft preferences (optimize for). Leave room for the model to be good, not just compliant.
- **Hallucination in factual generation** — You asked for a market analysis without providing market data. The model obliged with invented statistics. If generation must include facts, provide the facts. If you can't, instruct the model to mark uncertain claims.

## Quick Reference

- **Family:** Instructional action
- **Adjacent:** → compose (assembles from provided materials; generate creates from specifications), → constrain (narrows generation space), → filter (selects the best from multiple generated candidates)
- **Model fit:** Generation quality scales steeply with model size. Frontier models produce creative, specification-compliant output in a single pass. Small models produce generic first drafts needing heavy specification and iteration. For creative generation, model choice matters more than in any other operation.
