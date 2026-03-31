# signal-to-noise ratio

> The proportion of useful information to irrelevant clutter in the context window. High SNR means the model sees what matters. Low SNR means it's scanning static.

## The Scene

ResumeForge, the resume-optimization tool. A user uploaded their resume and a job description. My prompt included both documents — plus the full system prompt (800 tokens of instructions for edge cases that weren't occurring), a formatting preamble, and a "be helpful and professional" paragraph. Total context: 3,200 tokens. Actual signal — the resume and JD: 1,400 tokens. SNR: about 0.44.

The model produced a rewrite that referenced two of the system prompt's edge-case instructions (irrelevant to this candidate) and missed a key skill match between the resume and the JD. It was attending to noise and skipping signal.

I stripped the system prompt to 200 tokens of currently-relevant instructions. Removed the formatting preamble. Killed the "be helpful" paragraph (it was never helping). New context: 1,800 tokens. SNR: 0.78. The model caught the skill match, ignored the edge cases, and produced a tighter rewrite. Fewer tokens. Better output. Lower cost.

## What This Actually Is

Every token in the context is either signal (information the model needs for this task) or noise (information that's present but irrelevant). SNR is the ratio. A high-SNR context lets the model focus. A low-SNR context forces it to identify what matters among a sea of distractions — a task models perform inconsistently.

Noise accumulates predictably: **retrieval noise** (RAG returns topically related but task-irrelevant documents), **conversation history noise** (early turns about abandoned directions), **template bloat** (2,000-token system prompts where 300 tokens are relevant to any given query), and **metadata noise** (full database records when only three fields matter). The fix is never louder signal — it's less noise. Removing 500 tokens of irrelevant context frequently improves output more than adding 500 tokens of better instructions.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| (include the full employee handbook) | "Here is Section 4.2, paragraphs 3-4 only" | Excerpting removes 95% of irrelevant tokens |
| (pass all customer fields) | "Relevant fields: plan=Professional, billing_cycle=monthly, last_payment=March 1" | Pre-filtered data eliminates field-scanning |
| (include full conversation history) | Summarize prior turns into 2-3 sentences of relevant context | History compression maintains SNR across turns |
| "Here is the background" + 800 words | Cut to the 3 facts the model actually needs for this response | Every "just in case" token costs attention |
| (pass full agent output to next agent) | Extract structured findings; strip reasoning chains and meta-commentary | Pipeline SNR degrades at every handoff without filtering |

## Before → After

**Before:**
```
You are a helpful, professional assistant. Your goal is
to provide accurate, well-structured responses that
meet the user's needs. Always be thorough and considerate.

[800 tokens of edge-case handling instructions]
[formatting preamble]
[resume: 700 tokens]
[job description: 700 tokens]

Rewrite the resume for this job.
```

**After:**
```
Rewrite this resume for the target job description.

Rules:
- Every claim must trace to the source resume
- Do not invent experience the candidate lacks
- If a JD requirement has no resume match, flag it as
  { "gap": "description", "suggestion": "how to address" }

[resume: 700 tokens]
[job description: 700 tokens]
```

**What changed:** 1,400 tokens of noise removed. The instructions that remain are the ones that matter for *this* task. SNR went from 0.44 to 0.78.

## Try This Now

```
I'll give you a prompt with deliberate noise mixed in.
Your job: identify which parts are signal and which
are noise, then produce a cleaned version.

Prompt:
"You are an expert analyst with years of experience in
data science and machine learning. Your responses should
be thorough, well-researched, and professional. Remember
to consider multiple perspectives. Here is a CSV with
Q4 sales by region. Also attached is the company mission
statement and org chart. The CEO's favorite color is blue.
Last quarter we had an offsite in Aspen.

Question: Which region had the largest quarter-over-quarter
sales decline?"

For each piece of context, label it SIGNAL or NOISE.
Then rewrite the prompt with only signal. Calculate the
token reduction percentage.
```

## When It Breaks

- **Noise as insurance** — Including extra context "just in case." The model almost never needs it. The noise consistently hurts more than the insurance helps. Run the prompt without the extra context. If the output is unchanged, it was noise.
- **Retrieval without re-ranking** — RAG returns top-K by embedding similarity, which captures topical relatedness, not task relevance. A document about the same topic but not answering the question is noise. Add a re-ranking step that filters for query-specific relevance.
- **Accumulated state as context** — In pipelines, passing the full shared state to every agent rather than each agent's relevant slice. The state grows monotonically; relevance to any specific agent does not. Scope each agent's context to its read-access fields.

## Quick Reference

- **Family:** Context architecture
- **Adjacent:** → salience (the per-item property SNR aggregates), → context budget (total tokens available; SNR measures how well they're spent), → progressive disclosure (maintains high SNR across stages by revealing only what's relevant), → retrieval scaffolding (where retrieval noise most commonly originates)
- **Model fit:** SNR sensitivity varies inversely with model capability. Frontier models tolerate moderate noise. Small models degrade rapidly — cutting context by 50% while preserving all signal almost always improves small-model output quality. For every tier, less noise beats louder signal.
