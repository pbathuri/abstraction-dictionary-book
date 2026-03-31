# verification loop

> Generate, check, fix. Or: generate, ship, regret. Pick one.

## The Scene

Karpathy's autoresearch doesn't just run. It runs, *then checks*, then decides whether to keep running.

The pattern looks like this: the LLM executes a research step — say, extracting claims from a paper. Then it runs a verification pass: grep the output for required fields, count citations, check that every claim has a source_id. If the check passes, advance to the next phase. If it fails, *revert to the last good state and try again*. If it fails twice, log the failure and move on without that data rather than shipping garbage downstream.

Run → check → advance or revert. That IS a verification loop. It's the same pattern as a CI pipeline: run the tests, and if they fail, don't deploy.

I built the same thing into Form8 after the third time the market research pipeline produced a "competitive analysis" where two of the eight competitors were fabricated. Not hallucinated in the usual sense — the model didn't invent companies that don't exist. It confused companies. It attributed Company A's pricing to Company B, swapped feature lists, and blended two separate products into one fictional profile. Every individual fact was real. The *assembly* was wrong.

The fix wasn't a better prompt. The fix was a verification node between the profiler and the analyzer. The verifier didn't redo the research. It ran a simple check: "For each competitor, does the company name match the URL? Does the pricing match what's on the pricing page? Do the features appear on the features page?" Three questions. Two-minute runtime. Caught errors that would have poisoned the entire downstream analysis.

A single model pass is a first draft. Treating it as a finished product is a design error.

## What This Actually Is

A verification loop is a check that sits between generation and delivery. The generator produces output. The verifier reviews it against explicit criteria. If it passes, the output moves downstream. If it fails, it goes back for revision or gets escalated to a human. The loop is: *generate → verify → {pass: advance, fail: revise or escalate}*.

The critical word is *explicit*. "Check that this is good" is not verification — it's a vague prayer that the model will somehow evaluate itself honestly. "Check that every row has exactly four columns, every date is in ISO format, every source_id resolves to a file in the corpus, and no value exceeds 100" is verification with teeth. The verifier needs a checklist, not a vibe.

Three research patterns make the case. **Self-consistency** (Wang et al., 2022): run the same prompt multiple times, take the majority answer. Accuracy went up 17.9% on math benchmarks — not from a better prompt, but from running the same prompt more and *voting*. **Self-Refine** (Madaan et al., 2023): generate, critique, revise, repeat. GPT-4 improved 8-21 points across code and text tasks. **Chain-of-Verification** (CoVe): after answering, generate verification questions about your own claims, answer them independently, revise anything that fails. The pattern across all three: never trust the first pass.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Make sure it's good" | "Before returning, verify: every statistic cites a source, no two recommendations contradict, total under 300 words" | Turns vague quality into checkable criteria |
| "Double-check your work" | "After generating, re-read your output and answer: (1) Does every claim have a source_id? (2) Do any two claims contradict? (3) Is the format valid JSON?" | Gives the model specific verification questions |
| "Be accurate" | "Generate your answer, then for each factual claim, ask: 'Can I point to where in the source document this claim comes from?' Remove any claim where the answer is no" | Separates generation from verification explicitly |
| "Review and fix any issues" | "Run a 3-point check: schema valid? All required fields present? No duplicate entries? Return the check results alongside the output" | Makes the verification results visible |
| "Looks good, ship it" | "Gate: output must pass ALL criteria before being sent to the next agent. If any criterion fails, return to generator with the specific failure" | Turns quality into a hard gate, not a suggestion |

**Power verbs for verification:** verify, validate, gate, assert, confirm against, cross-check, audit, reconcile.

## Before → After

From Form8 — adding a verification node to the market research pipeline:

> **Before (no verification)**
> ```
> Node 1: Research competitors → Node 2: Profile competitors →
> Node 3: Analyze gaps → Node 4: Write strategy brief
> (output goes straight from research to analysis to writing)
> ```
>
> **After (with verification gates)**
> ```
> Node 1: Research competitors
>   ↓
> GATE 1: Does each competitor entry have name, URL, and
> one-sentence positioning? Are there at least 6 entries?
> If FAIL → return to Node 1 with: "These entries failed: [list]"
>   ↓
> Node 2: Profile competitors
>   ↓
> GATE 2: For each competitor, does the company name match the
> URL domain? Does the pricing tier appear on their actual pricing
> page? Does each feature listed appear on their features page?
> If FAIL → return to Node 2 with specific mismatches
>   ↓
> Node 3: Analyze gaps
>   ↓
> GATE 3: Does every gap cite at least one competitor by name?
> Does every recommendation trace to a gap from the analysis?
> If FAIL → return to Node 3
>   ↓
> Node 4: Write strategy brief
> ```
>
> **What changed:** Three gates, each with 2-3 concrete checks. Total added latency: ~30 seconds. Errors caught before they propagated: roughly 1 in 4 pipeline runs. The verification loop isn't overhead — it's the difference between a pipeline that works and a pipeline that *looks like it works*.

## Try This Now

Take any prompt that produces a factual output (analysis, summary, research brief) and add this verification wrapper:

```
I'm going to give you a prompt and an output that the prompt
generated. Your job is to be the verifier, not the generator.

Check the output against these criteria:
1. Every factual claim is supported by the provided source material
2. No two statements contradict each other
3. The format matches the specification in the prompt
4. Nothing is fabricated (if you're not sure, flag it)

For each criterion, score PASS or FAIL with evidence.
Then give an overall verdict: SHIP, REVISE (with specific fixes),
or REJECT (with explanation).

[Paste the original prompt]
[Paste the output]
```

Use a *different* model for the verification if you can. A model checking its own work tends to rubber-stamp. A different model applies genuine adversarial distance.

## From the Lab

Verification loops benefit from the same techniques as structured reasoning. The data shows clear gains from multi-step verification compared to single-pass generation:

![Reasoning Task Techniques](../art/figures/exp_reasoning_task_techniques.png)

**Key finding:** Self-Refine (generate → critique → revise) improved output quality by 8-21 points depending on task type, with the largest gains on the *first* revision cycle. Subsequent cycles showed diminishing returns. Practical recommendation: one verification pass catches most errors. Two catches almost all of them. Three is rarely worth the compute unless the stakes are very high.

## When It Breaks

- **Rubber-stamp verification** → The model checks its own output with the same framing it used to generate it and predictably approves everything. Fix: use a different prompt for verification, a different model, or a different agent. The verifier needs *adversarial distance* from the producer.
- **Infinite revision loops** → Strict criteria that always fail + vague revision instructions that never fix the root cause = the model generates, fails, revises identically, fails again, forever. Fix: cap iterations at 2-3 and escalate to a human or a different strategy after that.
- **Verification theater** → The gate checks easy things (word count, JSON validity) and waves through hard things (factual accuracy, logical coherence). You now have a quality stamp on low-quality output. Fix: design checks that target *the failure modes you've actually seen*, not the ones that are easy to automate.

## Quick Reference

- **Family:** Agent workflow
- **Adjacent:** → rubric (what the verifier checks against), → delegation (every delegation should have a paired verification step), → hallucination bait (verification is the primary defense), → escalation (what happens when verification repeatedly fails)
- **Model fit:** Frontier models are the best self-verifiers (~60-80% of their own factual errors caught). Small models catch ~30-40% and sometimes introduce *new* errors during verification. For small-model pipelines, use a frontier model exclusively for the verification stage — one verification call costs less than shipping bad output.
- **Sources:** Wang et al. (2022) self-consistency, Madaan et al. (2023) Self-Refine, Dhuliawala et al. (2023) CoVe, Karpathy (2025) autoresearch
