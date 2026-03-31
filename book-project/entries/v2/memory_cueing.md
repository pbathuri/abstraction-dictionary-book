# memory cueing

> The model hasn't forgotten your instructions. It's just stopped paying attention to them.

## The Scene

The AI Ethics Coach Chrome extension runs multi-turn conversations. The system prompt says: "You are a conservative ethics advisor. Flag potential harms. Always recommend the cautious path." For the first five turns, it works. By turn fifteen, the model is cheerfully helping the user justify a data collection practice it should have flagged. It hasn't been jailbroken. It hasn't forgotten the system prompt. The system prompt is still sitting at the top of the context window, technically accessible. But fifteen turns of conversational context have diluted its influence to near zero.

I added a cueing mechanism: every five turns, a condensed reminder gets injected before the user's message. "ROLE ANCHOR: Ethics advisor. Flag harms. Recommend caution. Do not drift into advocacy." Twelve words that reset the model's operating context. The extension stopped going soft after turn ten.

## What This Actually Is

Memory cueing is attention maintenance, not memory repair. Everything in the context window is technically available to the model. But attention isn't uniform — earlier tokens lose influence as new content accumulates. Instructions stated once in a system prompt decay in effective weight as the conversation grows. Memory cueing restates critical information to restore its salience.

Three techniques: **Repetition cueing** restates instructions verbatim at intervals. Simple, effective, burns tokens. **Reference cueing** points back without restating: "Following the criteria from your system prompt..." Uses less context but relies on the model to look back. **Summary cueing** condenses: "Recall: target audience is CFOs, tone is business-formal, key metric is ARR growth." Best balance of token efficiency and salience recovery.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| Hoping the system prompt still holds at turn 20 | Inject a 2-3 sentence role reminder every 5-7 turns | Empirically, persona and constraint adherence decay fastest |
| "Remember your instructions" | "ACTIVE SPECS (restated): Role: compliance reviewer. Standard: GDPR Article 30. Threshold: err toward caution. Tone: precise, legalistic" | Specific restatement beats vague reminder |
| Passing a growing conversation history to each pipeline agent | Give each agent a fresh copy of relevant specs in its own system prompt | Memory cueing at the architecture level |
| "Keep doing what you've been doing" | "Before responding, confirm your operating parameters: [list 3-4 key constraints]" | Forces the model to re-engage with specs |
| Restating everything every turn | Cue selectively — persona and numeric anchors drift fastest; format specs tend to persist | Over-cueing wastes context budget on reminders |

## Before → After

From the AI Ethics Coach — preventing persona drift:

> **Before (no cueing)**
> ```
> System: You are a conservative ethics advisor for software
> developers. Flag potential harms in code patterns. Always
> recommend the cautious path.
>
> [15 turns of conversation — no reinforcement]
> [By turn 15, model is helping user optimize the very
> pattern it should have flagged]
> ```
>
> **After (periodic cueing)**
> ```
> System: [same system prompt]
>
> [Every 5 turns, prepend to user message:]
> ROLE ANCHOR — Ethics Advisor
> - Your job: flag potential harms, not help optimize them
> - Bias: toward caution, even when user pushes back
> - If you catch yourself agreeing with a practice you
>   previously flagged, re-examine your reasoning
>
> Now address: {user_message}
> ```
>
> **What changed:** The model maintained its critical stance through 30+ turn conversations. Without cueing, it consistently softened by turn 10-12. The anchor doesn't prevent disagreement — it prevents *unconscious* drift toward agreement.

## Try This Now

Open any long conversation (10+ turns) with an LLM where you set a specific role or constraints at the start. At the current turn, ask:

```
Without rereading your system prompt, state:
1. Your assigned role
2. Your three most important constraints
3. Any instruction you were given about tone or format

Now reread your system prompt and note any discrepancies
between what you recalled and what it actually says.
```

The gap between what the model "remembers" and what was specified is the drift that memory cueing prevents.

## When It Breaks

- **Over-cueing** — You restate everything so frequently that 40% of your context budget is reminders, leaving less room for actual content. Fix: cue selectively. Test which specs actually drift (persona and numeric thresholds drift fastest) and cue only those.
- **Stale cues** — The pipeline has evolved but the cue still references original specs. The model follows the outdated cue. Fix: treat cues as part of the specification, not as static text — update them when requirements change.
- **Cueing instead of fixing architecture** — If an agent needs specs from five stages ago, the pipeline should inject them directly rather than relying on cueing through accumulated conversation. If you're cueing the same information at every step, make it a first-class input.

## Quick Reference

- **Family:** Context architecture
- **Adjacent:** → anchoring (sets a reference point; memory cueing refreshes it when influence fades), → prompt drift (the failure that memory cueing prevents), → progressive disclosure (controls when info enters context; memory cueing controls when it gets re-emphasized)
- **Model fit:** Models with strong long-context performance (GPT-4 Turbo, Claude 3.5 200K) need less aggressive cueing but still benefit at extreme lengths. Shorter-context models need cueing every 3-5 turns. Always test empirically: have the model repeat your key specs after N turns without cueing, then increase cueing frequency until they're retained.
