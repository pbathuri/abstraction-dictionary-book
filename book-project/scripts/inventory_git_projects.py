#!/usr/bin/env python3
"""
Scan Desktop (and optional extra roots) for git repositories, classify remotes,
and skip vendored / upstream training corpora / external deps.
Outputs TSV to stdout.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# Paths under these are treated as vendored / not "your project to publish as new"
SKIP_PREFIXES = (
    "/external/",
    "/Agentic_workflow_train_sample/",
    "/node_modules/",
    "/.venv/",
    "/venv/",
    "/site-packages/",
)

# Top-level Desktop dirs that are only third-party mirrors (optional; tune per machine)
SKIP_DIR_NAMES = frozenset()


def run_git(repo: Path, *args: str) -> tuple[int, str]:
    try:
        p = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as e:
        return 1, str(e)


def should_skip(git_dir: Path) -> str | None:
    s = str(git_dir)
    for pref in SKIP_PREFIXES:
        if pref in s:
            return f"skip:contains:{pref}"
    parts = git_dir.parts
    if "external" in parts:
        return "skip:external"
    if "Agentic_workflow_train_sample" in parts:
        return "skip:train_sample_corpus"
    return None


def find_git_roots(root: Path, maxdepth: int = 8) -> list[Path]:
    roots: list[Path] = []
    root = root.resolve()
    for dirpath, dirnames, _filenames in os.walk(root):
        depth = len(Path(dirpath).relative_to(root).parts)
        if depth > maxdepth:
            dirnames[:] = []
            continue
        if ".git" in dirnames:
            roots.append(Path(dirpath))
            dirnames[:] = [d for d in dirnames if d != ".git"]
    return roots


def parse_remote_github(out: str) -> list[tuple[str, str]]:
    """Return list of (name, github-owner/repo or empty)."""
    remotes: list[tuple[str, str]] = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        name, url = parts[0], parts[1]
        if "github.com" not in url:
            continue
        u = url.replace("git@", "https://").replace("https://github.com/", "").replace(".git", "")
        u = u.split("/")
        if len(u) >= 2:
            remotes.append((name, f"{u[0]}/{u[1]}"))
    return remotes


def main() -> int:
    roots = [Path(p).expanduser() for p in sys.argv[1:]] or [Path("/Users/prady/Desktop")]
    all_roots: dict[str, Path] = {}
    for r in roots:
        if not r.is_dir():
            continue
        for git_parent in find_git_roots(r):
            git_dir = git_parent / ".git"
            reason = should_skip(git_parent)
            if reason:
                continue
            key = str(git_parent.resolve())
            all_roots[key] = git_parent

    print(
        "path\tbranch\tremote_names\tdirty_summary\tgithub_remotes\tskip_reason"
    )
    for path in sorted(all_roots.values(), key=lambda p: str(p).lower()):
        rc, out = run_git(path, "remote", "-v")
        remotes_raw = out.strip()
        gh = parse_remote_github(remotes_raw)
        gh_s = ";".join(f"{a}:{b}" for a, b in gh) if gh else ""

        rc2, br = run_git(path, "branch", "--show-current")
        branch = br.strip() or "(detached)"

        rc3, st = run_git(path, "status", "--porcelain")
        dirty = "clean" if not st.strip() else "dirty"

        print(f"{path}\t{branch}\t{remotes_raw.replace(chr(9), ' ')}\t{dirty}\t{gh_s}\t")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
