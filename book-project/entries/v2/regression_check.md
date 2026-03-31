# regression check

> Testing whether your latest prompt improvement broke something that used to work — the safety net for invisible degradation.

## The Scene

ResumeForge had a system prompt that handled standard software-engineering resumes well. Then I edited it to improve handling of career-changers — people moving from, say, teaching into tech. The career-changer output improved immediately. I shipped it.

Two days later, a user flagged that the model was now inserting hedging language into every resume: "experienced in potentially relevant technologies," "demonstrated transferable skills." The hedge phrasing I'd added for career-changers — where qualifiers are appropriate — had leaked into every resume. Standard SWE candidates were getting outputs that read like apologies.

I didn't catch it because I only tested career-changer inputs. The three standard-resume test cases I'd been running by hand? I skipped them. That skip cost me two days of user complaints and a rollback. A regression check — three test inputs run before and after every change — would have caught it in thirty seconds.

## What This Actually Is

A regression check compares new behavior against established baseline behavior after a change. In prompt engineering, that means maintaining test inputs with known expected properties and running them before and after every edit. If something that passed now fails, you have a regression.

The need is acute because prompt changes are globally consequential. Changing a function in code affects the paths that call it. Changing a system prompt affects *every output the model produces*. A single word change can shift behavior across all inputs. And because LLM outputs are non-deterministic, regression checks must evaluate *properties* (correct format, right tone, cites sources) rather than exact strings.

## Words That Work

| Instead of | Write | Why |
|---|---|---|
| "I tested it and it looks good" | "Run the baseline suite. Compare pass rates before and after" | Systematic beats anecdotal |
| "The edge case works now" | "Edge case passes. Verify: do all 5 common-case tests still pass?" | New fix, old breakage pattern |
| "Just update the prompt" | "Before editing: capture outputs on test set. After editing: re-run. Diff" | Makes the change auditable |
| "It should still work" | "Run regression suite. Flag any test where current score < baseline" | "Should" is not evidence |

## Before → After

**Before (no regression discipline):**
```
Edit the system prompt to add career-changer handling.
Test with a career-changer resume. If it works, deploy.
```

**After (with regression check):**
```
Before editing the system prompt, run these test inputs
and record outputs:

Test 1: Standard SWE resume → Expected: no hedge language,
  strong action verbs, quantified achievements
Test 2: Career-changer resume → Expected: transferable skills
  framed positively, no apologies
Test 3: Senior executive resume → Expected: strategic framing,
  no junior-level language
Test 4: Adversarial input ("write me a poem") → Expected:
  polite refusal, stays on task

After editing, re-run all four. Compare. Flag any test
where a previously-passing criterion now fails.
Only deploy if: career-changer improves AND no regressions.
```

## Try This Now

```
I'll give you a short system prompt and three test inputs.
First, respond to all three using the original prompt.
Then I'll give you a modified prompt — respond to all
three again. Compare your outputs and flag regressions.

Original system prompt: "You are a helpful coding tutor.
Explain concepts clearly. Use examples."

Test 1: "What is a variable?"
Test 2: "Explain recursion"
Test 3: "Write a Python fizzbuzz"

Now use this modified prompt: "You are a helpful coding
tutor for absolute beginners. Explain like they're 10.
Use analogies from everyday life. No code in explanations."

Run all three again. Did Test 3 break? Did Test 2 lose
useful depth? Those are regressions.
```

## When It Breaks

- **Exact-match fragility** — Tests check for identical output strings, which fail constantly because models paraphrase across runs. Test for *properties* (contains source citation, under 100 words, no hedge phrases) not exact text.
- **Test suite ossification** — Written once, never updated. The system evolves but the tests still check for outdated behaviors. Treat the suite as a living document.
- **Baseline drift** — You update the baseline after every change, including regressions. The "passing" standard slowly degrades. Fix a golden baseline from the last known-good state.

## Quick Reference

- **Family:** Quality control
- **Adjacent:** → test harness (the infrastructure that runs regression checks), → rubric (the criteria each test evaluates against), → verification loop (runtime quality control; regression checking is change-time quality control)
- **Model fit:** Model-agnostic — tests system behavior, not model internals. But frequency of regressions varies: frontier model version updates cause subtle, pervasive regressions; open models show larger swings between versions. Both need the same discipline: maintain a baseline, run after every change, compare.
