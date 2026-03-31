---
headword: "compose"
slug: "compose"
family: "instructional_action"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# Compose

**Elevator definition** Constructing a new artifact by combining elements according to a design intent — assembly with architecture, not mere concatenation.

## What it is

Composition is the act of building something new from parts that already exist. It sits between generation (creating from nothing) and integration (merging separate wholes). Where generation is open-ended and integration demands seamless fusion, composition is architectural: you have materials, you have a blueprint, and you build.

In prompt engineering, "compose" signals that the model should construct an artifact — an email, a report section, a function, a strategy document — from specified ingredients according to specified rules. The ingredients might be bullet points from an analysis step, data from a retrieval step, constraints from a style guide, or user requirements from an intake form. The rules specify structure, tone, length, emphasis, and what to include or omit.

Composition differs from generation in an important way: composition implies raw materials. You're not asking the model to create from the void. You're asking it to assemble, arrange, and shape existing components into a new form. This distinction matters because it anchors the model's output to concrete inputs rather than letting it improvise freely.

The concept of composition borrows directly from functional programming, where composability is a design virtue — small, well-defined functions that combine predictably into larger behaviors. In prompt work, composability means that the output of one step can serve as a clean input to a composition step without reformatting, re-explaining, or re-contextualizing.

There are different modes of composition. **Sequential composition** builds an artifact linearly — introduction, then body, then conclusion. **Parallel composition** builds multiple sections independently and assembles them. **Hierarchical composition** builds sub-components first, then composes them into a parent structure. The mode you choose shapes both the prompt structure and the quality of the output.

The failure mode of composition is incoherence — parts that were assembled but not unified. A composed document where the introduction promises one thing and the body delivers another. A composed email where the tone shifts between paragraphs because each was generated independently. Good composition requires not just assembly but attention to transitions, consistency, and the emergent properties of the whole.

## Why it matters in prompting

"Compose" is the right verb when you have materials and need them shaped into an artifact. It tells the model: you are not starting from scratch, and you are not just formatting. You are building something with structure.

This matters practically because composition prompts naturally include their inputs — the materials to compose from. This grounds the model. A prompt that says "Compose a project update email from these five bullet points" gives the model concrete content to work with, which reduces hallucination and increases relevance compared to "Write a project update email about the project."

The best composition prompts specify both the materials and the architecture: what goes where, what gets emphasized, what gets subordinated, and how the parts connect. This combination of content and structure produces outputs that are simultaneously grounded and well-organized.

## Why it matters in agentic workflows

Agents compose constantly. The final output of most agent pipelines is a composed artifact — a report assembled from research, a recommendation built from analysis, a response constructed from retrieval results. The composition step is where all the upstream work becomes visible to the end user.

Composition agents benefit from receiving their inputs as structured objects rather than prose. When an analysis agent outputs a typed schema (themes, evidence, confidence scores) rather than narrative paragraphs, the composition agent can arrange those elements deliberately rather than extracting them from free text. The quality of composition is bounded by the structure of its inputs.

In multi-agent systems, composition is also the integration point where consistency must be enforced. If three agents researched three different topics, the composition agent must unify voice, resolve conflicting findings, and ensure the final artifact reads as one coherent document rather than three stapled-together fragments.

## What it changes in model behavior

The verb "compose" biases models toward architectural output — text with deliberate structure, transitions between sections, and attention to the relationship between parts. Compared to "write" (neutral) or "generate" (open-ended), "compose" signals that structure and integration matter, not just content.

## Use it when

- You have defined inputs (bullet points, data, prior step outputs) that need to become a unified artifact
- The output requires deliberate structure — not just flowing text but organized sections with clear relationships
- You need the model to assemble, not invent — grounding output in provided materials
- You're building the final output step of a pipeline where earlier steps produced the ingredients
- Consistency across sections matters (tone, terminology, level of detail)

## Do not use it when

- You have no materials to compose from — use `generate` instead
- You need to merge two complete, standalone documents — use `integrate` instead
- You're asking for creative free-form content where structure would constrain quality
- The output is a single, atomic unit (a one-sentence answer, a classification label)

## Contrast set

- **Generate** → Generation creates from specifications alone; composition creates from materials. Generation is open-field. Composition has building blocks.
- **Integrate** → Integration merges separate wholes into one; composition assembles parts into a new whole. Integration starts with complete things. Composition starts with components.
- **Synthesize** → Synthesis combines ideas into a new understanding; composition combines elements into a new artifact. Synthesis is conceptual. Composition is constructive.
- **Concatenate** → Concatenation joins items sequentially; composition joins them architecturally. Concatenation is mechanical. Composition is intentional.

## Common failure modes

- **Frankenstein composition → parts assembled without integration.** Each paragraph is fine alone, but transitions are abrupt, terminology shifts, and the document reads like three authors who never spoke. Fix: include explicit instructions about transitions, voice consistency, and unified terminology in the composition prompt.
- **Material override → the model ignores provided materials and generates from training data.** You gave it five bullet points, but the composed output contains information from none of them. Fix: reference materials by name or number in the prompt ("Bullet 1 becomes the opening paragraph; Bullet 3 becomes the key recommendation") and add a verification instruction: "Confirm that every provided bullet point is represented."
- **Structural collapse → the model produces a wall of text despite structural instructions.** You asked for sections with headers, but got one long paragraph. Fix: provide the structure as a template with placeholders, not just a description of the structure.

## Prompt examples

### Minimal example

```
Compose a one-paragraph product description from these features:
- Waterproof to 50 meters
- Solar-powered, no battery replacement needed
- Titanium case, 42mm diameter
- Heart rate and blood oxygen monitoring
Tone: premium but accessible. Length: 60-80 words.
```

### Strong example

```
Compose an executive summary from the following analysis outputs.

Materials:
- Market findings: {market_analysis_output}
- Technical assessment: {technical_review_output}
- Financial projection: {financial_model_output}

Architecture:
1. Opening hook: the single most important finding across all three inputs (1-2 sentences)
2. Market context: key market findings that frame the opportunity (2-3 sentences)
3. Technical viability: whether the proposed solution is buildable and at what cost (2-3 sentences)
4. Financial case: projected ROI and payback period (2-3 sentences)
5. Recommendation: go/no-go with primary justification and top risk (2-3 sentences)

Constraints:
- Total length: 200-300 words
- No jargon — audience is the board of directors
- Every claim must trace to one of the three input materials
- If materials conflict, note the conflict rather than resolving it silently
```

### Agentic workflow example

```
agent: report_composer
inputs:
  research_output: structured JSON with themes, evidence, sources
  analysis_output: structured JSON with findings, confidence, recommendations
  style_guide: { tone: "authoritative", audience: "senior leadership",
                  max_length: 2000, citation_style: "inline" }

composition_plan:
  1. Generate section outline from analysis_output.recommendations
  2. For each section:
     - Pull relevant evidence from research_output.themes
     - Apply finding and confidence from analysis_output
     - Compose prose following style_guide constraints
  3. Compose introduction: summarize the 3 most important findings
  4. Compose conclusion: state recommendation with confidence band
  5. Unity pass: review full draft for tone consistency,
     terminology alignment, and transition quality
  6. Emit composed report + composition_metadata:
     { sections_composed, sources_used, materials_unused, confidence_range }

checkpoint: verify all research_output.sources appear in citations
```

## Model-fit note

Composition quality scales with model capability more than most tasks. GPT-4-class and Claude 3.5+ models handle complex multi-material composition with structural awareness. Mid-range models (GPT-3.5-class) compose adequately with simple structures but lose coherence in multi-section documents. For smaller models, decompose composition into section-by-section generation with a final stitching step.

## Evidence and provenance

Composition as a design principle has roots in both software engineering (composability in functional programming, Dijkstra, 1972) and rhetoric (classical arrangement theory, Aristotle's *Rhetoric*). In prompt engineering, composition patterns are documented in template-based generation research (Bach et al., 2022) and agent orchestration literature (LangChain cookbook, CrewAI documentation, 2024).

## Related entries

- → **abstraction** — Composition is how abstractions combine; each composed artifact is built from abstracted components.
- → **integrate** — The tighter cousin: integration demands seamless fusion where composition allows visible seams.
- → **generate** — The open-ended counterpart: generation creates from specification; composition creates from materials.
- → **checkpoint** — Composition outputs are prime candidates for checkpoint verification before delivery.
