# vagueness

> Instructions so broad the model must invent the specifics you failed to provide — producing 500 words of well-structured nothing.

## The Scene

AI Ethics Coach, a prospective client demo. The client said: "Can it analyze our AI practices?" I typed: "Analyze this company's AI practices and give recommendations." The model returned 900 words covering bias, transparency, accountability, privacy, environmental impact, workforce displacement, and intellectual property. It was technically responsive, topically relevant, and practically useless. The client said: "But what should we actually *do*?"

The model hadn't failed. I had. The prompt said "analyze" without specifying: analyze *what* about their practices? Against *which* standard? For *whom*? To support *what decision*? The model filled every unspecified dimension with its most generic option. The result was a Wikipedia article wearing a consulting report costume.

Fix: "Compare the attached AI governance policy against the NIST AI Risk Management Framework. For each of the 4 framework functions (Govern, Map, Measure, Manage), state whether the policy addresses it fully, partially, or not at all. For each gap, recommend one specific action. Format: table." The 900-word blur became a 300-word action plan.

## What This Actually Is

Vagueness is the most common prompting failure. A vague prompt describes a direction without the specifics needed to arrive anywhere. "Analyze this data." "Write something about marketing." "Help me with my code." A human colleague would ask follow-up questions. A model answers — confidently, fluently, generically.

The mechanism: models predict the most probable next token given the context. A vague prompt provides weak context, so the model falls back on broad priors: common phrasings, safe opinions, middle-of-the-road analysis. The output reads like it was written by someone who has read a lot but experienced nothing.

The fix is not a longer prompt. It's the *right 30 words*: a clear goal, a defined audience, a specified format, and a bounded scope. Four species of vagueness to watch for: **goal** (what does success look like?), **audience** (who reads this?), **format** (paragraph? table? JSON?), and **scope** (what's in, what's out?).

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Analyze this data" | "Identify the three largest cost drivers in Q4, compare each to Q3, present as a table" | Goal + scope + format in one sentence |
| "Write about marketing" | "Write a 200-word positioning statement for [product] targeting [persona], emphasizing [differentiator]" | Goal + audience + constraint fills the vacuum |
| "Help me with this code" | "This function should return X but returns Y. Here's the input, expected output, and actual output" | Problem specification replaces vague request |
| "Give me insights" | "What is the single most actionable finding for the sales team?" | Forces one output instead of everything |
| "Make it better" | "The intro is too long. Cut it to 2 sentences. Keep the hook, drop the background" | Names the problem and the fix |

## From the Lab

We tested how instruction verb choice affects output specificity. Vague verbs ("analyze," "discuss," "explore") produced significantly more generic output than precise verbs ("compare against X," "rank by Y," "identify the three largest"):

![Instruction Verb Word Choice](../art/figures/exp_instruction_verbs_word_choice.png)

**Key finding:** Swapping a vague verb for a precise one — with no other prompt changes — reduced output vagueness by 30-50% across all model families. The verb sets the model's response mode before it reads the rest of the prompt.

## Before → After

**Before:**
```
Analyze this data and give me insights.
```

**After:**
```
You have Q4 2025 sales data for three product lines.

Task: Identify the single largest revenue decline.
For that decline:
1. Quantify: absolute drop and % vs. Q3
2. Top 2 contributing factors from the data
3. One specific action for the sales team in Q1 2026

Format: numbered list, 150-200 words.
Audience: VP of Sales.
```

## Try This Now

```
I'll give you a vague prompt. Your job: diagnose which
types of vagueness are present, then fix each one.

Vague prompt: "Review our strategy and let me know
what you think."

For each vagueness type, score it:
- Goal vagueness: present? what's missing?
- Audience vagueness: present? what's missing?
- Format vagueness: present? what's missing?
- Scope vagueness: present? what's missing?

Then rewrite the prompt with all four filled in.
Show the word count of both versions. The fixed
version should be under 50 words.
```

## When It Breaks

- **Vagueness laundering** — The prompt *sounds* specific because it uses formal language: "Conduct a comprehensive analysis leveraging cross-functional insights." Strip the jargon and ask: does this tell the model what to produce, for whom, in what format? If not, it's still vague.
- **Assumed context** — You assume the model knows your project, data, and goals. It doesn't. It fills the gap with generic assumptions. Fix: state context explicitly.
- **The vagueness cascade** — Vagueness in stage 1 produces generic output, which becomes generic input for stage 2. By stage 3, the output is content-free. Fix: enforce specificity gates at each pipeline stage.

## Quick Reference

- **Family:** Failure mode
- **Adjacent:** → underspecification (vagueness is a wide lens; underspecification is a missing piece — they overlap but are distinct), → specificity (the direct antidote), → scope (bounding the territory is one fix for scope vagueness), → constrain (adding constraints fills the format and length gaps)
- **Model fit:** All models suffer from vague prompts, but differently. Larger models produce sophisticated-sounding generic output — harder to recognize as generic. Smaller models produce obviously shallow output, making the problem visible faster. Neither size compensates for vagueness. Specificity is a prompt property, not a model capability.
