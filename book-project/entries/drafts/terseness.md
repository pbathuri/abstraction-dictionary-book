---
headword: "terseness"
slug: "terseness"
family: "tone_style"
status: "draft"
version: 1
created: "2026-03-27"
last_modified: "2026-03-27"
author_agent: "lexicographer_v1"
reviewer_agent: ""
related_entries: ["register", "authority", "specificity", "narrative glue", "audience specification"]
cross_links: ["register", "authority", "specificity", "narrative glue", "audience specification", "constrain", "framing", "warmth"]
tags: ["tone-style", "conciseness", "economy", "verbosity", "output-control"]
has_note_box: true
note_box_type: "which_word"
---

# terseness

**Elevator definition**
Terseness is the discipline of saying only what needs saying — cutting filler, hedges, and performative thoroughness so the output earns every word it uses.

## What it is

Language models are verbose by nature. Not because they are designed to be, but because their training objective rewards plausible continuation, and the most statistically plausible continuation of a sentence is often another sentence. The model does not know when to stop elaborating. It does not experience the reader's impatience. Left unconstrained, it will explain, then re-explain, then summarize its explanation, then offer a caveat about the summary. The result reads less like an expert talking and more like someone who is paid by the word.

Terseness is the corrective. It is the instruction — implicit or explicit — that every sentence must carry its own weight. Not brevity for its own sake (that is a different thing, and a worse one), but economy: the ratio of meaning to words. A terse response to "What is a mutex?" might be: "A mutex is a synchronization primitive that ensures only one thread accesses a shared resource at a time. If thread A holds the lock, thread B blocks until A releases it." That is forty words. It is complete. A typical model response to the same question, without terseness instructions, would be 150-250 words and would include a paragraph about why concurrency is important, a note about how mutexes differ from semaphores (which was not asked), and a closing sentence about how "understanding these concepts is crucial for writing robust software."

The extra words are not wrong. They are unwanted. And in professional contexts — engineering documentation, data analysis, operational communication — unwanted words are not neutral. They are costly. They dilute the signal. They force the reader to scan for the part that matters. They waste time, which is the one resource the reader was trying to save by asking a model in the first place.

Terseness is distinct from simplicity. A terse explanation can be highly technical, dense with domain terminology, and syntactically complex. What it cannot be is padded. Strunk and White's famous dictum — "Omit needless words" — is the heart of it. The question is not "is this word correct?" but "does this word earn its place?"

In model output, needless words follow recognizable patterns. Preambles ("That's a great question!"), throat-clearing ("When it comes to..."), false hedges ("It's worth noting that..."), redundant summaries ("In conclusion, to summarize what we've discussed..."), and performative comprehensiveness ("There are many factors to consider, including but not limited to..."). These patterns are deeply embedded in the training distribution because they appear constantly in web text, forum answers, and instructional content. The model is not padding on purpose. It is reproducing the padding it learned was normal.

## Why it matters in prompting

Most prompt instructions focus on what the model should *include*. Terseness is an instruction about what the model should *exclude*. This inversion is important because the model's default behavior is additive — it will keep generating until it runs out of things that seem relevant. Without a terseness instruction, the model does not know you wanted it to stop three paragraphs ago.

Effective terseness instructions are specific. "Be concise" is too vague — the model will trim slightly and still produce an output that is twice as long as you wanted. Better: "Answer in under 50 words." Or: "One paragraph. No preamble. No summary." Or: "Reply as if every word costs a dollar." The mechanism matters less than the specificity. The model needs to know what you consider excess, because its own threshold for excess is calibrated to the training data average, which is far more tolerant of bloat than most professionals are.

The Prompt Report identifies output formatting and style instructions as distinct components that shape model behavior independently of the content instruction [src_paper_schulhoff2025]. Terseness is a style instruction that is also, implicitly, a formatting instruction: it changes not just how the model writes but how much.

## Why it matters in agentic workflows

In pipelines where agents pass output to other agents, verbosity is a compounding problem. If a research agent produces 800 words when 200 would suffice, the analysis agent downstream must process four times the necessary input. Across a pipeline with five or six agents, verbose upstream agents can cause context window pressure, increased latency, and degraded performance in downstream agents that must distinguish signal from padding.

Terseness in agentic contexts is a resource management strategy. Agents that produce tight, information-dense output allow downstream agents to operate within smaller context windows, process faster, and make fewer errors caused by attending to filler. System prompts for pipeline agents should almost always include a terseness instruction — not "be concise" but a concrete constraint: word limits, structural limits ("findings only, no commentary"), or information-density requirements ("every sentence must contain a fact or a claim").

## What it changes in model behavior

Terseness instructions reduce output length, eliminate hedge phrases and preambles, increase information density per sentence, and shift the model toward declarative rather than discursive structures. The model produces fewer subordinate clauses, fewer transitional phrases, and fewer meta-commentary sentences ("Let me explain," "As mentioned above"). Paragraph count drops. Sentence-level specificity increases — when the model has fewer words to work with, it tends to choose more precise ones.

## Use it when

- The output is consumed by professionals who value density over completeness
- The model's output feeds into another system (another agent, a database, a report template) where excess text is noise
- You are working within token budget constraints and need maximum information per token
- The task is answerable in a known, bounded amount of text (a definition, a verdict, a recommendation)
- Previous model outputs on the same task were correct but bloated
- The output is a command, a status, or a decision — anything where padding delays action

## Do not use it when

- The task is pedagogical and the reader needs elaboration to understand
- You are asking the model to show its reasoning and cutting words would cut steps
- The audience is unfamiliar with the domain and needs contextual scaffolding
- The output is reader-facing long-form content where → narrative glue and transitions are part of the value

## Contrast set

**Closest adjacent abstractions**

- → brevity — Brevity is about length. Terseness is about density. A terse response can be moderately long if every sentence carries information. A brief response can be short and still padded. Terseness is the harder discipline.
- → specificity — Specificity controls what the model talks about; terseness controls how much it says about it. They compound well: specific and terse output is the highest signal-to-noise ratio achievable.
- → authority — Terseness often amplifies authority. An authoritative voice that is also concise reads as confident and expert. An authoritative voice that is also verbose reads as lecturing.

**Stronger / weaker / narrower / broader relatives**

- → register — Broader. Terseness is one dimension of register — you can specify a terse register or a discursive one.
- → constrain — Related. Length constraints are one form of constraint, but terseness is about more than length — it is about information density.
- → narrative glue — Opposite in function. Narrative glue adds connective prose; terseness removes it. The tension between them is a real design decision in any output that serves both human readability and information density.

## Common failure modes

- **Terseness as rudeness** → The model, instructed to be terse, strips out not just padding but also the minimal courtesies that make output readable to humans. "Mutex: synchronization primitive. One thread. Lock/unlock." is terse but hostile. Useful for machine consumption. Not useful in a customer-facing response. Fix: specify the register alongside the terseness instruction. "Be concise but not curt. Write for a colleague, not a parser."

- **False terseness** → The model interprets "be concise" by using shorter words but the same number of them. Or it adds a meta-sentence about being concise: "I'll keep this brief." (Narrator: it was not brief.) Fix: specify a hard word or sentence limit rather than relying on the word "concise."

- **Terseness that omits necessary qualification** → In domains where precision requires hedge language (medicine, law, risk assessment), forced terseness can strip out the qualifiers that make the output professionally responsible. "This drug interacts with warfarin" is terse. "This drug may interact with warfarin in patients with hepatic impairment; consult prescribing information" is longer but safer. Fix: instruct the model to "be terse in expression but complete in qualification."

## Prompt examples

### Minimal example

```text
What is the CAP theorem?

Answer in exactly three sentences: one per letter (C, A, P).
No preamble. No closing summary.
```

### Strong example

```text
I will give you a verbose paragraph from a draft technical document.
Rewrite it to say the same thing in half the words or fewer.

Rules:
- Preserve all factual claims and their qualifications
- Remove every sentence that restates something already said
- Remove every phrase that does not add information
  ("it is important to note," "as mentioned," "in other words")
- Do not add new information
- Do not change the meaning
- Do not summarize — rewrite

Verbose paragraph:
"When it comes to database indexing, it's important to understand
that there are several different types of indexes that can be used,
and each type has its own set of advantages and disadvantages. B-tree
indexes are perhaps the most commonly used type of index, and they
work well for a wide range of query patterns. However, it's worth
noting that for certain specific use cases, such as full-text search
or geospatial queries, specialized index types like GIN or GiST
indexes may be more appropriate and can offer significantly better
performance characteristics."
```

### Agentic workflow example

```text
Pipeline: Incident Response Summary

Agent 1 — Log Analyst
System prompt: You are a senior SRE analyzing production logs.
Produce a findings list. Each finding is one sentence.
Format: "[TIMESTAMP] [SEVERITY] [FINDING]"
No prose. No transitions. No context-setting. Findings only.

Agent 2 — Root Cause Identifier
System prompt: You receive structured findings from the Log Analyst.
Identify the most probable root cause in one paragraph of no more
than 60 words. State the cause, the evidence that supports it,
and your confidence level (high / medium / low). Nothing else.

Agent 3 — Action Recommender
System prompt: You receive a root cause assessment. Produce
exactly three recommended actions, ordered by priority.
Format: "1. [ACTION] — [REASON] — [ESTIMATED EFFORT]"
No introduction. No closing. Three lines.

Terseness constraint for all agents: Every token costs money
and time. Do not produce tokens that do not carry information.
If you are about to write "It's worth noting," stop. It isn't.
```

## Model-fit note

All model tiers respond to explicit length constraints (word counts, sentence counts). Frontier models also respond to subtler terseness cues ("write like a senior engineer, not a textbook") and maintain information density across long outputs. Midsize open models follow hard length limits but sometimes sacrifice content to meet them — they cut information rather than cutting padding. Small models tend to interpret "be concise" as "be short," producing responses that are brief but not dense. For small models, structural constraints ("three sentences, one per point") work better than stylistic instructions ("be terse").

## Evidence and provenance

Style and output formatting instructions as distinct prompt components are documented in The Prompt Report [src_paper_schulhoff2025]. The observation that models default to verbose output absent explicit constraints is a widely documented practitioner finding. The distinction between terseness (information density) and brevity (output length) is drawn from writing pedagogy, most notably Strunk and White's *The Elements of Style* (1959), applied here to model output control.

## Related entries

- **→ register** — terseness is one dimension of the register you set
- **→ authority** — terse output often reads as more authoritative
- **→ specificity** — specificity controls topic scope; terseness controls word budget
- **→ narrative glue** — the opposite force; adds connective tissue that terseness strips
- **→ constrain** — length constraints are one mechanism for enforcing terseness

---

> **Which Word?**
>
> *Terse* or *concise* or *brief*? They are not synonyms. Brief means short — it says nothing about density. A brief answer can be padded in five sentences as easily as in fifty. Concise means "no unnecessary words," which is closer, but in practice "be concise" has been so overused in prompts that models treat it as a mild suggestion rather than a hard constraint. Terse means compressed and dense — every word carries load. If you want tight, information-rich output, say "terse." If you just want fewer words, say "under 50 words." If you say "concise," expect the model to shave 15% and call it a day.
