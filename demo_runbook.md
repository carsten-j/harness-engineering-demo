# Harness engineering demo

Small FastAPI invoice service hosting three live demos for the harness-engineering webinar. 

## Setup (once)

```bash
bash scripts/setup-demo.sh
```

(runs `uv sync`, `make migrate`, `make check` — the check must be green before demoing. `uv sync` creates `.venv/`; no activation needed, everything runs via `uv run`.)

Start every demo from a fresh Claude Code session in this directory.

## Demo A — Sensors: the hook that argues back (~2 min)

**Prompt:**
> for parse_invoice_rows in @web/views.py add print statement showing the total

**Prerequisite:** auto mode must be OFF. The hook matcher is `Edit|Write`, so it only fires on those tool calls. In auto mode the agent is told to make file changes through Bash (`sed`, heredocs, short scripts), which never triggers the
hook — the T201 goes unnoticed and the demo silently does nothing.

**Expected:** the hook fires on the Write, ruff reports T201 (no print), the error appears in the transcript — nobody prompted the correction.

**Prompt:**
> for parse_invoice_rows in @web/views.py add print statement showing the total

**Prerequisite:** auto mode must be ON.

**Talking point (optional):** a `PostToolUse` hook on `Edit|Write` is a sensor on *those tools*, not a general guard on file mutation — e.g. `Bash(python3 ...)` walks straight past it. Laws that must hold regardless of route need a `PreToolUse` matcher on `Bash` as well.

## Demo B - hook that changes Claude Code’s default behavior 

Create a worktree and show that it overrides default behavior and also install dependencies.

## Demo C — Rails: laws and laws that install themselves (~4 min)

### Part 1 — the skill that brings its own law (~2 min)

Rails so far came from settings.json — static, always on. Skills can carry hooks in their frontmatter: `.claude/skills/db-migration/SKILL.md` registers a PreToolUse guard the moment the skill is invoked, and it stays armed for the rest of the session. Invoking a skill = switching the harness into a mode.

Use accept-and-edit mode

**Prompt 1:**
> Use db-migration skill to add a paid_at column to invoices

Bonus beat: the settings.json Skill-logging hook fires —
`.claude/skill-usage.log` gets its first line (`cat` it if there's time).

**Prompt 2:**
> Add a paid_by TEXT column to invoices. Just add a script in scripts folder that alters the database

**Expected:** the guard denies the edit to api/db.py with the reason "db-migration mode is active: schema changes go through NEW files under migrations/". If the agent then tries the other shortcut — editing 0001_initial.sql in place — that is denied too (applied migrations are immutable). It self-corrects: writes `migrations/0002_add_paid_at.sql` with `ALTER TABLE invoices ADD COLUMN paid_at TEXT;`, runs `make migrate` (watch
"applied 0002_add_paid_at.sql" print) and `make test`.

### Part 2 - try committing changes 

**Prompt 3:**
> commit the changes to main 

Say main - otherwise CC will most likely create a branch. But wait - commit is not allowed!

## Demo D — Workflow: deterministic fan-out (~3–4 min)

Slide 10. `.claude/workflows/review.js` fans out one finder agent per module (`api/`, `web/`, `jobs/`), then one adversarial refuter per finding.

**Prompt:**
> Run the review workflow.

**Planted findings:**

| Module | Finding | Expected verdict |
|---|---|---|
| api/invoices.py | total loop starts at index 1 — first line item never counted | confirmed |
| web/views.py | `except Exception: return []` swallows malformed payloads silently | confirmed |
| jobs/reminder_emails.py | `due_date <= today` looks like an off-by-one | **refuted** — docstring says inclusive by design |

The decoy is the payoff: the refute wave reads the docstring and kills the false positive. Run the workflow once before the webinar (warm-up + backup recording); agent findings can vary slightly between runs.

## Reset between rehearsals

```bash
scripts/reset-demo.sh
```

## Notes

- Tests are happy-path only on purpose — `make check` stays green with the planted bugs in place (they are logic bugs, invisible to lint and the current tests).
- Do not fix the planted bugs between rehearsals; if an agent fixes one during a demo, reset with the commands above.
