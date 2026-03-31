---
headword: "constrain"
slug: "constrain"
family: "instructional_action"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["specificity", "filter", "scope", "framing", "overspecification", "decomposition", "rubric"]
cross_links: ["specificity", "filter", "scope", "framing", "overspecification", "decomposition", "rubric", "context budget", "hallucination bait", "format collapse"]
tags: ["instructional-action", "prompting-fundamental", "control", "boundaries"]
has_note_box: true
note_box_type: "upgrade_prompt"
---

# constrain

**Elevator definition**
To constrain is to draw a boundary around what the model may do, say, produce, or consider, narrowing the output space to what you actually need.

## What it is

Every prompt is an open door. Without constraint, the model walks through it in whatever direction its training weights find most probable. Constraining is the act of posting signs on that door: *not that way*, *only this far*, *nothing larger than this*, *in this format and no other*.

Constraint is the verb form of → specificity. Where specificity is a property of a prompt (it is more or less specific), constraining is something you *do* to a prompt — you add a rule that eliminates some region of the output space. "Write a summary" is unconstrained. "Write a summary in three sentences, using only information from the attached document, and do not include any recommendations" is constrained along three axes: length, source, and content type.

The 5C Prompt Contract framework identifies Constraint as one of five core components of effective prompt design — alongside Character, Cause, Contingency, and Calibration [src_paper_ari2025]. In controlled experiments across four major LLM providers, prompts structured with explicit constraints achieved 84% lower input token cost while maintaining comparable output quality against both DSL-structured and unstructured alternatives. The economy is revealing: constraints do not add bloat. They add *precision*, and precision is cheap in tokens and expensive to do without.

Constraints come in several species. **Format constraints** dictate structure: "Return JSON," "Use a table with these columns," "Maximum 200 words." **Content constraints** dictate substance: "Only cite the attached sources," "Do not discuss pricing," "Focus on environmental impact." **Behavioral constraints** dictate conduct: "If you are unsure, say so," "Do not make assumptions about the user's expertise level," "Ask clarifying questions before proceeding." **Scope constraints** dictate reach: "Only address sections 3 through 7," "Limit your analysis to Q3 data," "Do not consider competitors outside North America."

Each species does different work. Format constraints reduce post-processing. Content constraints reduce irrelevance. Behavioral constraints reduce risk. Scope constraints reduce drift. A well-constrained prompt usually deploys at least two species simultaneously.

## Why it matters in prompting

A prompt without constraints is a prompt that trusts the model to make every decision itself. Sometimes that trust is warranted — in creative brainstorming, for instance, you might want the model to roam. But for any task with definable success criteria, unconstrained prompts produce what could charitably be called creative variance and what honestly looks like inconsistency.

The Prompt Report's taxonomy of 58 prompting techniques reveals that nearly every effective technique embeds constraints in some form: chain-of-thought constrains the reasoning path, output formatting constrains the structure, role prompting constrains the voice, and few-shot examples constrain the pattern [src_paper_schulhoff2025]. Constraining is not one technique among many. It is the mechanism underneath most of them.

Practically, constraints are how you turn a wish into a specification. "Help me write a marketing email" is a wish. "Write a 150-word marketing email for enterprise SaaS buyers, emphasizing time-to-value over features, ending with a single call-to-action, and using no exclamation marks" is a specification. The model can satisfy a specification. It can only guess at a wish.

## Why it matters in agentic workflows

In agent architectures, constraints serve a different and more structural function: they define the *authority boundary* of each agent. An agent without constraints is an agent with implicit permission to do anything its tools allow. A research agent with access to a web scraper, a database writer, and an email sender — constrained only by the instruction "research our competitors" — may scrape, store, and email results without anyone intending that chain of side effects.

Constraint in delegation is how you prevent → authority leak. "You may read the product database. You may not write to it. You may call the search API up to 10 times. You may not access any endpoint outside the /products scope." These are not suggestions. They are the agent's operating permissions, written in natural language.

The 5C framework's Contingency component — what to do when things go wrong — is itself a constraint: it bounds the agent's behavior under failure conditions rather than leaving it to improvise [src_paper_ari2025]. "If you cannot find pricing data, return a null value and a note explaining the gap" is a constraint that prevents the agent from fabricating a number to fill the space.

## What it changes in model behavior

Constraints reduce output variance and increase structural compliance. When you constrain length, the model produces output within that length. When you constrain format, the model produces output in that format. These effects are reliable across model tiers, though smaller models are more likely to violate constraints under pressure — particularly when multiple constraints compete for limited context.

More subtly, constraints redirect computational attention. Ari (2025) describes this as preserving the model's "entropy budget" — the model's capacity for creative or deep semantic processing [src_paper_ari2025]. A prompt bloated with DSL tags spends tokens on structural compliance. A prompt with clean, explicit constraints delivers the same control signal in fewer tokens, leaving more room for the model to process the actual task. The measured difference was striking: 54.75 input tokens for constrained 5C prompts versus 348.75 for DSL across four model families.

## Use it when

- The task has definable success criteria and you can articulate at least some of them as boundaries
- Previous unconstrained attempts produced outputs that were technically acceptable but not actually useful
- The output will feed a downstream process (another agent, a parser, a database) that requires a specific format
- You are delegating to an agent and need to limit what it may access, modify, or produce
- The model has a tendency to over-produce: adding scope constraints trims the output to what matters
- You are working with a model prone to → hallucination bait and need to constrain sourcing

## Do not use it when

- The task is genuinely exploratory and you do not yet know what shape the answer should take
- You are brainstorming and want divergent outputs (constraints kill divergence by design)
- The constraints you would add are so obvious that specifying them would waste tokens without adding information
- You have already constrained the prompt so heavily that the model has no room to produce useful output (→ overspecification)
- You are unsure of the correct constraints and risk biasing the output with wrong boundaries

## Contrast set

**Closest adjacent abstractions**

- → specificity — Specificity is the property of being narrow; constraining is the act of making something narrow. You achieve specificity by adding constraints, among other techniques.
- → filter — Filtering removes items from a set after generation; constraining prevents them from being generated in the first place. Constraint is preventive. Filtering is corrective.
- → scope — Scope defines the territory; constraints define the fences around it. Scoping says what is included. Constraining also says what is excluded.

**Stronger / weaker / narrower / broader relatives**

- → rubric — Broader. A rubric is a set of constraints organized into evaluation criteria.
- → format constraint — Narrower. One species of constraint targeting output structure only.
- → decomposition — Complementary. Decomposition breaks a task into parts; constraints govern what each part may do.
- → overspecification — The failure mode of excessive constraint.

## Common failure modes

- **Contradictory constraints** → Telling the model to "be concise" and "provide comprehensive detail" in the same prompt. The model will satisfy one and violate the other, and you cannot predict which. Before adding a constraint, check it against the existing set for conflicts.

- **Constraint without priority** → Listing five constraints with no indication of which matters most. When the model cannot satisfy all of them simultaneously (common in longer outputs), it needs to know which to preserve and which to relax. "If length and completeness conflict, prefer completeness."

- **Phantom constraints** → Constraining something the model was never going to do anyway. "Do not use offensive language in this financial report" wastes tokens on a constraint the model would have satisfied unprompted. Good constraints target realistic failure modes, not theoretical ones.

- **Constraint as substitute for instruction** → Saying only what the model should *not* do without ever saying what it *should* do. A list of prohibitions without a directive produces either a blank stare or a cautious, hedged response that avoids everything including usefulness.

## Prompt examples

### Minimal example

```text
Summarize the attached meeting transcript in 5 bullet points.
Each bullet must be one sentence.
Do not include action items — those will be handled separately.
Focus only on decisions made, not discussion that led to them.
```

### Strong example

```text
You are a regulatory compliance analyst reviewing product descriptions
for an e-commerce platform.

For each product description I provide:
1. Check whether it contains any health claims (e.g., "cures," "treats,"
   "clinically proven") that would require FDA substantiation.
2. Check whether it contains environmental claims (e.g., "eco-friendly,"
   "sustainable," "carbon-neutral") that lack a qualifying statement.
3. For each flagged claim, quote the exact phrase and classify it as:
   HEALTH_CLAIM | ENVIRONMENTAL_CLAIM | BOTH

Constraints:
- Only flag explicit claims, not implied ones.
- If the description is clean, return: {"status": "COMPLIANT", "flags": []}
- Do not rewrite the descriptions. Your job is audit, not editing.
- Do not flag comparative claims ("better than X") — those are handled
  by a different review process.
- If a claim is ambiguous, flag it but mark confidence as LOW.

Output format: JSON, one object per product.
```

### Agentic workflow example

```text
Agent: Data Extraction Agent
Pipeline position: After Document Ingester, before Analysis Agent

Input: OCR-processed PDF pages (plain text, may contain extraction artifacts)

Task: Extract all numerical financial figures from the text.

Constraints:
- Extract ONLY figures that appear in table rows or labeled fields
  (e.g., "Revenue: $4.2M"). Do not extract numbers from narrative prose.
- Return each figure with: label, value, unit, page_number, confidence
- If a figure appears to be corrupted by OCR (e.g., "$4.2N" instead
  of "$4.2M"), flag it as OCR_SUSPECT and pass the raw text.
- Do NOT attempt to correct OCR errors. The Correction Agent handles that.
- Do NOT infer figures not present in the source text.
- Maximum processing: 50 pages per invocation. If input exceeds 50 pages,
  return an error with page_count and request batching from the orchestrator.

Authority boundary:
- Read access: input text buffer only
- Write access: output JSON only
- Tool access: none (this is a text-processing-only agent)

Output: JSON array of extracted figures.
Handoff: Pass to Analysis Agent with extraction_confidence_summary.
```

## Model-fit note

Constraints are respected with increasing reliability as model capability rises. Frontier proprietary models handle complex multi-constraint prompts well, including implicit priority ordering. Midsize open models follow explicit constraints reliably but may drop softer constraints (hedging instructions, tone constraints) in favor of harder ones (format, length). Small open models require constraints to be few, explicit, and non-competing — stacking more than three or four constraints on a model with limited instruction-following capacity invites silent violations. Code-specialized models excel at format constraints and structured output requirements but may over-literalize behavioral constraints.

## Evidence and provenance

The 5C framework's empirical data on constraint efficiency comes from Ari (2025) [src_paper_ari2025], tested across OpenAI, Anthropic, DeepSeek, and Gemini. The taxonomy of prompt components including output formatting and style instructions draws from The Prompt Report's systematic review of 1,565 papers [src_paper_schulhoff2025]. The observation that constraints redirect model attention rather than merely filtering output is supported by the entropy-budget hypothesis in the 5C analysis. The classification of constraint species (format, content, behavioral, scope) is original to this entry.

## Related entries

- **→ specificity** — the property that constraining produces; constraining is one of several ways to achieve specificity
- **→ filter** — corrective where constraint is preventive; filtering removes after generation
- **→ scope** — defines what is in play; constraint defines what is out of bounds
- **→ rubric** — a structured collection of constraints organized as evaluation criteria
- **→ overspecification** — what happens when constraints are too many or too tight
- **→ hallucination bait** — constraint on sourcing is the primary defense against fabrication
- **→ decomposition** — constraints govern what each decomposed sub-task may do

---

> **Upgrade This Prompt**
>
> Before: "Write a blog post about remote work."
>
> After: "Write a 600-word blog post arguing that asynchronous communication improves deep work. Target audience: engineering managers. Tone: direct, evidence-informed, no buzzwords. Do not cover 'work-life balance' — that is a separate post. End with one concrete recommendation the reader can implement Monday."
>
> What changed: five constraints added — length, argument direction, audience, tone, scope exclusion — plus a structural requirement for the closing. The model now has boundaries. It can write *within* them instead of guessing what you wanted.
