#!/usr/bin/env python3
"""
V2 Book Compiler — The Abstraction Dictionary by Kastle Light

Compiles the interactive v2 entries into final manuscript.
Produces TWO versions:
1. Full version (all content, all appendices)
2. Compact version (entries only, minimal appendices, <300 pages target)
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONT_MATTER = PROJECT_ROOT / "front_matter"
ENTRIES_V2 = PROJECT_ROOT / "entries" / "v2"
APPENDICES = PROJECT_ROOT / "appendices"
EXPORTS = PROJECT_ROOT / "exports"
ART = PROJECT_ROOT / "art"
EXPORTS.mkdir(parents=True, exist_ok=True)

FRONT_MATTER_ORDER = [
    "preface.md",
    "how_to_use_this_book.md",
    "how_language_programs_models.md",
    "how_to_read_an_entry.md",
    "editorial_method.md",
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
    "core_abstraction": "These are the building blocks. Reach for them when constructing any prompt, any agent instruction, any evaluation.",
    "instructional_action": "The verbs of language-as-programming. Each one tells the model what kind of work to do.",
    "context_architecture": "How you manage what information the model sees and how it's organized.",
    "agent_workflow": "How agents receive tasks, transfer control, verify work, and coordinate.",
    "quality_control": "The testing and assurance layer. Rubrics, harnesses, audit trails, verification.",
    "tone_style": "How language sounds, not just what it means. The voice that makes output usable.",
    "failure_mode": "Named ways prompts break. Know these and you'll catch problems before they ship.",
}

APPENDIX_ORDER = [
    "model_fit_matrix.md",
    "agentic_workflow_phrasebook.md",
    "prompt_failure_modes.md",
    "abstraction_index.md",
    "bibliography.md",
]

COMPACT_APPENDICES = ["abstraction_index.md", "bibliography.md"]


def read_file(path):
    return path.read_text(encoding="utf-8") if path.exists() else ""


def get_entry_family(content):
    for line in content.split("\n"):
        if "Family:" in line:
            for _, fam_id in FAMILY_ORDER:
                if fam_id.replace("_", " ") in line.lower() or fam_id.replace("_", " ").title() in line:
                    return fam_id
            lw = line.lower()
            if "core" in lw: return "core_abstraction"
            if "instruct" in lw: return "instructional_action"
            if "context" in lw: return "context_architecture"
            if "agent" in lw or "workflow" in lw: return "agent_workflow"
            if "quality" in lw: return "quality_control"
            if "tone" in lw or "style" in lw: return "tone_style"
            if "failure" in lw: return "failure_mode"
    return "unclassified"


def get_headword(content):
    for line in content.split("\n"):
        if line.startswith("# ") and not line.startswith("## "):
            return line[2:].strip()
    return ""


def collect_v2_entries():
    families = {fam_id: [] for _, fam_id in FAMILY_ORDER}
    families["unclassified"] = []

    for f in sorted(ENTRIES_V2.glob("*.md")):
        if f.name == "part_iii_applied_patterns.md":
            continue
        content = f.read_text(encoding="utf-8")
        family = get_entry_family(content)
        headword = get_headword(content)
        families[family].append((headword, content))

    for fam_id in families:
        families[fam_id].sort(key=lambda x: x[0].lower())

    return families


def build_manuscript(compact=False):
    parts = []

    parts.append("---\n")
    parts.append("title: The Abstraction Dictionary\n")
    parts.append("subtitle: Natural Language as the New Programming Language\n")
    parts.append("author: Kastle Light\n")
    parts.append("date: 2026\n")
    parts.append("lang: en\n")
    parts.append("toc: true\n")
    parts.append("toc-depth: 2\n")
    parts.append("---\n\n")

    parts.append("\\newpage\n\n")
    parts.append("# Part I: How to Read This Book\n\n")
    fm_files = FRONT_MATTER_ORDER if not compact else FRONT_MATTER_ORDER[:3]
    for fname in fm_files:
        content = read_file(FRONT_MATTER / fname)
        if content:
            parts.append(content)
            parts.append("\n\n\\newpage\n\n")

    parts.append("# Part II: The Abstraction Dictionary\n\n")
    families = collect_v2_entries()

    for family_name, family_id in FAMILY_ORDER:
        entries = families.get(family_id, [])
        if not entries:
            continue
        parts.append(f"## {family_name}\n\n")
        intro = FAMILY_INTROS.get(family_id, "")
        if intro:
            parts.append(f"*{intro}*\n\n")
        parts.append("---\n\n")
        for headword, content in entries:
            parts.append(content)
            parts.append("\n\n---\n\n")

    parts.append("\\newpage\n\n")
    parts.append("# Part III: Applied Patterns\n\n")
    part_iii = read_file(ENTRIES_V2 / "part_iii_applied_patterns.md")
    if part_iii:
        parts.append(part_iii)
    parts.append("\n\n\\newpage\n\n")

    parts.append("# Part IV: Reference Appendices\n\n")
    app_list = COMPACT_APPENDICES if compact else APPENDIX_ORDER
    for fname in app_list:
        content = read_file(APPENDICES / fname)
        if content:
            parts.append(content)
            parts.append("\n\n\\newpage\n\n")

    return "".join(parts)


def export_markdown(manuscript, name):
    path = EXPORTS / f"{name}.md"
    path.write_text(manuscript, encoding="utf-8")
    print(f"  Markdown: {path} ({len(manuscript.split()):,} words)")
    return path


def export_epub(md_path, name, cover=None):
    import subprocess
    epub_path = EXPORTS / f"{name}.epub"
    cmd = [
        "pandoc", str(md_path),
        "-o", str(epub_path),
        "--metadata", "title=The Abstraction Dictionary",
        "--metadata", "author=Kastle Light",
        "--toc", "--toc-depth=2",
    ]
    if cover and Path(cover).exists():
        cmd.extend(["--epub-cover-image", str(cover)])
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        size_mb = epub_path.stat().st_size / (1024 * 1024)
        print(f"  EPUB: {epub_path} ({size_mb:.1f} MB)")
    except Exception as e:
        print(f"  EPUB failed: {e}")


def export_pdf(md_path, name):
    import subprocess
    pdf_path = EXPORTS / f"{name}.pdf"
    cmd = [
        "pandoc", str(md_path),
        "-o", str(pdf_path),
        "--toc", "--toc-depth=2",
        "--pdf-engine=xelatex",
        "-V", "geometry:margin=1in",
        "-V", "fontsize=11pt",
        "-V", "documentclass=book",
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=300)
        size_mb = pdf_path.stat().st_size / (1024 * 1024)
        print(f"  PDF: {pdf_path} ({size_mb:.1f} MB)")
        return pdf_path
    except Exception as e:
        print(f"  PDF failed: {e}")
        return None


def export_html(md_path, name):
    import subprocess
    html_path = EXPORTS / f"{name}.html"
    cmd = [
        "pandoc", str(md_path),
        "-o", str(html_path),
        "--standalone", "--toc", "--toc-depth=2",
        "--metadata", "title=The Abstraction Dictionary",
        "--metadata", "author=Kastle Light",
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        size_mb = html_path.stat().st_size / (1024 * 1024)
        print(f"  HTML: {html_path} ({size_mb:.1f} MB)")
    except Exception as e:
        print(f"  HTML failed: {e}")


def count_pdf_pages(pdf_path):
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        count = doc.page_count
        doc.close()
        return count
    except:
        return "unknown"


def main():
    cover = ART / "covers" / "front_cover_v2.png"
    print("=" * 60)
    print("THE ABSTRACTION DICTIONARY — V2 Compiler")
    print("Author: Kastle Light")
    print("=" * 60)

    # Full version
    print("\n[FULL VERSION]")
    full = build_manuscript(compact=False)
    md_full = export_markdown(full, "Abstraction_Dictionary_Full")
    export_epub(md_full, "Abstraction_Dictionary_Full", cover)
    export_html(md_full, "Abstraction_Dictionary_Full")
    pdf_full = export_pdf(md_full, "Abstraction_Dictionary_Full")
    if pdf_full:
        pages = count_pdf_pages(pdf_full)
        print(f"  Pages: {pages}")

    # Compact version
    print("\n[COMPACT VERSION]")
    compact = build_manuscript(compact=True)
    md_compact = export_markdown(compact, "Abstraction_Dictionary_Compact")
    export_epub(md_compact, "Abstraction_Dictionary_Compact", cover)
    export_html(md_compact, "Abstraction_Dictionary_Compact")
    pdf_compact = export_pdf(md_compact, "Abstraction_Dictionary_Compact")
    if pdf_compact:
        pages = count_pdf_pages(pdf_compact)
        print(f"  Pages: {pages}")

    # Manifest
    manifest = {
        "title": "The Abstraction Dictionary",
        "author": "Kastle Light",
        "compiled_at": datetime.now().isoformat(),
        "full_version": {"word_count": len(full.split()), "format": ["md", "epub", "html", "pdf"]},
        "compact_version": {"word_count": len(compact.split()), "format": ["md", "epub", "html", "pdf"]},
        "entry_count": sum(len(v) for v in collect_v2_entries().values()),
        "experiment_data_points": 11400,
        "charts": len(list((ART / "figures").glob("*.png"))),
    }
    with open(EXPORTS / "manifest_v2.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n{'=' * 60}")
    print("COMPILATION COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
