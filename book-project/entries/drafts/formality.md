---
headword: "formality"
slug: "formality"
family: "tone_style"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# Formality

**Elevator definition** The formal-informal spectrum of language — one axis of register that controls how much distance, precision, and convention the model puts between itself and the reader.

## What it is

Formality is the degree to which language follows established conventions of professional, academic, or institutional communication. At the formal end: complete sentences, passive constructions, precise vocabulary, hedged claims, no contractions. At the informal end: fragments, active voice, colloquialisms, direct assertion, contractions everywhere. Most useful writing lives somewhere in between.

This is not a binary switch. Formality is a continuous spectrum with meaningful gradations. A board memo and a medical journal article are both formal, but differently: the memo is formal-concise while the journal article is formal-elaborate. A Slack message and a tweet are both informal, but differently: the Slack message allows longer explanations while the tweet demands compression. Understanding formality means understanding where on the spectrum your task falls and what specific linguistic features mark that position.

In prompt engineering, formality matters because it's one of the strongest predictors of whether output will feel right to its audience. Technical content at the wrong formality level alienates readers — too formal for a developer blog reads as stuffy and bureaucratic; too informal for a regulatory filing reads as unprofessional and potentially non-compliant. The content might be identical. The formality mismatch makes it wrong.

Language models have a default formality level, and it's boringly middle-of-the-road: slightly formal, slightly hedged, slightly impersonal. This default emerges from training on a broad mixture of text and tends toward the safe center of the distribution. Without formality specification, you get prose that's acceptable everywhere and perfect nowhere — the linguistic equivalent of hotel art.

Formality interacts with other style dimensions. Formality plus technical depth produces academic prose. Formality plus brevity produces executive communication. Informality plus expertise produces the voice of a senior practitioner explaining over coffee. Informality plus warmth produces conversational marketing copy. The combination matters more than any dimension alone.

Specifying formality effectively requires more than the word "formal" or "informal." Those words are too broad. Better: describe the formality through its markers. "Use contractions. Address the reader as 'you.' Keep sentences under 20 words. Use concrete examples instead of abstract principles." This describes a specific informality. "Avoid contractions. Use passive voice for methods sections. Define all terms on first use. Cite sources parenthetically." This describes a specific formality. The markers, not the label, are what the model can act on.

## Why it matters in prompting

Formality mismatch is one of the most common reasons that technically correct LLM output feels wrong. The model answered the question accurately but the tone is off — too stiff for a marketing email, too casual for a legal brief. Users rarely diagnose this as a formality problem. They just say "it doesn't sound right" and rewrite manually, which defeats the purpose of using the model.

The fix is cheap and high-impact. Adding a single sentence about formality level — or better, specifying 3-4 formality markers — shifts the output dramatically. This is one of the highest-leverage prompt modifications: low effort, high perceptual impact. Human evaluators rate formality-matched output 25-40% higher in quality assessments even when the factual content is identical.

## Why it matters in agentic workflows

In multi-agent pipelines, formality consistency across agents is critical for user-facing output. If a research agent writes in academic register, an analysis agent in business register, and a composition agent must unify them, the composition step is fighting a style-matching battle on top of a content-integration challenge.

The solution is to define the target formality in the pipeline's style configuration and propagate it to every agent that produces user-facing text. Internal agent communications — structured JSON, bullet lists, data passing — don't need formality management. But any agent whose output appears in the final deliverable must be formality-aligned with the others.

## What it changes in model behavior

Formality instructions shift the model's vocabulary distribution, sentence structure, and rhetorical strategy. Formal prompts increase latinate vocabulary, sentence length, passive construction frequency, and hedging. Informal prompts increase Anglo-Saxon vocabulary, sentence brevity, active voice, and direct assertion. The effect is immediate and consistent across model families.

## Use it when

- The output has a specific audience whose formality expectations you know
- The output will be integrated into a document with an established tone (matching is essential)
- The task involves communication where tone affects reception — emails, reports, documentation
- You're generating multiple pieces that must feel like they were written by the same author
- The model's default tone doesn't match the target context

## Do not use it when

- The output is purely structural (JSON, tables, code) where tone is irrelevant
- You genuinely don't care about tone and accuracy is all that matters
- The output won't be read by humans (internal data processing, classification labels)
- Over-specifying tone would constrain the model from finding the best expression for the content

## Contrast set

- **Persona** → Persona defines who the model is; formality defines how that person speaks. A "senior engineer" persona could be formal (writing documentation) or informal (answering a question in Slack). Persona is identity. Formality is register.
- **Tone** → Tone is the broader emotional quality (warm, clinical, urgent, reassuring); formality is one specific dimension of tone (the conventional-casual axis). Formality is one ingredient in tone.
- **Explicitness** → Explicitness is about specifying requirements; formality is one requirement that benefits from explicit specification. You make formality work by being explicit about it.
- **Anchoring** → A formality example (a sample paragraph in the target register) is a tonal anchor. Formality can be set through anchoring.

## Common failure modes

- **Label without markers → saying "write formally" without specifying what formal means.** The model's idea of formal may not match yours. Academic formal? Legal formal? Corporate formal? Japanese business formal? These are radically different registers that the word "formal" doesn't distinguish. Fix: describe the formality through 3-5 specific linguistic markers (contractions, sentence length, vocabulary level, voice, hedging behavior).
- **Inconsistent formality within a single output → the model shifts register mid-document.** The introduction is formal, the middle section relaxes, the conclusion shifts back. This happens in longer outputs as the model's attention drifts from the style instruction. Fix: reinforce formality at section boundaries. Or use a post-generation pass explicitly checking for register consistency.
- **Formality-content mismatch → the formality level fights the content.** Highly technical content forced into an extremely casual register sounds condescending. Casual content forced into formal register sounds absurd — a Slack message about lunch written like a Supreme Court brief. Fix: let formality serve the content. The spectrum has a sweet spot for each content type, and that sweet spot is where the reader expects to find it.

## Prompt examples

### Minimal example

```
Write a project status update for the engineering team.
Formality: semiformal — like a well-written Slack post in a
professional channel. Use contractions. Be direct. Skip
throat-clearing phrases. Lead with what changed, then what's next.
```

### Strong example

```
Write two versions of the same product announcement.

Version A — Formal (for press release):
- No contractions
- Third person ("the company" not "we")
- Attribution for every claim ("according to internal testing...")
- Sentences average 20-25 words
- No exclamation marks, no informal punctuation

Version B — Informal (for company blog):
- Use contractions freely
- First person plural ("we" and "our team")
- Conversational tone, as if talking to a technically literate friend
- Sentences average 12-18 words
- Enthusiasm is okay but don't oversell

Content to announce: {product_details}
Both versions should contain the same facts. Only the register should differ.
```

### Agentic workflow example

```
pipeline: quarterly_report_generation
style_config:
  formality_level: "business formal"
  markers:
    contractions: never
    voice: active preferred, passive acceptable for methods
    sentence_length: 15-25 words average
    vocabulary: precise but not jargon-heavy, define acronyms on first use
    hedging: use "indicates" and "suggests" for uncertain findings,
             "shows" and "demonstrates" for strong evidence
    address: third person, no "you" or "we"

agents:
  - data_analyst:
      internal_output: structured JSON (formality N/A)
      user_facing: false
  - narrative_writer:
      inherits: style_config.formality_level + style_config.markers
      task: convert analysis into prose sections
      user_facing: true
  - editor:
      task: verify formality consistency across all narrative sections
      checks:
        - no contractions present
        - sentence length within range (flag outliers)
        - hedging language matches evidence strength
        - no register shifts between sections
      output: edited narrative with formality compliance report
```

## Model-fit note

All models respond to formality instructions, but the range of formality they can produce varies. Large models (GPT-4-class, Claude 3.5+) handle subtle gradations — they can distinguish "board presentation formal" from "technical documentation formal." Mid-range models handle broad strokes (formal vs. informal) but may struggle with fine gradations. For any model, providing 3-5 specific linguistic markers produces more consistent formality than a single-word label.

## Evidence and provenance

Formality as a dimension of linguistic register is established in sociolinguistics (Labov, 1966; Joos, 1961, "The Five Clocks"). In NLP, formality detection and transfer have been studied in style transfer research (Rao & Tetreault, 2018). The impact of formality specification on LLM output quality is documented in instruction-tuning evaluations (Ouyang et al., 2022) and prompt engineering guides from Anthropic and OpenAI (2023-2024).

## Related entries

- → **anchoring** — Formality is often established through tonal anchoring: a sample paragraph sets the register.
- → **explicitness** — Specifying formality markers is an exercise in explicitness; the more explicit, the more consistent the register.
- → **compose** — Composition agents must maintain formality consistency across assembled sections.
- → **contrast** — Contrasting formal and informal versions of the same content is a powerful technique for understanding register effects.
