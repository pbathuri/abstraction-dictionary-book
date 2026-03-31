# How to Read an Entry

Each entry in The Abstraction Dictionary follows a consistent structure. Here is what each section does and how to use it.

## Anatomy of an Entry

### Headword
The name of the abstraction. This is the term you will look up, reference, and use in your own work.

### One-Sentence Elevator Definition
The fastest possible answer to "what is this?" Read this when you need orientation, not depth.

### Expanded Definition
The full concept, explained in two to four paragraphs. This section draws boundaries: what the abstraction includes, what it excludes, and how it differs from ordinary usage of the same word.

### Why This Matters for LLM Prompting
The operational case for using this abstraction when constructing prompts. If you are a prompt engineer, this is your "why should I care" section.

### Why This Matters for Agentic Workflows
The same, but for multi-agent systems, delegation chains, and orchestrated tool use. If you build or manage agent workflows, start here.

### What It Does to Model Behavior
A brief, evidence-informed explanation of the measurable effect. Not speculation. Not vibes. What actually changes in the output when you deploy this abstraction.

### When to Use It
A checklist of situations where this abstraction is the right choice.

### When NOT to Use It
Equally important: situations where this abstraction will hurt more than it helps.

### Contrast Set
A table comparing this abstraction with its nearest neighbors. This is where you figure out whether you want *specificity* or *constraint*, *decomposition* or *hierarchy*, *delegation* or *handoff*.

### Failure Modes
Concrete ways this abstraction goes wrong when misapplied. Each failure mode includes a brief explanation of why it fails.

### Examples
Three levels:
- **Minimal** — the simplest correct use
- **Strong** — expert use, often combining multiple abstractions
- **Agent workflow** — how this abstraction appears in multi-step, multi-agent contexts

### Model-Fit Note
Which model tiers benefit most. This section uses evidence-based tier classifications, not invented specifications.

### Evidence / Provenance Note
Where the claims in this entry come from. Points to the entry's source file for full citation details.

### Related Entries
Where to go next. Each related entry includes a one-line description of why it is relevant.

### Note Box (when present)
Not every entry has one. When present, it contains a sharp, focused observation in one of six types: *Which Word?*, *Workflow Note*, *Model Note*, *Common Trap*, *Upgrade This Prompt*, or *Fun Aside*.

## Reading Strategies

**Five-second scan:** Headword + elevator definition.

**Two-minute read:** Add expanded definition + when to use + when not to.

**Full study:** Read the complete entry, follow two or three cross-references, and try the strong example in your own workflow.
