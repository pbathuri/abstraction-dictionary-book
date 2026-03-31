# warmth

> The quality that makes text feel like it was written by someone who cares about the reader — not sentimentality, not exclamation marks, but the sentence that anticipates your confusion before you have to ask.

## The Scene

Clap/OpsPilot, customer-facing error messages. The original message when a user's API key was rate-limited: "Error 429: Rate limit exceeded. Try again later." Technically correct. Emotionally tone-deaf. Users reported feeling "punished" — they didn't understand why, what to do, or when "later" was.

The rewrite: "You've hit your API rate limit (1,000 requests/hour on your plan). Resets at [time]. Options: wait, or upgrade [link]. This is a normal safeguard, not an error on your part." Same information. Different experience. The user knows what happened, why, what to do, and that they didn't break anything. That last sentence is warmth: anticipating an anxiety the user hasn't voiced.

The internal pipeline agents that assembled the error data? Cold, terse JSON. Warmth belonged in the terminal agent — the one whose text a human reads. Pipeline coldness with terminal warmth. That's the architecture.

## What This Actually Is

Warmth is the interpersonal dimension of output — the difference between a system that processes you and a person who addresses you. It's "you" instead of "the user." It's "This part is tricky — here's why" instead of just "Here's why." It's anticipating confusion and addressing it before the reader has to ask.

Models produce warmth easily — too easily. The default RLHF voice is warm in a hotel-lobby way: "Great question! I'd be happy to help!" That's performance, not warmth. Real warmth requires specificity: a role, a relationship to the reader, a reason for caring. "Be warm" produces the hotel-lobby voice. "Write as a senior colleague who remembers being confused by this" produces something earned.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Great question!" | (Delete it. Start with the answer) | Performative validation earns no trust |
| "The user should..." | "You can..." | Second person creates direct address |
| "Error: invalid input" | "That input didn't work — here's what it expects and a quick example" | Anticipates the reader's next question |
| "Be warm and friendly" | "Write as a senior colleague who remembers how confusing this topic was when they first learned it" | Role gives the model a *reason* for warmth |
| "Important to note" | "This is the part that trips people up" | Normalizes the reader's struggle instead of lecturing |

## From the Lab

We tested the same content at different register levels, from clinical to warm. The warmth dimension was independent of accuracy — warm outputs were equally factual, but readers rated them higher on clarity and trustworthiness:

![Register Comparison](../art/figures/exp_same_content_different_register_register.png)

**Key finding:** Calibrated warmth improved perceived clarity by 15-20% without reducing factual density. Readers didn't just *feel* the warm version was better — they extracted information from it more accurately. Warmth is not decoration. It's a readability intervention.

## Before → After

**Before:**
```
Write documentation for the authentication setup
in this library.
```

**After:**
```
You are a senior developer writing docs for a library
you built. You remember how confusing the setup was
before you understood it. Write for someone at that
stage now.

Task: Getting-started guide for authentication setup.

Voice:
- Warm but not folksy. The reader is a professional.
- Anticipate 2-3 common failure points. Frame them as
  "this is a known rough spot" not "here's what you're
  probably doing wrong."
- Use "you" and "your." Avoid "one" and "the user."
- If a step is tedious, acknowledge it: "This part is
  manual — but it only needs to happen once."
- Close with what the reader can do now. Give them
  momentum, not just a finish line.

Do not open with why authentication matters.
They already know. Start with step 1.
```

## Try This Now

```
I'll give you the same technical fact. Write it three
ways with different warmth levels.

Fact: "The database migration will cause 5-10 minutes
of downtime during the maintenance window."

Version 1: Cold (internal engineering log entry)
Version 2: Neutral (status page update for all users)
Version 3: Warm (email to a customer whose workflow
  will be interrupted)

After all three, explain: which words changed between
versions? Which version is longest and why? Where does
warmth add words that terseness would cut?
```

## When It Breaks

- **Warmth as condescension** — The model overshoots and sounds patronizing: "Don't worry, this is super tricky and it's totally okay to be confused!" Fix: pair warmth with audience specification. "Write warmly but respect the reader's competence. They are learning, not struggling."
- **Default warmth theater** — Without specific instructions, the model produces its RLHF default: "I'd be happy to help!" followed by personality-free explanation. Fix: either give a warmth *source* (role, relationship) or suppress the default ("Do not compliment the question. Do not express enthusiasm. Just help.").
- **Warmth in the wrong context** — An incident post-mortem that says "We totally understand your frustration!" imports customer-support warmth into an engineering document. The audience reads it as deflection. Fix: specify the audience and genre. Engineering warmth is candid acknowledgment, not empathetic hedging.

## Quick Reference

- **Family:** Tone / style
- **Adjacent:** → authority (independent dimension — best professional writing balances both), → register (warmth is one dimension of the register you set), → terseness (in tension — warmth requires some words terseness would cut; the craft is being warm efficiently), → audience specification (the audience determines how much warmth is appropriate)
- **Model fit:** All tiers produce warmer output when instructed. Frontier models calibrate well — warm without saccharine, empathetic without patronizing. Midsize models sometimes overshoot into effusiveness. Small models express warmth through exclamation marks and superlatives. For small models, role-based warmth ("You are a patient mentor") outperforms abstract instructions ("Be warm").
