---
headword: "clarity"
slug: "clarity"
family: "core_abstraction"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# clarity

**Elevator definition**
Clarity is the structural property of an instruction that ensures every sentence can be interpreted in exactly one way, eliminating ambiguity before the model begins to generate.

## What it is

Ambiguity is not vagueness. Vagueness is saying too little. Ambiguity is saying something that could mean two things. Both are problems, but they are different problems, and they require different solutions. Clarity solves ambiguity.

Consider this instruction: "Summarize the key points and email them to the team lead." Does "them" refer to the key points or the summaries? Should the model write an email or produce a summary? Is the output a summary, an email, or both? A human reader might guess from context. A model will pick the most probable parse and proceed without telling you which one it chose. You will not know it misinterpreted until you read the output — and sometimes not even then, because the wrong interpretation can produce plausible-looking text.

Clarity requires attention to three sources of ambiguity. **Referential ambiguity** is the pronoun problem: when "it," "they," or "this" could refer to more than one antecedent. The fix is simple and always the same — repeat the noun. **Scope ambiguity** is the modifier problem: "Review the financial data from Q3 and Q4 reports" could mean data from Q3 and data from Q4, or it could mean Q4 reports specifically and financial data generally. Restructure: "From the Q3 report and the Q4 report, review the financial data sections." **Instructional ambiguity** is the goal problem: "Improve this code" could mean optimize for speed, improve readability, fix bugs, add error handling, or all of the above. The model cannot ask which you meant. It will choose.

Clarity is distinct from both → precision and → specificity. You can write a precise prompt that is ambiguous: "Evaluate the statistical significance of this result" is precise vocabulary applied to an ambiguous instruction (evaluate how? report the p-value? rerun the test? interpret the implications?). You can write a specific prompt that is ambiguous: "Give me five examples of design patterns used in this codebase, noting which files use them" is specific in count and scope but ambiguous about what counts as "used" (imported? instantiated? referenced?). Clarity is the property that removes double readings. It is orthogonal to both precision and specificity, and you need all three.

## Why it matters in prompting

Most prompt debugging is ambiguity debugging. The user writes an instruction, the model produces something unexpected, and the user concludes the model is "bad at this task." But in a majority of cases, the model did something reasonable — it just interpreted the instruction differently than the user intended. The instruction had two valid readings, and the model picked the other one.

The cost of ambiguity scales with prompt length. A short, ambiguous prompt might produce one wrong turn. A long, complex prompt with multiple ambiguous instructions produces a combinatorial explosion of possible interpretations. If three instructions each have two possible readings, the model is navigating eight possible interpretation paths, and only one is yours. Clarity at each instruction narrows this to one path.

The practical discipline is re-reading every instruction as if you had no context about what you meant. Ask: could a literal-minded, context-free reader interpret this differently? If yes, rewrite. Models are exactly that literal-minded, context-free reader.

## Why it matters in agentic workflows

In a multi-agent pipeline, ambiguity does not just cause one bad output — it causes a cascade. Agent A produces an ambiguous intermediate result. Agent B interprets it one way. Agent C, receiving Agent B's output, has no way to detect that the ambiguity originated two steps earlier. The error is invisible at the point where it matters.

System prompts for agents are instructions that execute hundreds or thousands of times without revision. An ambiguity in a system prompt is not a one-time misinterpretation. It is a systematic bias that warps every interaction the agent processes. Clarity in agent instructions is not a style preference. It is a reliability requirement. Write agent system prompts as if they were function signatures: every parameter named, every behavior specified, every edge case addressed.

## What it changes in model behavior

Unambiguous instructions produce lower-variance outputs across runs. When a prompt has one valid interpretation, the model converges on it consistently. When a prompt has multiple valid interpretations, different sampling runs (or different conversation contexts) may resolve the ambiguity differently, producing inconsistent outputs that look like model instability but are actually prompt instability. Fixing clarity fixes consistency, often more effectively than adjusting temperature or other generation parameters.

## Use it when

- When a previous prompt produced output that was reasonable but not what you intended
- When your instruction contains pronouns that could refer to multiple antecedents
- When you are writing system prompts for agents that will execute repeatedly without human review
- When the prompt includes conditional logic ("if X, do Y") that could be parsed with different scope
- When the task involves multiple steps and the relationship between steps could be misread
- When collaborating with others who will read or modify the prompt

## Do not use it when

- When the ambiguity is intentional and you want the model to explore multiple interpretations
- When the instruction is so simple that no ambiguity exists ("Translate this to French")
- When over-specifying for clarity would make the prompt so verbose that it obscures the task

## Contrast set

- → precision — precision is about the accuracy of individual words; clarity is about the unambiguity of the instruction as a whole. You can use precise words in an ambiguous structure.
- → specificity — specificity is about narrowing scope; clarity is about eliminating double readings. A highly specific prompt can still be ambiguous if its structure allows multiple parses.
- → explicitness — explicitness makes hidden assumptions visible; clarity ensures visible instructions are unambiguous. They solve related but distinct problems.

## Common failure modes

- **Assumed shared context** → Writing prompts that depend on knowledge the model does not have. "Fix the issue we discussed" is clear to the human who had the discussion. To the model, it is an ambiguous instruction with no referent. Clarity requires that every reference resolve within the prompt itself or the provided context.
- **Compound instructions with unclear scope** → "Summarize and critique the methodology in sections 3 and 4." Does "summarize and critique" apply to both sections, or summarize section 3 and critique section 4? Does "methodology" scope to both sections or just the one that contains methodology? Each ambiguity doubles the interpretation space. Decompose compound instructions into sequential, unambiguous steps.

## Prompt examples

### Minimal example

```text
Read the attached customer review.
Identify the single product feature the reviewer is most
dissatisfied with. State the feature name in one phrase.
Then quote the sentence from the review that best supports
your identification.
```

### Strong example

```text
You will receive two documents: a contract (labeled DOC_A) and
an amendment (labeled DOC_B).

Task 1: List every clause in DOC_A that DOC_B explicitly modifies.
For each clause, state:
  - The clause number in DOC_A
  - The specific change made by DOC_B (addition, deletion,
    or replacement)
  - The exact text that was changed (quote from DOC_A) and
    the replacement text (quote from DOC_B)

Task 2: List every clause in DOC_A that DOC_B does NOT modify.
For each, state only the clause number.

Task 3: Identify any new clauses in DOC_B that have no
corresponding clause in DOC_A. State the clause number
from DOC_B and summarize its content in one sentence.

Do not infer modifications. A clause is "modified" only if
DOC_B explicitly references it by number or by quoted text.
If DOC_B uses language similar to DOC_A but does not
explicitly reference the clause, classify it as a new clause
under Task 3, not a modification under Task 1.
```

### Agentic workflow example

```text
Agent: Intake Classifier
Input: Unstructured support ticket text from {queue}

Classification rules (apply in this order, stop at first match):
1. If the ticket mentions "billing," "charge," "invoice," or
   "payment" → route to Billing Agent
2. If the ticket mentions "crash," "error," "bug," or "not
   working" → route to Technical Agent
3. If the ticket mentions "cancel," "close account," or
   "unsubscribe" → route to Retention Agent
4. If none of the above keywords appear → route to General Agent

For each ticket, output:
- ticket_id: the original ID
- matched_rule: the rule number (1-4) that triggered
- matched_keyword: the specific keyword found (or "none" for rule 4)
- routed_to: the agent name

Do not classify based on inferred intent. Classify based on
keyword presence only. If multiple rules match, use the first
match in the order listed above.
```

## Model-fit note

Clarity benefits all model tiers equally because it addresses a structural problem in the prompt, not a capability problem in the model. Frontier models are better at resolving ambiguity through context, but "better" still means they guess — they just guess more plausibly. Smaller models resolve ambiguity toward their most common training patterns, which may be far from your intent. For all tiers, the cheapest way to improve output consistency is to remove ambiguity from the input.

## Evidence and provenance

The Prompt Report identifies clear instruction formulation as a foundational prompt component and notes that ambiguity in task description is a primary source of prompt failure [src_paper_schulhoff2025]. Sahoo et al. (2025) document the effectiveness of structured, unambiguous instruction formatting in zero-shot and few-shot prompting [src_paper_sahoo2025]. The distinction between ambiguity and vagueness draws on standard linguistic pragmatics.

## Related entries

- → precision — precision sharpens word choice; clarity removes structural ambiguity. You need both.
- → specificity — specificity narrows scope; clarity ensures that narrowed scope is unambiguous.
- → decomposition — decomposing compound instructions is often the fastest path to clarity.
