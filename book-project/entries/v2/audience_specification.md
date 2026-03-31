# audience specification

> Tell the model who's reading, and watch vocabulary, depth, structure, and assumed knowledge all shift at once.

## The Scene

You're building the AI Ethics Coach Chrome extension. It needs to explain the same ethical concept — say, algorithmic bias — three different ways: for a product manager deciding whether to ship, for an ML engineer debugging a model, and for an executive writing a public statement. Same facts. Completely different outputs. The only thing that changes between prompts is one line: the audience.

That single line does more work than a paragraph of formatting instructions. It implicitly controls what to assume, what to explain, what to skip, and how to organize.

## What This Actually Is

Every piece of writing has a reader. When you tell the model who that reader is, you're not adjusting style — you're restructuring the entire output. An expert audience gets jargon, compressed reasoning, and no preamble. A novice audience gets analogies, definitions, and a build-up from simple to complex. A decision-maker gets implications first, evidence second, and no implementation details.

The model *always* writes for an audience. If you don't specify one, it defaults to a vaguely educated, vaguely curious nobody — the textual equivalent of a one-size-fits-all t-shirt.

Specify the audience along three dimensions: **domain familiarity** (what they know), **role** (what they need the information for), and **reading context** (where they'll consume it). "A senior data engineer evaluating migration options for a quarterly planning doc" covers all three. "A technical reader" covers none.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Explain this simply" | "Explain this for a product designer who has never trained a model" | Defines what "simple" means for this specific reader |
| "Write for a technical audience" | "Write for a senior backend engineer who knows PostgreSQL but has never used CockroachDB" | Tells the model exactly what to assume and what to teach |
| "Make it accessible" | "The reader is a non-technical VP who will skim this in 2 minutes between meetings" | Controls length, structure, and jargon simultaneously |
| "Use appropriate language" | "The reader is a regulatory affairs specialist reviewing an IND submission" | Domain + role + context in one line |

## Before → After

**Before:**
```
Explain how DNS resolution works.
```

**After:**
```
Explain how DNS resolution works.

Audience: A backend developer who has never debugged a DNS issue.
They understand HTTP, TCP/IP basics, and client-server architecture,
but they do not know what happens between typing a URL and the
first SYN packet.
```

**What changed:** The model now knows what to assume (HTTP, TCP/IP) and what to teach (the DNS lookup chain). It won't waste time explaining what a server is, and it won't skip the recursive resolver.

## Try This Now

```
Explain what a database index is — but do it three times:

1. For a junior frontend developer who has only used ORMs
2. For a DBA with 10 years of PostgreSQL experience
3. For a CEO deciding whether to fund a database optimization project

Keep each version under 80 words. After all three, note which
details you included and excluded in each, and why.
```

The model will produce three genuinely different explanations — not just rewrites at different reading levels, but different *information architectures*.

## When It Breaks

- **Phantom audience** → The prompt specifies an audience but contradicts it: "Write for a five-year-old. Include citations to the primary literature." The model can't serve both. Ensure all instructions are consistent with the stated reader.
- **Audience as jargon filter only** → You treat audience specification as vocabulary control ("don't use jargon") instead of structural instruction. The model simplifies words but keeps expert-level organization. Fix: specify what the audience needs to *understand*, not just what words they tolerate.

## Quick Reference

- Family: tone & style
- Adjacent: → authority (audience-dependent tonal choice), → context (information the model has vs. who it's presenting to), → clarity
- Model fit: Audience adaptation is reliable across all model tiers. Even small models shift vocabulary and depth. Frontier models handle nuanced descriptions ("a regulatory affairs specialist at a mid-size pharma company") and maintain calibration across long outputs.
