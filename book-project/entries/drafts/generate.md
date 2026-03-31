---
headword: "generate"
slug: "generate"
family: "instructional_action"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
---

# Generate

**Elevator definition** Creating new content from specifications — the most open-ended instructional action, and the one most in need of guardrails.

## What it is

Generation is the act of producing something that didn't exist before. It's the verb at the core of what language models do: given a prompt, generate text. But as a prompt engineering concept, "generate" is more specific than that. It's the instructional action you choose when you want the model to create new content from a set of specifications, without requiring it to assemble from provided materials (that's compose) or merge existing pieces (that's integrate).

Generation is the most open-ended operation in the instructional-action family. When you say "generate," you're giving the model the widest latitude. You're saying: here are the parameters, now create. This latitude is simultaneously generation's power and its danger. Power because the model can draw on its full training distribution to produce surprising, creative, high-quality output. Danger because without sufficient specification, the model draws on the wrong parts of that distribution and produces generic, irrelevant, or hallucinated content.

The key to effective generation is the specification — the set of constraints, requirements, and guidelines that bound the creative space without choking it. Too few specifications and you get the model's default: an average of everything it's seen. Too many and you get robotic output that satisfies every requirement and inspires no one.

Generation comes in several modes. **Divergent generation** asks the model to produce many diverse options: "Generate ten possible headlines for this article." **Convergent generation** asks for a single, optimized output: "Generate the best headline for this article given these criteria." **Conditional generation** provides some elements and asks the model to produce the rest: "Given this opening paragraph, generate the next three paragraphs." **Constrained generation** specifies what the output must include or exclude: "Generate a product description that mentions sustainability, avoids superlatives, and is under 50 words."

Each mode has different prompt requirements. Divergent generation needs instructions about diversity ("make each option stylistically distinct"). Convergent generation needs clear optimization criteria ("optimize for click-through rate among developers"). Conditional generation needs the seed content and continuation instructions. Constrained generation needs the constraints stated explicitly.

The relationship between generation and hallucination is direct. Generation is the operation where hallucination risk is highest because the model is creating rather than extracting, analyzing, or transforming. Any factual claim in generated text is a potential hallucination unless it's grounded in provided context or verifiable knowledge. This means generation prompts in factual domains should always include grounding instructions: what sources to draw from, what claims need citation, and what to do when the model isn't sure.

## Why it matters in prompting

"Generate" is the default assumption of most prompts. When someone types "Write me an email about..." they're asking for generation. Because it's the default, it's the operation that suffers most from under-specification. People assume the model knows what they want because generation feels like the model's natural mode. It is — and that's exactly why you need to specify more, not less.

The strongest generation prompts work by specifying the output space precisely. Not the output itself — that's the model's job — but the space it should explore: the topic, the audience, the tone, the format, the length, the constraints, the success criteria. Each specification closes off a region of bad output space while leaving the region of good output space open for the model to explore.

## Why it matters in agentic workflows

In agent pipelines, generation steps are where new content enters the system. Everything upstream — retrieval, analysis, planning — is preparation for the generation step where something is actually produced. This makes generation the highest-stakes step in many pipelines: if the generation is wrong, all the upstream preparation is wasted.

Agent systems that depend on generation benefit from separating the specification step from the execution step. One agent prepares the generation specification (audience, requirements, constraints, materials). Another agent executes the generation. A third agent evaluates the result. This separation ensures that the generation prompt is itself a deliberate artifact rather than an implicit hand-wave.

## What it changes in model behavior

The verb "generate" activates a broadly creative mode where the model draws on patterns across its entire training distribution. Compared to more specific verbs (analyze, filter, contrast), "generate" produces output with higher variance, more creative flourishes, and weaker grounding. Pairing "generate" with explicit constraints narrows the variance while preserving the creative range.

## Use it when

- You need new content that doesn't exist yet — text, ideas, options, solutions
- The task requires creativity, originality, or exploration of a design space
- You have a clear specification for what the output should be but not a template to fill
- You want multiple options to choose from (divergent generation)
- The model's training data is likely to contain relevant patterns for this type of content

## Do not use it when

- The content already exists and needs to be extracted, summarized, or transformed (use the appropriate extraction or transformation verb)
- You have specific materials that should be assembled into the output (use `compose`)
- The task is primarily evaluative or analytical rather than creative (use `analyze` or `evaluate`)
- Factual accuracy is paramount and the model has no provided source material to draw from (generation without grounding is hallucination with a smile)

## Contrast set

- **Compose** → Composition builds from provided materials; generation creates from specifications. Compose starts with ingredients. Generate starts with requirements.
- **Synthesize** → Synthesis combines existing ideas into a new understanding; generation creates new content. Synthesis is integrative. Generation is productive.
- **Transform** → Transformation changes the form of existing content (summarize, translate, reformat); generation creates content that didn't exist. Transform has an input artifact. Generate has an input specification.
- **Brainstorm** → Brainstorming is a mode of divergent generation with looser quality constraints. Brainstorm values quantity and diversity. Generate values quality and specification-compliance.

## Common failure modes

- **Specification vacuum → "generate a blog post" with no further guidance.** The model produces a generic, personality-free post on an assumed topic with assumed structure. It hits the center of the training distribution, which is the center of mediocrity. Fix: specify audience, topic, angle, tone, length, structure, and what makes this post different from every other post on the topic.
- **Over-constrained generation → so many requirements that the model produces stilted, mechanical output.** You wanted creative copy but provided fifteen hard constraints and a rigid template. The model dutifully fills every box and produces something that technically satisfies every requirement but reads like a compliance document. Fix: distinguish between hard constraints (must satisfy) and soft preferences (optimize for). Give the model room to be good, not just compliant.
- **Hallucination in factual generation → the model generates plausible but incorrect facts.** You asked it to generate a market analysis without providing market data. The model obliged, inventing statistics and citing imaginary reports. Fix: if generation must include facts, provide the facts as input. If you can't provide facts, instruct the model to mark uncertain claims and avoid fabricating specifics.

## Prompt examples

### Minimal example

```
Generate 5 tagline options for a productivity app aimed at freelancers.
Each tagline: under 8 words, active voice, emphasizes time savings.
Make each stylistically distinct — one playful, one authoritative,
one minimal, one question-based, one using a metaphor.
```

### Strong example

```
Generate a technical blog post introduction (150-200 words).

Specification:
- Topic: why database migrations should be backward-compatible
- Audience: mid-level backend engineers who've been burned by bad migrations
- Angle: practical consequences, not theoretical best practices
- Opening: start with a concrete scenario (a deploy that went wrong)
- Tone: experienced practitioner sharing hard-won lessons — direct,
  slightly wry, zero corporate polish
- Must include: one specific technical detail that shows domain knowledge
- Must avoid: generic advice ("always test your migrations"), fear-mongering,
  and any sentence that could appear in a different blog post unchanged
- Success criteria: a reader should think "this person has actually done this"
  within the first two sentences
```

### Agentic workflow example

```
pipeline: content_creation
stages:
  - spec_builder:
      task: convert editorial brief into generation specification
      input: editorial brief (topic, audience, goals)
      output:
        audience_profile: { role, knowledge_level, pain_points }
        content_spec: { angle, structure, tone_markers, length, exclusions }
        quality_criteria: { must_include, must_avoid, success_definition }

  - generator:
      task: generate draft from specification
      input: spec_builder output
      constraints:
        - every claim must be supportable (mark [NEEDS SOURCE] if not)
        - follow structure from content_spec exactly
        - match tone_markers within 2 Flesch-Kincaid grade levels of target
      output: draft with inline annotations

  - evaluator:
      task: score draft against quality_criteria
      scoring:
        specification_compliance: 0-10 (does it match the spec?)
        originality: 0-10 (could this have been written by anyone, or does it have a point of view?)
        engagement: 0-10 (would the target audience read past paragraph two?)
      threshold: minimum 7 on all dimensions
      on_fail: return to generator with specific feedback (max 2 iterations)
```

## Model-fit note

Generation quality scales steeply with model size. Large models (GPT-4-class, Claude 3.5+) produce generation that is creative, specification-compliant, and stylistically aware in a single pass. Mid-range models produce adequate first drafts that benefit from inner-loop revision. Small models produce generic output that requires heavy specification and multiple iterations. For creative generation tasks, the model choice matters more than in any other operation.

## Evidence and provenance

Text generation is the foundational capability of language models, studied since the earliest statistical language models (Shannon, 1951) through neural language models (Bengio et al., 2003) to modern transformers (Vaswani et al., 2017). The importance of generation specification in prompting is documented in the InstructGPT work (Ouyang et al., 2022) and in systematic studies of prompt specificity effects on generation quality (Mishra et al., 2022).

## Related entries

- → **compose** — When you have materials and need them assembled, compose. When you have specifications and need new content, generate.
- → **explicitness** — Generation quality is directly proportional to specification explicitness.
- → **filter** — Generation often benefits from a subsequent filter step that selects the best output from multiple candidates.
- → **falsifiability** — Factual claims in generated text should be falsifiable; unfalsifiable generated claims are likely hallucinations.
