# Appendix A: Model Fit Matrix

> A comprehensive guide to which abstractions work best with which model tiers.

---

## How to Read This Matrix

This matrix maps each of the 75 headwords in Part II to the six model tiers defined below. Its purpose is practical: when you know what model you are working with, this matrix tells you which abstractions will be most effective, which will require supporting techniques, and which you should skip or replace.

**Ratings** use a four-level scale:

- **Excellent** — The abstraction works reliably and produces measurable improvement at this tier. You can use it as described in the entry with confidence.
- **Good** — The abstraction works in most cases with occasional lapses. Minor adjustments or a second pass may be needed.
- **Partial** — The abstraction works sometimes but requires supporting techniques, simpler phrasing, or decomposition into sub-steps. Results will be inconsistent if used alone.
- **Weak** — The abstraction is unreliable at this tier. The model frequently misinterprets, ignores, or degrades the instruction. Consider alternatives or pair it heavily with simpler directives.

**Blank cells** indicate insufficient evidence or inapplicability.

**How the ratings were determined.** Ratings synthesize three sources: (1) empirical patterns from published benchmarks and model evaluations, (2) documented behavior from model provider guidance (OpenAI, Anthropic, Google, Meta), and (3) practitioner experience during entry development. They are directional, not absolute — a "Partial" rating means the abstraction works under favorable conditions but should not be relied upon without testing. Model capabilities change with each release; treat this matrix as a snapshot, not a permanent truth.

**How to use this in practice.** Find the model tier you are targeting. Scan down the column. Entries rated Excellent or Good are your primary toolkit. Entries rated Partial can be used if paired with simpler supporting abstractions (see each entry's "When to Use" section for guidance). Entries rated Weak should be replaced with the alternatives listed in each entry's contrast table.

---

## Model Tier Definitions

| Tier | Description | Representative Models (as of publication) |
|------|-------------|-------------------------------------------|
| **Small Open** | Open-weight models typically under 10B parameters. Strong at focused, well-constrained tasks. Limited instruction-following and reasoning depth. | Llama 3 8B, Mistral 7B, Phi-3 Mini, Gemma 2 2B/9B |
| **Midsize Open** | Open-weight models in the 10B–70B range. Capable of moderate reasoning and multi-step instructions. Good cost-performance balance. | Llama 3 70B, Mixtral 8x22B, Qwen 72B, DeepSeek-V2-Lite |
| **Large Open** | Open-weight models above 70B parameters. Near-frontier capability on many tasks. Strong instruction-following and nuanced reasoning. | Llama 3 405B, DeepSeek V3, Qwen-Max |
| **Frontier Proprietary** | Closed-weight frontier models with the broadest capability range. Strongest general instruction-following, nuance detection, and context handling. | GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro |
| **Reasoning-Specialized** | Models optimized for chain-of-thought, multi-step reasoning, and deliberation. Excel at complex analysis and self-correction. | o1, o3, DeepSeek-R1, Claude with extended thinking |
| **Code-Specialized** | Models optimized for code generation, tool use, and structured output. Strong at formal syntax and execution-oriented tasks. | Codex, StarCoder 2, DeepSeek-Coder-V2, Qwen-Coder |

---

## Matrix: Core Abstraction Family

These 15 entries form the foundation of the prompting vocabulary. They define how instructions frame, scope, and ground model behavior.

| Headword | Small Open | Midsize Open | Large Open | Frontier | Reasoning | Code | Notes |
|----------|-----------|-------------|-----------|---------|-----------|------|-------|
| **specificity** | Partial | Good | Good | Excellent | Excellent | Good | Smaller models need more explicit specificity but also hit the overspecification ceiling faster |
| **precision** | Partial | Good | Good | Excellent | Excellent | Good | Precision in verb choice matters most at midsize tier, where models are sensitive to wording |
| **clarity** | Good | Good | Excellent | Excellent | Excellent | Good | Even small models benefit from clear structure; this is tier-universal |
| **explicitness** | Good | Good | Excellent | Excellent | Excellent | Excellent | Critical at all tiers — implicit assumptions fail everywhere |
| **decomposition** | Weak | Partial | Good | Excellent | Excellent | Good | Small models struggle with multi-part decomposed tasks; flatten to single steps |
| **hierarchy** | Weak | Partial | Good | Excellent | Excellent | Good | Nested hierarchies require strong instruction-following |
| **modularity** | Weak | Partial | Good | Excellent | Good | Excellent | Code-specialized models handle modular structure naturally |
| **abstraction** | Weak | Partial | Good | Excellent | Excellent | Partial | Operating at the right abstraction level requires meta-reasoning |
| **framing** | Partial | Good | Good | Excellent | Excellent | Partial | Role and context framing improves output at all tiers; code models less responsive to narrative framing |
| **perspective** | Weak | Partial | Good | Excellent | Excellent | Weak | Perspective-shifting requires strong theory-of-mind capability |
| **scope** | Partial | Good | Good | Excellent | Good | Good | Explicit scope boundaries help all tiers; smaller models more prone to scope creep |
| **context** | Partial | Good | Good | Excellent | Excellent | Good | Context utilization scales with model size; small models lose track of long context |
| **grounding** | Partial | Good | Good | Excellent | Excellent | Good | Grounding reduces hallucination at every tier; most impactful at smaller tiers |
| **anchoring** | Partial | Good | Good | Excellent | Excellent | Good | Anchoring to source material is universally effective |
| **reference** | Partial | Good | Good | Excellent | Excellent | Good | Reference resolution improves with model size |

---

## Matrix: Instructional Action Family

These 15 entries are the verbs of prompt engineering — they tell the model what cognitive operation to perform.

| Headword | Small Open | Midsize Open | Large Open | Frontier | Reasoning | Code | Notes |
|----------|-----------|-------------|-----------|---------|-----------|------|-------|
| **compare** | Partial | Good | Good | Excellent | Excellent | Partial | Structured comparison requires holding multiple objects in working context |
| **contrast** | Partial | Good | Good | Excellent | Excellent | Partial | Contrast is harder than comparison; requires identifying salient differences |
| **analyze** | Weak | Partial | Good | Excellent | Excellent | Partial | Deep analysis requires reasoning depth; smaller models produce surface-level output |
| **evaluate** | Weak | Partial | Good | Excellent | Excellent | Partial | Evaluation requires judgment; reasoning models excel when given explicit criteria |
| **synthesize** | Weak | Partial | Good | Excellent | Excellent | Weak | Synthesis across multiple sources is one of the hardest instructional actions for smaller models |
| **summarize** | Good | Good | Excellent | Excellent | Good | Partial | Summarization is well-trained across all tiers; reasoning models may over-elaborate |
| **integrate** | Weak | Partial | Good | Excellent | Excellent | Partial | Combining information from disparate sources requires strong context management |
| **generate** | Good | Good | Good | Excellent | Good | Excellent | Generation is the default mode; all models handle it, but quality varies |
| **compose** | Partial | Good | Good | Excellent | Good | Good | Structured composition benefits from instruction-following strength |
| **elaborate** | Partial | Good | Good | Excellent | Excellent | Partial | Controlled elaboration (not rambling) requires constraint pairing |
| **constrain** | Good | Good | Good | Excellent | Good | Excellent | Constraint-following is well-trained; code models handle formal constraints best |
| **filter** | Partial | Good | Good | Excellent | Good | Excellent | Filtering requires reliable condition evaluation; code models strong here |
| **critique** | Weak | Partial | Good | Excellent | Excellent | Weak | Genuine critique (not summary) requires adversarial reasoning |
| **rank** | Partial | Good | Good | Excellent | Excellent | Good | Ranking requires consistent application of criteria across items |
| **justify** | Weak | Partial | Good | Excellent | Excellent | Partial | Justification chains require reasoning depth proportional to claim complexity |

---

## Matrix: Context Architecture Family

These 10 entries deal with how information is structured, routed, and managed within prompts and across turns.

| Headword | Small Open | Midsize Open | Large Open | Frontier | Reasoning | Code | Notes |
|----------|-----------|-------------|-----------|---------|-----------|------|-------|
| **context windowing** | Weak | Partial | Good | Excellent | Good | Good | Small models have narrow effective context even when window is large |
| **context budget** | Partial | Good | Good | Excellent | Good | Good | Budget discipline matters most at smaller tiers where tokens are scarce |
| **retrieval scaffolding** | Weak | Partial | Good | Excellent | Good | Excellent | RAG architectures work at all tiers but quality of retrieval utilization scales with model size |
| **memory cueing** | Weak | Partial | Good | Excellent | Excellent | Good | Explicit recall cues compensate for limited in-context memory |
| **source anchoring** | Partial | Good | Good | Excellent | Excellent | Good | Anchoring to specific sources reduces hallucination universally |
| **information routing** | Weak | Partial | Good | Excellent | Good | Good | Multi-source routing requires strong attention and instruction-following |
| **scaffolding** | Good | Good | Good | Excellent | Good | Good | Structural scaffolding (templates, outlines) works at all tiers |
| **signal-to-noise ratio** | Good | Good | Excellent | Excellent | Good | Good | Noisy context degrades all models; small models degrade fastest |
| **salience** | Weak | Partial | Good | Excellent | Excellent | Partial | Identifying what matters requires judgment that scales with capability |
| **progressive disclosure** | Weak | Partial | Good | Excellent | Good | Good | Staged information delivery requires multi-turn management |

---

## Matrix: Agent Workflow Family

These 12 entries define the language patterns for multi-agent systems, delegation, and orchestration.

| Headword | Small Open | Midsize Open | Large Open | Frontier | Reasoning | Code | Notes |
|----------|-----------|-------------|-----------|---------|-----------|------|-------|
| **delegation** | Weak | Partial | Good | Excellent | Good | Good | Clean delegation requires precise instruction-following |
| **handoff** | Weak | Partial | Good | Excellent | Good | Excellent | Structured handoff protocols work well when formalized; code models handle format well |
| **routing** | Weak | Partial | Good | Excellent | Good | Excellent | Routing logic maps naturally to conditional structures; code models excel |
| **planner-executor split** | Weak | Weak | Partial | Excellent | Excellent | Good | This pattern requires meta-reasoning about task structure |
| **verification loop** | Weak | Partial | Good | Excellent | Excellent | Good | Self-verification requires the model to evaluate its own output |
| **watchdog** | Weak | Partial | Good | Excellent | Good | Good | Watchdog patterns require reliable condition monitoring |
| **escalation** | Weak | Partial | Good | Excellent | Good | Good | Escalation requires honest uncertainty assessment; smaller models overconfident |
| **orchestration** | Weak | Weak | Partial | Excellent | Good | Good | Multi-agent orchestration is frontier-tier work for now |
| **pipeline** | Partial | Good | Good | Excellent | Good | Excellent | Sequential pipeline steps work at all tiers if each step is simple |
| **shared state** | Weak | Partial | Good | Excellent | Good | Excellent | State management maps to code patterns; code models strong |
| **tool selection** | Weak | Partial | Good | Excellent | Good | Excellent | Tool selection requires understanding tool capabilities and matching to intent |
| **checkpoint** | Partial | Good | Good | Excellent | Good | Good | Explicit checkpoints help all tiers maintain progress tracking |

---

## Matrix: Quality Control Family

These 8 entries provide the verification, evaluation, and provenance mechanisms.

| Headword | Small Open | Midsize Open | Large Open | Frontier | Reasoning | Code | Notes |
|----------|-----------|-------------|-----------|---------|-----------|------|-------|
| **rubric** | Partial | Good | Good | Excellent | Excellent | Good | Rubric-based evaluation requires consistent criteria application |
| **test harness** | Weak | Partial | Good | Excellent | Good | Excellent | Test harness patterns are native to code models |
| **regression check** | Weak | Partial | Good | Excellent | Good | Excellent | Regression detection requires comparing against a known baseline |
| **audit trail** | Partial | Good | Good | Excellent | Good | Good | Logging and trace maintenance works at all tiers with explicit instructions |
| **provenance tracking** | Weak | Partial | Good | Excellent | Excellent | Good | Source attribution requires reliable recall and citation |
| **falsifiability** | Weak | Partial | Good | Excellent | Excellent | Partial | Testing claims against counter-evidence requires strong reasoning |
| **contradiction detection** | Weak | Partial | Good | Excellent | Excellent | Partial | Detecting contradictions requires holding and comparing multiple statements |
| **feedback loop** | Weak | Partial | Good | Excellent | Good | Good | Iterative refinement based on feedback requires multi-turn coherence |

---

## Matrix: Tone/Style Family

These 8 entries control the voice, register, and rhetorical character of model output.

| Headword | Small Open | Midsize Open | Large Open | Frontier | Reasoning | Code | Notes |
|----------|-----------|-------------|-----------|---------|-----------|------|-------|
| **register** | Partial | Good | Excellent | Excellent | Good | Weak | Register control improves with model size; code models rarely need it |
| **formality** | Partial | Good | Good | Excellent | Good | Weak | Formality levels are well-trained in larger general-purpose models |
| **authority** | Partial | Good | Good | Excellent | Excellent | Weak | Authoritative voice requires confidence calibration |
| **warmth** | Partial | Good | Good | Excellent | Partial | Weak | Warmth and interpersonal tone are poorly supported in reasoning and code models |
| **terseness** | Good | Good | Good | Excellent | Partial | Good | Terseness is achievable at all tiers; reasoning models tend to be verbose |
| **narrative glue** | Weak | Partial | Good | Excellent | Partial | Weak | Smooth narrative transitions require strong language modeling |
| **rhetorical precision** | Weak | Partial | Good | Excellent | Good | Weak | Precise rhetorical choices require broad vocabulary and pragmatic understanding |
| **audience specification** | Partial | Good | Good | Excellent | Good | Partial | Audience-aware output scaling improves with model sophistication |

---

## Matrix: Failure Mode Family

These 7 entries describe what goes wrong and how to recognize it. The matrix here indicates how susceptible each model tier is to the failure mode (reversed scale: Excellent means the model is most resistant to the failure).

| Headword | Small Open | Midsize Open | Large Open | Frontier | Reasoning | Code | Notes |
|----------|-----------|-------------|-----------|---------|-----------|------|-------|
| **vagueness** | Weak | Partial | Good | Good | Good | Partial | Small models default to vague outputs; all tiers benefit from specificity |
| **underspecification** | Weak | Partial | Good | Good | Good | Partial | Frontier models tolerate underspecification better but still underperform |
| **hallucination bait** | Weak | Weak | Partial | Good | Good | Partial | All models susceptible; grounding is the universal fix |
| **overcompression** | Partial | Good | Good | Good | Partial | Partial | Reasoning models sometimes over-elaborate instead; code models may strip context |
| **prompt drift** | Weak | Partial | Good | Good | Partial | Partial | Multi-turn coherence scales with context management; reasoning models can lose thread in extended chains |
| **sycophancy** | Weak | Weak | Partial | Partial | Good | Good | RLHF-trained models are broadly susceptible; reasoning models best resist with explicit critique instructions |
| **tool misfire** | Weak | Partial | Good | Good | Good | Excellent | Code-specialized models have the strongest tool-use training |

---

## Key Patterns Across the Matrix

Several cross-cutting patterns emerge from the full matrix:

1. **The instruction-following threshold.** Most abstractions that require multi-step reasoning, self-evaluation, or meta-cognitive operations (decomposition, planner-executor split, critique, falsifiability) show a sharp capability jump between midsize and large open models. Below that threshold, these abstractions should be decomposed into simpler directives.

2. **Tone/style is general-purpose territory.** Tone and style abstractions (register, warmth, narrative glue) are weakest in code-specialized and reasoning-specialized models, which are trained for correctness rather than rhetorical nuance. If your workflow requires both precise reasoning and appropriate tone, consider a pipeline where a reasoning model produces content and a frontier model polishes tone.

3. **Code models as structure engines.** Code-specialized models outperform on abstractions with formal, structural character: constrain, filter, routing, handoff, test harness, shared state, tool selection. Use them when the abstraction maps naturally to conditional logic, data structures, or function signatures.

4. **Grounding is universal.** Abstractions related to grounding, anchoring, and source management improve output quality at every tier. They are the highest-ROI abstractions for smaller models where other techniques are unreliable.

5. **Sycophancy crosses tiers.** Unlike most failure modes, which are worst in small models, sycophancy affects even frontier models. It requires explicit counter-instructions (→ critique, → falsifiability) regardless of tier.

6. **Reasoning models have blind spots.** Despite their strength in analysis and evaluation, reasoning-specialized models can be verbose, struggle with terseness constraints, and sometimes lose thread in extended multi-turn workflows. Pair them with explicit checkpointing and format constraints.
