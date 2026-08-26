# Practical Advice

## If you are starting out with Harness Engineering

Prioritized list:

* CLAUDE.md (short, build/test, stack, architecture/design)
* Permissions (think about auto-mode and/or sandboxing)
* Hooks
* Skills

## Skills

Description: how the skill is triggered

Body: step-by-step runbook

Include scripts or CLI tools and explain in the skill body how they are used.

Make sure skills are distinguishable; otherwise you will end up confusing the agent.

Log skill calls to get an idea of which skills are triggered and how often.

[Demystifying Agent Skills: Why They Work-Until They Don't](https://arxiv.org/abs/2608.14036)

## Pick the right model

Fable might be the "best" model, but Opus and even Sonnet are equally good for some tasks.

## Usage

What are you spending tokens on:

[AgentsView](https://www.agentsview.io/)

[CodeBurn](https://github.com/getagentseal/codeburn)

## Prompt caching

Cache is invalidated when changing model, effort, etc.

TTL (5 min) — do not go for lunch in the middle of a long-running session.

## Various

/insights

keep your log-files longer!
