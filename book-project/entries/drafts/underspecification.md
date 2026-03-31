---
headword: "underspecification"
slug: "underspecification"
family: "failure_mode"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# Underspecification

**Elevator definition** Omitting information the model needs but cannot reliably infer, forcing it to fill gaps with assumptions you never approved.

## What it is

Underspecification is the failure of missing pieces. Unlike vagueness, which paints with too broad a brush, underspecification leaves holes in an otherwise clear instruction. The prompt may have a clear goal, a defined format, a specified audience — but it's missing the data, the constraints, the context, or the criteria the model needs to execute faithfully. The model doesn't know it's missing something. It doesn't pause. It fills the gap.

Consider the difference: "Write a summary" is vague — what summary? of what? for whom? By contrast, "Write a 200-word summary of this earnings report for investors" is clear in goal, format, audience, and scope — but it's underspecified if you haven't stated which quarter, whether to compare year-over-year, whether to focus on revenue or profitability, or whether to mention forward guidance. The prompt has shape but not substance in certain dimensions.

Underspecification is particularly insidious because the output often looks correct. The model fills gaps plausibly. It picks a quarter (the most recent one mentioned, probably). It includes both revenue and profitability (hedging). It mentions forward guidance (because earnings reports usually do). The output is fluent, structured, and wrong — because the model's assumptions don't match yours, and you can't tell by reading the output which assumptions it made.

The taxonomy of what can be underspecified is broad:

**Missing input data** — The prompt references information that isn't provided. "Summarize the key findings" when the findings aren't in the context. The model will invent plausible-sounding findings rather than say "I don't see any findings."

**Missing constraints** — The prompt doesn't bound the response. No word count, no format, no explicit limits on what to include or exclude. The model's defaults may not match your expectations.

**Missing criteria** — The prompt asks for a judgment ("Is this a good strategy?") without defining what "good" means. Good for short-term revenue? Long-term market position? Risk minimization? Employee morale? The model picks a frame and you may never notice it chose wrong.

**Missing context** — The prompt assumes background knowledge the model doesn't have about your specific situation. "Update the deployment process" — which deployment process? What's wrong with the current one? What constraints exist?

**Missing examples** — The prompt describes a task but doesn't show what success looks like. For tasks with subjective quality criteria (writing style, analysis depth, classification boundaries), examples are not optional — they are specification.

The danger of underspecification increases with model capability. Weaker models produce visibly incomplete output when information is missing — they stumble, repeat themselves, or produce generic filler. Stronger models produce convincing output that smoothly papers over the gaps. GPT-4 is worse for underspecification than GPT-3.5, not because it's a worse model, but because it's a better confabulator. Its outputs are so polished that missing specification is invisible in the result.

The fix for underspecification is a pre-flight checklist. Before running a prompt, ask: Does the model have everything it needs? Not "everything that might be relevant" — everything it *needs*. What data does it require? What constraints must it respect? What criteria should it apply? What context about my situation must it know? What does a correct output look like? If any of these are absent, the model is flying blind in at least one dimension, and it won't tell you.

## Why it matters in prompting

Prompt engineering is, in large part, the discipline of anticipating what the model doesn't know but needs to. Every prompt is a specification, and every specification can be underspecified. The skill is not in writing longer prompts — it's in identifying which pieces of information, if absent, will cause the model to make assumptions that diverge from your intent.

Experienced prompt engineers develop an instinct for underspecification. They read their own prompts from the model's perspective and ask: "What would I assume if this were all I knew?" Each assumption the model must make is a degree of freedom that may or may not resolve in the user's favor. The goal is to eliminate the assumptions that matter while accepting the ones that don't.

## Why it matters in agentic workflows

In agentic systems, underspecification in a task description or system prompt compounds through the agent chain. If the orchestrator's task description is underspecified, every agent downstream inherits the ambiguity. Worse, each agent may resolve the underspecification differently — Agent A assumes one interpretation, Agent B assumes another, and their outputs are incompatible.

Agentic systems should include **specification validation** at the intake stage. Before an agent begins work, it (or a validation layer) should check whether the task description contains all required fields. Missing fields should trigger a clarification request rather than silent assumption-making. This is the agent equivalent of a form with required fields — the system refuses to proceed until the specification is complete.

## What it changes in model behavior

When specification is complete, the model operates in a constrained space — its output is largely determined by the inputs and instructions. When specification is incomplete, the model operates with hidden degrees of freedom — it makes choices you can't see, can't predict, and can't reproduce. Underspecification converts deterministic behavior into stochastic behavior, even when the model's temperature is zero.

## Use it when

This is a failure mode. You never want underspecification. But recognizing it lets you diagnose problems:

- When the output is plausible but doesn't match what you expected, check for missing constraints
- When different runs produce different outputs from the same prompt, check for missing specification that the model resolves randomly
- When an agent in a pipeline produces output incompatible with the next stage, check for underspecified interface contracts
- When a model makes a surprising assumption, trace it back to the gap in the prompt that forced the assumption
- When stakeholders disagree about whether the output is correct, the prompt is underspecified on the criteria for correctness

## Do not use it when

- The missing information is genuinely irrelevant to the task
- The model can reliably infer the missing information from the context provided (test this — don't assume it)
- You are deliberately leaving room for model judgment in areas where you trust its defaults

## Contrast set

- **Vagueness** — Vagueness is a broad lens: the instruction is too general. Underspecification is a missing piece: the instruction is specific in some dimensions but has gaps in others. A prompt can be specific (clear goal, format, audience) and still underspecified (missing data, constraints, or criteria). Vagueness is diffuse. Underspecification is punctate.
- **Ambiguity** — Ambiguity means the instruction supports multiple interpretations and the model must choose one. Underspecification means information is simply absent. Ambiguity is a fork in the road. Underspecification is a gap in the map.
- **Implicit specification** — Sometimes what appears to be underspecification is actually implicit specification — context that a skilled model can infer from other elements of the prompt. "Write a haiku about autumn" is not underspecified despite omitting "use 5-7-5 syllable structure" because "haiku" implicitly specifies that structure. The line between implicit specification and underspecification depends on what the model can reliably infer.
- **Overspecification** — The opposite failure: so much specification that constraints conflict, the prompt is unwieldy, or the model has no room for necessary flexibility. The craft is in specifying exactly enough.

## Common failure modes

- **The invisible assumption** — The model makes a reasonable but wrong assumption about something the prompt didn't specify, and the output looks correct until you compare it against your actual intent. You asked for a "product comparison" without specifying the comparison criteria, and the model chose criteria that favor the wrong product. Fix: specify comparison dimensions explicitly.
- **Specification drift across turns** — In multi-turn conversations, early specification gets buried as the context grows. The model "forgets" constraints mentioned 10 turns ago because they've been pushed out of effective attention. What was once specified becomes, through context length, effectively underspecified. Fix: re-state critical constraints in later turns.
- **Platform-dependent underspecification** — The same prompt is underspecified on one model and fully specified on another, because models differ in what they can infer. A prompt that works on GPT-4 (which infers your intent from subtle cues) may be underspecified on a smaller model. Fix: test prompts on the actual model you'll deploy to, not the one you prototyped on.

## Prompt examples

Minimal (underspecified — the failure case):

```
Summarize this article.
```

Strong (fully specified):

```
Summarize the following article for a product manager who has not read it.
- Length: 3-4 bullet points, each 1-2 sentences
- Focus: product implications only (ignore methodology, background, and author credentials)
- Include: any quantitative findings with exact numbers
- Exclude: speculation, opinions, and recommendations from the original author
- If the article contains no quantitative findings, state that explicitly.
```

Agentic workflow (specification validation before execution):

```yaml
specification_gate:
  agent: "spec_validator"
  required_fields:
    - goal: "What output is expected?"
    - input_data: "What data is provided or accessible?"
    - constraints:
        - format: "What structure should the output take?"
        - length: "What are the size bounds?"
        - scope: "What should be included/excluded?"
    - audience: "Who will consume this output?"
    - success_criteria: "How will correctness be judged?"
    - examples: "At least one example of desired output (recommended)"

  validation_logic: |
    For each required field, check if the task description provides it.
    Score each field: present / partially present / missing.
    If any critical field (goal, input_data, format) is missing:
      return {status: "underspecified", missing_fields: [...], clarification_questions: [...]}
    If only optional fields are missing:
      return {status: "acceptable", assumptions: [...]}

  on_underspecified:
    action: "request_clarification_from_user"
  on_acceptable:
    action: "proceed_with_stated_assumptions"
    log: "assumptions made: {assumptions}"
```

## Model-fit note

Frontier models are both the best and worst at handling underspecification. Best, because they can sometimes infer missing specification from subtle context cues. Worst, because they fill gaps so smoothly that you don't notice the specification was missing. With smaller models, underspecification produces obviously bad output, which forces you to fix the prompt. With frontier models, it produces subtly wrong output, which you might ship. Test for underspecification explicitly — don't rely on output quality as a proxy.

## Evidence and provenance

Underspecification as a concept originates in requirements engineering (IEEE 830, 1998) and linguistics (Chomsky's notion of underspecified representations). In the LLM context, the prompt sensitivity literature (Debnath et al., 2025; Sclar et al., 2024) demonstrates that minor specification changes produce disproportionate output variance, confirming that models are resolving underspecification stochastically. The concept of "specification debt" — where underspecified prompts work in testing but fail in production — is documented in engineering blogs from Scale AI and Anthropic (2024-2025).

## Related entries

- **vagueness**
- **specificity**
- **constraints**
- **prompt drift**
- **overcompression**
