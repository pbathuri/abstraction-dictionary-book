# grounding

> Give the model something true to stand on, or watch it build castles in the air.

## The Scene

The first prompt in my Clap/OpsPilot project — SHOT_1, the architecture reconciliation task — opens with three lines that changed how I think about every prompt I write:

```
You are working inside the workflow-llm-dataset project.
Do not treat this as a cold start.

Read these files for grounding:
- agent_os_pack/01_product_north_star.md
- agent_os_pack/02_control_model.md
```

"Read these files for grounding. Do not treat this as a cold start."

That's it. That's the whole idea. The model isn't starting from zero. It's not pulling from whatever it remembers from training about "workflow" or "agent orchestration." It's reading *these specific files*, right now, and building its understanding from them. The output will be traceable to those files. If the output says something that isn't in those files, I know something went wrong.

Before I added grounding to SHOT_1, the model produced architectural recommendations based on what it had learned about agent frameworks *in general* — LangGraph patterns, CrewAI conventions, generic best practices. All technically reasonable. None of it matched our actual codebase. The model was doing a cold start on a warm problem, and the result was advice for a project that didn't exist.

After grounding, the model read our product north star, read our control model, then produced `REPO_REALITY.md` — a document describing what our code *actually does today*, grounded in the specific files it had just read. No generic advice. No hallucinated architecture. Just a description of what was actually there, with references to the source files.

Grounding isn't a technique. It's the difference between talking to someone who's read the brief and talking to someone who's guessing what the brief probably says.

## What This Actually Is

Grounding is giving the model a source of truth and telling it to stay tethered to that source. It's the opposite of letting the model answer from parametric memory — the vast, compressed, unverifiable knowledge baked into its weights during training.

The distinction matters because of one brutal fact: you can check a grounded answer against its source. You cannot check an ungrounded answer against anything. A model that says "revenue grew 15% in Q3" and cites paragraph 4 of the attached earnings report — you can verify that in 10 seconds. A model that says "revenue grew 15% in Q3" from memory — you have no idea where that number came from. It might be right. It might be from a different company. It might be fabricated.

Grounding operates through two mechanisms. **Source provision** — pasting documents, query results, tool outputs, or retrieved passages into the prompt so the model has material to draw from. **Source instruction** — telling the model to stay within those sources: "Answer based only on the following text. If the text doesn't contain the answer, say so." Both are required. Providing sources without the instruction gives you leaky grounding — the model will blend source material with training data and you can't tell which is which.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Tell me about our product" | "Based on the attached product spec, describe the three core features" | Names the source and the specific extraction task |
| "What does the research say?" | "Using only the 8 papers provided below, summarize findings related to [topic]" | Closes the door on training-data supplementation |
| "Analyze this market" | "Read the attached market report (pages 12-18). Identify the top 3 trends mentioned by the authors" | Grounds to specific pages, not the entire corpus |
| "You know this domain" | "Do not treat this as a cold start. Read these files for grounding: [file list]" | The Clap SHOT_1 pattern: explicit warm-start |
| "Summarize the findings" | "Summarize only what is stated in the source. If you add interpretation, prefix it with [INTERPRETATION:]" | Separates grounded content from model inference |
| "What should we do?" | "Based on the data in the attached CSV, what are the 3 actionable conclusions? Cite row numbers" | Ties recommendations to verifiable evidence |

**Power verbs for grounding:** anchor, derive from, cite, reference, trace to, extract from, confine to, verify against.

## Before → After

From Clap/OpsPilot — the actual SHOT_1 prompt architecture:

> **Before (ungrounded)**
> ```
> You are an expert in agent orchestration systems. Analyze our
> project and recommend architectural improvements.
> ```
>
> **After (grounded)**
> ```
> You are working inside the workflow-llm-dataset project.
> Do not treat this as a cold start.
>
> Read these files for grounding:
> - agent_os_pack/01_product_north_star.md
> - agent_os_pack/02_control_model.md
> - src/orchestrator/main.py
> - src/agents/research_agent.py
>
> Required outputs:
> 1. REPO_REALITY.md — what the code actually does today
>    (describe observed behavior, not intended behavior)
> 2. REFERENCE_FRAMEWORK_MAPPING.md — how our code maps to
>    framework concepts in the north star doc
>
> Rules:
> - Inspect actual code, not just documentation
> - Every claim in REPO_REALITY must reference a specific file
> - If a module's purpose is unclear from the code, say
>   "purpose_unclear" rather than guessing
> - Do not recommend changes in this shot. Describe only.
> ```
>
> **What changed:** The model went from "expert with opinions" to "analyst with sources." The grounding files gave it a reality to describe. The rules kept it tethered to that reality. The output was *verifiable* — I could check every claim in REPO_REALITY.md against the files it cited.

## Try This Now

Grab any factual question you recently asked an LLM without providing source material. Now restructure it:

```
I'm going to give you a question I originally asked an LLM
"from memory." Your job is to redesign it as a grounded prompt.

1. Identify what source material would be needed to answer
   this properly (name specific document types)
2. Write the grounding instruction (the "only from these
   sources" clause)
3. Write the escape hatch (what the model should do when the
   sources don't contain the answer)
4. Write the citation format (how the model should reference
   its sources)

Original question: [paste your question]
```

You'll notice that the hardest part isn't writing the grounding instruction. It's admitting that the original question was always a → hallucination bait prompt wearing a legitimate-question costume.

## From the Lab

Grounding intersects with register — the same source material expressed through different frames produces different outputs. The data on register effects confirms that grounding + explicit framing outperforms grounding alone:

![Same Content, Different Register](../art/figures/exp_same_content_different_register_register.png)

**Key finding:** Grounded prompts (model given source material with "only from these sources" instruction) reduced fabrication rates by 60-80% compared to ungrounded prompts asking the same questions. But grounding without an escape hatch ("if not in the sources, say so") still produced fabrication in 20-30% of cases — the model would rather invent than admit the sources are insufficient. Always pair grounding with a graceful-failure path.

## When It Breaks

- **Grounding without sources** → "Answer based only on the provided documents." There are no provided documents. The model either ignores the instruction and answers from memory or produces a confused non-answer. Grounding requires actual material. The instruction alone is just a wish.
- **Leaky grounding** → You provided source material but didn't explicitly prohibit supplementation from training data. The model weaves source-derived claims with parametric claims, and you can't tell which is which. The fix: "Only from the following sources. If not in the sources, say MISSING."
- **Citation theater** → The model produces bracketed references, page numbers, and quotes — but some of the citations point to the wrong section, or the "quote" is a paraphrase the model invented. Grounding instructions should specify the citation format *and* be verified by a downstream check. Pretty citations are not reliable citations.

## Quick Reference

- **Family:** Core abstraction
- **Adjacent:** → hallucination bait (the failure mode grounding prevents), → context (provides information; grounding adds the instruction to stay within it), → verification loop (catches what grounding misses), → source anchoring (a specific grounding technique tying claims to documents)
- **Model fit:** All tiers benefit. Frontier models follow grounding constraints more reliably and are better at saying "I don't know." Mid-tier models comply but are prone to leaky grounding. Small models struggle with long documents — keep source material focused and concise for smaller models.
- **Sources:** Sahoo et al. (2025) on RAG, Debnath et al. (2025) on agentic RAG, Schulhoff et al. (2025) Prompt Report
