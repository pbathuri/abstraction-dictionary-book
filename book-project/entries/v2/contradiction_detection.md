# contradiction detection

> Checking whether a body of text asserts two things that can't simultaneously be true — the immune system of reliable generation.

## The Scene

Your OpsPilot pipeline produces a market analysis. Paragraph two: "Revenue grew 12% year-over-year." Paragraph seven: "The company faced declining revenue in the second half." Both sentences were generated in local contexts where they seemed reasonable. The model doesn't maintain a global truth table — it maintains a sliding window of plausibility.

A human reviewer catches it, but only because the report is short. In a 3,000-word analysis, these contradictions hide in plain sight. Fluent prose is a camouflage for inconsistency.

## What This Actually Is

Contradiction detection systematically checks whether a text asserts conflicting things. It operates at three levels:

- **Internal**: Claim A in paragraph two conflicts with claim B in paragraph five
- **Source**: The output contradicts the input documents it was supposed to be based on
- **Logical**: The conclusions don't follow from the stated evidence

The approach is detective, not preventive. It doesn't stop contradictions from being generated — it catches them after. For prevention, use constraints, structured output, and grounding. Detection and prevention work best together.

Implementation options: **rule-based** (catch numeric mismatches), **entailment-based** (NLI models check sentence pairs), or **LLM-based** (a separate model pass whose only job is finding conflicts). The most robust approach combines all three.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| (no consistency check) | "Before finalizing, review your response for any claims that conflict with each other or with the source material." | Even a simple self-check reduces contradiction rates |
| "Check for errors" | "List every factual claim you made. For each pair of claims, check whether they are consistent." | Systematic review beats superficial scan |
| "Make sure it's accurate" | "Verify that no claim contradicts the provided source. If you find a conflict, quote both the source passage and your claim." | Source fidelity check, not just internal consistency |
| "Look it over" | "Check at three levels: internal consistency, source fidelity, and logical coherence between evidence and conclusions" | Three distinct passes catch different failure types |

## Before → After

**Before:**
```
Write a market analysis based on the data provided.
```

**After:**
```
Write a market analysis based on the data provided.

After drafting, perform a contradiction audit:
1. List every numeric claim. Check that no two conflict.
2. For each claim, verify it matches the source data.
3. Check that your conclusions follow from your evidence.

If you find contradictions, resolve them before presenting
the final version. Note what you corrected.
```

**What changed:** The model now runs a self-audit before delivery. It won't catch everything, but it catches the obvious stuff — and makes the less-obvious stuff more findable.

## Try This Now

```
Here is a paragraph with at least two internal contradictions.
Find them.

"TechCo's Q3 results were strong. Revenue hit $42M, up 15%
year-over-year, marking the third consecutive quarter of growth.
However, the company's annual revenue of $150M represents a
significant decline from the prior year. Customer satisfaction
scores rose to 4.2 out of 5, the highest in company history,
though the NPS score dropped 12 points due to widespread
dissatisfaction with recent product changes."

For each contradiction:
- Quote both conflicting claims
- Explain why they can't both be true
- Rate severity: CRITICAL / MODERATE / MINOR
```

## When It Breaks

- **Surface-only detection** → Catches "$5M vs. $3M" but misses "market is growing rapidly" alongside "customer acquisition costs are increasing unsustainably." Fix: use LLM-based detection alongside rule-based checks.
- **False positive flood** → Flags things that aren't contradictions. "Costs increased in Q1 but decreased in Q2" is temporal variation, not contradiction. Fix: require the detector to explain *why* claims conflict and check whether context resolves it.
- **Selective detection** → Checks internal consistency but not source fidelity. An output can be perfectly self-consistent while contradicting every source. Always run both modes.

## Quick Reference

- Family: quality control
- Adjacent: → falsifiability (falsifiable claims are easier to check), → checkpoint (contradiction detection lives at checkpoints), → audit_trail (contradiction reports become part of the trail)
- Model fit: GPT-4-class and Claude 3.5+ detect subtle semantic contradictions reliably. Smaller models catch numeric mismatches but miss logical tensions. Using a strong model as the detector is a cost-effective quality investment.
