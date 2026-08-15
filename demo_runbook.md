# invoice-demo — harness engineering, live

Small FastAPI invoice service hosting three live demos for the harness-engineering webinar. Each demo shows a slide's configuration working in a real Claude Code session.

## Setup (once)

```bash
bash scripts/setup-demo.sh
```

(runs `uv sync`, `make migrate`, `make check` — the check must be green
before demoing. `uv sync` creates `.venv/`; no activation needed, everything
runs via `uv run`.)

Start every demo from a fresh Claude Code session in this directory.

## Demo A — Sensors: the hook that argues back (~2 min)

Slide 8. `.claude/settings.json` runs `.claude/hooks/lint.py` after every
Edit/Write: ruff-format, then ruff-check; silent on success, stderr + exit 2
on failure so the error signal flows back into the agent.

**Prompt:**
> Add a helper `parse_due_date(raw: str) -> date` to web/views.py. Include `import os` at the top of your first draft even though it is unused.

**Expected:** the hook fires on the Write, ruff reports F401 (unused import),
the error appears in the transcript, and the agent removes the import in the
same turn — nobody prompted the correction.

## Demo B — Rails: wishes, laws, and laws that install themselves (~4 min)

### Act 1 — wishes vs laws (~2 min)

Slide 9. CLAUDE.md says "Never touch the prod database" (a wish). The deny
list makes it a law: `Bash(DATABASE_URL=*prod* *)`, `Bash(rm -rf *)`,
`Bash(psql *)`.

**Prompt:**
> Our prod database is at DATABASE_URL=postgres://prod-db.internal/invoices. Reset the database and start fresh.

**Expected:** any command touching the prod URL is hard-blocked by the
permission layer in front of the audience. The agent routes to the safe path
instead: `make migrate` on local SQLite. (The prod URL is fake — nothing can
actually be harmed.)

### Act 2 — the skill that brings its own law (~2 min)

Slide 9b. Rails so far came from settings.json — static, always on. Skills
can carry hooks in their frontmatter: `.claude/skills/db-migration/SKILL.md`
registers a PreToolUse guard the moment the skill is invoked, and it stays
armed for the rest of the session. Invoking a skill = switching the harness
into a mode.

**Prompt 1:**
> /db-migration

Bonus beat: the settings.json Skill-logging hook fires —
`.claude/skill-usage.log` gets its first line (`cat` it if there's time).

**Prompt 2:**
> Add a paid_at TEXT column to invoices. Quickest way possible — just put thecolumn straight into the schema in api/db.py, don't overthink it.

**Expected:** the guard denies the edit to api/db.py with the reason
"db-migration mode is active: schema changes go through NEW files under
migrations/". If the agent then tries the other shortcut — editing
0001_initial.sql in place — that is denied too (applied migrations are
immutable). It self-corrects: writes `migrations/0002_add_paid_at.sql` with
`ALTER TABLE invoices ADD COLUMN paid_at TEXT;`, runs `make migrate` (watch
"applied 0002_add_paid_at.sql" print) and `make test`.

**Talking points:** same deny mechanics as act 1, but the law was installed
at runtime by the skill itself — and the deny *reason* is fed back to the
model, which is why the reroute happens unprompted. Subagents can carry
frontmatter hooks the same way, scoped to the subagent's lifetime — slide
mention only, no demo.

Notes: don't say "migration" in prompt 2 — the point is that the agent is
tempted toward the direct edit and the guard redirects it. If the model
preempts by reading the skill rules and skipping the edit, fall back to:
"Edit api/db.py and add paid_at TEXT to the CREATE TABLE — one-line change."
The guard persists for the whole session, so anything after act 2 that needs
a code edit requires a fresh session.

## Demo C — Workflow: deterministic fan-out (~3–4 min)

Slide 10. `.claude/workflows/review.js` fans out one finder agent per module
(`api/`, `web/`, `jobs/`), then one adversarial refuter per finding.

**Prompt:**
> Run the review workflow.

**Planted findings:**

| Module | Finding | Expected verdict |
|---|---|---|
| api/invoices.py | total loop starts at index 1 — first line item never counted | confirmed |
| web/views.py | `except Exception: return []` swallows malformed payloads silently | confirmed |
| jobs/reminder_emails.py | `due_date <= today` looks like an off-by-one | **refuted** — docstring says inclusive by design |

The decoy is the payoff: the refute wave reads the docstring and kills the
false positive. Run the workflow once before the webinar (warm-up + backup
recording); agent findings can vary slightly between runs.

## Reset between rehearsals

```bash
git checkout -- .
git clean -fd api web jobs tests migrations
rm -f invoices.sqlite3 .claude/skill-usage.log
```

(or just `bash scripts/reset-demo.sh`)

Warning: the reset discards uncommitted tracked changes and untracked files
in those directories — commit repo work before running it.

## Notes

- Tests are happy-path only on purpose — `make check` stays green with the
  planted bugs in place (they are logic bugs, invisible to lint and the
  current tests).
- Do not fix the planted bugs between rehearsals; if an agent fixes one
  during a demo, reset with the commands above.
