---
headword: "contradiction_detection"
slug: "contradiction_detection"
family: "quality_control"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# Contradiction Detection

**Elevator definition** Identifying claims within an output that conflict with each other, with source material, or with established facts — the immune system of reliable generation.

## What it is

Contradiction detection is the practice of systematically checking whether a body of text asserts two or more things that cannot simultaneously be true. It operates at three levels: internal contradiction (claim A in paragraph two conflicts with claim B in paragraph five), source contradiction (the output asserts something that contradicts the input documents), and factual contradiction (the output asserts something that conflicts with established, verifiable knowledge).

Language models contradict themselves more often than most users realize. The generation process is locally coherent — each sentence follows plausibly from the one before it — but globally inconsistent. A model can state that revenue grew 12% in one paragraph and that the company faced declining revenue in another, because each statement was generated in a local context where it seemed reasonable. The model doesn't maintain a global truth table. It maintains a sliding window of plausibility.

This is not a minor flaw to be tolerated. In any domain where consistency matters — legal analysis, financial reporting, medical information, technical documentation — a single internal contradiction can invalidate an entire output. Worse, contradictions embedded in confident-sounding prose are easy to miss. Humans reading LLM output often trust the fluency and skip the verification.

Contradiction detection can be implemented in several ways. **Rule-based detection** checks for specific numeric inconsistencies (the same metric reported with different values). **Entailment-based detection** uses NLI (natural language inference) models to check whether pairs of sentences entail, contradict, or are neutral to each other. **LLM-based detection** uses a separate model pass to review the output specifically for contradictions — a red-team reader whose only job is finding conflicts.

The most robust approach combines methods. Rule-based checks catch obvious numeric errors. Entailment models catch logical contradictions. LLM-based review catches subtle tensions that neither rules nor entailment models would flag — cases where two claims are not formally contradictory but cannot both be supported by the same evidence.

Contradiction detection is detective, not preventive. It doesn't stop the model from generating contradictions. It catches them after the fact. For prevention, you need constraints, structured output, and grounding — techniques that reduce the probability of contradiction in the first place. Detection and prevention work best in concert.

## Why it matters in prompting

In single-prompt work, contradiction detection is a self-check instruction: "Before finalizing your response, review it for any claims that conflict with each other or with the source material provided." This simple instruction measurably reduces contradiction rates, especially in long-form outputs where the model has more room to drift.

The effect is strongest when you make the check explicit and structured. "List every factual claim you made. For each pair of claims, check whether they are consistent" is more effective than "check for contradictions," because it forces the model into a systematic review rather than a superficial scan.

For prompts that reference source documents, contradiction detection should also check the output against the source: "Verify that no claim in your output contradicts the provided source material. If you find a contradiction, quote the relevant source passage and your conflicting claim."

## Why it matters in agentic workflows

Multi-agent systems are contradiction factories. Each agent generates output in its own context, with its own prompt, and potentially with its own interpretation of shared inputs. When these outputs are combined — in a composition step, a report, or a final answer — contradictions between agents' outputs are common and dangerous.

A dedicated contradiction-detection agent, placed at composition checkpoints, can compare outputs across agents and flag inconsistencies before they reach the end user. This agent doesn't generate content — it verifies consistency. Its output is a list of conflicts with references to the originating agents and claims, enabling targeted resolution rather than wholesale regeneration.

## What it changes in model behavior

Explicit contradiction-detection instructions cause models to engage in a review pass that they would otherwise skip. This review activates different attention patterns than generation — the model reads its own output as a critic rather than an author, which surfaces inconsistencies that were invisible during the creative flow.

## Use it when

- The output is long enough that global consistency is not guaranteed (generally 500+ words)
- The task involves factual claims, numbers, dates, or logical arguments where contradictions are harmful
- Multiple sources are being synthesized and their claims may conflict
- Multiple agents contribute to a shared output and their outputs may be inconsistent
- The domain has low tolerance for error (legal, medical, financial, technical)

## Do not use it when

- The output is deliberately exploratory or dialectical (presenting multiple perspectives as a feature, not a bug)
- The output is creative fiction where internal tension may be intentional
- The output is too short for meaningful contradiction (a single sentence or classification)

## Contrast set

- **Falsifiability** → Falsifiability makes claims testable; contradiction detection checks whether tested claims conflict. Falsifiability is about individual claims. Contradiction detection is about claim pairs.
- **Checkpoint** → A checkpoint is a verification gate; contradiction detection is one type of verification performed at a checkpoint. Detection is a check. Checkpoint is the gate that uses it.
- **Feedback loop** → A feedback loop improves the system over time; contradiction detection catches errors in the current output. Detection is acute. Feedback is chronic.
- **Constraint** → Constraints prevent certain outputs; contradiction detection flags outputs that violate the implicit constraint of internal consistency.

## Common failure modes

- **Surface-only detection → catching obvious number mismatches but missing semantic contradictions.** The check finds "revenue: $5M" vs. "revenue: $3M" but misses "market is growing rapidly" vs. "customer acquisition costs are increasing unsustainably" — claims that don't formally contradict but cannot coexist as a coherent picture. Fix: use LLM-based detection alongside rule-based checks. The LLM can catch tensions that rules miss.
- **False positive flood → flagging contradictions that aren't.** Two claims that seem contradictory in isolation but are reconciled by context ("costs increased in Q1 but decreased in Q2" is not a contradiction). Fix: require the detector to explain why the claims conflict and evaluate whether context resolves the apparent conflict.
- **Selective detection → checking the output against itself but not against the source material.** Internal consistency is necessary but not sufficient. An output can be perfectly self-consistent while contradicting every source it was supposed to be based on. Fix: always run contradiction detection in both modes — internal consistency and source fidelity.

## Prompt examples

### Minimal example

```
Review the following report for internal contradictions.
List any pairs of claims that cannot both be true.
For each contradiction, quote both claims and explain the conflict.
If no contradictions are found, state "No contradictions detected."

Report: {report_text}
```

### Strong example

```
You are a consistency auditor. Your task is to check a generated
analysis for contradictions at three levels:

1. Internal: Do any claims within the analysis conflict with each other?
2. Source fidelity: Do any claims contradict the source documents provided?
3. Logical coherence: Do the conclusions follow from the stated evidence,
   or do they require assumptions that conflict with other parts of the text?

For each contradiction found, provide:
- Claim A (quoted, with paragraph number)
- Claim B or source passage (quoted, with location)
- Type: internal / source / logical
- Severity: critical (invalidates conclusions) / moderate (misleading) / minor (cosmetic)
- Suggested resolution: which claim should be revised and why

Source documents: {sources}
Analysis to audit: {analysis_text}
```

### Agentic workflow example

```
agent: contradiction_detector
position: runs after composition, before delivery
inputs:
  composed_output: the full text to check
  source_materials: original inputs the output was derived from
  agent_outputs: individual outputs from each contributing agent

detection_protocol:
  pass_1: internal consistency
    - Extract all factual claims as (subject, predicate, object) triples
    - Compare all triples pairwise for logical contradiction
    - Flag any pair with contradiction score > 0.7
  pass_2: source fidelity
    - For each factual claim, find the closest source passage
    - Score entailment vs. contradiction using NLI
    - Flag any claim that contradicts its closest source
  pass_3: cross-agent consistency
    - Compare outputs from different agents for conflicting claims
    - Identify which agent's claim has stronger source support

output:
  contradictions: [{ claim_a, claim_b, type, severity, resolution }]
  verdict: clean | warnings | critical_contradictions
  
routing:
  clean → proceed to delivery
  warnings → proceed with contradictions flagged in metadata
  critical → return to composition agent with contradiction report
```

## Model-fit note

Contradiction detection quality varies significantly by model. GPT-4-class and Claude 3.5+ models detect subtle semantic contradictions reliably. Smaller models catch numeric mismatches but miss logical tensions. For production systems, using a strong model as the contradiction detector — even if smaller models handle other pipeline steps — is a cost-effective quality investment.

## Evidence and provenance

Contradiction detection in NLP has deep roots in natural language inference (Bowman et al., 2015, SNLI dataset) and textual entailment (Dagan et al., 2005). Applied to LLM output verification, it draws on self-consistency checking (Wang et al., 2023) and factual consistency evaluation in summarization (Kryscinski et al., 2020, FactCC). Production implementations appear in guardrail frameworks (Guardrails AI, NeMo Guardrails, 2024).

## Related entries

- → **falsifiability** — Falsifiable claims are easier to check for contradiction because they have testable truth values.
- → **checkpoint** — Contradiction detection is a verification operation typically performed at checkpoints.
- → **audit_trail** — The contradiction report becomes part of the audit trail, documenting what was caught and how it was resolved.
- → **integrate** — Integration is where contradictions between separately-produced pieces are most likely to emerge.
