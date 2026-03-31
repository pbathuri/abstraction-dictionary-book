---
headword: "context"
slug: "context"
family: "core_abstraction"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# context

**Elevator definition**
Context is the total information environment surrounding a model's generation — the system prompt, conversation history, attached documents, and retrieved content that collectively determine what the model knows at inference time.

## What it is

A language model does not know things the way a person does. It has two sources of information: what it learned during training (parametric knowledge) and what you give it right now (contextual knowledge). Context is the second one. It is everything in the prompt window that is not the model's own weights — and for most production use cases, it is the more important of the two.

The Prompt Report identifies several distinct context components that together form the model's information environment [src_paper_schulhoff2025]. **System prompts** set the behavioral baseline — who the model is, what rules it follows, what it should and should not do. **Conversation history** provides the sequential record of prior exchanges, giving the model continuity across turns. **Attached documents** supply reference material — reports, code files, data sets, transcripts — that the model can draw on. **Retrieved content** from RAG pipelines or tool calls provides dynamically fetched information relevant to the current query. Each component enters the same context window, but they serve different functions and interact in different ways.

Context has a hard constraint: the context window. Every model has a maximum number of tokens it can attend to simultaneously. GPT-4 class models offer 128K+ tokens. Smaller models may offer 4K-32K. The constraint is not just size but attention quality: models attend to tokens at the beginning and end of the context more reliably than tokens in the middle, a phenomenon documented across architectures. This means that context is not just what you provide — it is what you provide, where you place it, and how much of it the model can effectively use.

The critical distinction is between context and → framing. Context is *information*. Framing is *orientation*. You can have excellent context — all the right documents, complete conversation history, a well-written system prompt — and still get bad output because the model does not know which part of that context to prioritize or what lens to apply. Context is the library. Framing is the research question. You need both, but providing one without the other is a common and expensive mistake.

Context is also distinct from → grounding, though they interact. Providing context gives the model information. Grounding instructs the model to *derive its answers from* that information rather than supplementing from training data. Context without grounding means the model has the information but may not use it. Grounding without context means the model has instructions to cite sources but no sources to cite.

## Why it matters in prompting

The single most common source of prompt failure is context mismatch — the model either lacks information it needs, has information it does not need, or has the right information in the wrong place. Each of these produces a distinct failure pattern.

Missing context forces the model to guess. If you ask "Should we proceed with the Johnson deal?" without providing any information about the deal, the model will either ask for clarification (if it is instruction-tuned to do so) or fabricate a plausible-sounding analysis based on nothing. Insufficient context is the prompt equivalent of calling a consultant, refusing to give them any documents, and then asking for strategic advice.

Excess context creates noise. A 50-page document pasted into a prompt when the model only needs page 12 does not just waste tokens — it dilutes attention. The model must allocate processing capacity across all provided material, and irrelevant material competes with relevant material for that capacity. In long-context scenarios, this is the "needle in a haystack" problem: the answer is in the context, but it is buried under material that the model must wade through.

Misplaced context — relevant information in the wrong position — exploits the model's positional biases. Critical information in the middle of a long context is less likely to influence the output than the same information at the beginning or end. Context placement is an engineering decision, not a filing convenience.

## Why it matters in agentic workflows

In agent architectures, context management is the infrastructure problem. Every agent in a pipeline has a context window, and that window must contain everything the agent needs to do its job — and nothing it does not. This is harder than it sounds. A research agent needs access to source documents. An analysis agent needs the research agent's output. A synthesis agent needs the analysis agent's output and possibly the original documents. A review agent needs everything.

The naive approach — pass all context to all agents — fails at scale. It exceeds context windows, dilutes attention, and exposes agents to information that is not their concern (creating → scope leakage). The disciplined approach is context routing: each agent receives a curated context package containing its task description, the upstream outputs relevant to its scope, and the reference material it needs. Nothing more.

Context persistence across turns is another architectural concern. In multi-turn agent workflows, the conversation history grows with each exchange. If the full history is passed to every agent at every step, the ratio of historical noise to current signal worsens over time. Context summarization — compressing prior turns into a summary while preserving key facts and decisions — is an emerging pattern for managing this degradation. The tradeoff is lossy compression: summarization inevitably drops details that might have been relevant.

## What it changes in model behavior

The content and structure of context directly shapes the distribution of model outputs. Provide a model with three documents that agree and it will produce confident analysis. Provide three documents that conflict and it will hedge, qualify, and present multiple perspectives. Provide one document and instruct the model that it is the authoritative source and it will treat every claim in that document as fact. Context does not just inform the model's answer — it shapes the model's confidence, tone, and willingness to commit to a position.

## Use it when

- When the model needs information that may not be in its training data (recent events, proprietary data, specific documents)
- When accuracy matters and you want the model to work from provided evidence rather than memory
- When building multi-turn workflows that need continuity across exchanges
- When different agents in a pipeline need different subsets of information
- When you want to control not just what the model says but how confident it is (by controlling the evidence it sees)

## Do not use it when

- When the model's parametric knowledge is sufficient and providing context would be redundant
- When the available context is unreliable and would anchor the model to bad information
- When context window limits would force you to truncate critical information (in that case, redesign the context strategy first)

## Contrast set

- → framing — context is the information the model has; framing is how the model interprets it. Rich context with no frame produces unfocused output. A sharp frame with no context produces confident fabrication.
- → grounding — context provides information; grounding instructs the model to stay within it. Context without grounding is a library with no research methodology. Grounding without context is methodology with no library.
- → scope — scope limits what the model addresses; context determines what information is available to address it. You can scope a task narrowly while providing broad context (the model ignores what is out of scope) or provide narrow context for a broad task (the model lacks material to address the full scope).

## Common failure modes

- **Context overload** → Providing so much context that the model's attention is diluted across irrelevant material. The fix is not always to provide less — it is to structure context with clear sections, labels, and hierarchy so the model can navigate it efficiently.
- **Stale context** → In multi-turn conversations or long-running agent workflows, context from early turns may become outdated by later developments. If the model continues to reference stale context, it produces output that was correct five turns ago but is wrong now. Context pruning or summarization addresses this.
- **Context-framing confusion** → Providing extensive context and assuming the model will figure out what to do with it. Context tells the model what it knows. Framing and instructions tell the model what to do with what it knows. These are separate jobs and require separate prompt components.

## Prompt examples

### Minimal example

```text
System: You are a customer support agent for Acme Corp.
You may only reference the product documentation provided below.

[Product Documentation]
{doc_text}

User: {customer_question}
```

### Strong example

```text
You are a policy analyst preparing a briefing for a government
committee on renewable energy subsidies.

CONTEXT — Source Documents:
[DOC 1: Current Subsidy Framework]
{current_policy_text}

[DOC 2: Proposed Amendment]
{amendment_text}

[DOC 3: Industry Impact Assessment]
{impact_assessment_text}

CONTEXT — Background:
The committee is reviewing whether to extend existing subsidies
for an additional 5 years. The committee chair has publicly
expressed concern about fiscal cost. The minority position
favors expansion of subsidies to include nuclear energy.

TASK:
Using ONLY the three documents above and the background context:
1. Summarize the key changes in the proposed amendment (DOC 2)
   relative to the current framework (DOC 1)
2. For each change, cite the relevant finding from DOC 3
3. Flag any change where DOC 3's assessment is ambiguous
   or inconclusive
4. In a final paragraph, note any policy areas that the
   amendment does NOT address but the committee background
   suggests they will ask about

Label each section clearly. Cite documents as [DOC 1], [DOC 2],
or [DOC 3] with section numbers where available.
```

### Agentic workflow example

```text
Pipeline: Context-Managed Research System

Context Router Agent:
Input: User query + full document corpus
Task: Determine which documents are relevant to the query.
Return: A relevance-ranked subset (max 5 documents) with a
one-sentence explanation of each document's relevance.
Pass ONLY these 5 documents to downstream agents.

Research Agent:
Context received: 5 documents from Context Router + user query
Task: Extract key facts relevant to the query. For each fact,
cite [Doc X, Section Y]. Do not use knowledge outside the
provided documents.
Output: Structured fact list with citations.

Synthesis Agent:
Context received: Fact list from Research Agent + user query
(NOT the original documents — work from the extracted facts)
Task: Compose a 300-word briefing answering the user's query.
Every claim must trace to a fact in the fact list.
If the fact list is insufficient, state what is missing
rather than filling gaps from training data.

Context management rules:
- Each agent receives ONLY what it needs
- No agent sees the full document corpus except the Router
- The Synthesis Agent works from extracted facts, not raw documents
- Source traceability is maintained at every handoff
```

## Model-fit note

Context utilization varies significantly by model tier and architecture. Frontier models with 128K+ context windows can attend to large documents, but attention quality still degrades in the middle of very long contexts. Smaller models with limited windows require more aggressive context curation — only the most relevant material should be included. All tiers benefit from structured context (labeled sections, clear document boundaries) over unstructured dumps. RAG architectures help all tiers by pre-filtering context to the most relevant passages.

## Evidence and provenance

The Prompt Report provides the most comprehensive taxonomy of context components (system prompts, user prompts, conversation history, retrieved documents) and their roles in shaping model behavior [src_paper_schulhoff2025]. The interaction between context and RAG architectures is documented in Sahoo et al. (2025) [src_paper_sahoo2025]. The "lost in the middle" phenomenon in long-context models is from Liu et al. (2023), widely replicated across architectures.

## Related entries

- → framing — context provides information; framing provides interpretive orientation. Both are needed, and the distinction between them is one of the most productive concepts in prompt engineering.
- → grounding — grounding is the instruction to derive answers from provided context rather than from parametric memory. Context is the prerequisite; grounding is the constraint.
- → hierarchy — hierarchy determines how context is structured within the prompt, which affects how the model attends to it.
