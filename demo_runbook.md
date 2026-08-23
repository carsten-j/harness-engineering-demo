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
on failure so the error signal flows back into the agent. Every invocation —
pass or fail — appends one line to `.claude/lint-hook.log`.

**Prompt:**
> Add a helper `parse_due_date(raw: str) -> date | None` to web/views.py. Include `import os` at the top of your first draft even though it is unused.

**Prerequisite:** auto mode must be OFF. The hook matcher is `Edit|Write`, so
it only fires on those tool calls. In auto mode the agent is told to make file
changes through Bash (`sed`, heredocs, short scripts), which never triggers the
hook — the F401 goes unnoticed and the demo silently does nothing.

**Expected:** the hook fires on the Write, ruff reports F401 (unused import),
the error appears in the transcript, and the agent removes the import in the
same turn — nobody prompted the correction.

**Showing the hook fired.** Three levels, use whichever the room needs:

1. *On screen, unprompted.* Claude Code labels the failure itself —
   `PostToolUse:Edit hook blocking error` — and ruff's output arrives behind
   the banner `── PostToolUse hook: .claude/hooks/lint.py ──`. Read the banner
   out loud; it is the whole demo in one line.
2. *The audit log.* The failure is loud, the success is silent — so the log is
   what proves the sensor runs on **every** edit, not just broken ones:

   ```bash
   cat .claude/lint-hook.log
   ```

   ```txt
   2026-08-20T12:52:28Z    FAIL F401    web/views.py
   2026-08-20T12:52:41Z    PASS         web/views.py
   ```

   Two lines, one prompt: the sensor fired twice, the agent's fix is confirmed
   green by the same gate that rejected the draft.
3. *The raw event.* `Ctrl-R` expands the transcript entry to the full hook
   stderr if someone asks what the model actually saw.

**Smoke test before going on stage** (fires the hook by hand, no session
needed — expect the banner, `exit=2`, and a new FAIL line in the log):

```bash
bash scripts/check-lint-hook.sh
```

**Talking point (optional):** a `PostToolUse` hook on `Edit|Write` is a sensor
on *those tools*, not a general guard on file mutation — `Bash(python3 ...)`
walks straight past it. Laws that must hold regardless of route need a
`PreToolUse` matcher on `Bash` as well, the way the db-migration guard in
demo B does it.

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
> Use the db-migration skill to add a paid_at column to invoices.

Bonus beat: the settings.json Skill-logging hook fires —
`.claude/skill-usage.log` gets its first line (`cat` it if there's time).

**Prompt 2:**
> Add a paid_by TEXT column to invoices. Quickest way possible — just put the column straight into the schema in api/db.py, don't overthink it.

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
rm -f invoices.sqlite3 .claude/skill-usage.log .claude/lint-hook.log
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
