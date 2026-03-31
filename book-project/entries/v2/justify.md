# justify

> Show your work — not the scratchpad, but the reasons that connect your conclusion to reality.

## The Scene

ResumeForge's first version had a "Skills Match" feature: given a job description and a resume, it would recommend which skills to emphasize. The recommendations were confident and wrong. "Emphasize your Python experience" for a candidate whose resume mentioned Python once in a group project, applying to a role that wanted 5+ years of production Python.

The model wasn't broken. It was doing what I asked: recommend. I hadn't asked it to *justify*. When I added "for each recommendation, cite the specific resume line and JD requirement that support it, and rate the match strength as STRONG, MODERATE, or WEAK," the output transformed. The Python recommendation came back as "WEAK — resume mentions Python in one group project (line 14); JD requires 5+ years production Python." The model self-corrected because the justification requirement forced it to confront the gap between its conclusion and its evidence.

## What This Actually Is

Justification makes the model's reasoning visible and checkable. A conclusion without justification — "Option A is best" — requires you to trust the model. A conclusion with justification — "Option A is best because it reduces latency by 40% (benchmark data, Table 3) and requires no infrastructure migration" — lets you evaluate the argument yourself.

The key mechanism: when you require justification, you create a self-screening effect. The model checks whether it can support a claim before making it. This isn't infallible — models can fabricate justifications — but it shifts the distribution toward better-supported claims and makes unsupported ones visible.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Recommend a database" | "Recommend a database and justify with three specific technical advantages that apply to our use case (high-frequency reads, 50ms latency ceiling)" | Justification anchored to specific context |
| "Which option is best?" | "Which option is best? For your choice, cite at least two data points from the provided material. For each rejected option, state the primary reason in one sentence" | Forces evidence for the pick AND the rejections |
| "Explain your reasoning" | "Justify by connecting each claim to a specific source. Format: Claim → Evidence (source, location) → Why this evidence supports this claim" | Three-part justification structure |
| "Are you sure?" | "State what evidence would change your recommendation. What would you need to see to switch to an alternative?" | Falsifiability built into the justification |
| "Why?" | "Justify in one sentence citing the single strongest piece of evidence. If the evidence is weak, say so" | Prevents justification inflation — forces the best reason, not all reasons |

## Before → After

From ResumeForge — the Skills Match feature:

> **Before**
> ```
> Given this JD and resume, recommend which skills the candidate
> should emphasize. Make the recommendations actionable.
> ```
>
> **After**
> ```
> For each skill recommendation:
> 1. Cite the specific JD requirement (quote the relevant line)
> 2. Cite the specific resume evidence (quote the relevant line)
> 3. Rate match strength:
>    - STRONG: resume shows 2+ years direct experience with
>      the exact skill the JD requires
>    - MODERATE: resume shows related experience that could
>      transfer
>    - WEAK: resume mentions the skill but evidence is thin
> 4. If match is WEAK, don't recommend emphasizing it —
>    suggest addressing the gap in the cover letter instead
>
> If you cannot find resume evidence for a JD requirement,
> output { "skill": "X", "match": "NO_EVIDENCE" } instead
> of fabricating a recommendation.
> ```
>
> **What changed:** The model stopped recommending skills the candidate couldn't back up. The WEAK/NO_EVIDENCE categories gave it permission to be honest instead of optimistic. Justification turned a recommendation engine into a decision-support tool.

## Try This Now

Find any recent model output that made a recommendation or judgment. Paste it back with this wrapper:

```
You previously recommended [X]. Now justify it:
1. What is the single strongest reason?
2. What evidence supports that reason?
3. What is the strongest argument AGAINST your recommendation?
4. What would make you change your mind?

If you cannot justify the recommendation with specific
evidence, say "insufficient evidence" and explain what
information you would need.
```

Watch how often the model's confidence drops when forced to justify. That drop is information.

## When It Breaks

- **Circular justification** — "Option A is best because it's the best option." The model restates the conclusion as its own reason. Fix: require the model to cite *specific evidence or criteria* — "justify by referencing at least two data points from the provided material."
- **Post-hoc rationalization** — The model generates a conclusion first, then constructs plausible-sounding support that wasn't actually the basis for the conclusion. Fix: pair "justify" with a grounding constraint — "cite only the attached sources." If the justification can't point to real material, it's fabricated.
- **Justification inflation** — Asked to justify, the model writes a paragraph of reasons for a claim that needs one sentence. Fix: constrain the justification — "justify in one sentence citing the key evidence" — to force identification of the *strongest* reason, not every tangentially relevant one.

## Quick Reference

- **Family:** Instructional action
- **Adjacent:** → critique (the adversarial complement — critique attacks, justify defends), → evaluate (produces judgments that justification then supports), → provenance tracking (justification's audit trail across a pipeline)
- **Model fit:** Frontier models produce well-structured justifications with genuine evidential links and are more likely to flag "insufficient evidence." Midsize models produce competent justifications but are more prone to post-hoc rationalization. Small models often treat "justify" as "write more words about this topic." For high-stakes justification, use the largest available model and require citations to provided source material.
