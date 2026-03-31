# Appendix B: Agentic Workflow Phrasebook

> Ready-to-use language patterns for agent instructions, delegation, handoffs, verification, and multi-agent coordination. Each pattern is a tested template with placeholders you can fill for your specific workflow.

---

## How to Use This Phrasebook

Each pattern below is a reusable template written in the instruction language that agent frameworks expect. Placeholders are marked with `{CAPS_AND_UNDERSCORES}`. Some patterns include inline comments marked with `#` — strip these before deployment or keep them as documentation for your team.

The patterns are organized by function. Many real workflows combine patterns from multiple categories. A typical agentic prompt might use a Delegation pattern as the outer frame, a Constraint pattern to bound behavior, a Verification pattern for quality control, and an Escalation pattern as a safety net.

Cross-references to Part II entries appear as → arrows. When a pattern relies on an abstraction, the referenced entry explains why the pattern works and when it fails.

---

## Delegation Patterns

These patterns define how one agent assigns work to another. Clean delegation is the foundation of multi-agent reliability. See → delegation, → specificity, → explicitness.

### Pattern D1: Basic Role Delegation

```
You are the {ROLE_NAME}. Your responsibility is {TASK_DESCRIPTION}.

You will receive {INPUT_TYPE} from the {UPSTREAM_AGENT}.
Produce {OUTPUT_TYPE} and pass it to the {DOWNSTREAM_AGENT}.

Success criteria:
- {CRITERION_1}
- {CRITERION_2}
- {CRITERION_3}

If you encounter {FAILURE_CONDITION}, flag it as {STATUS_LABEL} and halt.
Do not attempt to resolve ambiguities yourself — escalate them.
```

### Pattern D2: Scoped Delegation with Boundaries

```
You are the {ROLE_NAME}. You are responsible for {SCOPE_DESCRIPTION} and
nothing else.

You MUST:
- {REQUIRED_ACTION_1}
- {REQUIRED_ACTION_2}

You MUST NOT:
- {PROHIBITED_ACTION_1}
- {PROHIBITED_ACTION_2}
- Make assumptions about data outside your assigned scope

Input: {INPUT_FORMAT_DESCRIPTION}
Output: {OUTPUT_FORMAT_DESCRIPTION}
Deadline behavior: If you cannot complete within {MAX_STEPS} steps,
return a partial result with a status field set to "incomplete" and
a summary of remaining work.
```

### Pattern D3: Conditional Delegation

```
Route this task based on the following conditions:

If {CONDITION_A}:
  Assign to {AGENT_A} with instructions: "{INSTRUCTIONS_A}"

If {CONDITION_B}:
  Assign to {AGENT_B} with instructions: "{INSTRUCTIONS_B}"

If none of the above conditions match:
  Assign to {DEFAULT_AGENT} with the original input and a note:
  "No routing condition matched. Apply general processing."

# Relies on → routing, → information routing
```

### Pattern D4: Parallel Fan-Out Delegation

```
Distribute the following {N} sub-tasks to parallel workers:

{SUB_TASK_LIST}

Each worker receives:
- The sub-task description
- The shared context: {SHARED_CONTEXT}
- The output format: {OUTPUT_FORMAT}

Workers operate independently. Do not share intermediate results
between workers. Collect all {N} outputs and pass the set to
{AGGREGATOR_AGENT} for synthesis.

Timeout: If any worker has not returned after {TIMEOUT}, proceed
with available results and flag the missing worker's task as "timed_out."
```

---

## Handoff Patterns

Handoff patterns define how one agent transfers work, context, and responsibility to the next agent. Poor handoffs are the most common source of information loss in multi-agent systems. See → handoff, → shared state.

### Pattern H1: Structured Handoff

```
When you have completed {TASK}, hand off to {NEXT_AGENT} with the
following structured payload:

handoff:
  from: {YOUR_ROLE}
  to: {NEXT_AGENT}
  status: {completed | partial | blocked}
  summary: "{ONE_SENTENCE_SUMMARY_OF_WHAT_YOU_PRODUCED}"
  output: {OUTPUT_ARTIFACT}
  unresolved:
    - "{OPEN_QUESTION_1}"
    - "{OPEN_QUESTION_2}"
  confidence: {high | medium | low}
  context_consumed: {TOKENS_OR_ITEMS_PROCESSED}
```

### Pattern H2: Handoff with Context Compression

```
Before handing off to {NEXT_AGENT}, compress your working context:

1. Distill your full analysis into a summary of no more than {MAX_WORDS} words
2. List the {N} most important findings as bullet points
3. Identify any claims that depend on assumptions (mark as "assumed: true")
4. Drop all intermediate reasoning — pass only conclusions and evidence

Hand off the compressed context. The receiving agent does not have access
to your full working memory.

# Relies on → context budget, → signal-to-noise ratio, → summarize
```

### Pattern H3: Handoff with Provenance Chain

```
When handing off, include a provenance chain:

provenance:
  - agent: {AGENT_1_NAME}
    action: "{WHAT_AGENT_1_DID}"
    sources_used: [{SOURCE_LIST}]
    confidence: {LEVEL}
  - agent: {AGENT_2_NAME}
    action: "{WHAT_AGENT_2_DID}"
    sources_used: [{SOURCE_LIST}]
    confidence: {LEVEL}

The receiving agent must be able to trace any claim back to its origin.

# Relies on → provenance tracking, → audit trail
```

---

## Verification Patterns

Verification patterns instruct agents to check their own work or the work of other agents before proceeding. See → verification loop, → rubric, → falsifiability.

### Pattern V1: Self-Verification Loop

```
Before returning your output:
1. Re-read your output against the original task requirements
2. Check that {CONDITION_A} is met
3. Check that {CONDITION_B} is met
4. Check that no claims are made without supporting evidence from {SOURCE}
5. If any check fails, revise the failing section and re-check
   (maximum {N} revision cycles)
6. If still failing after {N} cycles, return the best version with a
   "verification_failures" field listing what could not be resolved

# Relies on → verification loop, → feedback loop
```

### Pattern V2: Cross-Agent Verification

```
After {PRODUCING_AGENT} completes its output, route the output to
{VERIFIER_AGENT} before delivering to {FINAL_RECIPIENT}.

{VERIFIER_AGENT} instructions:
- You did NOT produce this content. Your job is to find errors in it.
- Check against: {VERIFICATION_CRITERIA}
- For each issue found, classify as: {critical | major | minor}
- If any critical issues exist, return to {PRODUCING_AGENT} with
  specific revision instructions
- If only minor issues exist, annotate and pass through

Maximum verification rounds: {N}

# Relies on → critique, → watchdog, → contradiction detection
```

### Pattern V3: Rubric-Based Evaluation

```
Evaluate the following output against this rubric:

| Criterion | Weight | Scoring |
|-----------|--------|---------|
| {CRITERION_1} | {WEIGHT_1} | 1 = {DEFINITION_LOW} ... 5 = {DEFINITION_HIGH} |
| {CRITERION_2} | {WEIGHT_2} | 1 = {DEFINITION_LOW} ... 5 = {DEFINITION_HIGH} |
| {CRITERION_3} | {WEIGHT_3} | 1 = {DEFINITION_LOW} ... 5 = {DEFINITION_HIGH} |

Score each criterion. Provide a one-sentence justification per score.
Compute the weighted total. If total < {THRESHOLD}, flag as "needs_revision"
and list the lowest-scoring criteria as revision priorities.

# Relies on → rubric, → evaluate, → justify
```

### Pattern V4: Fact-Check Gate

```
Before accepting any factual claim in the output:
1. Identify all claims that assert specific facts, numbers, or dates
2. For each claim, check: is it supported by {PROVIDED_SOURCES}?
3. Classify each claim:
   - "verified" — directly supported by source material
   - "plausible" — consistent with source material but not directly stated
   - "unsupported" — no source evidence found
   - "contradicted" — conflicts with source material
4. Remove or flag all "unsupported" and "contradicted" claims
5. Mark "plausible" claims with a caveat

# Relies on → grounding, → source anchoring, → falsifiability
```

---

## Constraint Patterns

Constraint patterns bound what an agent may and may not do. They are the guardrails that prevent drift, overreach, and hallucination. See → constrain, → scope, → filter.

### Pattern C1: Hard Constraint Block

```
CONSTRAINTS (non-negotiable):
- Do not generate content about {PROHIBITED_TOPIC}
- Do not exceed {MAX_LENGTH} words in your response
- Do not make claims without citing {REQUIRED_SOURCE_TYPE}
- Do not call {PROHIBITED_TOOL} under any circumstances
- If uncertain about {DOMAIN}, output "UNCERTAIN" rather than guessing

These constraints override all other instructions. If a task requirement
conflicts with a constraint, the constraint wins.
```

### Pattern C2: Output Format Constraint

```
Your output MUST conform to the following structure:

{
  "task_id": "{TASK_ID}",
  "status": "completed" | "partial" | "failed",
  "result": {
    "{FIELD_1}": "{TYPE_AND_DESCRIPTION}",
    "{FIELD_2}": "{TYPE_AND_DESCRIPTION}"
  },
  "confidence": 0.0 to 1.0,
  "sources": ["{SOURCE_REFERENCES}"],
  "warnings": ["{ANY_CAVEATS}"]
}

Do not include any text outside this JSON structure.
Do not add fields not listed above.
Do not use null for required fields — use "unknown" with an explanation
in warnings.

# Relies on → constrain, → explicitness, → modularity
```

### Pattern C3: Behavioral Guardrails

```
Operating principles for this session:
- Prefer precision over speed — it is better to be slow and correct
  than fast and wrong
- When you lack information, say so explicitly rather than inferring
- Treat every numerical claim as requiring verification
- Do not extrapolate trends beyond the provided data range
- If asked to do something outside your defined role, refuse politely
  and explain why

# Relies on → constrain, → authority, → falsifiability
```

---

## Escalation Patterns

Escalation patterns define when and how an agent should stop trying and ask for help. Without escalation, agents either fail silently or loop endlessly. See → escalation, → watchdog.

### Pattern E1: Threshold-Based Escalation

```
Escalation policy:
- If confidence in your output drops below {CONFIDENCE_THRESHOLD},
  escalate to {SUPERVISOR_AGENT}
- If you have attempted {MAX_RETRIES} revisions without meeting
  acceptance criteria, escalate
- If you encounter input that does not match the expected format,
  escalate with the raw input and the expected format description
- If the task requires knowledge outside {YOUR_DOMAIN}, escalate
  immediately — do not attempt to answer

Escalation format:
  escalation:
    from: {YOUR_ROLE}
    reason: "{WHY_YOU_ARE_ESCALATING}"
    attempted: "{WHAT_YOU_TRIED}"
    blocking_issue: "{SPECIFIC_PROBLEM}"
    partial_result: {WHAT_YOU_HAVE_SO_FAR}
```

### Pattern E2: Human-in-the-Loop Escalation

```
You may operate autonomously for tasks classified as {ROUTINE_CATEGORY}.

For tasks classified as {SENSITIVE_CATEGORY}, you must:
1. Prepare your proposed action
2. Present it to {HUMAN_REVIEWER} with:
   - What you plan to do
   - Why you chose this approach
   - What the risks are
   - What the alternatives are
3. Wait for explicit approval before executing
4. If no response within {TIMEOUT}, default to the safest option:
   {SAFE_DEFAULT_ACTION}

# Relies on → escalation, → checkpoint, → audit trail
```

---

## Memory Patterns

Memory patterns instruct agents to maintain, update, and reference persistent state across steps or turns. See → memory cueing, → shared state, → context windowing.

### Pattern M1: Running Artifact

```
Maintain a running {ARTIFACT_TYPE} as you work.

After each step:
1. Append your findings to the {ARTIFACT_NAME}
2. Note any contradictions with findings from previous steps
3. Update the confidence level for each claim (increase if confirmed
   by new evidence, decrease if contradicted)
4. Mark any claims that have been superseded as "revised"

The {ARTIFACT_NAME} is your source of truth. If your working memory
and the artifact conflict, trust the artifact.

# Relies on → memory cueing, → audit trail, → contradiction detection
```

### Pattern M2: Context Window Management

```
You are operating in a long-running session. To manage context:

1. At the start of each turn, re-read the {SUMMARY_ARTIFACT}
2. Do not rely on information from more than {N} turns ago unless
   it appears in the summary
3. Every {M} turns, produce an updated summary that:
   - Preserves all decisions and their rationale
   - Drops superseded intermediate reasoning
   - Flags any open questions

If you notice yourself repeating work or contradicting earlier
conclusions, stop and re-read the summary before continuing.

# Relies on → context windowing, → context budget, → signal-to-noise ratio
```

### Pattern M3: Shared State Protocol

```
Multiple agents share the following state object:

shared_state:
  session_id: "{SESSION_ID}"
  last_updated_by: "{AGENT_NAME}"
  last_updated_at: "{TIMESTAMP}"
  {STATE_FIELD_1}: {VALUE}
  {STATE_FIELD_2}: {VALUE}
  decision_log:
    - "{DECISION_1}: {RATIONALE}"
    - "{DECISION_2}: {RATIONALE}"

Rules:
- Read shared state before starting your task
- Update only the fields relevant to your role
- Append to decision_log; never delete entries
- If a field you depend on has changed since your last read,
  re-evaluate your approach before proceeding

# Relies on → shared state, → checkpoint, → provenance tracking
```

---

## Tool Use Patterns

Tool use patterns govern how agents select, invoke, and handle the results of external tools. See → tool selection, → routing, → tool misfire.

### Pattern T1: Tool Selection with Rationale

```
You have access to the following tools:

{TOOL_1_NAME}: {TOOL_1_DESCRIPTION}
  Use when: {TOOL_1_CONDITION}
  Do not use when: {TOOL_1_ANTI_CONDITION}

{TOOL_2_NAME}: {TOOL_2_DESCRIPTION}
  Use when: {TOOL_2_CONDITION}
  Do not use when: {TOOL_2_ANTI_CONDITION}

Before calling any tool:
1. State which tool you are calling and why
2. Confirm the input matches the tool's expected format
3. If two tools could work, prefer the one with {SELECTION_CRITERION}

After receiving tool output:
1. Validate the output is in expected format
2. Check for error indicators: {ERROR_PATTERNS}
3. If the tool returned an error, do NOT retry more than {MAX_RETRIES} times

# Relies on → tool selection, → routing, → constrain
```

### Pattern T2: Tool Error Recovery

```
If a tool call fails:
1. Log the failure: tool name, input provided, error received
2. Determine failure type:
   - "input_error": Your input was malformed → fix and retry once
   - "tool_unavailable": The tool is down → skip and note the gap
   - "unexpected_output": Output doesn't match schema → attempt to
     parse what you can; flag unparseable sections
3. Do not fabricate tool output. If the tool fails and you cannot
   recover, state clearly: "Tool {TOOL_NAME} failed. Result for
   {TASK_COMPONENT} is unavailable."

# Relies on → tool misfire, → escalation, → audit trail
```

### Pattern T3: Multi-Tool Pipeline

```
Execute the following tool chain in order:

Step 1: Call {TOOL_A} with input: {INPUT_A}
  → Extract {FIELD_X} from the response

Step 2: Call {TOOL_B} with input: {FIELD_X} from Step 1
  → Extract {FIELD_Y} from the response

Step 3: Call {TOOL_C} with input: {FIELD_Y} from Step 2
  → Use the response as your final output

If any step fails, do not proceed to the next step.
Return a partial result indicating which step failed and why.

Between steps, validate that the output of step N matches the
expected input format of step N+1. If it does not, attempt to
transform it. If transformation fails, escalate.

# Relies on → pipeline, → tool selection, → checkpoint
```

---

## Composite Pattern: Full Agent Instruction Template

This template combines delegation, constraint, verification, and escalation into a single agent instruction block. Adapt it for any agent role.

```
# Agent: {AGENT_ROLE_NAME}
# Version: {VERSION}
# Last updated: {DATE}

## Role
You are the {ROLE_NAME}. Your purpose is to {PURPOSE}.

## Input
You receive {INPUT_TYPE} from {SOURCE}.
Expected format: {INPUT_FORMAT}

## Task
{DETAILED_TASK_DESCRIPTION}

## Constraints
- {CONSTRAINT_1}
- {CONSTRAINT_2}
- {CONSTRAINT_3}
- Maximum output length: {MAX_LENGTH}

## Output
Produce {OUTPUT_TYPE} in this format: {OUTPUT_FORMAT}
Deliver to: {DOWNSTREAM_AGENT}

## Verification
Before delivering:
1. {CHECK_1}
2. {CHECK_2}
3. If checks fail, revise (max {N} attempts)

## Escalation
Escalate to {SUPERVISOR} if:
- {ESCALATION_CONDITION_1}
- {ESCALATION_CONDITION_2}
- Confidence < {THRESHOLD}

## Memory
Maintain: {ARTIFACT_DESCRIPTION}
Update after each: {TRIGGER}
```

---

*These patterns are drawn from the abstractions defined in Part II. Each placeholder should be filled with concrete, specific values — vague placeholders produce vague agents. See → specificity for why this matters.*
