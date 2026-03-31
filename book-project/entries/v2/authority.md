# authority

> The quality in writing that conveys earned expertise — the reader trusts it not because it claims credibility but because its precision demonstrates it.

## The Scene

You need a technical explanation of why VACUUM FULL is dangerous on production PostgreSQL tables. The model's default output: "It's important to note that VACUUM FULL can cause issues in production environments. There are several key considerations..."

That voice — smooth, hedged, peppered with "it's worth noting" — is the uncanny valley of expertise. It sounds like it might know something. It commits to nothing.

You rewrite the prompt: "You are a database reliability engineer with 10 years of PostgreSQL at scale. A junior engineer asks why VACUUM FULL is dangerous on production tables. Answer directly. Use correct terminology. Do not oversimplify."

The output transforms. Specific lock types. Actual failure scenarios. The difference between routine VACUUM and FULL. The tone shifts from cautious intern to someone who has seen things break at 3 AM.

## What This Actually Is

Authority is not confidence turned up. "It is absolutely certain that transformers will dominate for a decade" has zero authority — that's bluster. Authority sounds like this: "Transformers have dominated sequence modeling since 2017. No competing paradigm has matched their performance at scale, though state-space models are narrowing the gap in specific domains." The second knows what it knows, names what it doesn't, and lets the reader draw conclusions. That restraint *is* the authority.

Authority in model output comes from three things: domain-appropriate vocabulary (the right words, not jargon for show), structural confidence (assertions that build on each other), and calibrated certainty (strong claims where evidence is strong, qualified claims where it's not).

Role prompting is the most direct tool. But "You are an expert" is nearly useless. Expert in what? For whom? The specificity of the role *is* the authority.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "You are an expert" | "You are a senior staff engineer at a company running PostgreSQL clusters serving 50M DAUs" | Specificity produces authority; "expert" is a compliment, not an instruction |
| "Write authoritatively" | "State claims with confidence where evidence supports them. Flag uncertainty explicitly where it does not." | Prevents the model from just dropping all hedges (some are warranted) |
| "Be confident" | "Do not use phrases like 'it's important to note' or 'there are several key factors.' State what you know. Qualify what you don't." | Kills filler while preserving honest uncertainty |
| "Sound professional" | "Write as if presenting findings at a technical conference where the audience will challenge vague claims" | The imagined audience enforces rigor |

## Before → After

**Before:**
```
Explain the impact of the HTTP/2 Rapid Reset vulnerability.
```

**After:**
```
Role: Senior security researcher presenting at a technical conference.
Audience: Experienced practitioners who will challenge vague claims.

Explain the practical impact of CVE-2023-44487 (HTTP/2 Rapid Reset).
- Open with the core mechanism in 2-3 sentences
- Explain why existing rate-limiting was insufficient
- Quantify the amplification factor where data exists
- Distinguish confirmed findings from speculation
- Close with mitigation steps ordered by priority
```

**What changed:** The role, audience, and structure conspire to produce output that sounds like it was written by someone who has done the work — because the prompt forced the model to operate like someone who has.

## Try This Now

```
Write two versions of the same technical explanation:

Topic: Why connection pooling matters for database performance

VERSION A: No role. Just "Explain why connection pooling matters."

VERSION B: "You are a platform engineering lead who has personally
debugged connection exhaustion incidents at 2 AM. A new hire asks
why your team mandates connection pooling. Explain directly.
No filler. Use specific numbers where possible."

After both, identify three specific differences in how authority
manifests between the two versions.
```

## When It Breaks

- **Authority through assertion** → The model drops all hedges, including warranted ones. The output sounds confident but is now less accurate. True authority includes knowing when to hedge.
- **The empty expert** → Prestigious role ("world-renowned neuroscientist") but no domain context or source material. The model generates sophisticated-sounding vagueness. Pair role prompting with actual reference material.
- **Authority as verbosity** → The model interprets "authoritative" as "thorough" and produces sprawling output. A genuinely authoritative voice knows what to leave out. Add length constraints.

## Quick Reference

- Family: tone & style
- Adjacent: → audience_specification (determines how much authority to deploy), → clarity, → explicitness
- Model fit: Frontier models produce convincing authority with specific roles and domain context. Smaller models interpret "authoritative" as "formal" and produce stiff textbook prose. Code-specialized models have natural authority in technical domains but struggle with non-technical prose.
