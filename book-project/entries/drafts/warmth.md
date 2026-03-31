---
headword: "warmth"
slug: "warmth"
family: "tone_style"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["authority", "register", "audience specification", "framing", "terseness"]
cross_links: ["authority", "register", "audience specification", "framing", "terseness", "narrative glue", "constrain", "specificity"]
tags: ["tone-style", "empathy", "interpersonal", "user-experience", "voice"]
has_note_box: true
note_box_type: "common_trap"
---

# warmth

**Elevator definition**
Warmth is the interpersonal dimension of model output — the quality that makes text feel like it was written by someone who cares about the reader, not just the task.

## What it is

There is a sentence a doctor can say after reading a test result: "The biopsy came back negative." And there is another way to say it: "Good news — the biopsy is clear. You can stop worrying." The medical information is identical. The second version does something the first does not: it acknowledges that the person receiving the information is a person. That acknowledgment — that the reader has feelings, concerns, a stake in the outcome — is warmth.

Warmth in writing is not sentimentality. It is not exclamation marks, not emoji, not the performative cheerfulness of a chatbot that opens with "Great question!" before answering. Those are warmth *signals* that have been so overused they now signal the opposite: a system that has been instructed to seem friendly without understanding what friendliness requires. Genuine warmth is subtler. It is the choice to say "you" instead of "the user." It is anticipating a reader's confusion and addressing it before they have to ask. It is the sentence that says "This part is tricky — here's why" instead of just "Here's why." It is taking the reader's side without condescending to them.

Language models produce warmth easily — arguably too easily. The default voice of most instruction-tuned models is already warm in a generic, customer-service way: agreeable, encouraging, mildly effusive. "Absolutely! Let me help you with that. That's a fantastic approach!" This is not warmth. This is what warmth looks like after it has been optimized for inoffensiveness across millions of interactions. It reads as a persona rather than a presence. It is warm in the way that a hotel lobby is warm: designed to give the impression of comfort without any actual intimacy.

The prompt engineer's challenge with warmth is twofold. First, *calibrating* it: the right level of warmth for customer support is wrong for a legal memorandum. An API error message should not sound nurturing. A termination letter should not sound friendly. Warmth is appropriate when the reader has an emotional stake in the content — when they are confused, frustrated, learning, or making a difficult decision. It is inappropriate when the content demands clinical precision, when warmth would dilute the gravity of the message, or when the reader would perceive it as manipulative.

Second, *authenticating* it: making model-generated warmth feel earned rather than default. This requires specificity. "Be warm and friendly" produces the hotel-lobby voice. "Write as a senior colleague who remembers how confusing this topic was when they first encountered it" produces something closer to genuine empathy — because the instruction gives the model a reason for the warmth and a specific relationship to model it on.

Warmth and → authority are the two most important tonal dimensions for professional text, and they are independent, not opposed. A pediatrician explaining a treatment plan has high warmth and high authority. A military operations briefing has high authority and low warmth. A casual mentoring session has moderate warmth with moderate authority. The common mistake is treating them as a zero-sum trade-off — turning down authority to turn up warmth, or suppressing warmth to sound more expert. The best professional writing does both, and the balance depends entirely on → audience specification.

## Why it matters in prompting

Warmth controls whether the reader feels addressed or processed. This matters most in three contexts: teaching, customer communication, and sensitive topics.

In teaching, warmth is the difference between a model that explains and one that teaches. Explanation is information transfer. Teaching is information transfer plus the awareness that learning is hard. A warm teaching voice normalizes confusion ("This notation trips up everyone the first time"), anticipates frustration ("If this seems circular, you're not wrong — here's why it works anyway"), and celebrates progress without patronizing ("Now you have the pieces — let's put them together"). These micro-gestures keep the reader engaged where a purely informational tone would lose them.

In customer communication, warmth is a design requirement. Users contacting support are often already frustrated. A terse, factual response that solves their problem technically may still leave them feeling dismissed. The same solution wrapped in a voice that acknowledges the inconvenience, explains the fix clearly, and closes with genuine (not performative) helpfulness produces a materially different customer experience.

Role prompting is the most effective mechanism for warmth calibration [src_paper_schulhoff2025]. "You are a patient, experienced tutor" produces warmer output than "Explain X." The role gives the model a relationship to simulate, and relationships carry warmth more naturally than abstract style instructions do.

## Why it matters in agentic workflows

In agent pipelines, warmth is almost always a property of the final output agent — the one whose text is seen by a human. Internal pipeline agents passing data between each other do not need warmth; it wastes tokens and can introduce ambiguity. (A warm phrasing like "You might want to check the error rate" is less useful to a downstream agent than "Error rate: 4.7%, above 3% threshold.") But the agent that compiles the final user-facing report, email, or message needs warmth calibrated to the recipient.

This creates an architectural pattern: **pipeline coldness with terminal warmth**. The internal agents operate with terse, precise, machine-optimized communication. The final agent translates structured findings into human-readable, audience-appropriate, tonally calibrated output — including warmth where warranted. The warmth instruction belongs in the terminal agent's system prompt, not in the pipeline's shared configuration.

## What it changes in model behavior

Warmth instructions increase the use of second person ("you"), inclusive first person ("we"), empathetic acknowledgments ("this can be frustrating"), softened imperatives ("you might try" vs. "do"), and transitional phrases that guide the reader. Sentence rhythm shifts toward shorter sentences interspersed with longer ones, creating a conversational cadence. The model is more likely to anticipate questions, address potential confusion proactively, and close with a forward-looking or encouraging statement.

## Use it when

- The reader has an emotional stake in the content (health information, error messages, rejections, difficult decisions)
- The output is pedagogical and the reader is learning something new or difficult
- The output is customer-facing and represents a brand that values empathy
- The reader may be frustrated, confused, or anxious, and a purely informational tone would feel dismissive
- You are building a conversational agent whose personality is part of the product experience
- The output delivers bad news and the reader needs to feel that the author understands the weight of it

## Do not use it when

- The output is a legal document, contract, or regulatory filing where warmth would undermine precision or create ambiguity
- The audience is technical peers who would perceive warmth as condescension
- The output is machine-consumed (agent-to-agent, data pipelines) and warmth wastes tokens
- The content is clinical or forensic (incident reports, audit findings) and emotional tone would compromise perceived objectivity

## Contrast set

**Closest adjacent abstractions**

- → authority — Independent dimension. Authority conveys expertise; warmth conveys care. A pediatric oncologist explaining a treatment plan needs both at maximum. A parking ticket does not need warmth. A lab report does not need either.
- → register — Broader. Warmth is one dimension of register. You can set a warm register, a cold register, or a neutral one. Register also includes formality, technicality, and directness, which are orthogonal to warmth.
- → terseness — Tension. Warmth requires some words that terseness would cut — the empathetic aside, the "here's why this matters to you" sentence. Getting both right means being warm efficiently: caring with few words rather than padding with caring words.

**Stronger / weaker / narrower / broader relatives**

- → audience specification — Broader. The audience determines how much warmth is appropriate. Expert peers need less. Novices need more. Upset customers need the most.
- → framing — Complementary. Framing sets the model's analytical orientation; warmth sets its interpersonal orientation.
- → narrative glue — Related. Narrative glue (transitional prose) can carry warmth or not. "Now that we've covered X, let's look at Y" is warm narrative glue. "Section 2: Y" is cold structure.

## Common failure modes

- **Warmth as condescension** → The model overshoots warmth and produces text that sounds patronizing. "Don't worry, this is a really tricky concept and it's totally okay to be confused!" is warm in a way that insults the reader's intelligence. This happens when warmth is instructed without specifying the audience's competence level. Fix: pair warmth with audience specification. "Write warmly but respect the reader's technical competence. They are not confused — they are learning."

- **Default warmth theater** → Without specific warmth instructions, the model produces its RLHF-trained default: "Great question! I'd be happy to help!" followed by competent but personality-free explanation. This is not warmth — it is performance. It reads as genuine to no one. Fix: either specify a warmth *source* (a role, a relationship, a reason for caring) or explicitly suppress the default ("Do not open with a compliment about the question. Do not express enthusiasm about helping. Just help.").

- **Warmth in the wrong context** → A model writing an incident post-mortem that says "We know this has been really frustrating, and we totally understand your concern!" has imported customer-support warmth into an engineering document. The audience — other engineers — reads this as deflection or as a sign that the author does not take the incident seriously. Fix: specify the audience and the genre. Warmth in an incident report means something different: it means candid acknowledgment of impact, not empathetic hedging.

## Prompt examples

### Minimal example

```text
A user's API key has been rate-limited. Write the error
message they see in the dashboard.

Tone: Calm, helpful, not apologetic. Explain what happened,
what they can do (wait or upgrade), and where to find more
information. Treat the user as competent. Do not blame them.
Do not be effusive.
```

### Strong example

```text
Role: You are a senior developer writing documentation for
a library you built. You remember how confusing the setup
was before you understood it, and you are writing for someone
at that stage now.

Task: Write a getting-started guide for configuring
authentication in this library.

Voice requirements:
- Warm but not folksy. The reader is a professional.
- Anticipate the two or three points where setup commonly
  fails and address them before the reader hits them.
  Frame these as "this is a known rough spot" not
  "here's what you're probably doing wrong."
- Use "you" and "your." Avoid "one" and "the user."
- If a step is genuinely tedious, acknowledge it:
  "This part is manual and there's no shortcut — but it
  only has to be done once."
- Close with what the reader can do now that setup is
  complete — give them momentum, not just a finish line.

Do not open with a paragraph about why authentication matters.
The reader already knows. Start with step 1.
```

### Agentic workflow example

```text
Pipeline: Patient Communication Generator

Agent 1 — Clinical Data Extractor
System prompt: Extract structured clinical data from the
physician's notes. Output JSON. Fields: diagnosis, treatment
plan, medications, follow-up timeline, restrictions.
No prose. No warmth. Machine output only.

Agent 2 — Risk and Context Annotator
System prompt: Annotate the clinical data with patient-relevant
context. For each medication: common side effects the patient
should know about. For each restriction: plain-language
explanation of why. For the follow-up timeline: what the
patient should expect at each stage. Output structured
annotations keyed to the original fields.

Agent 3 — Patient Letter Writer
System prompt: You are the patient's doctor. Write a letter
the patient will read at home after their appointment.
Use the clinical data and annotations from the upstream agents.

Warmth requirements:
- Address the patient by name. Use "you" and "your."
- Open by acknowledging the visit and the patient's concern.
- Explain the diagnosis in plain language. Do not minimize it,
  but do not catastrophize. State what it means for them
  specifically.
- For each medication, explain what it does and what to watch
  for. Use the side-effect annotations but present them as
  "most people don't experience these, but if you do..."
- Close with the follow-up plan and an explicit invitation
  to call with questions.
- The letter should feel like it was written by a human who
  cares about this specific patient, not generated by a
  system processing a queue.

Warmth boundary: Do not make promises about outcomes.
Do not use phrases like "everything will be fine."
Honest warmth, not false comfort.
```

## Model-fit note

All model tiers produce warmer output when instructed, but the *quality* of warmth varies. Frontier models calibrate warmth well — they can be warm without being saccharine, empathetic without being patronizing, and can sustain calibrated warmth across long documents. Midsize open models sometimes overshoot warmth into effusiveness or undershoot into the default hotel-lobby tone. Small models tend to express warmth through exclamation marks and superlatives rather than through the subtler mechanisms (anticipating confusion, using "you," acknowledging difficulty). For small models, role-based warmth instructions ("You are a patient mentor") outperform abstract style instructions ("Be warm").

## Evidence and provenance

Role prompting as a mechanism for tonal control, including interpersonal dimensions like warmth, is documented in The Prompt Report [src_paper_schulhoff2025]. The observation that instruction-tuned models default to a generic positive tone is a widely noted consequence of RLHF alignment training. The distinction between authentic warmth (earned through specificity and relationship modeling) and performative warmth (default agreeableness) is a practitioner finding. The independence of warmth and authority as tonal dimensions draws on communication studies (Cuddy, Fiske, & Glick, 2008), where warmth and competence are established as the two primary dimensions of social judgment.

## Related entries

- **→ authority** — the expertise dimension, independent of warmth; the best professional writing balances both
- **→ register** — warmth is one dimension of the register you set
- **→ audience specification** — the audience determines how much warmth is appropriate
- **→ terseness** — in tension with warmth; warm prose needs words that terse prose cuts
- **→ narrative glue** — transitional prose that can carry warmth or operate without it

---

> **Common Trap**
>
> The most common warmth failure is not too little — it is too much of the wrong kind. Models trained with RLHF have a deep prior toward agreeableness: they validate, they encourage, they compliment. "That's a great insight!" "Absolutely, you're on the right track!" This is not warmth. It is a reflex. Real warmth is in the sentence that says "This part is harder than it looks — here's the trick that makes it click." That sentence does three things the compliment does not: it validates the reader's struggle without being asked, it demonstrates the writer's experience, and it promises specific help. If your model's warmth sounds like a customer satisfaction survey, the warmth instruction needs to be more specific, not more emphatic.
