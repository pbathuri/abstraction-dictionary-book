# anchoring

> Fixing a reference point that orients the model's reasoning, calibrates its output, and bounds what counts as a reasonable response.

## The Scene

You ask a model: "Is this job offer competitive?" It gives you a wishy-washy "it depends on many factors" answer. You try again: "The current market rate for senior software engineers in Austin is $165,000–$195,000 base. Is this offer competitive?" Now every number the model generates orbits that anchor. It doesn't hedge — it compares, calculates, and tells you where the offer lands.

That opening number changed everything. Not because you gave the model more information (though you did). Because you gave it a *reference point* that organized all its downstream reasoning.

## What This Actually Is

An anchor is a fixed reference — a fact, a standard, a value, an example — that the model treats as gravitational center. The term comes from cognitive psychology (Tversky & Kahneman, 1974), where an initial number disproportionately influences later judgments. In prompting, you exploit this deliberately.

Anchoring works because every token is predicted based on what came before it. An early anchor casts a shadow across the entire output. This isn't a bug — it's a lever. There are several types:

- **Numeric**: "This company has 50 employees" changes what "large team" means
- **Tonal**: A sample output anchors voice and structure
- **Epistemic**: "Given high uncertainty..." vs. "Based on established evidence..." changes hedge density entirely

The critical distinction: anchoring is not instruction. Instructions tell the model *what to do*. Anchors tell it *where to stand while doing it*. Same instruction, different anchor, very different output.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Is this salary competitive?" | "The market rate for this role in this city is $X–$Y. Evaluate this offer against that range." | Numeric anchor eliminates the model's guesswork |
| "Write in a professional tone" | [Provide a 2-sentence sample of the exact tone you want] | Tonal anchor via example beats adjective-based instruction |
| "Be careful with your estimates" | "Given high uncertainty and limited data, treat all projections as provisional" | Epistemic anchor calibrates confidence level |
| "Assess the risk" | "The risk tolerance is conservative: reject anything above 15% downside probability. Benchmark return: 7.2% annualized." | Parametric anchors make "risk" concrete and auditable |

## Before → After

**Before:**
```
Evaluate whether this investment proposal is worth pursuing.
```

**After:**
```
Anchoring parameters:
- Risk tolerance: conservative (reject anything above 15% downside probability)
- Time horizon: 18 months
- Benchmark return: 7.2% annualized (S&P 500 trailing 10-year average)

Using these anchors, evaluate the following investment proposal.
For each metric, state whether it falls above, below, or within
the anchored range.
```

**What changed:** The model now has a coordinate system. Every judgment is relative to explicit reference points, not vibes.

## Try This Now

```
I'll give you the same question twice with different anchors.

VERSION A:
"A mid-stage startup is growing at 15% month-over-month.
Is that good growth?"

VERSION B:
"The top-decile growth rate for Series B SaaS companies is
20% MoM. A mid-stage startup is growing at 15% MoM.
Is that good growth?"

Answer both. Then explain how the anchor changed your response.
```

Watch how Version B produces a sharper, more specific, more useful answer — same question, better anchor.

## When It Breaks

- **Competing anchors** → Your system prompt says "be concise" but your example output is 500 words. The model splits the difference into mediocrity. Audit your prompts for anchor consistency.
- **Stale anchors** → You anchor salary analysis to 2019 figures. The model dutifully generates numbers around a pre-pandemic baseline. Always date and source your anchors.
- **Anchor drift in pipelines** → A conservative risk threshold set in step one fades by step five as the context fills. Re-inject critical anchors at each agent handoff.

## Quick Reference

- Family: core abstraction
- Adjacent: → explicitness, → feedback_loop, → context
- Model fit: Larger models respond to subtle anchors (a single reference number). Smaller models need heavier anchoring — more repetition, more explicit framing. All models are vulnerable to anchor override from strong user input.
