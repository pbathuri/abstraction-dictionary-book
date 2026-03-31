---
headword: "source anchoring"
slug: "source_anchoring"
family: "context_architecture"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["grounding", "provenance tracking", "retrieval scaffolding", "hallucination bait", "verification loop", "falsifiability"]
cross_links: ["grounding", "provenance tracking", "retrieval scaffolding", "hallucination bait", "verification loop", "falsifiability", "rubric", "context windowing", "audit trail"]
tags: ["context-architecture", "citation", "factual-accuracy", "hallucination-prevention", "grounding"]
has_note_box: true
note_box_type: "model_note"
---

# source anchoring

**Elevator definition**
Source anchoring is the technique of tying every model claim to a specific, verifiable passage in a provided source document — the citation mechanism that prevents hallucination.

## What it is

Language models do not distinguish between what they know and what they invent. A model will state that "revenue grew 14% in Q3" with the same syntactic confidence whether the number comes from a document in the context, from training data vaguely resembling the topic, or from thin air. The model does not flag the difference. It cannot, by architecture — the generation process produces tokens based on probability, not on epistemic certainty.

Source anchoring is the engineering response to this architectural limitation. It is a prompt-level technique that forces the model to connect each claim to a specific, locatable passage in a provided document. Not "based on the documents" in a vague, hand-wavy sense, but *this claim, from this passage, on this page, in this source*. The anchor is the specific text span that supports the claim. If the model cannot produce the anchor, it should not produce the claim.

The technique draws its power from an asymmetry in model capabilities. Models are mediocre at spontaneous factual recall — they confabulate, they approximate, they hallucinate with confidence. But they are substantially better at *extraction and attribution* when given explicit source material and explicit instructions to cite it. Source anchoring exploits this gap. Instead of asking the model "what do you know about this topic?" (unreliable), you ask "what does *this document* say about this topic, and where exactly does it say it?" (far more reliable).

The distinction between source anchoring and the broader concept of grounding is important. Grounding is any technique that ties model output to external reality — tool use, retrieval, code execution, human verification. Source anchoring is a specific, narrow form of grounding: it ties model *text claims* to *specific passages in provided documents*. A model that calls a calculator API to verify arithmetic is grounded but not source-anchored. A model that quotes paragraph 4 of the attached report to support its summary is source-anchored.

Provenance tracking, by contrast, operates at the pipeline level. It records the chain of custody — which source was retrieved by which system, passed to which agent, used to support which claim. Source anchoring is the *act* of tying a claim to a source. Provenance tracking is the *bookkeeping* that records the tie.

## Why it matters in prompting

In single-turn prompting, source anchoring transforms the model from an unreliable narrator into a diligent research assistant. The instruction pattern is straightforward: provide the source documents, instruct the model to cite specific passages when making claims, and instruct it to state when a question cannot be answered from the provided material.

This works because it changes the task from *generation* (producing claims from internal knowledge) to *extraction* (locating claims in provided text). Extraction is a task models perform well. The instruction "quote the relevant passage before stating your conclusion" forces the model to ground every claim in verifiable text, and it simultaneously gives the reader the ability to verify — they can check the quote against the original.

The absence of source anchoring is how most hallucination enters production systems. A prompt that says "summarize this document" without anchoring instructions gives the model implicit permission to summarize *its understanding of documents like this one*, blending retrieved content with parametric knowledge. The output looks like a summary of the document. Parts of it are not.

## Why it matters in agentic workflows

In multi-agent pipelines, source anchoring becomes a data integrity mechanism. When a Research Agent passes claims to a Synthesis Agent, and the Synthesis Agent passes a summary to a Review Agent, any unanchored claim becomes untraceable. The Review Agent sees a statement — "the market grew 9% year-over-year" — and cannot determine whether it came from a retrieved source, from the Research Agent's parametric knowledge, or from a hallucination that propagated through two pipeline stages.

Anchored claims carry their provenance with them. Each claim is a tuple: (statement, source_id, passage_reference). Downstream agents can verify. The Verification Agent can check whether the passage actually supports the claim. The Audit Agent can log which sources informed which parts of the final output. Without anchoring, the pipeline is a game of telephone. With it, every link in the chain is inspectable.

## What it changes in model behavior

Source anchoring shifts the model's generation strategy from parametric recall to extractive reasoning. The model searches the provided context for supporting evidence before producing claims, rather than generating claims and retroactively justifying them. This reduces hallucination rates for factual claims substantially — not to zero, but by a meaningful margin.

Anchoring also changes failure modes productively. An unanchored model that lacks information invents it. An anchored model that lacks information is more likely to say "I cannot find support for this in the provided documents." The failure mode shifts from *fabrication* to *omission*, which is far easier to detect and correct.

## Use it when

- The output contains factual claims that must be accurate and traceable
- The source material is provided in the context and the model should not go beyond it
- The output will be reviewed by humans or verification agents who need to check claims
- The domain has low tolerance for errors (legal, medical, financial, regulatory)
- Previous outputs from the same pipeline contained hallucinated or unattributed claims
- You are building a research or analysis tool where trust depends on transparency

## Do not use it when

- The task is creative writing, brainstorming, or opinion generation where no source document applies
- The model is being used for its parametric knowledge intentionally (general knowledge Q&A without specific sources)
- No source documents are available — you cannot anchor to documents that do not exist
- The task involves synthesizing a novel argument that goes beyond any single source (though individual supporting claims should still be anchored)

## Contrast set

**Closest adjacent abstractions**

- → grounding — Broader. Grounding includes tool use, code execution, human feedback — any reality tie. Source anchoring is specifically about tying text claims to document passages.
- → provenance tracking — Complementary. Anchoring is the act; provenance tracking is the bookkeeping system that records and maintains the anchoring trail across pipeline stages.
- → retrieval scaffolding — Prerequisite. Scaffolding organizes retrieved documents and labels them. Anchoring uses those labels to tie claims to specific sources.

**Stronger / weaker / narrower / broader relatives**

- → hallucination bait — Antagonist. Hallucination bait is the set of prompt conditions that invite fabrication. Source anchoring is one of the strongest defenses.
- → falsifiability — Ally. Anchored claims are inherently falsifiable — you can check the source. Unanchored claims are not.
- → verification loop — Consumer. Verification loops check claims against criteria. Anchored claims give verification loops something concrete to check.

## Common failure modes

- **Anchor fabrication** → The model invents the anchor. It says "According to paragraph 3 of the attached report..." and the quote does not appear in paragraph 3, or the report has no paragraph 3. This happens because the model generates plausible-sounding citations without actually locating the text. Fix: instruct the model to *quote the exact text* it is citing, not paraphrase it. Quotes are verifiable; paraphrased citations are not.

- **Lazy anchoring** → The model anchors every claim to the same source or the first source in the context, regardless of which source actually supports the claim. Fix: require per-claim anchoring with distinct passage references. Add a verification step that checks whether the cited passage actually supports the claim.

- **Anchoring without boundaries** → The model is instructed to cite sources but not instructed to *refrain from claims it cannot anchor*. It cites sources for some claims and silently generates others from parametric knowledge. The output is a mix of anchored and unanchored claims with no visible boundary between them. Fix: add the explicit instruction "if you cannot anchor a claim to the provided sources, do not make the claim — instead, note what information is missing."

- **Over-anchoring** → The model cites a source for every clause, including common knowledge and its own reasoning. "The sky is blue (Source: Environmental Report, p. 12)" clutters the output and dilutes the value of real citations. Fix: instruct the model to anchor factual claims and data points, not general knowledge or logical inference.

## Prompt examples

### Minimal example

```text
Read the attached document carefully.

Answer the following question using ONLY information from this document.
For each factual claim in your answer, quote the specific passage that
supports it in [brackets].

If the document does not contain enough information to answer, say
"The document does not address this" rather than guessing.

Question: What were the primary risk factors identified in the audit?
```

### Strong example

```text
You are a legal research assistant reviewing a contract for compliance risks.

Source document: Master Services Agreement (attached)

For each risk you identify:
1. State the risk in plain language.
2. Quote the EXACT contract clause that creates or relates to the risk.
   Use this format: [Section X.X: "exact quote..."]
3. Explain why this clause poses a risk.
4. Rate severity: HIGH | MEDIUM | LOW

Rules:
- ONLY identify risks present in the actual contract language.
  Do not flag risks based on what the contract *should* contain
  but does not (that is a gap analysis, not a risk review).
- If a clause is ambiguous, flag it as a risk and quote the
  ambiguous language.
- Do not paraphrase contract language — exact quotes only.
  Paraphrased quotes cannot be verified.
- If you identify fewer than 3 risks, that is fine. Do not
  manufacture risks to fill a quota.

Output: Numbered list of identified risks with anchored citations.
```

### Agentic workflow example

```text
Pipeline: Retrieve → Extract → Anchor → Synthesize → Verify

--- ANCHOR AGENT ---

Input from Extract Agent:
{
  claims: [
    { claim_id, claim_text, probable_source_id }
  ],
  source_documents: [
    { source_id, full_text, metadata }
  ]
}

Task: For each claim, locate the supporting passage in the
indicated source document.

For each claim, produce:
{
  "claim_id": "",
  "claim_text": "",
  "source_id": "",
  "anchor": {
    "status": "ANCHORED | UNANCHORED | WEAK_ANCHOR",
    "passage": "exact quoted text from source",
    "location": "section/page/paragraph reference",
    "support_strength": "DIRECT | INFERENTIAL | PARTIAL"
  }
}

Definitions:
- ANCHORED: exact passage found that directly supports the claim
- WEAK_ANCHOR: passage found that partially or inferentially
  supports the claim
- UNANCHORED: no supporting passage found in the indicated source

Rules:
- Do NOT paraphrase the passage. Copy it verbatim.
- Do NOT search outside the indicated source_id. If the claim's
  source is wrong, mark UNANCHORED and note "passage not found
  in indicated source."
- WEAK_ANCHOR claims must include an explanation of the gap
  between claim and supporting text.

Handoff: Pass anchored claims to Synthesize Agent.
Flag UNANCHORED claims for Research Agent re-processing.
If > 20% of claims are UNANCHORED, escalate to orchestrator.
```

## Model-fit note

Source anchoring reliability scales with model capability. Frontier models anchor accurately to specific passages and can distinguish direct support from inferential support. They occasionally fabricate anchors for claims they are confident about but that lack explicit textual support — overconfidence leaks through even with anchoring instructions. Midsize open models anchor reliably when the source document is short and the anchoring instructions are simple, but degrade when asked to anchor across multiple long documents. Small models struggle with accurate quoting — they paraphrase even when instructed to quote verbatim. For small models, consider a two-pass approach: first extract relevant passages, then generate claims from the extracted passages only.

## Evidence and provenance

The distinction between source anchoring, grounding, and provenance tracking is original to this entry, synthesized from practitioner patterns in production RAG and research pipelines. The observation that models are better at extraction and attribution than spontaneous factual recall is supported by findings across the RAG literature, including Sahoo et al. (2025) [src_paper_sahoo2025] and Debnath et al. (2025) [src_paper_debnath2025]. The failure mode of anchor fabrication (models citing non-existent passages) is documented in hallucination studies and practitioner reports across model families.

## Related entries

- **→ grounding** — the broader category; source anchoring is one specific form of grounding
- **→ provenance tracking** — the bookkeeping system that records the anchoring trail
- **→ retrieval scaffolding** — organizes retrieved material so anchoring can reference it clearly
- **→ hallucination bait** — the conditions that make anchoring most necessary
- **→ falsifiability** — anchored claims are falsifiable; unanchored claims may not be
- **→ verification loop** — uses anchored claims as verifiable inputs to quality checks

---

> **Model Note**
>
> The most dangerous form of hallucination is the one with a citation. A model that invents a fact *and* invents a source reference for it is harder to catch than a model that invents a fact with no attribution. Source anchoring with exact quoting is the defense: when the model must produce the verbatim passage, fabricated citations become detectable because the quote will not match the source document. Instructing the model to quote rather than paraphrase is not a stylistic preference — it is a verification mechanism.
