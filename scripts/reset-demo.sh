#!/usr/bin/env bash
# Reset the repo between rehearsals: discard demo edits, drop the local DB.
# Deliberately leaves invoices.sqlite3 absent — Demo B ends with `make migrate`.
set -euo pipefail

cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"

echo "==> discarding tracked changes"
git checkout -- .

echo "==> removing untracked files in api web jobs tests migrations"
git clean -fd api web jobs tests migrations

echo "==> removing invoices.sqlite3"
rm -f invoices.sqlite3

echo "==> removing .claude/skill-usage.log and .claude/lint-hook.log"
rm -f .claude/skill-usage.log .claude/lint-hook.log

echo "==> reset complete"
