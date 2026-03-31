#!/usr/bin/env python3
"""
Book Compiler

Assembles front matter + entries + appendices into final manuscript.
Exports markdown first, then epub/pdf via Pandoc.

Usage:
    python scripts/compile_book.py --format markdown
    python scripts/compile_book.py --format epub
    python scripts/compile_book.py --format pdf
    python scripts/compile_book.py --format all
"""

import argparse
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONT_MATTER = PROJECT_ROOT / "front_matter"
ENTRIES_FINAL = PROJECT_ROOT / "entries" / "final"
APPENDICES = PROJECT_ROOT / "appendices"
EXPORTS = PROJECT_ROOT / "exports"
EXPORTS.mkdir(parents=True, exist_ok=True)

BOOK_TITLE = "The Abstraction Dictionary"
BOOK_SUBTITLE = "Natural Language as the New Programming Language"

FRONT_MATTER_ORDER = [
    "preface.md",
    "how_to_use_this_book.md",
    "editorial_method.md",
    "how_language_programs_models.md",
    "how_to_read_an_entry.md",
]

APPENDIX_ORDER = [
    "model_fit_matrix.md",
    "agentic_workflow_phrasebook.md",
    "prompt_failure_modes.md",
    "verification_patterns.md",
    "abstraction_index.md",
    "further_reading.md",
]


def read_file(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"<!-- Missing: {path} -->\n"


def collect_entries() -> list[tuple[str, str]]:
    """Collect all final entries, sorted by headword."""
    entries = []
    for f in sorted(ENTRIES_FINAL.glob("*.md")):
        headword = f.stem.replace("_", " ").title()
        content = f.read_text(encoding="utf-8")
        entries.append((headword, content))
    return entries


def build_manuscript() -> str:
    """Assemble the complete manuscript in markdown."""
    parts = []

    parts.append(f"# {BOOK_TITLE}\n\n## {BOOK_SUBTITLE}\n\n---\n\n")

    parts.append("# Part I: How to Read This Book\n\n")
    for fname in FRONT_MATTER_ORDER:
        content = read_file(FRONT_MATTER / fname)
        parts.append(content)
        parts.append("\n\n---\n\n")

    parts.append("# Part II: The Abstraction Dictionary\n\n")
    entries = collect_entries()
    if entries:
        for headword, content in entries:
            parts.append(content)
            parts.append("\n\n---\n\n")
    else:
        parts.append("*Entries pending. See entries/final/ for completed entries.*\n\n")

    parts.append("# Part III: Applied Patterns\n\n")
    parts.append("*To be written after core dictionary entries are complete.*\n\n---\n\n")

    parts.append("# Part IV: Reference Appendices\n\n")
    for fname in APPENDIX_ORDER:
        content = read_file(APPENDICES / fname)
        parts.append(content)
        parts.append("\n\n---\n\n")

    return "".join(parts)


def export_markdown(manuscript: str):
    path = EXPORTS / "abstraction-dictionary.md"
    path.write_text(manuscript, encoding="utf-8")
    print(f"Markdown exported: {path}")
    return path


def export_epub(md_path: Path):
    epub_path = EXPORTS / "abstraction-dictionary.epub"
    cmd = [
        "pandoc", str(md_path),
        "-o", str(epub_path),
        f"--metadata=title:{BOOK_TITLE}",
        f"--metadata=subtitle:{BOOK_SUBTITLE}",
        "--toc",
        "--toc-depth=2",
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"EPUB exported: {epub_path}")
    except FileNotFoundError:
        print("Pandoc not found. Install with: brew install pandoc")
    except subprocess.CalledProcessError as e:
        print(f"EPUB export failed: {e.stderr}")


def export_pdf(md_path: Path):
    pdf_path = EXPORTS / "abstraction-dictionary.pdf"
    cmd = [
        "pandoc", str(md_path),
        "-o", str(pdf_path),
        f"--metadata=title:{BOOK_TITLE}",
        "--toc",
        "--toc-depth=2",
        "--pdf-engine=xelatex",
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"PDF exported: {pdf_path}")
    except FileNotFoundError:
        print("Pandoc or xelatex not found. Install with: brew install pandoc mactex")
    except subprocess.CalledProcessError as e:
        print(f"PDF export failed: {e.stderr}")


def main():
    parser = argparse.ArgumentParser(description="Compile the Abstraction Dictionary")
    parser.add_argument("--format", choices=["markdown", "epub", "pdf", "all"], default="markdown")
    args = parser.parse_args()

    print(f"Compiling {BOOK_TITLE}...")
    manuscript = build_manuscript()
    md_path = export_markdown(manuscript)

    if args.format in ("epub", "all"):
        export_epub(md_path)
    if args.format in ("pdf", "all"):
        export_pdf(md_path)

    print("Compilation complete.")


if __name__ == "__main__":
    main()
