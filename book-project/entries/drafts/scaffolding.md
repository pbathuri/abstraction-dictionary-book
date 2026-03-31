---
headword: "scaffolding"
slug: "scaffolding"
family: "context_architecture"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["constrain", "retrieval scaffolding", "decomposition", "framing", "specificity", "context budget"]
cross_links: ["constrain", "retrieval scaffolding", "decomposition", "framing", "specificity", "context budget", "rubric", "verification loop", "delegation", "context windowing"]
tags: ["context-architecture", "prompting-fundamental", "structure", "templates", "guidance"]
has_note_box: true
note_box_type: "model_note"
---

# scaffolding

**Elevator definition**
Scaffolding is temporary supporting structure — templates, outlines, partially-filled formats — that guides the model's output without dictating its content.

## What it is

In construction, scaffolding is the temporary framework erected around a building so that workers can reach the parts they need to build. It is not the building. It does not stay. It exists to make the real work possible and then it comes down.

In prompt engineering, scaffolding serves the same function. It is the structure you provide so the model can produce output that would be difficult or impossible to achieve from a blank page. A template with headers and placeholder descriptions. An outline with numbered sections and one-sentence summaries of what each section should contain. A partially-filled JSON object with keys defined and values left for the model to populate. A table with column headers and one example row. These are all scaffolding — structures that the model fills in, builds on, or follows.

The concept is borrowed from educational psychology, where *instructional scaffolding* refers to temporary support structures that help learners accomplish tasks they cannot yet manage independently. Vygotsky's zone of proximal development — the gap between what a learner can do alone and what they can do with support — is exactly the gap that prompt scaffolding addresses. A language model can produce structured output alone, sometimes. With scaffolding, it produces structured output reliably.

The critical distinction is between scaffolding and constraint. A → constraint draws a boundary: *do not exceed 300 words*, *do not include recommendations*, *output must be valid JSON*. A constraint says what the model must not do or what the output must not violate. Scaffolding, by contrast, says what the output should look like — positively, structurally, by example. "Use this format" is scaffolding. "Do not use any other format" is a constraint. They often appear together, but they do different work. Scaffolding supports. Constraints restrict.

Scaffolding also differs from → framing. Framing sets the interpretive lens — "you are a financial analyst," "this document is a legal brief," "approach this as a debugging exercise." Framing shapes *how the model thinks*. Scaffolding shapes *what the model produces*. A framed prompt without scaffolding produces output in the right voice but in an unpredictable structure. A scaffolded prompt without framing produces output in the right structure but in a default voice. The best prompts use both.

In practice, scaffolding comes in four forms. **Template scaffolding** provides a fill-in-the-blank structure: headers, labels, placeholders that the model replaces with content. **Outline scaffolding** provides a hierarchical structure — sections, sub-sections, bullet points — that the model populates. **Example scaffolding** (few-shot prompting) provides one or more completed examples that the model pattern-matches against. **Partial-output scaffolding** provides the beginning of the output and asks the model to continue, channeling it into a structure established by the opening.

## Why it matters in prompting

Scaffolding is the primary mechanism for getting structured output from a model that generates one token at a time. Without scaffolding, asking a model to produce a comparison table, a formatted report, or a structured analysis is a request for the model to *invent* the structure and *fill* the structure simultaneously. Some models do this well for familiar formats. None do it reliably for novel or complex structures.

With scaffolding, the structure is given. The model's only job is to fill it. This separation of concerns — structure provided by the prompter, content provided by the model — is the simplest and most reliable way to get complex output. It works because it eliminates an entire category of decision-making (what structure to use) and lets the model spend its computational budget on the actual task (what content to produce).

Few-shot examples are the most studied form of scaffolding. The Prompt Report identifies few-shot prompting as one of the foundational techniques, noting that it provides both pattern and expectation [src_paper_schulhoff2025]. But few-shot examples are expensive — each example consumes context budget. Template and outline scaffolding achieve similar structural guidance at a fraction of the token cost.

## Why it matters in agentic workflows

In multi-agent architectures, scaffolding defines the *interface contracts* between agents. When the Orchestrator tells the Research Agent to produce output, the scaffolding defines the shape of that output — which fields, in what format, with what metadata. The downstream Synthesis Agent is designed to consume that shape. If the Research Agent deviates from the scaffold, the Synthesis Agent fails or produces garbage.

Scaffolding in agentic contexts is not optional guidance — it is protocol. It is the schema definition that makes agent-to-agent communication possible. A Research Agent that returns a free-form narrative cannot reliably feed a Synthesis Agent that expects `{ findings: [], sources: [], confidence: float }`. The scaffold ensures they speak the same language.

This is why scaffolding in agentic workflows tends to be more rigid than in single-turn prompting. A human can adapt to an unexpected output format. An agent pipeline cannot — or rather, it can only adapt if you build a format-normalization agent between every pair, which is expensive and defeats the purpose of scaffolding.

## What it changes in model behavior

Scaffolding reduces structural variance to near zero. A template-scaffolded prompt produces output in the template's structure with high reliability across model tiers. This consistency is the primary value — it makes output parseable, comparable, and pipeline-compatible.

Scaffolding also improves content quality indirectly. By eliminating the need for the model to decide on structure, it frees the model's reasoning capacity for content decisions. This is the same "entropy budget" dynamic that the 5C framework identifies for constraints [src_paper_ari2025]: structure imposed externally is structure the model does not have to invent, leaving more capacity for the actual intellectual work.

## Use it when

- The output requires a specific structure (reports, tables, JSON, forms, comparisons)
- The output must be consumed by downstream systems that expect a particular format
- The model is producing acceptable content in unpredictable structures
- You want to reduce variance across multiple runs of the same prompt
- The task is complex enough that starting from a blank page produces inconsistent results
- You are building agent-to-agent interfaces and need a stable output contract

## Do not use it when

- The task is genuinely open-ended and you want to see what structure the model chooses
- The scaffolding would be so detailed that it leaves no room for the model's contribution (at that point, you have written the output yourself)
- You are testing the model's ability to organize information independently
- The output format does not matter — only the content matters

## Contrast set

**Closest adjacent abstractions**

- → constrain — Constraints draw boundaries (what *not* to do). Scaffolding provides structure (what to build *within*). They are complementary: scaffolding says "use this format," constraints say "do not deviate."
- → framing — Framing shapes how the model thinks. Scaffolding shapes what the model produces. Framing is cognitive; scaffolding is structural.
- → retrieval scaffolding — The specific application of scaffolding to retrieved information: labeling, ordering, and organizing fetched documents.

**Stronger / weaker / narrower / broader relatives**

- → few-shot examples — A specific type of scaffolding that provides completed examples for pattern-matching. Token-expensive but effective.
- → decomposition — Complementary. Decomposition breaks the task into parts; scaffolding provides the structure for each part's output.
- → context budget — Scaffolding costs tokens. The budget determines how much scaffolding you can afford.

## Common failure modes

- **Over-scaffolding** → Providing such detailed templates that the model has no meaningful work to do. The output is the scaffold with trivial fill-ins. Fix: scaffold the structure, not the content. Leave substantive decisions to the model.

- **Scaffold-task mismatch** → Using a scaffolding structure that does not match the task's natural organization. A comparison task scaffolded as a linear report, or an analytical task scaffolded as a bullet list. Fix: choose scaffolding that matches the task's cognitive structure, not just any structure that seems organized.

- **Rigid scaffolding for fluid tasks** → Scaffolding a brainstorming session with a rigid template. The model fills in every field but the output feels mechanical and constrained. Fix: use light scaffolding (an outline or a few guiding questions) rather than rigid templates for creative or exploratory tasks.

- **Orphaned scaffolding** → Including scaffolding that is never used or referenced in the instructions. A template with ten fields when the instructions only discuss three. The model fills all ten, wasting tokens and diluting focus. Fix: align scaffolding to instructions — every scaffold element should correspond to an instruction, and vice versa.

## Prompt examples

### Minimal example

```text
Analyze the product below. Use this format:

**Strengths**
- [bullet points]

**Weaknesses**
- [bullet points]

**Recommendation**
[One paragraph: buy, hold, or avoid, with reasoning]

Product: [product description]
```

### Strong example

```text
I need a competitive analysis comparing three CRM platforms.
Use the following template. Fill in every cell. If data is
unavailable, write "Data not found" rather than guessing.

| Feature          | Platform A   | Platform B   | Platform C   |
|------------------|-------------|-------------|-------------|
| Price (per seat) |             |             |             |
| Free tier        |             |             |             |
| API access       |             |             |             |
| Mobile app       |             |             |             |
| Integrations     |             |             |             |
| User limit       |             |             |             |

After the table, write a 150-word recommendation identifying
which platform suits:
1. A 5-person startup
2. A 50-person mid-market company
3. A 500-person enterprise

Base recommendations ONLY on the data in the table above.
```

### Agentic workflow example

```text
Pipeline: Research → Synthesize → Review

--- RESEARCH AGENT OUTPUT SCAFFOLD ---

The Research Agent MUST return output in this exact JSON structure.
The Synthesis Agent is programmed to consume this schema.
Deviations will cause pipeline failure.

{
  "task_id": "<from orchestrator>",
  "timestamp": "<ISO 8601>",
  "findings": [
    {
      "finding_id": "F001",
      "claim": "<one-sentence factual claim>",
      "source_id": "<matches a source_card.id>",
      "passage": "<exact quote from source>",
      "confidence": "<HIGH | MEDIUM | LOW>",
      "tags": ["<category tags>"]
    }
  ],
  "source_cards": [
    {
      "id": "S001",
      "title": "<source title>",
      "date": "<publication date>",
      "trust_tier": "<T1 | T2 | T3>",
      "url": "<if applicable>"
    }
  ],
  "gaps": [
    "<questions the research could not answer>"
  ],
  "meta": {
    "search_queries_used": 0,
    "sources_consulted": 0,
    "sources_discarded": 0,
    "total_tokens_consumed": 0
  }
}

Rules:
- Every finding MUST reference a source_card by id.
- Every source_card MUST be referenced by at least one finding.
- Orphaned source_cards or unanchored findings will fail
  the Verification Agent's schema check.
```

## Model-fit note

Scaffolding compliance is high across all model tiers for simple templates (tables, bullet lists, basic JSON). Complex scaffolding (nested JSON with conditional fields, multi-level outlines with cross-references) is reliably followed by frontier models, approximately followed by midsize models (which may drop optional fields or flatten nested structures), and unreliably followed by small models. For small models, keep scaffolding flat and simple — one level of nesting maximum, few optional fields, explicit examples of the completed scaffold.

## Evidence and provenance

The identification of few-shot prompting as a foundational scaffolding technique draws from The Prompt Report's systematic review [src_paper_schulhoff2025]. The entropy-budget concept — that externally imposed structure frees model capacity for content — is from Ari (2025) [src_paper_ari2025]. The taxonomy of scaffolding forms (template, outline, example, partial-output) and the distinction between scaffolding, constraint, and framing are original to this entry.

## Related entries

- **→ constrain** — constraints restrict; scaffolding supports. Complementary techniques.
- **→ framing** — framing shapes thinking; scaffolding shapes output structure
- **→ retrieval scaffolding** — scaffolding applied specifically to retrieved documents
- **→ context budget** — scaffolding consumes tokens; budget governs how much
- **→ decomposition** — scaffolding defines output shape for each decomposed sub-task
- **→ few-shot examples** — one form of scaffolding; token-expensive but effective

---

> **Model Note**
>
> The strongest scaffold is a partially completed example. If you show the model two rows of a filled table and ask it to complete the remaining eight, it will match the format, style, and level of detail of your examples with high fidelity. If you show it an empty table with headers only, it will match the structure but make its own decisions about detail level. If you describe the table in prose without showing it, you get the widest variance. The more concrete the scaffold, the tighter the output — at the cost of more tokens spent on the scaffold itself. Choose your scaffold specificity based on how much structural variance you can tolerate.
