# audit trail

> A chronological record of what happened in your pipeline — making every step inspectable and every failure traceable.

## The Scene

Your Clap orchestration pipeline spits out a bad recommendation. The user is confused, your PM is annoyed, and you're staring at a final output with no idea where it went wrong. Was it the retrieval step? The analysis? The generation? You don't know, because you didn't log the intermediate states. You're debugging a five-step pipeline by reading the last page of the book.

Next iteration, you add structured logging at every agent boundary. Now when something breaks, you trace backward: the synthesis was fine, the analysis was fine, but the retrieval step returned irrelevant documents because the query reformulation mangled the user's intent. Twenty minutes of tracing, not two days of guessing.

## What This Actually Is

An audit trail is the contemporaneous log — not the summary, not the post-mortem narrative, the actual record of what was done, by which agent, with what inputs, producing what outputs, at what time. In traditional systems, audit trails are a compliance requirement. In LLM systems, they're a survival requirement. Without one, you can't debug, reproduce, or improve.

At minimum, log: the prompt sent (including system prompt and injected context), the raw output, any post-processing, the model version and parameters, and a timestamp. For agent systems, add: which agent, what tools were called with what arguments, and how routing decisions were made.

The critical distinction: designed-in trails capture the actual prompts and responses as they flow. Bolted-on trails rely on after-the-fact logging that misses retries, intermediate states, and the context that explains *why*.

## Words That Work

| Instead of... | Write... | Why |
|---|---|---|
| (no logging) | "Before acting, emit: `{step_id, action, input_summary, reasoning, confidence}`" | Structured logs at every step make failures traceable |
| "Log the output" | "Log the prompt, raw response, model version, temperature, and latency at every agent boundary" | Intermediate states are where bugs hide |
| "We'll figure out what went wrong" | "Trace backward from the bad output to find the step where the pipeline diverged" | Audit trails turn mysteries into diagnostic exercises |
| "Keep a record" | "Append-only log, JSON lines, PII hashed, 24-month retention" | Specify format, privacy, and lifecycle upfront |

## Try This Now

```
You are processing a request in 3 steps: Research, Analyze, Recommend.

For each step, before producing your output, emit a log entry:
- step_id: (1, 2, or 3)
- action: what you're about to do
- input_summary: first 50 characters of your input
- confidence: 0.0-1.0
- flags: any concerns

After all steps, produce a TRAIL_SUMMARY table listing step_ids,
actions, and confidence levels. Flag any step where confidence < 0.7.

Topic: "Should a small startup use microservices or a monolith?"
```

You'll see how the trail makes the model's reasoning visible and auditable at every stage.

## When It Breaks

- **Incomplete capture** → You log the final output but not intermediate steps. You can see the answer was wrong but not *where* it went wrong. Log at every agent boundary.
- **Retroactive reconstruction** → Building the "audit trail" from memory after a failure. That's a story, not a log. Stories have narrative bias. Design the trail in from the start.
- **Unredacted sensitive data** → The audit trail becomes a liability. Medical queries, financial details in plaintext logs. Define a redaction policy *before* building the trail.

## Quick Reference

- Family: quality control
- Adjacent: → checkpoint (verification points within the trail), → feedback_loop (mines the trail for improvement signals), → falsifiability (trails make claims checkable)
- Model fit: Audit trail generation works across all model sizes — it's primarily a formatting task. Constrain entry size for smaller-context models.
