---
headword: "narrative glue"
slug: "narrative_glue"
family: "tone_style"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["register", "terseness", "audience specification", "warmth", "framing"]
cross_links: ["register", "terseness", "audience specification", "warmth", "framing", "authority", "specificity", "constrain", "decomposition"]
tags: ["tone-style", "transitions", "coherence", "document-structure", "readability"]
has_note_box: true
note_box_type: "which_word"
---

# narrative glue

**Elevator definition**
Narrative glue is the transitional prose between content blocks — the sentences and phrases that connect ideas, create reading flow, and turn a sequence of points into a coherent document a human can follow without effort.

## What it is

Open a well-written technical book to any chapter break. Between the section on, say, hash tables and the section on binary search trees, there will be a sentence or two. Something like: "Hash tables give us constant-time lookup, but they sacrifice ordering. When we need both fast access *and* sorted traversal, we need a different structure." Those two sentences do not contain new information. They do not teach anything about hash tables or binary search trees that the surrounding sections don't cover in detail. But without them, the reader experiences a hard cut: one topic ends, another begins, and the connection between them is left as an exercise. Narrative glue is what prevents that cut.

The term itself is a metaphor, and an accurate one. Glue does not replace the materials it joins — it is not the wood, not the stone, not the glass. It is the thin layer between them that makes the assembly hold together. In writing, narrative glue is the transitional sentences, the bridging paragraphs, the introductory clauses, and the retrospective callbacks that stitch discrete content blocks into something that reads as a single, continuous argument rather than a list of independent observations.

Language models are, by default, surprisingly bad at this. They are excellent at generating discrete content blocks: a clear explanation of concept A, a thorough treatment of concept B. But the transitions between those blocks tend toward one of two failure modes. The first is the *mechanical transition*: "Now that we have discussed A, let us move on to B." This is the literary equivalent of a GPS recalculating — it announces the move without motivating it. The reader knows the topic is changing. What they need to know is *why* it is changing and how B relates to A. The second failure mode is *no transition at all*: the model finishes discussing A, emits a heading, and starts discussing B as if the reader has no memory of the previous section. For short outputs, this is fine. For anything longer than a page, it produces text that reads like a collection of encyclopedia entries rather than a coherent document.

The difference matters because human reading is sequential and cumulative. Readers carry forward what they have just read, and they expect the writer to build on it. When a document lacks narrative glue, the reader must construct the connections themselves — which costs cognitive effort and often leads to misinterpretation. When the glue is present, the document carries the reader through its logic, and the effort shifts from the reader (who must figure out the connections) to the writer (who has already made them explicit).

Narrative glue is not always desirable. In some output formats — structured data, API responses, bullet lists, pipeline outputs between agents — glue is waste. It adds tokens without adding information. The decision to include or exclude narrative glue is a function of the output's purpose and → audience specification. If the reader is a human working through a long document, glue is essential. If the reader is another agent parsing structured input, glue is noise.

## Why it matters in prompting

Most prompting guidance focuses on what the model should produce. Narrative glue is about what goes *between* the things the model produces. And without explicit instruction, the model typically defaults to either too much (a paragraph of throat-clearing before each new section) or too little (bare juxtaposition of content blocks).

For document-length outputs — reports, guides, explanations, analyses — narrative glue is the difference between a professional document and a first draft that needs a human editor. The content might be complete. The structure might be sound. But if the sections don't flow into each other, the document reads as assembled rather than written. Readers sense this, even if they cannot articulate what is wrong.

The most effective approach is to instruct the model about transitions explicitly. Not "add transitions between sections" (which produces the mechanical "Now let us discuss..." pattern) but something more specific: "At the end of each section, write one sentence that connects the current topic to the next. The connection should be logical, not chronological — explain *why* the next topic follows, not just *that* it follows." This gives the model a reason for the transition, which produces prose that reads as motivated rather than procedural.

The Prompt Report's taxonomy of prompt components identifies structural and stylistic output specifications as separate concerns [src_paper_schulhoff2025]. Narrative glue sits at the intersection — it is structural in that it affects document architecture, but stylistic in that it must match the document's → register to sound natural.

## Why it matters in agentic workflows

Multi-agent pipelines have a narrative glue problem by design. When different agents produce different sections of a document — a research agent writes the findings, an analysis agent writes the interpretation, a recommendation agent writes the action items — there is no agent responsible for the spaces *between* those sections. Each agent optimizes its own output. No one optimizes the seams.

This produces a specific artifact: the patchwork document. Each section is individually coherent. The whole reads like a committee report where each member wrote their section in isolation and someone stapled the pages together. Readers notice the tonal shifts, the redundant context-setting (each section re-introduces material the previous section covered), and the absence of forward references and callbacks.

The architectural solution is a **final-pass stitching agent** whose sole job is narrative glue. It receives the assembled sections and adds: (1) transitions between sections, (2) forward references ("as we will see in the risk assessment below"), (3) backward callbacks ("the latency issues identified in the previous section compound here"), and (4) a cohesive opening and closing that frame the whole document. This agent does not change content. It changes continuity. Its system prompt should specify the document's → register and → audience specification so the glue matches the material it joins.

## What it changes in model behavior

Instructing for narrative glue increases the model's production of transitional sentences, backward references to previously stated material, forward references to upcoming content, and introductory framing at section boundaries. The model produces fewer hard breaks between topics and more connective clauses. Paragraph endings shift from conclusive ("This completes the analysis of X.") to bridging ("This pattern becomes especially relevant when we examine Y.").

## Use it when

- The output is a long document (more than 500 words) intended for human readers who will read sequentially
- Multiple content blocks need to be connected into a single coherent argument or narrative
- The document is a report, guide, tutorial, or analysis where reading flow matters for comprehension
- Multiple agents produce sections of the same document and the seams need smoothing
- The reader is a non-expert who needs guidance on how topics connect to each other
- The output will be presented as a polished document rather than a working draft

## Do not use it when

- The output is structured data, JSON, or machine-consumed format where transitions are noise
- The output is a list, a table, or a set of independent items where each stands alone
- The audience values → terseness and would perceive transitions as padding
- The output feeds another agent in a pipeline and information density is more important than readability

## Contrast set

**Closest adjacent abstractions**

- → terseness — Direct opposition. Terseness strips every word that does not carry information. Narrative glue adds words whose purpose is continuity, not information. The tension is real and must be resolved by → audience specification: who is reading, and do they need flow or density?
- → register — Narrative glue must match the register of the surrounding content. Academic glue ("Having established the theoretical framework, we now turn to the empirical evidence") sounds wrong in a casual technical blog. Casual glue ("OK, so that's the theory — but does it actually work?") sounds wrong in a whitepaper.
- → decomposition — Decomposition breaks a task into parts. Narrative glue reassembles parts into a whole. They are sequential operations: decompose to generate, then glue to compose.

**Stronger / weaker / narrower / broader relatives**

- → framing — Broader. Framing orients interpretation; narrative glue orients reading sequence.
- → audience specification — Broader. The audience determines whether narrative glue is needed at all and what register it should take.
- → warmth — Complementary. Narrative glue can carry warmth ("Now comes the part that trips up most people — but once you get it, the rest falls into place") or be affectively neutral ("The next section addresses performance implications").

## Common failure modes

- **The robotic transition** → "Now that we have discussed X, let us move on to Y." This is the most common form of model-generated narrative glue and it is functionally useless. It announces a topic change the reader can see from the heading. It does not explain *why* Y follows X, what the connection is, or what the reader should carry forward. Fix: instruct the model to make transitions *logical*, not *procedural*. "Connect sections by explaining why the next topic follows from the previous one, not by announcing that it does."

- **Glue that introduces content** → The transitional paragraph starts summarizing the next section, spoiling the structure and creating redundancy. The reader gets a preview paragraph and then the section itself, which repeats the same points in more detail. Fix: instruct the model that transitions should create *expectation*, not *preview*. "End each section with a question or tension that the next section resolves. Do not summarize the next section in the transition."

- **Inconsistent glue density** → The model adds elaborate transitions between some sections and none between others, creating an uneven reading experience. Sections 1-2 flow beautifully. Sections 3-4 collide with a hard cut. This is especially common in long outputs where the model's attention to the transition instruction decays. Fix: reinforce the instruction at regular intervals, or use a post-generation editing pass (human or agent) specifically for transition quality.

## Prompt examples

### Minimal example

```text
Write a 1,000-word explanation of how neural networks learn,
covering: forward pass, loss calculation, backpropagation,
and gradient descent.

Between each topic, write one or two sentences that connect
the current concept to the next. The reader should understand
why each step follows from the previous one — not just that
the topics are listed in order.
```

### Strong example

```text
I have four completed sections of a technical report. Each
section was written independently. I need you to add the
connective tissue that makes them read as a single document.

Your job is NOT to rewrite the sections. Your job is to add:

1. An opening paragraph (3-4 sentences) that frames the
   entire report and sets reader expectations.

2. A transition paragraph between each pair of sections
   (3 each, so 3 transition paragraphs total). Each
   transition should:
   - Briefly connect the conclusion of the previous section
     to the opening of the next
   - Explain WHY the next topic follows logically
   - Not summarize either section — create a bridge, not a
     recap

3. A closing paragraph (3-4 sentences) that ties the report's
   findings together without simply restating the section
   headings.

Register: Match the register of the existing sections.
They are written in a direct, technical style for a senior
engineering audience. Your transitions should sound like the
same author wrote them — not like an editor stitched them in.

[Section 1 attached]
[Section 2 attached]
[Section 3 attached]
[Section 4 attached]
```

### Agentic workflow example

```text
Pipeline: Long-Form Report Assembly

Agent 1 — Research Agent
Task: Produce the Findings section (800-1000 words).
Output: Prose. No transitions to other sections — write
this section as a standalone block.

Agent 2 — Analysis Agent
Task: Produce the Implications section (600-800 words).
Input: Research Agent's findings.
Output: Prose. Reference the findings by content, not by
section ("The latency patterns described above" not "As
discussed in Section 1").

Agent 3 — Recommendation Agent
Task: Produce the Recommendations section (400-600 words).
Input: Both previous agents' outputs.
Output: Numbered recommendations with one paragraph of
justification each.

Agent 4 — Stitching Agent
Task: You receive three independently written sections.
Your job is narrative glue ONLY. Do not modify the content
of any section. Add:
- An executive summary opening (100 words) that frames the
  whole report
- A transition between Findings and Implications (2-3
  sentences) explaining why the implications matter given
  the findings
- A transition between Implications and Recommendations
  (2-3 sentences) framing the recommendations as responses
  to the implications
- A closing paragraph (50-75 words) that creates a sense
  of completion

Register: Direct, professional. Match the tone of the source
sections. The final document should read as if one author
wrote it in a single sitting.

Quality check: Read the assembled document start to finish.
If any transition sounds mechanical ("Having reviewed the
findings, we now turn to..."), rewrite it to sound motivated.
```

## Model-fit note

Frontier models produce natural-sounding narrative glue when instructed, with logical transitions that connect content rather than merely announcing topic changes. They maintain transition quality across long documents. Midsize open models follow explicit transition instructions but tend toward the mechanical pattern ("Now let us discuss...") unless the instruction specifically prohibits it. Small models struggle with narrative glue — they either omit it entirely or produce formulaic connectors. For small models, the most reliable approach is structural: instruct the model to end each section with a question that the next section answers, rather than asking for transitional prose.

## Evidence and provenance

The distinction between structural and stylistic output formatting is drawn from The Prompt Report's component taxonomy [src_paper_schulhoff2025]. Narrative glue sits at the intersection of both categories. The concept of coherence through transitional devices is well-established in writing pedagogy (Williams & Bizup, *Style: Lessons in Clarity and Grace*, 12th ed.) and discourse analysis (Halliday & Hasan, *Cohesion in English*, 1976). The specific problem of patchwork documents in multi-agent pipelines is a practitioner observation from production agentic systems.

## Related entries

- **→ terseness** — the opposing force; terseness removes what glue adds
- **→ register** — narrative glue must match the register of the content it connects
- **→ audience specification** — the audience determines whether narrative glue is needed at all
- **→ decomposition** — decomposition breaks tasks apart; narrative glue reassembles outputs into wholes
- **→ warmth** — narrative glue can carry warmth or operate without it

---

> **Which Word?**
>
> *Narrative glue* or *transitions* or *coherence*? Transitions is the narrower and more common term — it covers the sentences between paragraphs and sections. But narrative glue covers more than transitions. It includes opening frames, closing callbacks, forward references, and the general continuity of voice across a long document. Coherence is the outcome that narrative glue produces; it is a property of the reader's experience, not a technique the writer uses. Say "transitions" when you mean the specific sentences between sections. Say "narrative glue" when you mean the full set of techniques that make a multi-section document read as one piece. Say "coherence" when you mean the result, not the cause.
