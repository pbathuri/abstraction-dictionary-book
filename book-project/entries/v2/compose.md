# compose

> Build a new artifact by combining elements according to a design intent — assembly with architecture, not mere concatenation.

## The Scene

Your ResumeForge pipeline has done the hard work. The research agent pulled the job posting requirements. The analysis agent matched them to the user's experience. The strategy agent ranked which achievements to emphasize. Now the composition agent needs to turn three JSON objects into a cover letter that reads like one person wrote it.

This is where most pipelines fumble. The parts are good individually, but the assembled document sounds like three authors who never talked. The introduction promises one thing, the body delivers another, and the tone lurches between paragraphs. That's not a model failure — it's a composition failure.

## What This Actually Is

Composition is building something new from parts that already exist. It sits between generation (creating from nothing) and concatenation (stacking things end-to-end). The distinction from "generate" matters: composition implies *raw materials*. You're not asking the model to create from void. You're asking it to assemble, arrange, and unify existing components into a coherent whole.

The concept borrows from functional programming, where composability is a virtue: small, well-defined functions that combine predictably. In prompt work, it means the output of one step can serve as clean input to a composition step without re-explaining or reformatting.

There are different modes: **sequential** (introduction → body → conclusion), **parallel** (build sections independently, assemble them), **hierarchical** (build sub-components, then compose into parent structure). The mode shapes both the prompt and the output quality.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Write an email about the project" | "Compose a project update email from these five bullet points" | Grounds the model in concrete materials, reducing hallucination |
| "Put these together" | "Compose an executive summary. Opening hook: strongest finding. Then: market context, technical viability, financial case, recommendation." | Architecture, not concatenation |
| "Combine the outputs" | "Unify voice across all sections. Flag any terminology conflicts. Ensure transitions connect each section to the next." | Explicitly asks for coherence, not just assembly |
| "Write a report from the analysis" | "Bullet 1 → opening paragraph. Bullet 3 → key recommendation. Verify every bullet is represented." | Maps materials to architecture; includes verification |

## Before → After

**Before:**
```
Write a product description. It should be about a watch that's
waterproof, solar-powered, titanium, with health monitoring.
```

**After:**
```
Compose a one-paragraph product description from these features:
- Waterproof to 50 meters
- Solar-powered, no battery replacement needed
- Titanium case, 42mm diameter
- Heart rate and blood oxygen monitoring

Tone: premium but accessible. Length: 60-80 words.
Lead with the feature that most differentiates from competitors.
```

**What changed:** The model has explicit materials, an output shape, and a strategic instruction (lead with differentiation). It's composing, not generating from a vague spec.

## Try This Now

```
Here are three findings from a quarterly analysis:

1. Revenue grew 12% QoQ, driven by enterprise expansion
2. Customer churn increased 0.8 points, concentrated in SMB segment
3. New product launch exceeded targets by 40% in first month

Compose a 100-word executive summary with this architecture:
- Opening: the single most important headline across all three
- Middle: the tension between good news and bad news
- Close: one-sentence recommendation

Do NOT just list the findings in order. Compose them into a narrative
where each finding illuminates the others.
```

## When It Breaks

- **Frankenstein composition** → Parts assembled without integration. Each paragraph is fine alone but transitions are abrupt and terminology shifts. Fix: include explicit instructions about transitions, voice consistency, and unified terminology.
- **Material override** → The model ignores your materials and generates from training data. Fix: reference materials by number ("Bullet 1 becomes the opening") and add verification: "Confirm every bullet is represented."
- **Structural collapse** → You asked for sections with headers, got a wall of text. Fix: provide the structure as a template with placeholders, not just a description.

## Quick Reference

- Family: instructional action
- Adjacent: → abstraction (composition is how abstractions combine), → checkpoint (composition outputs are prime candidates for verification), → context (composition agents need structured inputs)
- Model fit: Composition quality scales with capability more than most tasks. Large models handle multi-material composition with structural awareness. Smaller models lose coherence in multi-section documents — decompose into section-by-section generation with a stitching step.
