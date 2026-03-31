# information routing

> Send each agent only the data it needs. Everything else is noise with a token cost.

## The Scene

Form8's n8n pipeline had five nodes. By the time the Strategy Writer node ran, it received everything: raw search results, competitor profiles, the filter log, the gap analysis, and the original product description. Four thousand tokens of accumulated context. The writer needed maybe 800 of them.

The result was strategy briefs that referenced stale search results instead of the refined gap analysis. The writer was drowning in upstream artifacts and grabbing whatever floated to the surface. The fix was a routing layer — a simple n8n function node before each major stage that assembled only the fields that stage needed. The Strategy Writer received: gap analysis (structured), product description (original), and audience spec. Nothing else. The briefs got sharper because the writer stopped being distracted by data meant for earlier stages.

## What This Actually Is

Information routing is the postal system of a pipeline. Routing decides where *work* goes (which agent handles the task). Information routing decides what *data* accompanies the work at each stop. It's the discipline of curating each agent's context so every component receives precisely the information it needs — no more, no less.

The practice involves four operations: **assembly** (selecting which data an agent gets), **filtering** (removing irrelevant upstream output), **transformation** (reshaping data to match the receiver's expected format), and **aggregation** (combining outputs from multiple upstream agents into one coherent context package).

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| Pass the full output to the next step | "Extract fields [X, Y, Z] from the research output. Discard reasoning and search logs. Pass only the extracted fields to the analyst" | Names exactly what crosses the boundary |
| "Here's everything so far" | "You will receive a curated context packet: task summary (2 sentences), verified findings (JSON array), and open questions. Nothing else" | Tells the agent its world is intentionally scoped |
| Forwarding raw API responses to the synthesis agent | Transform upstream output into the downstream agent's expected schema before passing | Format mismatch is a routing failure, not a model failure |
| Letting accumulated shared state grow unbounded | "Context Router: for each agent, define read_from (which state keys), transform (how to reshape), exclude (what to strip)" | Formal routing spec prevents pass-through syndrome |
| "The agent can figure out what's relevant" | "You do not have access to upstream reasoning or search logs. Work only with the findings provided" | Explicit scope prevents attention dilution |

## Before → After

From Form8 — routing context to the Strategy Writer node:

> **Before (pass-through)**
> ```
> [Node 5 receives: raw search results (20 items) + filter
> log + competitor profiles (5) + gap analysis + product
> description + audience spec + workflow metadata]
>
> "Write a strategy brief based on the above."
> ```
>
> **After (routed context)**
> ```
> CONTEXT PACKET FOR STRATEGY WRITER:
>
> You receive exactly three inputs:
> 1. Gap analysis (from Node 4): JSON array of 3-5 gaps,
>    each with description, evidence, and confidence level
> 2. Product description: original, unmodified
> 3. Audience: product team, technical but non-engineering
>
> You do NOT receive: raw search results, filter logs,
> competitor profiles, or workflow metadata. These were
> consumed by earlier nodes and are not relevant to your task.
>
> Task: Write a 500-word strategy brief. Cite specific gaps
> by name. Every recommendation must trace to a gap.
> ```
>
> **What changed:** The Strategy Writer stopped referencing raw search results because it never saw them. Recommendations became traceable because the only input was the structured gap analysis.

## Try This Now

Map your most recent multi-step prompt or pipeline. For each step, list: (1) what data it actually uses from its input, and (2) what data it receives but ignores. If any step receives more than 2x what it uses, add a routing layer that strips the excess. Run both versions and compare focus.

## When It Breaks

- **Pass-through syndrome** — Every node gets the full accumulated output of every predecessor. The fifth node receives 4,000+ tokens when it needs 200. Fix: at every handoff, explicitly filter to include only fields the downstream agent needs.
- **Over-filtering** — You strip too aggressively and a downstream agent lacks data it turns out to need. The writer can't cite sources because you filtered out the citations. Fix: define each agent's input requirements *before* building the pipeline, and filter based on the receiver's needs.
- **Format mismatch** — Information is routed correctly but in the wrong shape. Research produces prose paragraphs; verification expects a JSON claim array. Fix: include a transformation step in the routing layer that converts upstream output to downstream expectations.

## Quick Reference

- **Family:** Context architecture
- **Adjacent:** → routing (decides where work goes; information routing decides what data accompanies it), → progressive disclosure (sequences when info appears; information routing selects what appears), → handoff (the transfer event; information routing curates what's transferred)
- **Model fit:** Implemented in code, not in models — the orchestrator or context router is a programmatic layer. Small models benefit most from aggressive routing (they're most sensitive to irrelevant context). Frontier models tolerate noisier contexts but still produce better output with well-routed information.
