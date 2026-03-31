#!/usr/bin/env python3
"""
Final Book Compiler

Assembles the complete Abstraction Dictionary from all components.
Outputs a single markdown file ready for Pandoc conversion.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONT_MATTER = PROJECT_ROOT / "front_matter"
ENTRIES = PROJECT_ROOT / "entries" / "drafts"
APPENDICES = PROJECT_ROOT / "appendices"
EXPORTS = PROJECT_ROOT / "exports"
EXPORTS.mkdir(parents=True, exist_ok=True)

FRONT_MATTER_ORDER = [
    "preface.md",
    "how_to_use_this_book.md",
    "editorial_method.md",
    "how_language_programs_models.md",
    "how_to_read_an_entry.md",
]

FAMILY_ORDER = [
    ("Core Abstractions", "core_abstraction"),
    ("Instructional Actions", "instructional_action"),
    ("Context Architecture", "context_architecture"),
    ("Agent Workflows", "agent_workflow"),
    ("Quality Control", "quality_control"),
    ("Tone & Style", "tone_style"),
    ("Failure Modes", "failure_mode"),
]

FAMILY_INTROS = {
    "core_abstraction": "The entries in this family name the fundamental properties of effective language when it is aimed at AI systems. These are the building blocks: the concepts you reach for when constructing any prompt, any agent instruction, any evaluation criterion. They are to language-as-programming what data types are to traditional code — the irreducible elements from which everything else is composed.",
    "instructional_action": "These entries name the verbs of language-as-programming — the operations you perform on information when you write a prompt. Each one tells the model what kind of cognitive work to do: compare, synthesize, critique, rank, filter. Choosing the right action verb is choosing the right operation. The wrong one produces a valid output to the wrong question.",
    "context_architecture": "The entries here address the structures that govern what information a model has access to and how that information is organized. Context is not just 'what you paste into the prompt.' It is an architecture — a designed environment with budgets, scaffolding, retrieval mechanisms, and signal management.",
    "agent_workflow": "These entries describe the patterns of multi-agent systems: how agents receive tasks, transfer control, verify work, escalate failures, and coordinate through shared state. If the instructional actions are the operations, the workflow entries are the control flow — the loops, branches, and exception handlers of agentic language.",
    "quality_control": "These entries name the mechanisms for ensuring that AI outputs are reliable, traceable, and improvable. They are the testing and assurance layer of language-as-programming — the rubrics, harnesses, audit trails, and verification checks that separate a prototype from a production system.",
    "tone_style": "The entries in this family address how language sounds, not just what it means. Register, authority, warmth, terseness — these are the stylistic dimensions that determine whether an output is usable by its intended audience. Getting the facts right is necessary. Getting the voice right is what makes the output actually useful.",
    "failure_mode": "These entries name the ways prompting and agent instructions break. Each failure mode is a diagnostic: a named pattern of malfunction with identifiable symptoms, known causes, and documented fixes. Knowing the failure modes is as valuable as knowing the techniques, because the failure modes tell you what to check for before you ship.",
}

APPENDIX_ORDER = [
    "model_fit_matrix.md",
    "agentic_workflow_phrasebook.md",
    "prompt_failure_modes.md",
    "verification_patterns.md",
    "abstraction_index.md",
    "further_reading.md",
    "bibliography.md",
]


def read_file(path):
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def strip_yaml_frontmatter(content):
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            return content[end + 3:].strip()
    return content


def get_entry_family(content):
    match = re.search(r'family:\s*"?(\w+)"?', content)
    return match.group(1) if match else "unclassified"


def get_entry_headword(content):
    match = re.search(r'headword:\s*"?([^"\n]+)"?', content)
    return match.group(1).strip() if match else ""


def collect_entries_by_family():
    families = {fam_id: [] for _, fam_id in FAMILY_ORDER}
    families["unclassified"] = []

    for f in sorted(ENTRIES.glob("*.md")):
        if f.name == "part_iii_applied_patterns.md":
            continue
        if f.name.endswith(".packet.json"):
            continue

        content = f.read_text(encoding="utf-8")
        family = get_entry_family(content)
        headword = get_entry_headword(content)
        stripped = strip_yaml_frontmatter(content)

        target_family = family if family in families else "unclassified"
        families[target_family].append((headword, stripped))

    for fam_id in families:
        families[fam_id].sort(key=lambda x: x[0].lower())

    return families


def build_manuscript():
    parts = []

    parts.append("---\n")
    parts.append("title: The Abstraction Dictionary\n")
    parts.append("subtitle: Natural Language as the New Programming Language\n")
    parts.append("date: 2026\n")
    parts.append("lang: en\n")
    parts.append("toc: true\n")
    parts.append("toc-depth: 2\n")
    parts.append("---\n\n")

    parts.append("\\newpage\n\n")
    parts.append("# Part I: How to Read This Book\n\n")
    for fname in FRONT_MATTER_ORDER:
        content = read_file(FRONT_MATTER / fname)
        parts.append(content)
        parts.append("\n\n\\newpage\n\n")

    parts.append("# Part II: The Abstraction Dictionary\n\n")
    families = collect_entries_by_family()

    for family_name, family_id in FAMILY_ORDER:
        entries = families.get(family_id, [])
        if not entries:
            continue

        parts.append(f"## {family_name}\n\n")
        intro = FAMILY_INTROS.get(family_id, "")
        if intro:
            parts.append(f"{intro}\n\n")
        parts.append("---\n\n")

        for headword, content in entries:
            parts.append(content)
            parts.append("\n\n---\n\n")

    parts.append("\\newpage\n\n")
    parts.append("# Part III: Applied Patterns\n\n")
    part_iii = read_file(ENTRIES / "part_iii_applied_patterns.md")
    if part_iii:
        parts.append(strip_yaml_frontmatter(part_iii))
    parts.append("\n\n\\newpage\n\n")

    parts.append("# Part IV: Reference Appendices\n\n")
    for fname in APPENDIX_ORDER:
        content = read_file(APPENDICES / fname)
        if content:
            parts.append(content)
            parts.append("\n\n\\newpage\n\n")

    return "".join(parts)


def main():
    print("Compiling The Abstraction Dictionary...")

    manuscript = build_manuscript()
    word_count = len(manuscript.split())
    page_estimate = word_count // 275

    md_path = EXPORTS / "The_Abstraction_Dictionary.md"
    md_path.write_text(manuscript, encoding="utf-8")
    print(f"Markdown exported: {md_path}")
    print(f"Word count: {word_count:,}")
    print(f"Estimated pages: {page_estimate}")

    manifest = {
        "title": "The Abstraction Dictionary",
        "subtitle": "Natural Language as the New Programming Language",
        "compiled_at": datetime.now().isoformat(),
        "word_count": word_count,
        "page_estimate": page_estimate,
        "entry_count": sum(
            len(entries)
            for entries in collect_entries_by_family().values()
        ),
        "parts": {
            "front_matter": len(FRONT_MATTER_ORDER),
            "dictionary_entries": "by family",
            "applied_patterns": 6,
            "appendices": len(APPENDIX_ORDER),
        },
    }

    manifest_path = EXPORTS / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest: {manifest_path}")

    print("\nCompilation complete.")


if __name__ == "__main__":
    main()
