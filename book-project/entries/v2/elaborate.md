# elaborate

> Expand on a point with additional detail, examples, or reasoning — adding depth where the current treatment is too thin.

## The Scene

Your code review agent flags: "Security vulnerability in line 47." Correct. Completely unhelpful. Nobody can act on that.

An elaboration step takes that flag and produces: "Line 47 passes user input directly to a SQL query without parameterization, which allows SQL injection attacks. An attacker could craft a username containing `'; DROP TABLE users; --` to delete the users table. Fix: use parameterized queries via your ORM's `.where()` method."

Same finding. Now it's actionable. That's the difference between a flag and an elaboration — one identifies, the other explains.

## What This Actually Is

Elaboration is the anti-summary. Where summarize strips detail to reveal the skeleton, elaborate adds flesh to the bones. They sit at opposite ends of the information density spectrum.

The fundamental tension: it's easy to produce more words and hard to produce more *substance*. Models are biased toward elaboration — their training rewards longer, more detailed answers. Ask a question with no length constraint and the model will elaborate whether you want it to or not. This makes the instruction paradoxically powerful (the model is good at it) and dangerous (the model overdoes it).

The craft isn't getting the model to elaborate — it'll do that eagerly. It's *constraining* the elaboration to produce depth, not bloat. Unconstrained elaboration balloons. Constrained elaboration deepens. "Elaborate on this point in 100 words" forces the model to pick its highest-value expansion strategy instead of exhausting every strategy.

The distinction between elaboration and padding: good elaboration increases understanding. It adds a concrete example, surfaces an implication, explains a mechanism. Bad elaboration restates the original in different words, wraps it in transitions, and decorates it with obvious examples.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Elaborate" | "Elaborate with a concrete example from the healthcare industry" | Specifies *what kind* of depth |
| "Tell me more" | "Explain the underlying mechanism — not just what happens, but why" | Targets causal depth, not volume |
| "Expand on this" | "Elaborate in 80-120 words. Add one data point and one risk the original glosses over." | Constraint + specific expansion types |
| "Go deeper" | "Elaborate on point three specifically" (not "elaborate on your response") | Directs elaboration to the right target |
| "Can you explain more?" | "If you don't have specific information to add, say so rather than generating speculative detail" | Safety valve against hallucination under expansion pressure |

## Before → After

**Before:**
```
You wrote: "The migration will require downtime."
Tell me more.
```

**After:**
```
You wrote: "The migration will require downtime."
Elaborate in 3-4 sentences. Specifically:
- How much downtime (estimate a range)?
- What causes the downtime?
- What is at risk if the migration is interrupted?
```

**What changed:** Three specific expansion axes. The model can't pad with generic transition prose — it has to answer three concrete questions.

## Try This Now

```
Here's a compressed finding from an analysis:

"Our customer support response times have increased 40% in Q3."

Elaborate this into a full paragraph (80-100 words) for two
different audiences:

VERSION A: For the VP of Customer Success (wants business impact)
VERSION B: For the engineering lead (wants root cause)

After both, note: what information did you add for A that you
skipped for B, and vice versa? This shows how audience shapes
what "elaborate" means in practice.
```

## When It Breaks

- **Padding masquerading as depth** → More words, no more information. The original restated three ways with transition padding. Fix: require *specific* types of depth — examples, mechanisms, implications.
- **Elaboration of the wrong point** → The model enthusiastically expands the point it finds interesting, not the one you need. Fix: "Elaborate on your third point" — be precise about *which* point.
- **Hallucination under expansion pressure** → Asked to elaborate on a thin-knowledge topic, the model fabricates plausible detail. Fix: "If you don't have specific information to add, say so."

## Quick Reference

- Family: instructional action
- Adjacent: → critique (critique first, elaborate after — elaboration makes bad points longer, not better), → context_budget (elaboration consumes tokens; budget determines whether it's worth it), → audience_specification (determines what "depth" means)
- Model fit: All models elaborate willingly. Prompt design matters more than model tier. The single most impactful change: specify *what kind of depth* instead of leaving "elaborate" open-ended. Length constraints improve output at every tier.
