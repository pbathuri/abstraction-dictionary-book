---
headword: "justify"
slug: "justify"
family: "instructional_action"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["critique", "evaluate", "elaborate", "falsifiability", "verification loop", "constrain"]
cross_links: ["critique", "evaluate", "elaborate", "falsifiability", "verification loop", "constrain", "framing", "rank", "rubric", "hallucination bait", "specificity"]
tags: ["instructional-action", "argumentation", "reasoning", "evidence-linking", "verification"]
has_note_box: true
note_box_type: "model_note"
---

# justify

**Elevator definition**
To justify is to provide reasons, evidence, or logical grounds for a claim, decision, or recommendation, forcing the model to connect its conclusions to the premises that support them.

## What it is

A language model can make claims all day. It is trained on billions of sentences that assert things, and it can reproduce that pattern effortlessly: "Option A is the best choice." "This approach is more efficient." "The evidence suggests X." These sentences arrive with the tone of authority. They lack the substance of it. They are conclusions without visible foundations, and conclusions without foundations are just opinions that happen to sound confident.

Justification is the instruction that demands the foundation be made visible. When you ask a model to justify, you are asking it to do something it does not naturally do: show its work. Not the chain-of-thought scratchpad (that is a reasoning technique), but the *evidential and logical structure* that connects a conclusion to the reasons that support it. "Option A is the best choice *because* it reduces latency by 40% based on our benchmark data, requires no migration of existing infrastructure, and aligns with the team's existing expertise in language X." The claim is the same. The justification transforms it from an assertion into an argument.

The intellectual operation has a simple structure: premise, therefore conclusion. But the simplicity is deceptive. Good justification requires the model to identify *which* premises are relevant (not all facts matter equally), *how* they connect to the conclusion (the inferential link), and *how strong* that connection is (certainty vs. probability vs. possibility). A model that merely lists facts related to the conclusion has not justified — it has associated. Justification requires the inferential step: these premises *entail* or *support* this conclusion, and here is why.

This is why justification is so closely related to → falsifiability. A justification that cannot be challenged is not a justification — it is a tautology. "Option A is best because it is the best option" is a circle, not an argument. "Option A is best because it scored highest on the three criteria we defined: cost, latency, and compatibility" is falsifiable — you can check the scores, challenge the criteria, or question the measurements. Justification invites scrutiny. That is its purpose.

The prompting literature reveals that justification is embedded in many high-performing techniques without being named. Chain-of-thought prompting is, at its core, a justification technique: it asks the model to show the reasoning that leads to the answer, making each inferential step visible [src_paper_sahoo2025]. Self-consistency generates multiple justificatory chains and selects the one that appears most often. Self-Refine asks the model to justify *why* its initial output is weak before revising it. The pattern is consistent: techniques that force justification improve output quality, because they force the model to construct reasoning rather than retrieve conclusions.

## Why it matters in prompting

Justification is the single most effective instruction for improving the trustworthiness of model output. A claim without justification requires you to trust the model. A claim with justification allows you to evaluate the reasoning and decide for yourself. This is the difference between "the model said so" and "the model argued, and I can check the argument."

For prompt authors, the instruction "justify" serves a diagnostic function: it reveals whether the model actually has supporting evidence or is confabulating. A model asked to "recommend a database" will recommend one with confidence. A model asked to "recommend a database and justify your recommendation with specific technical evidence" will either produce a well-reasoned argument (in which case the recommendation is credible) or produce vague generalities and hand-waving (in which case the recommendation is not). The justification makes the model's epistemic state legible.

The instruction is particularly valuable in decision-support contexts. When a model produces a recommendation for a human decision-maker, the recommendation is only useful if the decision-maker can understand *why* and evaluate whether those reasons apply to their specific situation. A recommendation without justification is a black box. A recommendation with justification is a transparent argument that the decision-maker can accept, adjust, or reject based on the quality of the reasoning.

## Why it matters in agentic workflows

In multi-agent pipelines, justification is the audit trail. When Agent B acts on Agent A's output, and the pipeline eventually produces a final result, the question "why did the pipeline conclude X?" must be answerable. If Agent A's outputs include justifications, the audit trail is built into the pipeline's intermediate artifacts. If they do not, the pipeline is a black box at every stage.

Justification also serves as a handoff mechanism between agents. When a Research Agent passes findings to a Decision Agent, the findings alone are insufficient — the Decision Agent needs to know *why* each finding matters and *how strongly* the evidence supports it. Justification provides that meta-information. A finding with justification ("Market share declined 12% because competitor Y launched product Z at 30% lower price point, as documented in [source]") is actionable. A finding without justification ("Market share declined") is a data point that the Decision Agent must re-research before acting on.

The connection to → verification loop is structural. A verification step that checks a claim's justification — does this reason actually support this conclusion? does this evidence actually say what it is claimed to say? — is more powerful than one that checks only the claim itself. Justification makes verification possible at the reasoning level, not just the assertion level.

## What it changes in model behavior

The instruction "justify" activates the model's argumentative reasoning mode. The output shifts from assertive to evidential: more citations or references to source material, more causal language ("because," "therefore," "given that," "as evidenced by"), more explicit premise-conclusion structures, and fewer unsupported generalizations. The model produces longer outputs, but the additional length carries inferential content rather than padding.

Critically, justification also changes what the model *avoids*. A model asked to "recommend" may offer a recommendation it cannot defend. A model asked to "recommend and justify" is less likely to recommend something it lacks evidence for, because the justification requirement creates a self-screening effect — the model checks whether it can support the claim before making it. This is not infallible (the model can fabricate justifications), but it shifts the distribution toward better-supported claims.

## Use it when

- The model has produced a conclusion, recommendation, or judgment and you need to see the reasoning behind it
- The output will be reviewed by a decision-maker who needs to evaluate the reasoning, not just the conclusion
- You are building a pipeline and need audit trails at each stage
- You want to test whether the model's claim is well-founded or confabulated
- A downstream → verification loop will check the justification for soundness
- The claim is one that could reasonably be challenged and needs to withstand scrutiny

## Do not use it when

- The task is purely creative and justification would constrain divergent generation
- The conclusion is a factual lookup, not a judgment — "What is the capital of France?" does not need justification
- You are in an exploratory phase and premature justification would narrow the solution space
- The model has already provided reasoning (e.g., through chain-of-thought) and additional justification would be redundant
- You need the model to argue for a position it does not hold — that is → framing (e.g., "argue the bull case"), not justify

## Contrast set

**Closest adjacent abstractions**

- → critique — Critique tears down an argument by finding its weaknesses. Justification builds up an argument by providing its foundations. They are adversarial complements: critique asks "why is this wrong?", justification asks "why is this right?"
- → elaborate — Elaboration adds depth in any direction: examples, context, nuance, implications. Justification adds depth specifically through *reasons and evidence*. All justification is a form of elaboration. Not all elaboration is justification.
- → evaluate — Evaluation assesses quality. Justification supports a specific claim. You evaluate *before* deciding what to claim. You justify *after*.

**Stronger / weaker / narrower / broader relatives**

- → falsifiability — A prerequisite. Justification must be falsifiable — the reasons must be checkable, or the justification is decorative.
- → verification loop — The mechanism that checks justifications for soundness in a pipeline.
- → chain-of-thought — A narrower technique that elicits step-by-step justification of a reasoning process.
- → constrain — Requiring justification is itself a constraint: it eliminates unsupported claims from the output.

## Common failure modes

- **Circular justification** → "Option A is recommended because it is the best option." The justification restates the conclusion in different words without providing independent support. Fix: require the model to cite *specific evidence or criteria* in its justification. "Justify by citing at least two specific data points from the provided material."

- **Post-hoc rationalization** → The model generates a conclusion first, then constructs a plausible-sounding justification that was not actually the basis for the conclusion. The justification is coherent but fictional — the reasoning was reconstructed, not reported. Fix: this is inherent to how LLMs generate text (conclusion and justification are both sampled sequentially). Mitigate by checking the justification against source material rather than trusting it at face value.

- **Justification inflation** → Asked to justify, the model produces a paragraph of reasons for a claim that needs only a sentence. The justification becomes performance — a display of reasoning that adds volume without adding confidence. Fix: constrain the justification — "justify in one sentence citing the key evidence" — to force the model to identify the *strongest* reason rather than listing every tangentially relevant one.

- **Fabricated evidence** → The model invents statistics, citations, or data points to support its justification. This is → hallucination bait under argumentative pressure — the instruction to justify creates demand for evidence, and if real evidence is not available, the model fabricates it. Fix: require justifications to cite only provided source material. "Justify using only data from the attached document. If the document does not contain sufficient evidence, say so."

## Prompt examples

### Minimal example

```text
You recommended migrating from REST to GraphQL.

Justify this recommendation. Cite at least two specific
technical advantages that apply to our use case (high-frequency
mobile clients with variable data needs), and one specific
risk that you believe is manageable.
```

### Strong example

```text
You have been asked to recommend one of three architectural
approaches for our new notification system.

For the approach you recommend:
1. Justify the recommendation by citing at least three specific
   technical advantages over the alternatives. Each advantage
   must reference a concrete characteristic of our system
   (from the architecture doc attached), not a generic property
   of the approach.
2. Acknowledge the strongest argument AGAINST your recommendation.
   Do not dismiss it — explain why you believe it is outweighed
   by the advantages.
3. State what evidence would change your recommendation. What
   would you need to see to switch to one of the alternatives?

For the approaches you did not recommend:
4. In one sentence each, state the primary reason you did not
   recommend them.

This justification will be reviewed by the principal engineer
and the VP of Infrastructure. It must be technically precise
and honest about trade-offs. Do not oversell.
```

### Agentic workflow example

```text
Agent: Justification Agent
Pipeline position: After Decision Agent, before Audit Agent

Input: decision_record from Decision Agent containing
{ decision_id, chosen_option, rejected_options[],
  criteria_scores, source_materials }

Task: Produce a justification document for the decision
that would satisfy a skeptical reviewer.

Justification protocol:
1. For the chosen option: provide 3 evidence-linked reasons
   supporting the selection. Each reason must:
   - State the claim
   - Cite the specific evidence from source_materials
   - Explain the inferential link (why this evidence
     supports this claim)
   - Rate the strength of the link: STRONG (direct evidence),
     MODERATE (inferential), or WEAK (suggestive only)

2. For each rejected option: state why it was not selected,
   citing the specific criterion or criteria where it fell
   short.

3. Falsifiability section: state 2-3 conditions under which
   this decision should be revisited. What future evidence
   or changed circumstances would invalidate the justification?

4. Confidence assessment: given the strength of the available
   evidence, rate overall confidence in the decision as
   HIGH / MEDIUM / LOW with a one-sentence explanation.

Output format:
{
  "decision_id": "",
  "justification": {
    "supporting_reasons": [...],
    "rejected_option_rationales": [...],
    "falsifiability_conditions": [...],
    "confidence": { "level": "", "explanation": "" }
  }
}

Constraint: Every claim must trace to source_materials. If
the source materials are insufficient to justify the decision,
flag as INSUFFICIENT_EVIDENCE and escalate to human review
rather than fabricating support.

Handoff: Pass to Audit Agent for verification of evidence links.
```

## Model-fit note

Justification quality varies significantly by model tier. Frontier models produce well-structured justifications with genuine evidential links, and they are more likely to refuse to justify claims they cannot support (responding with "insufficient evidence" rather than fabricating). Midsize open models produce competent justifications but are more susceptible to post-hoc rationalization — the justification sounds reasonable but may not reflect the actual basis for the claim. Small open models produce justifications that are often circular, generic, or fabricated; they treat "justify" as "write more words about this topic" rather than "connect this conclusion to specific evidence." For high-stakes justification tasks, use the largest available model and require citations to provided source material.

## Evidence and provenance

Chain-of-thought prompting as a justification technique is documented in Wei et al. (2022) and reviewed extensively in Sahoo et al. (2025) [src_paper_sahoo2025]. The self-screening effect — where the requirement to justify reduces the frequency of unsupported claims — is observed in the Self-Refine literature (Madaan et al., 2023) [src_paper_sahoo2025]. The Prompt Report identifies reasoning chain generation as a core prompting capability and documents its relationship to output quality [src_paper_schulhoff2025]. The connection between justification and falsifiability draws from Popper's philosophy of science as applied to LLM output verification. Post-hoc rationalization as a failure mode of LLM justification is discussed in the evaluation and alignment literature.

## Related entries

- **→ critique** — the adversarial complement: critique attacks, justify defends
- **→ evaluate** — produces a judgment that justification then supports
- **→ elaborate** — the broader category: justification is elaboration through argumentation
- **→ falsifiability** — justification must be falsifiable or it is decorative
- **→ verification loop** — checks the soundness of justifications in a pipeline
- **→ hallucination bait** — justification demand under thin knowledge triggers fabrication

---

> **Model Note**
>
> Watch for the fabrication trap. When you ask a model to justify a claim, you create demand for evidence. If the model does not have real evidence, it will manufacture convincing-sounding evidence — invented statistics, plausible but nonexistent citations, made-up benchmark results. This is not malice; it is pattern completion under pressure. The stronger the justification instruction ("provide strong evidence"), the stronger the incentive to fabricate if real evidence is thin. Always pair "justify" with a grounding constraint: "cite only the attached sources" or "if you lack evidence, say so explicitly." A model that says "I cannot fully justify this" is more trustworthy than one that invents a reason.
