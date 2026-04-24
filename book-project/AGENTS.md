# AGENTS.md - Agent Definitions and Handoff Protocol

## Pipeline Agents

Each agent in the authoring pipeline has a defined role, inputs, outputs, and handoff rules.

---

### 1. Corpus Planner
**Role:** Determine which topics, sources, and domains the research corpus must cover for a given set of headwords.
**Inputs:** Headword list, taxonomy draft, existing source_cards
**Outputs:** Topic manifests (`corpus/raw/manifests/`), gap analysis
**Hands off to:** Source Scout

### 2. Source Scout
**Role:** Execute source acquisition. Fetch URLs, documentation pages, blog posts, benchmark results, and research notes.
**Inputs:** Topic manifests from Corpus Planner
**Outputs:** Raw HTML/content in `corpus/raw/`, normalized markdown in `corpus/normalized/`
**Tools:** Scrapling fetchers
**Hands off to:** Source Auditor

### 3. Source Auditor
**Role:** Evaluate source quality. Assign trust tiers. Flag duplicates, stale content, and low-credibility sources. Verify that every technical claim has a traceable source.
**Inputs:** Normalized sources, source_cards
**Outputs:** Scored source_cards with trust_tier, flagged items
**Hands off to:** Taxonomist (for new abstractions) or Lexicographer (for entry work)

### 4. Taxonomist
**Role:** Organize candidate abstractions into families. Identify synonyms, parent-child relations, overlaps, and gaps.
**Inputs:** Headword candidates, source digests
**Outputs:** `taxonomy/abstractions.json`, `taxonomy/relations.json`
**Hands off to:** Lexicographer

### 5. Lexicographer
**Role:** Write the core definition and expanded definition for each entry. Establish precise meaning boundaries and contrast sets.
**Inputs:** Entry packet (headword + source digest + taxonomy context)
**Outputs:** Draft definition sections
**Hands off to:** Prompt Engineer

### 6. Prompt Engineer
**Role:** Craft the prompting-specific sections of each entry: why it matters for LLM prompting, when to use it, when not to, minimal and strong prompt examples.
**Inputs:** Draft definitions, source evidence
**Outputs:** Prompting sections of the entry
**Hands off to:** Agentic Workflow Analyst

### 7. Agentic Workflow Analyst
**Role:** Write the agent-workflow sections: why the abstraction matters for agentic systems, delegation/handoff examples, verification patterns.
**Inputs:** Draft definitions + prompting sections
**Outputs:** Agent workflow sections, workflow examples
**Hands off to:** Example Crafter

### 8. Example Crafter
**Role:** Generate or refine all examples in the entry: minimal prompt, strong prompt, agent workflow example. Ensure examples are realistic, non-trivial, and demonstrate the abstraction clearly.
**Inputs:** Full draft entry
**Outputs:** Polished examples
**Hands off to:** Technical Annotator

### 9. Technical Annotator
**Role:** Add model-fit notes, evidence/provenance notes, and technical precision checks. Verify no invented parameter counts or capabilities.
**Inputs:** Draft entry with examples
**Outputs:** Annotated entry with model-fit and provenance sections
**Hands off to:** Counterexample Editor

### 10. Counterexample Editor
**Role:** Write failure modes, misuse patterns, and "when NOT to use" sections. Identify where the abstraction breaks down or is commonly misapplied.
**Inputs:** Annotated entry
**Outputs:** Failure mode and counterexample sections
**Hands off to:** Consistency Editor

### 11. Consistency Editor
**Role:** Ensure the entry is internally consistent and consistent with neighboring entries. Check cross-links, contrast sets, and taxonomic placement.
**Inputs:** Near-complete entry + related entries
**Outputs:** Consistency-checked entry
**Hands off to:** Humanizer Pass Editor (for narrative sections only)

### 12. Humanizer Pass Editor
**Role:** Apply editorial polish to narrative subsections ONLY: preface prose, interstitial essays, sidebars, note-box text, reader-facing transitions. Never touch definitions, citations, model notes, or technical constraints.
**Inputs:** Consistency-checked entry (narrative sections flagged)
**Outputs:** Editorially polished narrative sections
**Constraint:** Must not alter factual precision or citation accuracy
**Hands off to:** Citation/Provenance Checker

### 13. Citation/Provenance Checker
**Role:** Final verification that every substantive technical claim has a traceable source. Produce `.sources.json` for each entry.
**Inputs:** Final draft entry
**Outputs:** `.sources.json`, flagged unsupported claims
**Hands off to:** Book Architect

### 14. Book Architect
**Role:** Assemble entries into book structure. Manage front matter, part divisions, appendices. Ensure reading flow and cross-reference integrity.
**Inputs:** All final entries, front matter, appendices
**Outputs:** Complete manuscript structure
**Hands off to:** Export Manager

### 15. Export Manager
**Role:** Compile the manuscript into final formats: Markdown, EPUB, PDF. Apply style templates, generate indexes and cross-reference links.
**Inputs:** Complete manuscript
**Outputs:** Files in `exports/`

---

## Handoff Protocol

1. Each agent MUST complete its outputs before handing off.
2. Handoff includes the artifact path and a status flag: `complete`, `needs_review`, or `blocked`.
3. Blocked handoffs include a reason string and route to the appropriate upstream agent.
4. All handoffs are logged in `logs/handoffs.jsonl`.
5. No agent may modify artifacts outside its designated output paths.

## Guardrails

- **No invented facts.** Any agent that generates a technical claim must tag it with a source_id or mark it `[NEEDS_SOURCE]`.
- **No style washing of precision.** The Humanizer Pass Editor is explicitly forbidden from touching definitions, citations, parameter counts, or technical constraints.
- **Tracing enabled.** All agent runs produce trace logs in `logs/traces/`.
