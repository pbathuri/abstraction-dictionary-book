---
headword: "reference"
slug: "reference"
family: "core_abstraction"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# reference

**Elevator definition**
A reference is a pointer to external material — a document, dataset, standard, or source — that the model should consult, cite, or treat as authoritative for the task at hand.

## What it is

Language models know things. That is both their strength and their most dangerous quality. What they know is a compressed, lossy encoding of their training data — statistically likely patterns, not verified facts. A reference is how you override that default knowledge with specific, authoritative material that the model should treat as ground truth for the current task.

The distinction between a model's parametric knowledge (what it learned during training) and its contextual knowledge (what you provide in the prompt) is the most consequential distinction in applied prompt engineering. Parametric knowledge is vast, stale, unverifiable, and confidently delivered. Contextual knowledge — references — is specific, current, verifiable, and under your control. When you provide a reference, you are telling the model: use this, not what you think you know.

References take many forms. **Document references** are the most common: a report, article, contract, or dataset included in the context or accessible via tool use. **Standard references** point to norms the model should follow: "Follow the APA 7th edition citation format" or "Apply the OWASP Top 10 security checklist." **Example references** provide model outputs to emulate: "Here is an example of a correctly formatted entry. Follow this pattern." **Constraint references** define boundaries via external material: "The attached style guide defines acceptable and unacceptable language."

The crucial property of a reference is that it is *external to the model's weights*. It exists in the context window, in a retrieval system, or in a tool's output. This externality is what makes references trustworthy in ways the model's own knowledge is not. A reference can be checked, updated, versioned, and replaced. The model's training data cannot.

In retrieval-augmented generation (RAG) architectures, references are the central mechanism. A user asks a question, a retrieval system finds relevant documents, and those documents are injected into the prompt as references. The model is instructed to answer based on the retrieved material rather than its own knowledge. The quality of a RAG system is largely determined by the quality of its references: relevance, recency, accuracy, and completeness.

References differ from generic context in their normative status. Context is information the model can use as it sees fit. A reference is information the model *should prefer over its own knowledge*. This preference must be stated explicitly. Without an instruction like "Answer based only on the attached documents" or "If the reference contradicts your training data, follow the reference," the model will blend its parametric knowledge with the provided reference, producing outputs that feel sourced but are actually a mix of grounded and confabulated material.

This blending problem is the core failure mode of reference-based prompting. The model is a natural synthesizer. Given a reference and its own knowledge, it will synthesize them unless explicitly told not to. And because the blend is seamless — the model does not flag which parts came from the reference and which from memory — the result is unauditable without → provenance tracking.

## Why it matters in prompting

References transform a model from an unreliable encyclopedia into a reliable reader. An unreferenced model answering "What is our company's refund policy?" will produce something plausible but possibly wrong — it might hallucinate a policy based on training data from other companies. The same model given the company's actual refund policy document as a reference and instructed to "answer based only on the attached document" will produce an accurate, verifiable answer.

The quality of the reference matters as much as its presence. A vague, outdated, or contradictory reference produces vague, outdated, or contradictory output. References should be curated: relevant to the task, recent enough to be accurate, clear enough to be unambiguous, and scoped enough not to overwhelm. A single well-chosen page from a technical specification is a better reference than the entire specification dumped into the context.

Labeling references clearly is critical. "The attached document" is ambiguous when multiple documents are attached. "[REF-1] Company Refund Policy, updated January 2026" is unambiguous and supports → provenance tracking in the output.

## Why it matters in agentic workflows

In multi-agent systems, references are how you establish shared ground truth. When multiple agents analyze the same material, each should receive the same reference set or a clearly scoped subset. Without shared references, agents may reach inconsistent conclusions because they are drawing on different versions of the same information — or because one agent is using its parametric knowledge while another uses the provided documents.

References also enable tool-augmented workflows. When an agent calls a search tool or database query, the returned results become references for the next stage. The agent should treat these references with the same discipline applied to manually curated documents: label them, scope them, cite them, and prefer them over background knowledge.

## What it changes in model behavior

Providing a reference anchors the model's generation in specific material, reducing hallucination and improving factual precision. Models given clear references with explicit grounding instructions ("answer only from the provided documents") show measurably lower hallucination rates than models answering from parametric knowledge alone. The anchoring effect is strongest when the reference is labeled, the grounding instruction is explicit, and the task is scoped to what the reference covers.

## Use it when

- The task requires factual accuracy that the model's training data cannot guarantee
- You have authoritative source material the model should prefer over its own knowledge
- The output must be auditable — a reader should be able to verify every claim against its source
- Multiple agents or pipeline stages need to reason about the same ground truth
- The model's parametric knowledge on the topic is likely outdated or domain-specific enough to be unreliable

## Do not use it when

- The task is creative and grounding in external material would constrain the output unhelpfully
- The reference material is irrelevant to the question, which would only add noise to the context
- The task draws on widely known, stable facts where the model's training data is reliable (basic math, well-established science)

## Contrast set

- → **context** — Context is all the information the model receives. A reference is a specific piece of context with normative authority — the model should not just know about it but defer to it.
- → **grounding** — Grounding is the practice of anchoring generation in reality. A reference is one mechanism for grounding. You can also ground through tool use, verification, or constraining output to known entities.
- → **source anchoring** — Source anchoring is the prompt instruction that tells the model to stay close to a reference. The reference is the material; source anchoring is the instruction governing how the model uses it.
- → **retrieval scaffolding** — Retrieval scaffolding is the architecture that finds and delivers references. The reference is what gets delivered.

## Common failure modes

- **Ungrounded reference** — Providing a reference but not instructing the model to prioritize it. The model treats the reference as additional context and freely blends it with parametric knowledge. The output looks grounded but is partially confabulated. Fix: add explicit grounding instructions: "Answer based only on the attached documents. If the answer is not in the documents, say so."

- **Reference overload** — Providing too many references, diluting the model's attention and forcing it to choose which references to emphasize. In RAG systems, this often manifests as the model citing only the first or last few documents and ignoring the middle. Fix: curate references to include only material relevant to the specific question. Less is more.

- **Stale reference, confident output** — Providing an outdated reference that contradicts current reality. The model follows the reference faithfully, producing an answer that was correct in 2023 but not in 2026. Fix: version and date all references. Include recency in the model's evaluation criteria: "If the source is more than 12 months old, note the date and flag potential staleness."

## Prompt examples

### Minimal example

```text
Here is our company's data retention policy [REF-1].

A customer has asked: "How long do you keep my data after
I delete my account?"

Answer using only the information in REF-1. If the policy
does not address this question, say so.
```

### Strong example

```text
You are answering investor questions based on the following
source documents. Use ONLY these sources.

Sources:
[REF-1] Q4 2025 Earnings Call Transcript
[REF-2] FY2025 10-K Filing, Risk Factors (Section 1A)
[REF-3] Board-Approved 2026 Guidance Memo

Rules:
- Every factual claim must cite its source as [REF-X, p.Y]
  or [REF-X, Section Y].
- If a question cannot be answered from these sources, respond:
  "This question is not addressed in the available materials."
- Do not supplement with information from your training data.
- If two sources conflict, note the conflict and cite both.

Question: What is the company's projected revenue growth
for FY2026, and what are the primary risks to that projection?
```

### Agentic workflow example

```text
Pipeline: Reference-Grounded Research Synthesis

Shared reference corpus:
- SRC-001 through SRC-012 (academic papers, stored in
  corpus/papers/)
- SRC-100 through SRC-108 (industry reports, stored in
  corpus/reports/)

Agent 1 — Research Agent
Input: User question + corpus index (titles and abstracts)
Task: Select the 5 most relevant sources for the question.
Output: List of source IDs with relevance justification.

Agent 2 — Extraction Agent
Input: Full text of the 5 selected sources
Task: Extract key findings relevant to the question. Each
finding must include: source_id, page/section, exact quote.
Output: Structured findings array.

Agent 3 — Synthesis Agent
Input: Findings array + original question
Task: Write a 400-word synthesis. Every sentence must cite
at least one finding by source_id. If findings conflict,
present both positions. Append a reference list mapping
each source_id to its full citation.

Constraint: No agent may generate claims not traceable to
a source document. Unsourced claims are treated as errors.
```

## Model-fit note

All models respond to reference grounding, but compliance varies. Frontier models follow "answer only from the documents" instructions reliably and produce accurate citations 80–90% of the time. Midsize models occasionally supplement references with parametric knowledge despite explicit instructions not to — adding a verification step catches most of these leaks. Small models are the least reference-compliant and benefit from structural enforcement: require JSON output with mandatory source fields, and programmatically reject any output missing source citations.

## Evidence and provenance

Retrieval-augmented generation (RAG) as a reference-grounding mechanism was formalized by Lewis et al. (2020). The distinction between parametric and contextual knowledge is discussed across LLM survey literature [src_paper_sahoo2025]. The "lost in the middle" finding by Liu et al. (2023) demonstrates that reference placement affects retrieval quality [src_paper_sahoo2025]. The Prompt Report catalogues source-citing and grounding instructions as a recognized prompting technique [src_paper_schulhoff2025].

## Related entries

- **→ grounding** — the practice references enable
- **→ provenance tracking** — records which reference each claim came from
- **→ source anchoring** — the instruction that binds the model to its references
- **→ retrieval scaffolding** — the architecture that delivers references to the model
