# modularity

> Build prompts like software: each piece does one thing, each piece is replaceable.

## The Scene

The AI Ethics Coach started as one mega-prompt. Role description, analysis instructions, formality markers for the developer version, different formality markers for the compliance version, edge case handling, output format — all in one 400-token block. When the compliance team asked me to adjust the report format, I changed two lines and accidentally broke the developer-facing output. The format instructions were tangled with the tone instructions, and shifting one moved the other.

I refactored into modules. Role module (who you are). Analysis module (what to look for). Tone module — two versions, swapped based on output target. Format module — two versions, same swap. Constraint module (what you can't do). Now when compliance needs a format change, I edit the compliance format module. The developer output doesn't know or care. Same analysis engine, interchangeable clothes.

## What This Actually Is

Modularity separates a prompt system into self-contained, interchangeable components. Each module handles one concern: the role, the task, the format, the constraints, the examples. Each can be written, tested, versioned, and swapped independently. When the output format needs to change, you swap the format module without touching the task. When the same analysis applies to a different domain, you swap the context module.

This differs from decomposition. Decomposition breaks a *task* into sequential sub-tasks — the focus is on the work. Modularity breaks the *prompt itself* into reusable components — the focus is on the design. The strongest systems use both.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| One continuous prompt block | Label sections: `[ROLE MODULE]` `[TASK MODULE]` `[FORMAT MODULE]` `[CONSTRAINT MODULE]` | Visual separation enforces mental separation |
| Copy-pasting the same constraint block into five prompts | Create one constraint module, reference it everywhere | Single source of truth — update once, apply everywhere |
| "Write formally and analyze the quarterly data and output as a table" | Separate into: tone module (formal markers), task module (quarterly analysis), format module (table spec) | Each concern can change independently |
| Hardcoding the audience into the task description | Audience as a swappable module: "Audience: VP of Engineering, prefers data over narrative, max 200 words" | Same analysis, different audience — swap one module |
| A 500-token system prompt that does everything | A 100-token role module + a 100-token task module + a 50-token constraint module + a 50-token format module | Each module can be A/B tested in isolation |

## Before → After

From the AI Ethics Coach — modular prompt architecture:

> **Before (monolithic)**
> ```
> You are an AI ethics advisor for developers. Analyze code
> for ethical red flags. For developers, use contractions and
> address as "you." For compliance reports, no contractions,
> third person, include regulatory references. Output findings
> as a numbered list with severity ratings. Don't speculate
> beyond what the code shows. Always flag data collection,
> consent handling, and algorithmic bias.
> ```
>
> **After (modular)**
> ```
> --- MODULE: role/ethics_advisor ---
> You are an AI ethics advisor. You identify ethical risks in
> software code and recommend mitigations.
>
> --- MODULE: analysis/core_checklist ---
> Flag: data collection without consent mechanisms, missing
> bias testing, opaque algorithmic decisions, data retention
> without limits. Do not speculate beyond what the code shows.
>
> --- MODULE: tone/developer ---  [OR tone/compliance]
> Use contractions. Address as "you." Lead with what to fix.
>
> --- MODULE: format/findings_list ---  [OR format/compliance_report]
> Numbered list. Each finding: title, severity (HIGH/MED/LOW),
> what to fix, why it matters.
> ```
>
> **What changed:** Updating the compliance tone doesn't touch the analysis logic. Adding a new ethical check means editing one module. The system went from "edit with fear" to "edit with confidence."

## Try This Now

Take your longest prompt. Draw brackets around each functional section: role, task, constraints, format, examples. Label each bracket. Now answer: if you changed the format section, would anything else break? If you swapped the role for a different domain expert, would the task still make sense? If either answer is no, the boundaries are in the wrong place. Redraw them.

## When It Breaks

- **Boundaries in the wrong place** — The task description and constraints are in separate modules, but the constraints can't be understood without the task. Fix: modules should encapsulate one complete concern. If two pieces are inseparable, they belong in the same module.
- **Interface drift** — Module A expects input format X, but Module B has been updated to produce format Y. In software, compilers catch this. In prompt systems, broken outputs catch it too late. Fix: document what each module expects and produces, and validate at every boundary.
- **Premature modularity** — You modularized before understanding the problem. The prompt structure is still evolving, and now every change requires coordinating across four files. Fix: modularize once the structure has stabilized, not during exploration.

## Quick Reference

- **Family:** Core abstraction
- **Adjacent:** → decomposition (breaks tasks into steps; modularity breaks prompts into reusable components), → hierarchy (orders by importance within modules; modularity separates by concern across modules), → pipeline (each pipeline stage is a module with defined interfaces)
- **Model fit:** Benefits all tiers equally — modularity affects prompt structure, not model capability. Smaller models benefit particularly from the clarity modular prompts provide (single-concern instructions beat tangled multi-concern monoliths). The primary beneficiary is the human maintainer, not the model.
