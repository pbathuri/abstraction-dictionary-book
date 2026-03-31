# checkpoint

> A gate between pipeline stages where progress is saved, quality is verified, and the system decides whether to proceed, retry, or escalate.

## The Scene

Your Form8 n8n workflow has five steps: retrieve sources, extract claims, verify claims, synthesize findings, format report. You built it as a straight pipeline — each step feeds the next, no checks. It works great on your test cases. Then real data hits, and the extraction step hallucinates a statistic. The verification step can't catch it because the hallucinated number looks plausible. The synthesis step builds a conclusion around it. The report goes out with a fabricated data point wearing a suit.

One checkpoint — "verify that every extracted claim appears verbatim in the source document" — between extraction and verification would have caught it. That's a 30-second addition that prevents a career-limiting email.

## What This Actually Is

A checkpoint serves three jobs at once: **preservation** (save what you have so failure doesn't erase progress), **verification** (check that quality criteria are met), and **routing** (decide what happens next based on what the check found).

Hope is not a quality strategy. A well-designed checkpoint specifies: what to verify, what criteria to use, what to do when it fails (retry? fallback? escalate?), and what "pass" looks like — not "looks okay" but explicit pass criteria.

The placement matters: too few checkpoints and failures propagate silently; too many and the pipeline spends more time checking than working. Put them at abstraction boundaries — the seams where one type of work hands off to another. After retrieval, before analysis. After analysis, before generation.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| (no verification between steps) | "CHECKPOINT: Verify every extracted figure appears verbatim in the source. Do not proceed until verified or flagged." | Active gate, not passive hope |
| "Check that it's okay" | "Verify: format is valid JSON, all required fields present, no field is null" | Testable criteria, not vibes |
| "Review before continuing" | "If any checkpoint fails: retry with modified prompt (max 2 retries), then escalate to human review" | Failure handler is mandatory — what happens when it fails? |
| "Make sure it's good" | "Score each section 1-5 on accuracy, completeness, and source fidelity. Proceed only if all scores ≥ 3." | Quantified gate with explicit threshold |

## Before → After

**Before:**
```
Step 1: List the three strongest arguments.
Step 2: Write a summary paragraph.
```

**After:**
```
Step 1: List the three strongest arguments in this article.
Step 2: For each argument, check whether the article provides
        supporting evidence. Mark each as SUPPORTED or UNSUPPORTED.
Step 3: Using only SUPPORTED arguments, write a summary paragraph.
```

**What changed:** Step 2 is a checkpoint. It forces verification before the summary is written, preventing unsupported claims from sneaking into the final output.

## Try This Now

```
Process this claim in three stages with checkpoints:

Claim: "Remote workers are 13% more productive than office workers."

Stage 1 — Source check: Is this a real statistic? If so, who
published it, when, and with what methodology?
CHECKPOINT: Can you trace this to a specific study? If not,
flag as UNVERIFIED and do not proceed to Stage 2.

Stage 2 — Context check: What caveats or limitations apply?
CHECKPOINT: List at least 2 limitations. If you can't find any,
flag as SUSPICIOUSLY CLEAN.

Stage 3 — Verdict: Should someone cite this in a business presentation?
```

## When It Breaks

- **Rubber-stamp checkpoint** → Verification that always passes. The checkpoint exists in the architecture diagram but catches nothing. If you can't articulate what "fail" looks like, the checkpoint is theater.
- **Checkpoint as bottleneck** → Full evaluator-model review at every step turns a 30-second pipeline into a 5-minute one. Match checkpoint weight to failure cost.
- **Missing recovery logic** → The checkpoint detects failure but has no next action. It logs "FAIL" and then... what? Every checkpoint needs a failure handler.

## Quick Reference

- Family: agent workflow
- Adjacent: → audit_trail (records checkpoint outcomes), → contradiction_detection (common verification at checkpoints), → feedback_loop (checkpoint failure data feeds improvement)
- Model fit: Self-verification works best with large models. Smaller models rubber-stamp their own work — use a separate evaluator or structural/programmatic checks instead.
