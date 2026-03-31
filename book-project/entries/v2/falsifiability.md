# falsifiability

> Structure claims so they can be checked, tested, or disproven — forcing the model to put its assertions where evidence can reach them.

## The Scene

Your investment research pipeline produces: "The market is trending positively, suggesting strong growth potential in the coming quarters." Sounds authoritative. Says nothing checkable. What market? Which metric? Compared to what? Over what period? "Trending positively" is a fortune cookie, not analysis.

You add a falsifiability protocol: every claim must include the number, the unit, the source, and the time period. Now the output reads: "The S&P 500 returned 8.2% YTD as of March 2026 (source: Bloomberg), outperforming the 10-year average of 7.1% annualized." You can check that. You can disagree with it. You can build on it. That's the difference.

## What This Actually Is

A falsifiable claim is one that could, in principle, be shown to be wrong. "The company is doing well" is unfalsifiable — what does "well" mean? "Q3 revenue was $4.2M, a 15% increase over Q2" is falsifiable — check the numbers, verify the calculation, determine true or false.

Models are generators of plausible text. Plausibility is not accuracy. Falsifiability doesn't make the model more accurate — it forces output into a form where inaccuracy is *detectable*.

Two levels: **claim-level** (specific, checkable assertions instead of vague generalizations) and **structural** (output carries metadata for verification — sources, confidence levels, falsification criteria).

The concept comes from Popper's philosophy of science. The bar for LLMs is lower but the principle holds: can I check this? If a claim can't be traced to a source, tested against data, or evaluated against a criterion, it's decoration.

Falsifiable text is clunkier than unfalsifiable text. Specificity has a syntactic cost. But it's dramatically more trustworthy and easier to verify, correct, and improve.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "The market is growing" | "The market grew 23% YoY per [source], measured by [metric]" | Specific, sourced, checkable |
| "Studies show..." | "According to [Author, Year, Publication], the finding was [specific result]" | Full citation prevents hand-waving |
| "This is a significant risk" | "This risk has a 30-40% probability based on [data]. It would manifest as [observable event] within [timeframe]." | Testable prediction, not vague concern |
| "The approach is promising" | "The approach reduced error rates by X% in [specific test], though it hasn't been tested at scale" | Scoped, qualified, and checkable |
| "Our analysis suggests" | "Our analysis suggests X. This would be wrong if [falsification condition]." | States what would disprove the conclusion |

## Before → After

**Before:**
```
List three risks to this project.
```

**After:**
```
List three risks to this project. For each risk:
- State it as a specific, testable prediction
- Name the metric or event that would confirm it
- Estimate probability (low/medium/high) with one sentence of justification

Do not state risks as vague concerns. Every risk must be falsifiable.
```

**What changed:** Each risk is now a prediction that can be checked against reality, not a worry that can never be confirmed or denied.

## Try This Now

```
Here are three claims. Rate each as FALSIFIABLE, PARTIALLY
FALSIFIABLE, or UNFALSIFIABLE. Then rewrite any non-falsifiable
claim to make it falsifiable.

1. "Our product is best-in-class."
2. "Customer churn increased 2.3 percentage points in Q3 2025,
    from 4.1% to 6.4%, per our internal analytics dashboard."
3. "AI will transform the healthcare industry in the coming years."

For each rewrite, explain what you added that makes it checkable.
```

## When It Breaks

- **Performative falsifiability** → "According to recent studies, the rate is approximately 15-25%." Which studies? What rate? The claim has the *syntax* of falsifiability without the substance. Fix: require full citations and specific figures.
- **Falsifiability at the wrong level** → Individual facts are falsifiable but the conclusion isn't. Revenue grew 10%, headcount grew 5%, therefore "the company is more efficient" — but efficient by what definition? Fix: require falsifiable conclusions, not just inputs.
- **Precision paralysis** → The demand for falsifiability prevents the model from saying anything uncertain. Fix: distinguish hard claims (must be falsifiable) from estimates (must state confidence and basis). An honest estimate with stated uncertainty is more useful than silence.

## Quick Reference

- Family: quality control
- Adjacent: → contradiction_detection (falsifiable claims make contradictions detectable), → audit_trail (falsifiable outputs are auditable; unfalsifiable ones can only be logged), → explicitness (input-side cousin — explicitness in prompts produces falsifiability in outputs)
- Model fit: Large models produce more naturally falsifiable output when prompted — they cite more readily and quantify more precisely. Smaller models tend toward vague generalizations. Provide explicit templates: "Claim: [statement]. Source: [citation]. Verification: [how to check]."
