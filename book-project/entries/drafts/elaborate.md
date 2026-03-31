---
headword: "elaborate"
slug: "elaborate"
family: "instructional_action"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["summarize", "constrain", "specificity", "decomposition", "justify", "framing"]
cross_links: ["summarize", "constrain", "specificity", "decomposition", "justify", "framing", "evaluate", "hallucination bait", "scope", "register"]
tags: ["instructional-action", "expansion", "detail-generation", "compression-spectrum"]
has_note_box: true
note_box_type: "which_word"
---

# elaborate

**Elevator definition**
To elaborate is to expand on a point with additional detail, examples, reasoning, or explanation, adding depth where the current treatment is too thin.

## What it is

Elaboration is the anti-summary. Where → summarize strips away detail to reveal the skeleton, elaborate adds flesh to the bones. The operations sit at opposite ends of the information density spectrum: summarize compresses, elaborate expands. Both are transformations of scale, and both are lossy in their own way — summarize loses detail, elaboration risks losing focus.

The instruction "elaborate" asks the model to take something — a claim, a concept, a step in an argument — and make it *more*. More specific. More concrete. More thoroughly explained. More richly exemplified. The model has several expansion strategies available to it: it can add examples ("for instance..."), add reasoning ("because..."), add nuance ("however, in cases where..."), add context ("historically, this arose because..."), or add implications ("which means that..."). Each strategy produces a different kind of depth. The prompt author who says "elaborate" without specifying which kind gets the model's default mix, which tends to be heavy on generic examples and light on substantive reasoning.

This is the fundamental tension of elaboration: it is easy to produce more words and hard to produce more *substance*. A model asked to elaborate will rarely refuse. It will always generate additional text. The question is whether that text carries new information or merely inflates the word count. Unconstrained elaboration is the native habitat of padding — those comfortable, flowing paragraphs that say nothing new but sound like they do.

The distinction between elaboration and padding is not about length. It is about information gain. Good elaboration increases the reader's understanding of the original point. It adds a concrete example that makes an abstract claim tangible. It surfaces an implication the reader had not considered. It explains a mechanism that the original statement merely asserted. Bad elaboration restates the original point in different words, adds generic examples that could apply to anything, and wraps it all in transitional padding. The model does both. The prompt determines which.

Language models are biased toward elaboration. Their training on human-written text — where longer, more detailed answers are often rated higher — means that "elaborate" is close to the model's default behavior. Ask a question with no length constraint and the model will elaborate whether you want it to or not. This makes the instruction paradoxically both powerful (the model is good at it) and dangerous (the model over-does it). The craft of prompting for elaboration is not in getting the model to elaborate — it will do that eagerly — but in constraining the elaboration so it produces depth, not bloat.

## Why it matters in prompting

Elaboration is the instruction you reach for when you have a skeleton and need it fleshed out. You have a bullet-point outline, an executive summary, a set of key findings — and now you need the full version. The instruction is also useful when a model's initial response is too sparse: "elaborate on point three" is the natural follow-up when one section of a response is underdeveloped compared to the others.

The key to effective elaboration prompts is specifying *what kind of depth you want*. "Elaborate on the security implications" is better than "elaborate." "Elaborate on the security implications by providing a concrete attack scenario, the likelihood of exploitation, and the cost of mitigation" is better still. Each specification constrains the elaboration along a productive axis, preventing the model from padding with generic filler.

Elaboration prompts interact powerfully with → constrain. Unconstrained elaboration balloons. Constrained elaboration deepens. "Elaborate on this point in 100 words" forces the model to choose its expansion strategy — it cannot add examples *and* reasoning *and* context *and* implications in 100 words, so it picks the highest-value expansion. This forced selection often produces better depth than unlimited elaboration, because the model must prioritize instead of exhausting every strategy.

## Why it matters in agentic workflows

In multi-agent pipelines, elaboration is the operation that transforms compressed intermediate representations back into full, usable outputs. A Research Agent passes key findings as bullet points to preserve context budget. A Writing Agent elaborates those bullets into full paragraphs for the final deliverable. An Explanation Agent takes a technical conclusion from an Analysis Agent and elaborates it into language a non-technical stakeholder can follow.

The Elaboration Agent needs two things in its system prompt: the compressed input to elaborate, and the target audience and format for the elaborated output. Without audience specification, the agent does not know how much to assume — an elaborate explanation of a technical concept for a fellow engineer is very different from an elaborate explanation for an executive.

Elaboration agents also serve as a form of quality enrichment. When an upstream agent produces a correct but sparse output, the elaboration step adds the detail that makes the output useful. A code review agent that returns "security vulnerability in line 47" is correct but unhelpful. An elaboration agent that takes that flag and produces "Line 47 passes user input directly to a SQL query without parameterization, which allows SQL injection attacks. An attacker could craft a username containing `'; DROP TABLE users; --` to delete the users table" is the same finding, made actionable.

## What it changes in model behavior

The instruction "elaborate" shifts the model into expansion mode: it generates more tokens per concept, selects for lower-density output, and activates example-generation and reasoning-chain subroutines. The output contains more illustrative examples, more causal explanations, more qualifying clauses, and more transitional language than compressed or default-length outputs.

The risk is mode-lock. Once the model is in elaboration mode, it may over-elaborate — expanding points that need only a sentence into paragraphs, and paragraphs into sections. This is why constrained elaboration outperforms open-ended elaboration in most practical contexts: the constraint provides a stopping signal the model would otherwise lack.

## Use it when

- An initial response is too sparse and you need specific points developed further
- You have a compressed artifact (outline, bullet points, key findings) that needs to become full prose
- The audience needs more explanation, examples, or context than the current level of detail provides
- A technical finding needs to be made actionable through specific detail
- You are building a pipeline where upstream compression must be reversed for final delivery
- A concept is stated but not yet justified, exemplified, or explained

## Do not use it when

- The current level of detail is sufficient and elaboration would add bulk without insight
- You want the model to add *new information* rather than expand on existing points — that is research or generation, not elaboration
- You have not constrained the elaboration and risk getting padding instead of depth
- The point being elaborated is wrong or weak — elaboration makes bad points longer, not better (→ critique first, elaborate after)
- Token budget is tight and the elaboration is not worth the context cost

## Contrast set

**Closest adjacent abstractions**

- → summarize — The directional opposite. Summarize compresses. Elaborate expands. They are inverse operations on the information density spectrum. Applying both in sequence is a lossy round-trip: elaborate(summarize(x)) ≠ x.
- → justify — Justify provides *reasons* for a claim. Elaborate provides *depth* on a topic. Justification is a specific type of elaboration — one that expands through argumentation. Not all elaboration is justification: you can elaborate by adding examples, context, or nuance without arguing for anything.
- → explain — Near-synonym in casual usage, but with a different emphasis. "Explain" implies the reader does not understand. "Elaborate" implies the reader has the gist and wants more detail. Explain is pedagogical. Elaborate is expansive.

**Stronger / weaker / narrower / broader relatives**

- → decomposition — Complementary. Decomposition breaks a topic into parts; elaboration expands each part.
- → constrain — The essential companion to elaboration. Unconstrained elaboration bloats. Constrained elaboration deepens.
- → specificity — Elaboration that adds concrete specifics is more valuable than elaboration that adds generic filler.

## Common failure modes

- **Padding masquerading as depth** → The model produces more words but no more information. The original point is restated in three different ways, wrapped in transitions, and decorated with obvious examples. The word count rises. The insight does not. Fix: require *specific* types of depth — "elaborate with a concrete example from the healthcare industry" or "elaborate by explaining the underlying mechanism."

- **Elaboration of the wrong point** → The model elaborates enthusiastically on the point it finds most interesting, which may not be the point you need expanded. Fix: specify which point to elaborate. "Elaborate on your third point" is precise. "Elaborate" is an invitation for the model to choose.

- **Hallucination under expansion pressure** → When asked to elaborate on a topic where its knowledge is thin, the model fabricates plausible-sounding detail rather than admitting it has nothing to add. This is → hallucination bait triggered by an expansion instruction. Fix: add the safety valve — "if you do not have specific information to add, say so rather than generating speculative detail."

- **Infinite elaboration spiral** → In an agentic context, an elaboration agent with no length constraint generates increasingly verbose output with each revision cycle. Fix: always pair elaboration instructions with a target length or a "stop when" criterion.

## Prompt examples

### Minimal example

```text
You wrote: "The migration will require downtime."

Elaborate on this in 3-4 sentences. Specifically:
- How much downtime (estimate a range)?
- What causes the downtime?
- What is at risk if the migration is interrupted?
```

### Strong example

```text
Below is a bulleted outline of our Q3 strategy. Elaborate each
bullet into a full paragraph (80-120 words each).

For each bullet:
- Add one concrete example or data point that supports the claim
- Explain the mechanism — not just what will happen, but why
- Note one risk or assumption that the bullet glosses over
- Write for the audience: department heads who understand the
  business but have not seen the underlying analysis

Do NOT pad with generic transitions ("Moving on to the next
point...") or restate the bullet before elaborating it.
Start each paragraph with the substantive content.

Outline:
1. ...
2. ...
3. ...
```

### Agentic workflow example

```text
Agent: Elaboration Agent
Pipeline position: After Analysis Agent, before Report Agent

Input: analysis_results.json — array of findings, each
containing { finding_id, headline (10-15 words),
technical_detail (50-80 words), confidence, source_ids }

Task: Elaborate each finding from headline + technical_detail
into a full finding section (150-250 words) suitable for a
non-technical executive audience.

Elaboration protocol for each finding:
1. Open with the headline claim in plain language
2. Explain the mechanism: what is happening and why
3. Provide one concrete example or scenario that illustrates
   the impact in business terms
4. State the confidence level in plain language (e.g.,
   "high confidence based on three independent data sources")
5. Close with a one-sentence implication: what this means
   for the organization

Constraints:
- Do not invent information not present in the technical_detail.
   If the detail is insufficient for a full section, elaborate
   what is available and flag as NEEDS_ENRICHMENT.
- Do not use jargon from the technical_detail without defining it.
- Preserve all source_ids as inline citations [source_id].

Output: Same JSON schema with content field replaced by
elaborated text and a new field: word_count.

Handoff: Pass to Report Agent for assembly and formatting.
```

## Model-fit note

Elaboration is the instruction where model tiers matter least — all models elaborate willingly — and where prompt design matters most. Frontier models produce substantive, well-structured elaborations that add genuine insight when given specific expansion criteria. Midsize open models produce competent but occasionally generic elaborations, defaulting to safe examples and obvious implications. Small open models are prolific elaborators but poor discriminators: they pad reliably and deepen rarely. For all tiers, the single most impactful prompt modification is specifying *what kind of depth* you want (examples, mechanisms, implications, risks) rather than leaving "elaborate" open-ended. Length constraints improve output quality at every tier.

## Evidence and provenance

The compression-expansion spectrum (summarize-elaborate axis) is a conceptual framework for understanding instructional verbs, drawing on information density analysis in NLP research. The Prompt Report documents the relationship between instruction specificity and output quality for all instructional verbs, including elaboration tasks [src_paper_schulhoff2025]. The observation that constrained elaboration outperforms unconstrained elaboration is supported by the 5C framework's finding that explicit constraints improve output quality while reducing token waste [src_paper_ari2025]. The risk of hallucination under expansion pressure is documented in the hallucination literature reviewed by Sahoo et al. (2025) [src_paper_sahoo2025].

## Related entries

- **→ summarize** — the inverse operation: compression where elaboration expands
- **→ constrain** — the essential companion that prevents elaboration from becoming padding
- **→ justify** — a specific type of elaboration through argumentation
- **→ specificity** — elaboration that adds concrete specifics produces depth; generic elaboration produces bloat
- **→ decomposition** — breaks topics into parts that elaboration then expands individually
- **→ hallucination bait** — elaboration on thin-knowledge topics triggers fabrication

---

> **Which Word?**
>
> *Elaborate* or *explain*? In prompting, the distinction is about the reader's starting point. "Explain" implies the reader does not yet understand the concept — it is pedagogical, aimed at building comprehension from scratch. "Elaborate" implies the reader has the basic idea and wants more depth — more examples, more nuance, more mechanism. Use "explain" when introducing a concept for the first time. Use "elaborate" when developing a concept the reader already grasps. If you use "elaborate" when you should use "explain," the model will add depth to something the reader never understood at the surface level.
