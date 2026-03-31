# Preface

There was a morning — I remember it clearly because I was on my third coffee and my fourth hour of debugging — when I watched a perfectly good prompt destroy a perfectly good resume.

I was building ResumeForge, a tool that tailors resumes to job descriptions using a local LLM. The prompt was simple: "Improve this bullet point for the target job description." The model complied enthusiastically. It added a PMP certification the candidate didn't have, tripled the size of their team, and turned "contributed to a migration project" into "led the digital transformation initiative across three business units." The resume was now a masterpiece of fiction.

I stared at the output. I typed "that's not what I meant." I tried again. Same creativity. Same fabrication.

The problem wasn't intelligence. The model had plenty. The problem was language — mine.

I had said "improve" without defining what improvement means. I had left every decision to the model: what to change, how much to change it, what rules to follow, what to never do. The model made all of those decisions. Every one was wrong.

Thirty seconds of rewriting fixed it. I added five constraints: never fabricate, never inflate, flag what you can't verify, preserve the candidate's actual verbs, keep it ATS-safe. Same model. Same resume. Completely different output.

That moment — the gap between "improve this" and "improve this within these boundaries" — is what this book is about.

---

I kept seeing the same pattern everywhere. A radiologist getting wallpaper instead of summaries. A lawyer getting book reports instead of analysis. A product manager getting a list of everything instead of priorities. Smart people, capable tools, and a gap between intent and instruction that no amount of model improvement could close from the machine's side.

The people who got consistently good results weren't using secret prompts. They were doing something simpler and harder: they were choosing their words the way an engineer chooses load-bearing materials. They understood — whether they said it this way or not — that language had become executable.

This book is the result of that observation. It provides seventy-five named abstractions — the building blocks of effective prompts, agent instructions, and AI workflows. Each one is a tool with a known behavior profile. Each one comes with specific words to use, before-and-after examples from real projects, failure modes I've hit personally, and experiment data from 11,400 prompt variations across four model families.

I built ResumeForge, Clap/OpsPilot, Form8, an AI Ethics Coach, and more projects than I can count using these patterns. Karpathy's autoresearch `program.md` — a single markdown file that runs an autonomous research agent overnight — is one of the purest examples of language-as-programming I've ever seen. These aren't theoretical abstractions. They're the vocabulary I use every day.

The entries in this book are designed to work two ways. Read them straight through and they build a conceptual framework. Use them as a lookup when you need the right word for the right job. Some entries open with a story. Some lead with a table of words that work. Some hit you with a before-and-after that makes the point faster than any explanation could. I varied the format on purpose. Seventy-five entries in the same template is a textbook. Seventy-five entries that each find the best way to teach their concept is a book worth reading.

One more thing. I've included "Try This Now" exercises throughout — prompts you can paste into ChatGPT or Claude right now and see the abstraction in action. The best way to learn this material is to use it. The second-best way is to read the before-and-after examples and feel the difference.

— **Kastle Light**, 2026
