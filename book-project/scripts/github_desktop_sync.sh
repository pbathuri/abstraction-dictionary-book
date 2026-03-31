#!/usr/bin/env bash
# Sync local coding projects on Desktop with GitHub.
# Prerequisites:
#   1) brew install gh
#   2) gh auth login     OR export GH_TOKEN for non-interactive use
#
# This script does NOT push third-party clones (langchain, codex, etc.).
# It focuses on: repos under github.com/pbathuri, and no-remote projects you own.

set -euo pipefail
GH_BIN="${GH_BIN:-/opt/homebrew/bin/gh}"
DESKTOP="${DESKTOP:-$HOME/Desktop}"

if ! command -v "$GH_BIN" >/dev/null 2>&1; then
  echo "Install GitHub CLI: brew install gh"
  exit 1
fi

if ! "$GH_BIN" auth status >/dev/null 2>&1; then
  echo "Run: gh auth login"
  echo "Or set GH_TOKEN for API access (repo scope)."
  exit 1
fi

create_and_push() {
  local dir="$1"
  local name="$2"
  local visibility="${3:-private}"
  if git -C "$dir" remote get-url origin >/dev/null 2>&1; then
    echo "[$dir] already has origin; skipping create."
    return 0
  fi
  echo "[$dir] creating github.com/pbathuri/$name ($visibility) ..."
  "$GH_BIN" repo create "pbathuri/$name" \
    --"$visibility" \
    --source="$dir" \
    --remote=origin \
    --push
}

# --- Projects with no remote (update names/visibility as you like) ---
if [[ -d "$DESKTOP/Clap_OpsPilot/.git" ]]; then
  create_and_push "$DESKTOP/Clap_OpsPilot" "Clap_OpsPilot" private
fi

# Canonical ai-ethics (dedupe copies on disk before pushing)
if [[ -d "$DESKTOP/Liesure_Projects/Personal_prjs/ai-ethics-coach_v3_improved/.git" ]]; then
  create_and_push "$DESKTOP/Liesure_Projects/Personal_prjs/ai-ethics-coach_v3_improved" "ai-ethics-coach" private
fi

# Book monorepo (after git init at BOOK:LLM?)
if [[ -d "$DESKTOP/BOOK:LLM?/.git" ]]; then
  create_and_push "$DESKTOP/BOOK:LLM?" "abstraction-dictionary-book" private
fi

echo "Done. For existing pbathuri remotes with local commits: cd repo && git pull --rebase origin main && git push"
