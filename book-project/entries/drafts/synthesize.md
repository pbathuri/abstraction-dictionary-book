---
headword: "synthesize"
slug: "synthesize"
family: "instructional_action"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["summarize", "compare", "integrate", "elaborate", "framing", "decomposition"]
cross_links: ["summarize", "compare", "integrate", "elaborate", "framing", "decomposition", "constrain", "rank", "evaluate", "specificity"]
tags: ["instructional-action", "integrative-reasoning", "knowledge-construction", "prompting-fundamental"]
has_note_box: true
note_box_type: "which_word"
---

# synthesize

**Elevator definition**
To synthesize is to combine multiple sources, perspectives, or findings into a unified output that produces insight none of the inputs contained alone.

## What it is

Synthesis is not summary. This is the central fact of the entry, and it is the distinction that most prompt authors get wrong.

Summary takes one thing and makes it smaller. Synthesis takes multiple things and makes them *one*. The operation is integrative, not compressive. When you summarize a research paper, you reduce it. When you synthesize five research papers, you do not produce five summaries — you produce a single account of what they collectively say, where they agree, where they contradict, and what picture emerges from their intersection. The output of synthesis is a new thing that did not exist before the operation.

The intellectual work of synthesis has three phases, whether performed by a human or a language model. First, *comprehension*: understanding each input on its own terms. Second, *alignment*: identifying where the inputs speak to the same questions, use compatible frameworks, or address overlapping evidence. Third, *integration*: weaving the aligned inputs into a coherent whole that preserves the essential contributions of each while resolving or acknowledging tensions between them. The third phase is where the value lives. Comprehension is reading. Alignment is → compare. Integration is the thing that only synthesis does.

Language models are surprisingly capable synthesizers when prompted correctly, because the operation plays to their core strength: pattern recognition across large volumes of text. A model that has ingested five documents on the same topic can detect thematic convergences, terminological overlaps, and contradictory claims faster than a human reader. What the model lacks — and what the prompt must supply — is a framework for organizing those detections into something coherent. Without that framework, the model's synthesis devolves into either a list of "key points from each source" (which is multi-document summary, not synthesis) or a vague gesture at agreement ("all sources agree that X is important").

The Prompt Report's discussion of multi-document reasoning tasks underscores this point: models perform better on integrative tasks when the prompt specifies the output structure and the dimensions of integration [src_paper_schulhoff2025]. "Synthesize these five papers" is underspecified. "Synthesize these five papers into a single account of the current consensus on X, noting where the evidence converges, where it conflicts, and what questions remain unresolved" gives the model the three-phase structure it needs.

## Why it matters in prompting

Synthesis is the instruction you reach for when you have done your research and now need to *think*. You have gathered sources, collected data points, interviewed stakeholders, compiled reports. The material is spread across multiple documents. No single document contains the answer. The answer lives in the relationship between them.

This is where most prompters default to "summarize all of these" and get back a bulleted list of highlights from each source. The output is organized by source, not by theme. It is a stack of compressions, not an integration. The fix is to use the word "synthesize" and, critically, to specify the axis of integration: "Synthesize these customer interviews into a single description of the unmet need, drawing on all interviews but organized by theme, not by interviewee." The axis of integration is what transforms a reading list into an insight.

Synthesis also serves a quality function in prompting: it forces the model to confront contradictions rather than ignoring them. A summary of five sources can politely omit their disagreements. A synthesis cannot, because integration requires reconciliation. When two sources contradict each other, synthesis demands that the model either explain the contradiction, weigh the evidence, or flag the tension. This alone makes synthesis more truthful than summary in multi-source contexts.

## Why it matters in agentic workflows

In multi-agent pipelines, synthesis is the operation that sits at the convergence point — the node where multiple upstream agents' outputs merge into a single downstream product. A research pipeline with three specialized agents (one for academic literature, one for industry reports, one for practitioner interviews) needs a Synthesis Agent at the junction. Without it, the final output is a three-part report that reads like three separate reports stapled together.

The Synthesis Agent's job is to read the upstream outputs not as standalone documents but as partial views of a single landscape. Its system prompt must specify the integrative frame: "You are receiving three research streams. Your job is not to repeat them. Your job is to identify the picture that emerges only when you read them together." This is a → framing operation that prevents the agent from defaulting to multi-document summary.

## What it changes in model behavior

The instruction "synthesize" shifts the model from *source-organized* to *theme-organized* output. Instead of processing inputs sequentially (Source A says..., Source B says..., Source C says...), the model organizes by conceptual thread, pulling from multiple sources within each thread. This structural shift is observable in the output: synthesis produces more cross-references between sources, more comparative language, and more meta-level claims ("the evidence converges on..." "a tension emerges between...") than summary or description.

The shift also changes how the model handles contradictions. In summary mode, conflicting claims from different sources are often silently dropped or reported without comment. In synthesis mode, contradictions surface as explicit tensions to be addressed, because the integrative frame makes ignoring them structurally impossible.

## Use it when

- You have multiple sources, perspectives, or data streams and need a single coherent output
- The answer to your question does not live in any single source but in the relationship between sources
- You need to surface contradictions, tensions, or unexpected convergences across inputs
- A downstream consumer (human or agent) needs a unified view, not a collection of separate reports
- You are building a pipeline convergence point where multiple research streams merge
- The material is thematically overlapping and a source-by-source treatment would be redundant

## Do not use it when

- You have a single source and just need it compressed — that is → summarize
- You want a side-by-side comparison without integration — that is → compare
- The sources are on different topics and have no meaningful overlap to integrate
- You need the model to preserve each source's distinct voice or perspective (synthesis erases boundaries by design)

## Contrast set

**Closest adjacent abstractions**

- → summarize — Summary compresses a single source. Synthesis integrates multiple sources. Summary makes things smaller. Synthesis makes things *one*. These are different operations, though they are routinely confused.
- → compare — Compare places items side by side to identify similarities and differences. Synthesis goes further: it takes the comparison and builds a unified view from it. Compare is the second phase (alignment). Synthesis is the third (integration).
- → integrate — Near-synonym. In most prompting contexts, "integrate" and "synthesize" produce similar outputs. "Integrate" emphasizes mechanical combination. "Synthesize" implies that the combination produces new understanding.

**Stronger / weaker / narrower / broader relatives**

- → elaborate — Orthogonal direction. Elaboration expands a single idea. Synthesis combines multiple ideas.
- → decomposition — The inverse. Decomposition breaks one thing into parts. Synthesis assembles parts into one thing.
- → framing — The integrative frame that a synthesis prompt specifies determines the quality of the output.

## Common failure modes

- **Synthesis as multi-summary** → The model writes a paragraph about each source and calls it synthesis. No integration occurs. The output is organized by source, not by theme. Fix: explicitly instruct "organize by theme, not by source" and specify the themes or ask the model to identify them first.

- **Premature consensus** → The model papers over genuine disagreements to produce a smooth, unified account. This is the most insidious failure because the output *looks* like good synthesis — it is coherent, well-written, and integrated — but it has suppressed information that matters. Fix: require the model to "identify and discuss any tensions, contradictions, or unresolved disagreements between sources."

- **Theme invention** → When the synthesis prompt is too vague, the model invents organizing themes that are not present in the source material. The output reads well but maps poorly to the actual inputs. Fix: either specify the themes yourself or add a verification step that checks each claim back against the sources.

## Prompt examples

### Minimal example

```text
Here are four product review summaries from different analysts.

Synthesize them into a single product assessment. Organize
by theme, not by analyst. Note where the analysts agree,
where they disagree, and what picture emerges overall.
```

### Strong example

```text
I have attached three documents:
1. A quantitative market analysis (data-heavy, forward projections)
2. A qualitative user research report (interview-based, thematic)
3. A competitive landscape overview (positioning, feature comparison)

Synthesize these into a single strategic brief (800-1000 words)
that answers: "Should we enter this market in the next 12 months?"

Structure your synthesis around these three questions:
- Is there sufficient demand? (draw primarily on docs 1 and 2)
- Can we compete? (draw primarily on docs 2 and 3)
- What are the risks of entry vs. the risks of waiting? (all docs)

Where the documents contradict each other (e.g., the quantitative
projections say one thing but user interviews suggest another),
flag the contradiction explicitly and assess which evidence
is more reliable for the specific question.

Do not summarize each document. I have already read them.
I need the picture that emerges from reading them together.
```

### Agentic workflow example

```text
Agent: Synthesis Agent
Pipeline position: Convergence node after three parallel
research streams

Inputs:
- academic_findings.json from Literature Agent
- industry_data.json from Market Agent
- practitioner_insights.json from Interview Agent

Task: Synthesize all three streams into a unified research
brief (600-800 words).

Synthesis protocol:
1. First pass — Identify the 3-5 major themes that appear
   across at least two of the three inputs.
2. Second pass — For each theme, integrate the evidence from
   all relevant inputs. Cite the source stream for each claim
   using [ACADEMIC], [INDUSTRY], or [PRACTITIONER].
3. Third pass — Identify contradictions between streams and
   assess which stream's evidence is stronger for each
   contested claim. Do not resolve contradictions by averaging.
4. Final section — "What emerges": 2-3 sentences describing
   the picture that only becomes visible when all three
   streams are read together.

Constraints:
- Organize by theme, never by source stream.
- Every claim must cite at least one source stream.
- If a theme appears in only one stream, include it in a
  separate "Single-source findings" section with lower
  confidence flagging.

Output: Markdown document with sections per theme.
Handoff: Pass to Editorial Agent for final formatting.
```

## Model-fit note

Synthesis quality depends heavily on context window and instruction-following capacity. Frontier models handle multi-document synthesis well, maintaining thematic coherence across long inputs and producing genuinely integrative outputs. Midsize open models perform adequate synthesis with two or three short sources but degrade with more — they tend to revert to sequential summary when the input volume rises. Small open models rarely produce true synthesis; they default to multi-summary regardless of prompting. For small models, break the synthesis into explicit phases: compare first, then integrate, using separate prompts for each phase.

## Evidence and provenance

The Prompt Report's taxonomy of reasoning tasks includes multi-document synthesis and notes that explicit integration criteria improve output quality [src_paper_schulhoff2025]. The three-phase model of synthesis (comprehension, alignment, integration) draws from educational research on reading comprehension and is applied here to LLM output analysis. The observation that synthesis forces contradiction handling while summary allows contradiction avoidance is based on practitioner analysis of multi-source prompting outputs. The distinction between theme-organized and source-organized output as a marker of synthesis quality is original to this entry.

## Related entries

- **→ summarize** — compresses a single source; synthesis integrates multiple sources
- **→ compare** — the alignment step that often precedes synthesis
- **→ elaborate** — expands a single point; synthesis converges multiple points
- **→ decomposition** — the inverse operation: breaking apart vs. building together
- **→ framing** — the integrative frame determines synthesis quality
- **→ evaluate** — may follow synthesis to assess the unified picture

---

> **Which Word?**
>
> *Synthesize* or *summarize*? If you have one document and want it shorter, summarize. If you have multiple documents and want them *unified*, synthesize. The test: does your desired output organize information by source ("Document A says... Document B says...") or by theme ("The evidence on X suggests... The evidence on Y suggests...")? If by source, you are summarizing multiple things. If by theme, you are synthesizing. When in doubt, use "synthesize" — it is strictly more demanding, and a model that synthesizes well has necessarily also comprehended each source individually.
