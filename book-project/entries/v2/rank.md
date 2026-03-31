# rank

> Comparison with a verdict — ordering items from best to worst along criteria you choose, or the model chooses for you.

## The Scene

Form8, my n8n market-research workflow, had a node that returned eight competitor profiles. Good data. But the analyst downstream — a human, not a model — still had to decide which competitors mattered most. So I added a ranking node between collection and analysis.

First attempt: "Rank these competitors by threat level." The model returned a numbered list. Looked authoritative. But I couldn't tell what "threat level" meant — market overlap? funding? feature parity? The model had picked its own criteria and didn't mention which. The ranking was a coin flip wearing a suit.

Second attempt: I specified three criteria with weights — market overlap (0.4), feature overlap (0.35), and growth rate (0.25) — and required per-criterion scores. Now the ranking was auditable. When a stakeholder asked "why is Competitor D third?", the scores answered the question. The model hadn't changed. The prompt had.

## What This Actually Is

Ranking is comparison plus commitment. Where "compare" lays items side by side, ranking forces the model to declare a winner. That declaration requires criteria — and when you don't supply them, the model invents its own. The invented criteria are generic, invisible, and different every run.

The real work of ranking isn't the ordering — it's the criteria. A ranked list is only as rigorous as the scoring that produced it. A numbered list without visible criteria is opinion wearing the costume of analysis.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Rank these options" | "Rank these options by cost-effectiveness (0.5) and implementation speed (0.5). Show scores" | Named criteria make the ranking auditable |
| "Which is best?" | "Score each option 1-10 on security, scalability, and cost. Rank by weighted total" | Forces per-criterion evaluation before ordering |
| "Prioritize these features" | "Rank by customer impact (0.4), engineering effort (0.3, lower is better), dependency risk (0.3)" | Clarifies that "lower is better" for effort |
| "Sort by importance" | "Group into three tiers: must-have, should-have, nice-to-have. Within each tier, rank by user-facing impact" | Tier-then-rank avoids false precision |
| "What should we do first?" | "Rank these tasks. If two are within 0.5 points, flag as EFFECTIVELY_TIED" | Acknowledges that not all differences are meaningful |

## Before → After

**Before:**
```
Rank these eight competitors by how threatening they are
to our market position.
```

**After:**
```
Rank these eight competitors. For each, score 1-10 on:
- Market overlap with our ICP (weight: 0.40)
- Feature parity with our core product (weight: 0.35)
- YoY revenue growth rate (weight: 0.25)

Show the per-criterion score and weighted total.
Rank descending by weighted total. If two competitors
are within 0.5 points, flag as TIED and note what
would break the tie.

After the ranking, answer: are the top 3 clustered
or spread? What does that imply about market
concentration?
```

## Try This Now

```
I'll give you five items. Rank them twice — first using
criteria YOU choose (don't tell me the criteria yet),
then using criteria I specify.

Items: Python, Rust, Go, TypeScript, Java
(Context: choosing a language for a new CLI tool)

Round 1: Rank using your own criteria. After ranking,
reveal what criteria you used and how you weighted them.

Round 2: Rank using these criteria:
- Binary size (0.3) - smaller is better
- Developer hiring pool (0.4)
- Cross-platform support (0.3)

Compare the two rankings. Where do they disagree?
What does that tell you about implicit criteria?
```

## When It Breaks

- **Position bias** — Models tend to rank items higher when they appear earlier in the prompt. Randomize input order or run the ranking twice with shuffled items and flag any item that moves more than two spots.
- **False precision** — Ten items ranked 1-10 implies meaningful differences between every adjacent pair. They rarely exist. Allow ties, or ask for tier grouping instead of strict ordering.
- **Criteria conflation** — Multiple criteria specified but the model weights them inconsistently across items, evaluating item A on cost and item B on innovation. Require a per-criterion score table computed before the final ranking.

## Quick Reference

- **Family:** Instructional action
- **Adjacent:** → evaluate (assesses without ordering), → compare (maps differences without declaring a winner), → rubric (provides the criteria structure ranking requires), → justify (explains *why* the ranking is what it is)
- **Model fit:** Frontier models produce well-differentiated justifications. Mid-tier models handle explicit scoring reliably but give generic justifications. Small models fixate on one criterion — decompose into score-then-rank for reliability.
