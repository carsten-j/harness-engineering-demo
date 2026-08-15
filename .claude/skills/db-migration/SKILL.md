---
name: db-migration
description: Safe schema-change mode for the invoice database. Use when adding,
  removing, or altering columns/tables. Installs a guard that only permits new
  numbered migration files.
hooks:
  PreToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "python3 \"${CLAUDE_PROJECT_DIR}/.claude/hooks/migration-guard.py\""
---

# Database migration mode

You are making a schema change. The migration discipline in this repo:

1. Never change the schema by editing application code (`api/db.py` defines
   the runner, not the schema) and never edit an existing file under
   `migrations/` — applied migrations are immutable.
2. Write ONE new file `migrations/NNNN_short_name.sql`, where NNNN is the
   highest existing number plus one (zero-padded, e.g. `0002_add_paid_at.sql`).
   Plain SQL only. Use the Write tool, not shell redirection.
3. Apply it with `make migrate` (idempotent; prints each newly applied file).
4. Run `make test` and confirm green.
5. If application code must learn about the new column, propose that as a
   separate follow-up — do not bundle it into this mode.

A PreToolUse guard enforces rules 1–2 for the rest of this session: any
Edit/Write outside a new numbered migration file will be denied.
