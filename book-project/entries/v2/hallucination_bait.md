# hallucination bait

> You didn't ask the model to lie. You just made lying easier than saying "I don't know."

## The Scene

ResumeForge, day one. The very first prompt I tested:

```
The candidate has 3 years of experience in data analysis.
Rewrite their resume to be competitive for this Senior Data
Scientist role requiring 5+ years and a machine learning
background.
```

The model returned a resume that included two years of machine learning experience at a company the candidate had never worked at, a TensorFlow certification that didn't exist, and a "team of 12" that was actually a team of 3. Every fabrication was formatted identically to the real content. Indistinguishable. If I hadn't been holding the original resume in my other hand, I would have believed it.

I didn't ask the model to fabricate. But I *did* ask it to make a 3-year data analyst competitive for a senior ML role — and the only way to do that was to invent qualifications. The prompt didn't say "lie." The prompt said "make this work," and lying was the most efficient path to compliance.

That's hallucination bait. Not an error. Not a limitation. A *prompt structure* that makes fabrication the path of least resistance. The model doesn't know it's fabricating. It doesn't have an honesty module. It has a next-token predictor, and the next tokens that best satisfy your instruction happen to be fiction.

## What This Actually Is

Hallucination bait is any prompt structure where the model's instruction demands specifics it can't verify, and refusing to answer isn't presented as an option. It comes in three flavors:

**The specificity-without-source trap:** "What were Acme Corp's Q3 2025 revenue figures?" without providing the data. The model will generate plausible numbers. They'll be wrong. You asked for them anyway.

**The mandatory-answer trap:** "You must provide a definitive answer. Do not say you are unsure." You just disabled the model's already-weak uncertainty signals and guaranteed it will fill gaps with invention.

**The phantom citation trap:** "Cite three peer-reviewed studies supporting this claim." Without source material, the model will manufacture author names, journal titles, and DOIs that look exactly like real citations. This is the most dangerous form because the fabrication *looks verifiable* — you'd have to actually check each reference to discover it's fake.

The fix is never "tell the model to be honest." The model can't introspect on its own knowledge boundaries. The fix is structural: provide the source material (→ grounding), give the model permission to say "I don't know" (escape hatch), or build a → verification loop that catches fabrication after the fact.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "List the exact figures" | "List the figures from the attached report. If a figure isn't in the report, write MISSING" | Provides an escape hatch for unknowns |
| "Cite three studies" | "From the attached papers, cite relevant findings. Do NOT cite papers not in the provided set" | Closes the fabrication path |
| "Always provide an answer" | "If you cannot answer from the provided sources, say 'Insufficient data' and explain what's missing" | Makes refusal a legitimate response |
| "What are the stats?" | "Using only the data in the CSV below, calculate..." | Grounds the request to a specific source |
| "Be specific and detailed" | "Be specific using the source material. Flag any detail you're not confident about as [LOW_CONFIDENCE]" | Keeps specificity but adds a confidence valve |
| "Never say you don't know" | (Delete this instruction entirely) | This sentence is a fabrication accelerator |

**Defusal verbs:** ground, source, flag, mark as unverified, cite from (specific doc), escape to "unknown."

## Before → After

From ResumeForge — the actual anti-hallucination rewrite:

> **Before (hallucination bait)**
> ```
> Rewrite this resume to be competitive for the target role.
> Ensure all bullet points include quantified impact metrics.
> Every bullet should demonstrate leadership and technical depth.
> ```
>
> **After (bait defused)**
> ```
> Rewrite this resume for the target role. Rules:
>
> SOURCE CONSTRAINTS:
> - Every fact in the output must appear in the source resume
> - If the source says "contributed to," do not upgrade to "led"
> - If the source has no metrics, do not invent them. Instead:
>   { "bullet": "...", "flag": "no_metric_in_source",
>     "suggestion": "Ask candidate about: [specific question]" }
>
> GAP HANDLING:
> - If the JD requires experience the candidate lacks, do not
>   fabricate it. Return:
>   { "gap": "description", "severity": "hard_gap|soft_gap",
>     "mitigation": "how to address in cover letter" }
>
> VERIFICATION:
> - After rewriting, compare each bullet to the source.
> - Flag any claim that doesn't trace directly to source material.
> ```
>
> **What changed:** The first prompt rewarded fabrication. The second prompt punishes it — by providing a structured alternative (flag gaps, suggest questions, return JSON for missing data). The model doesn't need to lie anymore because there's a better-scoring path that tells the truth.

## Try This Now

Paste this into ChatGPT:

```
I'm going to give you a prompt. Your job is to identify every
place where this prompt creates hallucination bait — meaning it
asks for specifics the model probably can't verify, or it blocks
the model from saying "I don't know."

For each piece of bait you find, suggest a defusal: a rewrite
that gets the same information without tempting fabrication.

Prompt:
"Write a detailed market analysis for our SaaS product. Include
specific competitor revenue figures, market share percentages,
and cite industry reports with publication dates. Be comprehensive
and do not leave gaps."

Find the bait. Defuse it.
```

Count how many traps you find. Most people find 3-4 on the first read and 2 more on the second.

## From the Lab

The constraint-stacking data from → constrain applies directly here — the strongest anti-hallucination effect came from *content constraints that provided escape hatches*:

![Constraint Stacking Effect](../art/figures/exp_zero_to_five_constraints.png)

**Key finding:** Prompts with source-grounding constraints ("only from the attached data") *plus* an explicit escape hatch ("if not found, say MISSING") reduced fabrication rates by 60-80% compared to prompts with no constraints. Prompts with source constraints but *no* escape hatch reduced fabrication by only 30-40% — the model still invented content when cornered without an exit. The escape hatch is not optional.

## When It Breaks

- **The delegated assumption** → Agent A asks Agent B for specific data. Agent B doesn't have it, but treats the request as an instruction to *produce output*, not to *verify availability*. Agent B fabricates. Agent A trusts the fabrication. By Agent C, the invented data is load-bearing. The fix: every delegation should include "if you cannot obtain this, return { status: 'unavailable' } instead of generating."
- **Confidence-calibration mismatch** → Frontier models hallucinate *less often* but with *higher confidence*. When GPT-4 invents a citation, it formats it perfectly — correct-looking DOI, plausible journal name, real-sounding author. The fabrication is harder to detect because it's better crafted. Don't trust polish. Trust provenance.
- **Gradual specificity escalation** → The first question is broad, the model answers broadly. You ask follow-up questions demanding more detail. Each escalation pushes the model further past its knowledge boundary. By the fourth follow-up, every detail is confabulated — and the model can't tell you which ones.

## Quick Reference

- **Family:** Failure mode
- **Adjacent:** → grounding (the antidote — provide what you want the model to reference), → verification loop (catches fabrication after generation), → specificity (double-edged: reduces vagueness but can become bait when applied to unsourced facts), → constrain (the mechanism for closing fabrication paths)
- **Model fit:** All tiers fabricate. Small models fabricate more often. Frontier models fabricate less often but more convincingly. The defense is always structural (source material + escape hatches + verification), never behavioral ("just be honest").
- **Sources:** Hallucination survey literature, Anthropic calibration research, RAG as architectural defense
