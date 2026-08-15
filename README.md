# Kod med AI (4): Harness Engineering

Live-demo material for the webinar **Kod med AI (4): Harness Engineering**.

📅 26 August 2026, 16:00–16:45 · Online · Danish · Free
🔗 <https://ida.dk/arrangementer-og-kurser/arrangementer/kod-med-ai-4-harness-engineering-367935>

Organised by IDA AI. Presented by Carsten Jørgensen (Eksponent), hosted by
Simon Amtoft Pedersen.

## What the webinar is about

Harness engineering is the design of the system *around* the model. The talk
walks through seven harness components — guides, sensors, rails, scaffolds,
exemplars, mirrors, throttles — and borrows from control theory to treat
prompts, tools, sandboxes, permissions and feedback loops as one control
system rather than a pile of settings.

## What this repo is

A deliberately small FastAPI + SQLite invoice service, existing only so that
three of those components can be demonstrated running for real in a Claude
Code session rather than described on a slide:

| Demo | Topic | What the audience sees |
|---|---|---|
| A | Sensors | A lint hook feeds its own error back into the agent, which corrects itself unprompted |
| B | Rails | A CLAUDE.md "wish" vs. a deny list, then a skill that installs its own guard hook at runtime — the agent is blocked mid-edit and reroutes to a migration file |
| C | Workflow | A workflow fans out finder agents per module, then adversarially refutes each finding |

The application code is not the point. It contains planted bugs and
happy-path-only tests on purpose — see the notes in the runbook before
"fixing" anything.

## Running the demos

**[demo_runbook.md](demo_runbook.md)** has the prompts, the expected
behaviour for each demo, and the reset procedure between rehearsals.
