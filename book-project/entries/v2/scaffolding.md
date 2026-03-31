# scaffolding

> Temporary structure — templates, outlines, partial examples — that guides the model's output without dictating its content.

## The Scene

Karpathy's `autoresearch` project taught me what scaffolding actually means. The entry point is `program.md` — not code, but a structured outline: phases, sub-tasks, output formats, completion gates. The LLM reads the scaffold and fills it in. Each phase has an input, an output, and a pass/fail check. The model doesn't invent the research process. It executes a recipe that's been scaffolded into steps it can handle.

I stole the pattern for Form8. My market-research prompt had been a monolith: "Research this market and write a strategy brief." The output was a smoothie of half-baked analysis. When I scaffolded it — a template with four sections, each with a header, a one-sentence description, and an output schema — the model stopped guessing at structure and spent its capacity on content. Same model. Same data. The scaffold did the organizing so the model could do the thinking.

## What This Actually Is

Scaffolding separates structure from substance. You provide the format — headers, templates, partially-filled JSON, example rows in a table — and the model fills it in. This eliminates an entire category of decision-making (what structure to use) and lets the model spend its compute on content.

Four forms: **Template scaffolding** (fill-in-the-blank headers and placeholders), **Outline scaffolding** (hierarchical section structure), **Example scaffolding** (few-shot completed examples), and **Partial-output scaffolding** (you write the first paragraph, the model continues). The more concrete the scaffold, the tighter the output — at the cost of more tokens. In agentic pipelines, scaffolding is the *interface contract* between agents. It's not optional guidance; it's protocol.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Write a competitive analysis" | "Use this template: **Strengths** [bullets], **Weaknesses** [bullets], **Recommendation** [1 paragraph]" | Template eliminates structural guesswork |
| "Compare three options" | Provide an empty table with headers and one example row filled in | Example row sets the pattern for every row that follows |
| "Produce a JSON report" | Provide the exact JSON schema with keys defined and descriptions for each value | Schema prevents the model from inventing its own structure |
| "Summarize the research" | "Section 1: Key Findings (3 bullets). Section 2: Methodology Note (1 sentence). Section 3: Open Questions" | Outline scaffolding controls information architecture |
| "Give me your analysis" | "Start with this sentence: 'The primary risk is...' and continue for one paragraph" | Partial-output scaffolding channels the opening and tone |

## Before → After

**Before:**
```
Analyze these three CRM platforms and help me decide
which one to use.
```

**After:**
```
Compare three CRM platforms using this template.
Fill in every cell. If data unavailable, write "Not found."

| Feature        | Platform A | Platform B | Platform C |
|----------------|-----------|-----------|-----------|
| Price/seat     |           |           |           |
| Free tier      |           |           |           |
| API access     |           |           |           |
| Mobile app     |           |           |           |
| Integrations   |           |           |           |

After the table, write a 100-word recommendation for:
1. A 5-person startup
2. A 50-person company
3. A 500-person enterprise

Base recommendations ONLY on the table data above.
```

## Try This Now

```
I'll give you a messy prompt. Your job is to add scaffolding
— NOT to answer the prompt, but to restructure it so a
model could answer it better.

Original prompt:
"I need you to review this code and tell me what you think
about the architecture, any bugs, performance issues, and
also suggest improvements."

Add scaffolding by:
1. Breaking it into named passes (Pass 1: X, Pass 2: Y...)
2. Defining the output format for each pass
3. Adding one example of what a good finding looks like

Show the scaffolded version. Then explain which type of
scaffolding you used (template, outline, example, or
partial-output) and why.
```

## When It Breaks

- **Over-scaffolding** — Such detailed templates that the model has no real work to do. The output is the scaffold with trivial fill-ins. Scaffold the structure, not the content.
- **Scaffold-task mismatch** — A comparison task scaffolded as a linear report, or an analytical task scaffolded as a bullet list. Match the scaffold's shape to the task's cognitive structure.
- **Rigid scaffolding for fluid tasks** — Scaffolding a brainstorming session with a rigid template. The output feels mechanical. Use lighter scaffolding (guiding questions, loose outline) for creative or exploratory work.

## Quick Reference

- **Family:** Context architecture
- **Adjacent:** → constrain (constraints restrict; scaffolding supports — complementary), → framing (framing shapes thinking; scaffolding shapes output structure), → retrieval scaffolding (scaffolding applied specifically to retrieved documents), → decomposition (breaks the task into parts; scaffolding provides the shape for each part's output)
- **Model fit:** Simple scaffolding (tables, bullet lists, basic JSON) works across all tiers. Complex nested JSON with conditional fields is reliable on frontier models, approximate on midsize, unreliable on small. For small models, keep scaffolding flat — one nesting level maximum, few optional fields, and a completed example of the scaffold.
