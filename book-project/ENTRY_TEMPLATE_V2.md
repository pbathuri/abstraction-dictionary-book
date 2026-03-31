# Entry Template V2 — Interactive Practitioner's Format

> Author: Kastle Light
> This template replaces the 17-section rigid schema with a flexible,
> reader-engaging format. Not every entry uses every section.

## Structure (flexible — adapt per entry)

```markdown
# HEADWORD

> **One-line definition** (kept, but punchier — aim for memorable)

## The Scene
Open with a CONCRETE SCENARIO — a real moment where this abstraction
was missing and something went wrong. Name the project. Show the bad
prompt. Show the bad output. Make the reader feel the failure.

Sources: user's own projects (ResumeForge, Clap, Form8, Ethics Coach),
Karpathy's autoresearch, or constructed scenarios from real domains.

Length: 100-200 words. Story, not lecture.

## What This Actually Is
The definition — but written like you're explaining it to a smart
colleague at a whiteboard, not writing an encyclopedia entry.
2 paragraphs max. No "in the context of language-as-programming"
throat-clearing.

## Words That Work
THE UNIQUE VALUE OF THIS BOOK. A table or annotated list of specific
words, verbs, phrases, and sentence structures that ACTIVATE this
abstraction in a prompt. This is the thesaurus-meets-instruction-manual
section.

Format:
| Instead of...       | Write...                                    | Why it works |
|---------------------|---------------------------------------------|-------------|
| "Analyze this"      | "Identify the three largest cost drivers"   | Specificity |

## Before → After
Side-by-side prompt comparison. THE most visually valuable element.
Use real project examples where possible.

> ❌ **Before**
> ```
> Summarize this document.
> ```
>
> ✅ **After**
> ```
> Extract the 5 key decisions from this meeting transcript.
> For each: who decided, what was decided, and what action follows.
> Format as a numbered list. Skip discussion that didn't lead to decisions.
> ```
>
> **What changed:** Added specificity (5 items), scope (decisions only),
> format (numbered list), and exclusion (skip non-decisions).

## Try This Now
A 2-minute exercise the reader can paste into any LLM right now.
Conversational tone. "Open your chat window and try this..."

## From the Lab
Reference to experiment data. Include the chart filename and a
1-2 sentence interpretation of what the data shows.
"We ran 2,000 variations across four models. Here's what we found."

![Chart description](../art/figures/exp_XXXXX.png)

## When It Breaks
2-3 failure modes. Short, punchy, specific.
- **Pattern** → Why it fails, in one sentence.

## Quick Reference
Compact metadata at the bottom:
- **Family:** core_abstraction | instructional_action | etc.
- **Adjacent:** → term1, → term2, → term3
- **Model fit:** One sentence.
- **Source:** [citation]
```

## Voice Guidelines for V2

- Write like ONE person (Kastle Light) who has built these systems
- Open with stories, not definitions
- Use "I" occasionally — "When I built ResumeForge..."
- Use "you" always — talk TO the reader
- Short paragraphs. 2-4 sentences max.
- Vary the format: some entries are story-heavy, some are table-heavy,
  some lead with the Before→After
- NEVER sound like a committee. Sound like a builder who reads.
- Humor: dry, occasional, earned. Never forced.

## Length Targets for V2

- Full entries (flagships): 800-1,400 words
- Compact entries: 500-800 words
- The SHORT version is almost always better
