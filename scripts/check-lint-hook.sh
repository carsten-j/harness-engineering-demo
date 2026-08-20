#!/usr/bin/env bash
# Demo A smoke test: feed the lint hook a PostToolUse payload by hand and show
# what the agent would see. Expect the banner, F401, exit=2, and a FAIL line.
set -uo pipefail

cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
export CLAUDE_PROJECT_DIR="$PWD"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
printf 'import os\n' > "$tmp/draft.py"

echo "==> firing .claude/hooks/lint.py on a file with an unused import"
echo "{\"tool_input\":{\"file_path\":\"$tmp/draft.py\"}}" | python3 .claude/hooks/lint.py
echo "exit=$?  (2 = the agent gets the error back)"

echo "==> tail of .claude/lint-hook.log"
tail -n 3 .claude/lint-hook.log
