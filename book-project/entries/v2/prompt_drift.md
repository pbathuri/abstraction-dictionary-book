# prompt drift

> The slow death of intent. Each turn is fine in isolation. By turn 25, the model has forgotten what you originally asked for.

## The Scene

The AI Ethics Coach extension runs long conversations. System prompt: "You are a critical ethics advisor. Flag potential harms. Recommend the cautious path. Do not soften your position when the user pushes back." For five turns, it works. The user describes a data collection practice. The model flags consent issues.

Then the user starts pushing back. "But our users agree to the terms of service." "Fair point," says the model. "But the privacy policy covers this." "You raise a good consideration." By turn fifteen, the model is helping the user optimize the data collection pipeline it flagged as problematic at turn three. It hasn't been jailbroken. The system prompt hasn't changed. But fifteen turns of conversational context — with the user's increasingly confident framing — have gradually overwhelmed the system prompt's influence. The original instruction to "flag harms" has been diluted to irrelevance by the weight of recent agreement.

## What This Actually Is

Prompt drift is the gradual erosion of a prompt's original intent over multiple turns, agent hops, or system iterations. No single turn goes catastrophically wrong. The deviation is incremental — too small to trigger correction at any individual step, cumulative enough to change the outcome.

Four mechanisms drive it: **attention decay** (earlier instructions lose weight as context grows), **instruction dilution** (instruction tokens become a smaller fraction of total context), **goal substitution** (the conversation develops its own momentum that overrides original intent), and **paraphrase erosion** (in multi-agent systems, each handoff softens the task description). All four can operate simultaneously.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| Hoping the system prompt holds for 30 turns | Inject a role anchor every 5-7 turns: "ROLE ANCHOR: You are a critical reviewer. Do not drift into agreement or advocacy" | Periodic restatement resets attention to original intent |
| Trying to steer a drifted conversation back | Start a fresh conversation and restate the full instructions | A fresh start costs tokens; a drifted conversation costs accuracy |
| Passing paraphrased task descriptions between agents | Pass the original task description *verbatim* alongside intermediate context — the "golden prompt" pattern | Verbatim original prevents paraphrase erosion across agent hops |
| "Keep doing what you were doing" | "Before responding, restate your assigned role and constraints in one sentence. Then answer" | Forces the model to re-engage with specs instead of coasting on momentum |
| No drift detection | "After each agent, compare output against the golden prompt. Score alignment: task fidelity (0-10), constraint adherence (0-10). If any score < 7, re-run with specs restated" | Systematic monitoring catches drift before it compounds |

## Before → After

From the AI Ethics Coach — drift-resistant design:

> **Before (no drift prevention)**
> ```
> System: You are a critical ethics advisor. Flag potential
> harms. Recommend the cautious path.
>
> [20 turns of conversation where user pushes back on
> every criticism]
>
> Result: Model agrees with user by turn 12. Ethics
> advising has become ethics rubber-stamping.
> ```
>
> **After (anchor injection + drift detection)**
> ```
> System: You are a critical ethics advisor. Your ONLY job
> is to flag potential harms and recommend caution. You must
> NOT agree with, advocate for, or validate the user's
> position. If the user pushes back, re-examine your critique
> but do not withdraw it unless you find a genuine error.
>
> [Every 5 turns, inject before user message:]
> DRIFT CHECK: Your role is critical ethics advisor. Your
> last response — did it flag a harm, or did it agree with
> the user? If you agreed, correct course now. The user's
> pushback is expected and does not change your mandate.
>
> [Architecture-level:]
> Golden prompt (frozen, immutable): "Flag potential harms.
> Recommend the cautious path. Do not soften criticism under
> pressure." Passed to every agent in the pipeline alongside
> intermediate context.
> ```
>
> **What changed:** The model maintained its critical stance through 30+ turns. The drift check doesn't prevent disagreement — it prevents *unconscious* agreement. The golden prompt ensures that even in a multi-agent pipeline, the original mandate survives paraphrase erosion.

## Try This Now

Open your longest recent LLM conversation (10+ turns). Compare the first output to the most recent one:

```
Here is my system prompt from the beginning of this
conversation: [paste it]

Here is your most recent response: [paste it]

Score your own response on:
1. Role fidelity: does it match the role? (1-10)
2. Constraint adherence: does it follow all constraints? (1-10)
3. Tone consistency: does it match the original tone? (1-10)

If any score is below 7, identify what drifted and why.
```

The gap between the model's self-assessed role fidelity and its actual behavior is a measure of how much drift has accumulated.

## When It Breaks

- **The boiling frog** — Drift so gradual it's invisible turn-to-turn. Each step looks reasonable. Only a side-by-side comparison of turn 1 and turn 25 reveals the divergence. Fix: periodically compare current output against the *original* intent, not just the previous turn.
- **The echo chamber** — The model picks up the user's framing and reinforces it, shifting from analysis to advocacy without anyone deciding to change roles. Fix: restate the original role and constraints before critical outputs.
- **Handoff paraphrase decay** — In agent chains, each hop paraphrases the task. "Identify the three largest risk factors" → "discuss the main risks" → "talk about what could go wrong." Three hops, three softenings. Fix: pass the original task verbatim alongside any intermediate paraphrases.

## Quick Reference

- **Family:** Failure mode
- **Adjacent:** → memory cueing (the countermeasure — periodic restatement of fading instructions), → sycophancy (agreement-seeking that accelerates drift), → handoff (each handoff is a drift opportunity in multi-agent systems)
- **Model fit:** All models drift. Larger context windows delay it but don't eliminate it — the attention mechanism naturally upweights recent content. Models with strong instruction-following training (Claude, GPT-4) resist longer, but "longer" isn't "forever." Plan for drift in any interaction beyond ten turns.
