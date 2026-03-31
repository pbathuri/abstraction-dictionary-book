# constrain

> Draw the fence before you let the model off the leash.

## The Scene

ResumeForge, version zero. The prompt said: "Rewrite this resume bullet to be more impactful for the target job description." Ollama came back with a bullet that turned a junior data analyst into someone who "spearheaded an enterprise-wide analytics transformation impacting $40M in revenue." The candidate had worked at a twelve-person startup for eight months.

I didn't need a better model. I needed a fence.

The fix was five lines of constraint:

```
Rewrite the bullet for the target JD. Rules:
- Never fabricate employers, titles, dates, or certifications
- Never inflate team size, scope, or metrics beyond the source resume
- If a claim needs evidence the candidate hasn't provided, output
  evidence_required=true instead of inventing support
- Preserve the candidate's actual verbs ("contributed to" stays)
```

Same Ollama model. Same resume. The output went from dangerous fiction to honest, targeted prose. The only thing that changed was that I told the model what it *couldn't* do. That's constraining. You are not adding instructions. You are removing degrees of freedom until the remaining space is the space you actually want.

## What This Actually Is

Think of it like a mold for casting metal. The metal is the model's output — fluid, capable of taking any shape. Without a mold, it puddles. The constraint is the mold. It doesn't create the output. It forces the output into the shape you need.

Constraints come in four species: **format** (return JSON, max 200 words), **content** (only cite the attached sources, skip pricing), **behavioral** (if unsure say so, ask before proceeding), and **scope** (sections 3 through 7 only, North America only). Most weak prompts are missing at least two of these. Most strong prompts deploy at least three. The ResumeForge fix deployed content constraints and a behavioral escape hatch — and that was enough to turn a liability into a tool.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Be accurate" | "Do not fabricate any claim not present in the source document" | Names the specific failure you're preventing |
| "Keep it short" | "Maximum 150 words. If you exceed this, cut from the middle, not the conclusion" | Defines the limit AND the trade-off |
| "Use the data" | "Base every number on the attached CSV. If a figure is not in the CSV, write MISSING" | Creates an escape hatch instead of tempting invention |
| "Be professional" | "No exclamation marks. No superlatives. No sentences starting with 'Exciting'" | Turns a vibe into checkable rules |
| "Don't hallucinate" | "If you cannot verify a claim from the provided documents, flag it as [UNVERIFIED]" | Gives the model a legal alternative to lying |
| "Stay focused" | "Address only sections 2-4. Ignore all other sections even if relevant" | Draws a hard scope boundary |

**Power verbs for constraining:** limit, restrict, exclude, prohibit, cap, bound, require, enforce, forbid, permit (only).

## Before → After

From my ResumeForge truthfulness module — the actual prompt evolution:

> **Before**
> ```
> You are a resume optimization assistant. Improve this resume
> bullet point to better match the job description. Make it
> more impactful and quantified.
> ```
>
> **After**
> ```
> Rewrite this resume bullet for the target JD.
>
> Truthfulness constraints:
> - Never add employers, titles, dates, or certifications not in the source
> - Never inflate metrics (team size, revenue, scope) beyond the source
> - "Contributed to" does not become "led." Preserve the candidate's
>   actual role verbs unless the source resume explicitly supports a
>   stronger verb
> - If the JD asks for experience the candidate lacks, do not invent it.
>   Instead return: { "gap": "description", "suggestion": "how to address
>   in cover letter" }
>
> Format: Return the rewritten bullet + a confidence score (1-5) for
> how well the candidate's actual experience matches the JD requirement.
> ```
>
> **What changed:** Four content constraints kill fabrication. One behavioral constraint (the gap-handling rule) gives the model a way to be honest instead of creative. The confidence score forces the model to evaluate, not just generate.

## Try This Now

Open ChatGPT (or whatever you use) and paste this:

```
I'll give you a paragraph I wrote. Your job is to add constraints to
it — not to rewrite the content, but to add rules that would prevent
a model from producing bad output if given this paragraph as a prompt.

For each constraint you add, label it as one of:
FORMAT / CONTENT / BEHAVIORAL / SCOPE

Here's my paragraph:
"Write a product comparison for our enterprise customers comparing
our tool with the top 3 competitors."

Add at least 5 constraints. Then explain which failure mode each
one prevents.
```

Watch how the constraints reveal the hidden assumptions in the original paragraph — assumptions you were going to let the model guess at.

## From the Lab

We tested what happens when you stack constraints from zero to five on the same base prompt, across four model families. The results were unambiguous:

![Constraint Stacking Effect](../art/figures/exp_zero_to_five_constraints.png)

**Key finding:** Performance climbs steeply from zero to three constraints, plateaus between three and four, and *degrades* at five on smaller models. The sweet spot is two to four constraints that target distinct failure modes. Past that, the model spends so much attention on compliance that the actual task suffers. Constrain the things that matter. Leave room for the model to think.

## When It Breaks

- **Contradictory constraints** → "Be concise" + "Provide comprehensive detail." The model will satisfy one and ghost the other. Before adding a constraint, check it against the existing set.
- **All fence, no field** → A list of twenty prohibitions and zero instructions. The model knows what it can't do but has no idea what it should do. Constraints complement instructions — they don't replace them.
- **Phantom constraints** → "Do not use offensive language in this quarterly financial summary." You just spent tokens constraining something that was never going to happen. Good constraints target *realistic* failure modes.

## Quick Reference

- **Family:** Instructional action
- **Adjacent:** → specificity (the property constraints produce), → filter (corrective where constraint is preventive), → scope (defines territory; constraints define fences), → rubric (an organized collection of constraints for evaluation)
- **Model fit:** Respected across tiers. Frontier models handle 4-5 simultaneous constraints. Smaller models need constraints to be few, explicit, and non-competing — stack more than three on a 7B model and expect silent violations.
- **Sources:** Ari (2025) 5C framework, Schulhoff et al. (2025) Prompt Report
