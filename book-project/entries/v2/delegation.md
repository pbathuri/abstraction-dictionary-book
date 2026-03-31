# delegation

> Tell the agent what it owns, what it can't touch, and what "done" looks like. That's the whole game.

## The Scene

Karpathy's `program.md` is the cleanest delegation document I've ever read. It's not a prompt. It's a job description for an LLM — written with the same precision you'd use for a human contractor you're paying by the hour and will never meet face-to-face.

Here's what makes it work. Every phase has:
- **What you will do** (search for papers, extract claims, evaluate novelty)
- **What you will NOT do** (don't editorialize, don't skip the citation check, don't invent results)
- **What "done" looks like** (output file exists, all claims cite sources, novelty score computed)
- **What to do when stuck** (log the gap, revert to the last good state, don't guess)

That's delegation with teeth. Compare it to how most people write agent prompts: "You are a research assistant. Help me find relevant papers and write a summary." That's not delegation. That's a hope delivered in an imperative voice.

I learned this the hard way building Clap. The first version of OpsPilot had six agents, each with a one-sentence instruction. The orchestrator told the code-analysis agent: "Analyze the codebase and report findings." The agent returned 3,000 words of vaguely insightful commentary about code quality, none of it structured, none of it actionable, and none of it in the format the downstream agent expected. The pipeline choked. Not because the model was dumb — because the delegation was.

The fix was stealing Karpathy's pattern: define inputs, outputs, authorities, and boundaries for each agent like you're writing a contract. Not because you don't trust the agent. Because trust without structure is just hope.

## What This Actually Is

Delegation is the instruction that moves a task from one agent to another, carrying everything the receiver needs to succeed without reading your mind. It's a five-part contract:

1. **The deliverable** — what to produce (not "help with research" but "a JSON array of 10 papers with title, authors, year, and one-sentence finding")
2. **The format** — how to structure it (schema, length, file type)
3. **The criteria** — what counts as done (all fields populated, sources verified, score computed)
4. **The authority boundary** — what tools and data the agent may access (read the corpus, don't write to the database, don't call external APIs)
5. **The failure protocol** — what to do when something goes wrong (flag it, don't fake it)

Miss any of these and you're not delegating. You're wishing aloud near a computer.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| "Research this topic" | "Return a JSON array of the 10 most-cited papers published after 2023, each with title, authors, year, one-sentence finding" | Names the deliverable, format, count, and scope |
| "Analyze the code" | "Read src/ and produce REPO_REALITY.md documenting what the code actually does today. Inspect actual code, not just documentation" | Defines the output artifact and the method |
| "Help with this" | "Your task: extract all dates from the contract. Output: JSON with clause_id, date, and context. If a date is ambiguous, flag it" | Converts vague help into a structured assignment |
| "Be careful" | "You may read the product database. You may NOT write to it. You may call the search API up to 10 times" | Authority boundary with explicit permissions and limits |
| "Do your best" | "If you cannot complete the task, return { status: 'blocked', reason: '...', completed_so_far: [...] } and halt" | Failure protocol that preserves partial progress |
| "Check your work" | "Before returning, verify: every claim cites a source_id that exists in the corpus. If any don't, remove them" | Self-verification as part of the delegation |

**Power verbs for delegation:** assign, own, deliver, produce, return, escalate, halt, verify (before returning).

## Before → After

From Clap/OpsPilot — the actual agent instruction rewrite:

> **Before**
> ```
> You are the code analysis agent. Analyze the codebase and report
> your findings to the architecture agent.
> ```
>
> **After (modeled on program.md)**
> ```
> Agent: Code Reality Mapper
> Upstream: Orchestrator
> Downstream: Architecture Reconciler
>
> Input: Repository path and product_north_star.md
>
> Task: Produce REPO_REALITY.md — a document describing what the
> code actually does today, organized by module.
>
> You MUST:
> - Inspect actual source files, not just README or docs
> - For each module, describe: purpose, dependencies, and current state
> - Flag any module that has no tests
>
> You MUST NOT:
> - Rewrite any code in this shot
> - Speculate about intended architecture — describe only what exists
> - Treat documentation as truth — verify against source
>
> Output: REPO_REALITY.md (markdown, one section per module)
> Completion: Every directory in src/ has a corresponding section.
> If a directory cannot be analyzed, include it with status: "BLOCKED"
> and the reason.
>
> Handoff: Pass REPO_REALITY.md to Architecture Reconciler.
> ```
>
> **What changed:** One vague sentence became a contract. The agent knows its deliverable, its method, its permissions, its prohibitions, and its failure mode. The downstream agent knows exactly what format to expect.

## Try This Now

Take any agent instruction you've written and stress-test it with this:

```
I'll give you an agent instruction. Your job is to play the role of
a confused but diligent agent receiving this instruction.

For each of these five questions, tell me whether the instruction
answers it clearly, partially, or not at all:
1. What exactly am I supposed to produce?
2. What format should it be in?
3. How do I know when I'm done?
4. What am I NOT allowed to do?
5. What should I do if I get stuck?

Then rewrite the instruction to fill any gaps.

Here's the instruction:
[paste your agent instruction here]
```

If the original instruction can't answer at least 4 of the 5 questions, you haven't delegated — you've hoped.

## From the Lab

This entry draws on the same reasoning-task data as → decomposition. Structured delegation (with explicit phases and criteria) is decomposition applied to agent boundaries:

![Reasoning Task Techniques](../art/figures/exp_reasoning_task_techniques.png)

**Key finding:** Agents with structured delegation instructions (defined inputs, outputs, and completion criteria) required 40-60% fewer revision cycles before producing usable output compared to agents with unstructured "do this task" instructions. The time saved on revisions vastly exceeded the time spent writing the delegation.

## When It Breaks

- **Telephone-game degradation** → Agent A delegates to Agent B, who delegates to Agent C. By the time C starts working, the original intent has been paraphrased twice and distorted. Fix: include the original objective *verbatim* at every level, separate from hop-specific instructions.
- **Authority leak** → You delegated "find competitor pricing" to an agent with access to a web scraper, an email sender, and a database writer. Without explicit tool constraints, the agent might scrape, store, *and* email results. The delegation didn't say it could. It also didn't say it couldn't.
- **Delegation without verification** → The delegator accepts the output without checking it. In a pipeline, this means a fabricated claim from step 2 becomes load-bearing evidence in step 5, and nobody noticed because nobody looked.

## Quick Reference

- **Family:** Agent workflow
- **Adjacent:** → handoff (transfers control; delegation transfers a task), → routing (decides which agent; delegation defines what the task is), → decomposition (produces the tasks delegation assigns), → verification loop (the check that follows every delegation)
- **Model fit:** Frontier models handle complex multi-constraint delegations. Mid-tier models need explicit format specs (JSON schemas, numbered steps). Small models need delegations decomposed further — a single complex delegation often needs to become two simpler ones.
- **Sources:** Karpathy (2025) autoresearch program.md, OpenAI Agents SDK handoff patterns, LangGraph supervisor patterns
