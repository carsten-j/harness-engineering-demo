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
Code session rather than described on a slide.

The application code is not the point. It contains planted bugs and
happy-path-only tests on purpose — see the notes in the runbook before
"fixing" anything.
