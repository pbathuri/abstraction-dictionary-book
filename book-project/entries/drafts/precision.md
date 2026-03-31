---
headword: "precision"
slug: "precision"
family: "core_abstraction"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# precision

**Elevator definition**
Precision is the exactness of word choice in a prompt — selecting language that means what you intend, activating the right model behavior, and leaving no room for semantic drift.

## What it is

Precision operates at the level of individual words and phrases. It is not about how much you say — that is → specificity. It is not about whether your instruction can be misread — that is → clarity. Precision is about whether the words you chose are the *right* words. The difference between "analyze," "evaluate," "assess," and "review" is not stylistic. Each verb primes the model toward a different output pattern. "Analyze" triggers decomposition into components. "Evaluate" triggers judgment against criteria. "Assess" implies measurement. "Review" implies looking for problems. A prompt engineer who treats these as synonyms is writing code with the wrong opcodes.

Schreiter (2024) tested this directly. Across four language models and three domains — STEM, medicine, and law — word-level vocabulary substitutions produced statistically significant changes in model performance. Not paragraph-level changes. Not instruction-level restructuring. Single-word swaps [src_paper_schreiter2024]. The study tested verbs, nouns, and adjectives independently and found that each part of speech contributes differently to output quality. Verbs had the largest effect on reasoning tasks. Nouns mattered most for domain-specific content. Adjectives influenced the granularity and tone of responses. The finding is both intuitive and underappreciated: models are language machines, and the language you feed them is the program they run.

Precision has a second dimension that goes beyond vocabulary: quantitative exactness. "A few examples" is imprecise. "Three examples" is precise. "A short summary" is imprecise. "A summary under 80 words" is precise. Every time you use an approximate qualifier — "some," "various," "brief," "detailed" — you are ceding a decision to the model's default interpretation. Sometimes that is fine. Often it is the source of the gap between what you wanted and what you got.

The operational test for precision is substitution: could someone replace any word in your prompt with a near-synonym and get a different result? If yes, you have made a precise choice. If a synonym would work equally well, the word is not carrying information — it is filler.

## Why it matters in prompting

Precision is the smallest lever in prompt engineering and one of the most powerful per-character. A single verb change at the start of an instruction can redirect an entire response. Tell a model to "list" and it produces bullets. Tell it to "compare" and it produces analysis. Tell it to "critique" and it produces objections. The instruction is the same length. The output is fundamentally different.

Schreiter's research revealed something practitioners already suspected: there is an optimal vocabulary range for each task type, and that range varies by model [src_paper_schreiter2024]. For reasoning tasks, pushing verb precision beyond the optimal range actually degraded performance — the model spent capacity interpreting the instruction instead of executing it. This means precision is not a monotonic improvement. It has a sweet spot. The goal is not to use the most exotic verb possible. It is to use the verb that most accurately describes the cognitive operation you want the model to perform.

In practice, building a personal vocabulary of tested verbs pays compound returns. Know which verbs your target model responds to. Know the difference between "enumerate" and "list," between "synthesize" and "summarize," between "infer" and "deduce." These are not synonyms to a language model. They are different instructions.

## Why it matters in agentic workflows

Agent instructions execute without a human in the loop to catch misinterpretation. A planner agent that tells an executor to "handle the data" has given an imprecise instruction that could mean clean, transform, validate, analyze, or store the data. The executor will pick one interpretation — probably the most statistically likely one given its training — and proceed. If it picks wrong, the error cascades downstream through every subsequent agent.

Precision in agent delegation means using verbs that map unambiguously to actions: "extract," "validate," "transform," "classify." It means specifying quantities, formats, and thresholds with numbers rather than qualifiers. It means naming the output schema rather than describing it loosely. In a pipeline with five agents, imprecision at step one does not produce a 20% error. It produces a compounding error, because each downstream agent interprets the slightly-off output through its own slightly-off lens.

## What it changes in model behavior

Precise vocabulary focuses model attention on narrower, more relevant regions of its parameter space. When you write "enumerate the causal factors," the model activates patterns associated with causation and listing simultaneously, producing a structured causal analysis. When you write "describe what happened," it activates narrative patterns. The underlying knowledge may overlap, but the retrieval pathway differs. Schreiter's findings confirm this empirically: the same factual question, rephrased with different verb precision levels, produces accuracy swings of 5-15% depending on the model and domain [src_paper_schreiter2024].

## Use it when

- When you have tried a prompt and the output is close but subtly wrong in character or emphasis
- When you are writing agent delegation instructions that will execute without human oversight
- When the task requires a specific cognitive operation (analysis, comparison, synthesis, evaluation)
- When quantitative accuracy matters and approximate language could cause drift
- When working with smaller models that are more sensitive to vocabulary cues
- When you are defining tool descriptions or function signatures that agents will use for routing

## Do not use it when

- When you are brainstorming and want the model to interpret freely
- When the task is simple enough that any reasonable verb would produce the same output
- When optimizing for precision would make the prompt harder to read for human collaborators
- When you lack the domain vocabulary to choose precise terms confidently (imprecise-but-honest beats precise-but-wrong)

## Contrast set

- → specificity — specificity narrows the scope of what the model addresses; precision sharpens the accuracy of how you describe it. You can be specific but imprecise ("give me roughly five examples of bad code") or precise but unspecific ("write well").
- → clarity — clarity ensures the instruction cannot be misread; precision ensures the words themselves are accurate. A prompt can be clear (unambiguous) but imprecise ("do something useful with this data" is clear in intent, imprecise in instruction).
- → explicitness — explicitness makes hidden assumptions visible; precision makes visible language accurate. They often improve together but address different failure modes.

## Common failure modes

- **Thesaurus syndrome** → Using rare or technical vocabulary to sound precise when the model associates those terms with less common (and less reliable) generation patterns. Precision means choosing the *right* word, not the fanciest word. "Elucidate" is not more precise than "explain" — it is just rarer, and the model has seen fewer high-quality examples of its usage.
- **Qualifier fog** → Packing a prompt with approximate language — "fairly detailed," "somewhat technical," "relatively brief" — that the model cannot calibrate. Each qualifier offloads a decision to the model's default. Stack enough of them and the model is making all the decisions while you think you are making them.

## Prompt examples

### Minimal example

```text
Compare the error-handling approaches in these two code snippets.
For each approach, name the pattern used, state one strength,
and state one weakness. Do not recommend one over the other.
```

### Strong example

```text
You are a clinical trial statistician reviewing a study protocol.

For the attached protocol:
1. Identify the primary endpoint. State it in one sentence.
2. Classify the statistical test proposed as: parametric,
   non-parametric, or Bayesian.
3. Evaluate whether the sample size calculation matches the
   proposed test. If it does not, state the specific mismatch.
4. Flag any p-value thresholds that deviate from the
   pre-registration.

Use precise statistical terminology. Do not simplify for
a lay audience. If a choice in the protocol is ambiguous
between two valid interpretations, state both and note
which you are assuming.
```

### Agentic workflow example

```text
Agent: Data Validation Agent
Input: JSON array of customer records from {source_api}
Task: Validate each record against the schema in {schema_url}

For each record:
- Classify as VALID, INVALID, or PARTIAL
- For INVALID records: identify the specific field that fails
  validation and the rule it violates (type mismatch, range
  violation, missing required field, format error)
- For PARTIAL records: list fields present and fields missing

Do not infer missing values. Do not attempt corrections.
Flag and pass through.

Output: JSON array with original record plus a "validation"
object containing status, failed_fields, and failure_reasons.

Hand off VALID records to the Enrichment Agent.
Hand off INVALID and PARTIAL records to the Review Queue.
```

## Model-fit note

Precision sensitivity varies by model tier. Frontier models tolerate imprecise vocabulary better because they maintain broader activation patterns — they can infer your intent from context even with loose wording. Smaller open models are more literal: the verb you choose is closer to the verb they execute. Reasoning-specialized models respond strongly to precise cognitive verbs ("deduce," "infer," "derive") because these map to their trained reasoning patterns. For all tiers, quantitative precision (numbers over qualifiers) helps uniformly.

## Evidence and provenance

The central claim — that word-level vocabulary choices measurably affect LLM performance — comes directly from Schreiter (2024), who tested verb, noun, and adjective substitutions across Llama-3.1-70B, Granite-13B, Flan-T5-XL, and Mistral-Large 2 on MMLU, GPQA, and GSM8K benchmarks in STEM, medicine, and law domains [src_paper_schreiter2024]. The existence of an optimal precision range, and the finding that over-precise verbs can degrade reasoning performance, are also from this study.

## Related entries

- → specificity — precision is the accuracy of wording; specificity is the narrowness of scope. Frequently confused, fundamentally different.
- → clarity — precision ensures the right words; clarity ensures those words cannot be misread. Both are necessary; neither is sufficient alone.
- → register — precision in tonal vocabulary determines whether the model writes for experts or novices, formally or casually.
