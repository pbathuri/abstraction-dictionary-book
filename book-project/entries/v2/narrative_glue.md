# narrative glue

> The sentences between sections that turn a list of points into a document a human can actually read.

## The Scene

Clap/OpsPilot's pipeline produces a multi-section architectural review. The Research Agent writes findings. The Analysis Agent writes implications. The Recommendation Agent writes action items. Each section is individually excellent. Assembled together, they read like three strangers had written on the same flight without talking.

Section 1 ends with "Module X lacks error handling." Section 2 opens with "The architecture faces several scalability challenges." No connection. No "this missing error handling compounds when we consider scalability" — nothing that carries the reader from one thought to the next. I added a Stitching Agent as the final pipeline step. Its only job: read the assembled sections and add the connective tissue. Transitions between sections. A framing intro. A closing that ties findings to recommendations. No content changes. Just the glue that makes stapled pages read like a written document.

## What This Actually Is

Narrative glue is the transitional prose between content blocks — the sentences that connect ideas, create reading flow, and make a sequence of points cohere into an argument. It's not new information. It's the bridge that explains *why* the next topic follows from the previous one.

Models are surprisingly bad at this by default. They excel at generating discrete content blocks but default to either mechanical transitions ("Now let us discuss...") or no transitions at all. For anything longer than a page, the absence of glue produces text that reads like a collection of encyclopedia entries rather than a coherent document.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "Add transitions between sections" | "At the end of each section, write one sentence connecting the current topic to the next. The connection must be logical — explain *why* the next topic follows, not just *that* it follows" | Logical transitions over procedural announcements |
| No transition instruction (hoping for the best) | "The reader should never feel a hard cut between sections. Each paragraph must connect to the one before it" | Makes continuity an explicit requirement |
| Accepting "Now that we have discussed X, let us move on to Y" | "Do NOT use procedural transitions like 'Having discussed X, we now turn to Y.' Instead, end each section with a tension or question that the next section resolves" | Bans the mechanical pattern and offers an alternative |
| Having each agent write self-contained sections | Add a final-pass Stitching Agent: "You receive assembled sections. Add transitions, an opening frame, and a closing. Do not change content" | Dedicated agent for the glue that no other agent was responsible for |
| "Make it flow" | "Write as if one author wrote this in a single sitting. No section should re-introduce material the previous section covered. Use backward references ('the latency issues identified above') and forward references ('as we will see in the risk assessment')" | Specific techniques over vague aspirations |

## Before → After

From Clap/OpsPilot — adding the Stitching Agent:

> **Before (assembled, no glue)**
> ```
> ## Findings
> [Research Agent output — ends abruptly]
>
> ## Implications
> [Analysis Agent output — opens with new context-setting
> that repeats material from Findings]
>
> ## Recommendations
> [Recommendation Agent output — no reference to Implications]
> ```
>
> **After (stitched)**
> ```
> STITCHING AGENT:
> You receive three independently written sections of an
> architectural review. Your job is narrative glue ONLY.
> Do not modify content.
>
> Add:
> 1. Opening paragraph (3-4 sentences): frame the review's
>    purpose and what the reader should expect
> 2. Transition between Findings → Implications (2-3 sentences):
>    connect the most critical finding to its downstream impact
> 3. Transition between Implications → Recommendations (2-3
>    sentences): frame recommendations as responses to the
>    implications, not as a separate list
> 4. Closing paragraph (3-4 sentences): tie findings to
>    recommendations without restating section headings
>
> Quality check: if any transition sounds like "Having reviewed
> the findings, we now turn to..." — rewrite it to sound
> motivated, not procedural.
> ```
>
> **What changed:** The document reads as one continuous argument. The reader follows a thread from "here's what we found" through "here's why it matters" to "here's what to do about it" without having to construct those connections themselves.

## Try This Now

Take any multi-section document an LLM produced for you. Delete all transitions between sections. Now read it. Notice the hard cuts. Now paste the sections with this:

```
These sections were written independently. Add ONLY the
connective tissue:
- One bridge sentence between each pair of sections
- Each bridge explains why the next topic follows logically
- Do not summarize either section in the bridge
```

Compare the before and after reading experience. The content is identical. The comprehension effort is not.

## When It Breaks

- **The robotic transition** — "Now that we have discussed X, let us move on to Y." Announces a topic change without motivating it. Fix: instruct the model to make transitions *logical* ("this finding creates a tension that the next section resolves") not *procedural* ("we now turn to").
- **Glue that introduces content** — The transition paragraph previews the next section, creating redundancy. Fix: transitions should create *expectation*, not *preview*. "End with a question or tension the next section resolves. Don't summarize what's coming."
- **Inconsistent density** — Beautiful transitions between sections 1-2, hard cut between 3-4. The model's attention to the transition instruction decays. Fix: reinforce at regular intervals, or dedicate a post-generation pass specifically for transition quality.

## Quick Reference

- **Family:** Tone and style
- **Adjacent:** → integrate (fuses pieces into wholes; narrative glue is one technique integration uses), → formality (glue must match the register of surrounding content), → decomposition (breaks tasks apart; narrative glue reassembles outputs)
- **Model fit:** Frontier models produce natural-sounding logical transitions when instructed. Midsize models follow transition instructions but default to the mechanical "Now let us discuss..." pattern unless explicitly prohibited. Small models struggle — for them, instruct the model to end each section with a question the next section answers, rather than asking for transitional prose.
