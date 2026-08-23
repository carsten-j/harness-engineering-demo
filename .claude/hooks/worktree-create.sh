#!/usr/bin/env bash
# WorktreeCreate hook — replaces Claude Code's built-in `git worktree` logic
# (this event is a replacement, not an after-creation notification), then
# provisions the new tree with scripts/setup-demo.sh.
#
# Contract: stdout must contain ONLY the created worktree's path, which Claude
# Code uses as the session's working directory. So stash the real stdout on fd 3
# and point fd 1 at stderr — that way nothing below, including setup-demo.sh's
# own echoes and all of uv/ruff/pytest, can corrupt the path.
exec 3>&1 1>&2

input=$(cat)
name=$(jq -r '.name // empty' <<<"$input")
[[ -n "$name" ]] || { echo "worktree-create: hook payload has no .name"; exit 1; }

# The payload carries only .name and .cwd, so derive the rest ourselves.
# CLAUDE_PROJECT_DIR deliberately stays in the main checkout — what git -C wants.
repo=${CLAUDE_PROJECT_DIR:-$(jq -r '.cwd // empty' <<<"$input")}
repo=${repo:-$(git rev-parse --show-toplevel)}
path="$repo/.claude/worktrees/$name"
branch="worktree-$name"

# Reusing a name opens the existing worktree; don't re-provision it.
if [[ -d "$path" ]]; then
  echo "worktree-create: reusing existing worktree $path"
  echo "$path" >&3
  exit 0
fi

# baseRef "fresh" (the default): the default branch on the remote, else local HEAD.
base=$(git -C "$repo" rev-parse --verify --quiet origin/HEAD) || base=HEAD

mkdir -p "$(dirname "$path")"
if git -C "$repo" show-ref --verify --quiet "refs/heads/$branch"; then
  # Branch outlived an earlier worktree of the same name; reuse it.
  git -C "$repo" worktree add "$path" "$branch" || exit 1
else
  git -C "$repo" worktree add -b "$branch" "$path" "$base" || exit 1
fi

# A fresh checkout has no .venv/ or invoices.sqlite3 — both gitignored. Invoke the
# worktree's own copy so setup-demo.sh's `git rev-parse --show-toplevel` resolves
# to the worktree instead of the main checkout. Setup failure must not abort
# creation: a red base branch would otherwise make worktrees uncreatable.
if ! "$path/scripts/setup-demo.sh"; then
  echo "worktree-create: setup-demo.sh failed in $path"
  echo "worktree-create: worktree created anyway — run scripts/setup-demo.sh there manually"
fi

echo "$path" >&3
