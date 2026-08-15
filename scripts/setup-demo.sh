#!/usr/bin/env bash
# One-time setup before rehearsing or presenting: install deps into .venv/
# (created by uv sync, no manual activation needed — everything runs via
# `uv run`), create the local SQLite schema, and verify the repo is green.
set -euo pipefail

cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"

echo "==> uv sync (creates .venv/ and installs locked dependencies)"
uv sync

echo "==> make migrate (apply migrations to local invoices.sqlite3)"
make migrate

echo "==> make check (format + lint + tests — must be green before demoing)"
make check

echo "==> setup complete"
