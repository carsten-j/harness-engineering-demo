#!/usr/bin/env python3
"""PreToolUse guard installed by the db-migration skill.

While the skill is active, Edit/Write is denied everywhere except NEW
numbered files under migrations/. Applied migrations are immutable.
"""

import json
import os
import re
import sys

MIGRATION_NAME = re.compile(r"^\d{4}_[a-z0-9_]+\.sql$")


def deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                },
                "systemMessage": f"db-migration guard: {reason}",
            }
        )
    )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    path = (payload.get("tool_input") or {}).get("file_path", "")
    if not path:
        return 0

    root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    # macOS filesystems are case-insensitive: ~/Dev and ~/dev are the same
    # directory but compare unequal as strings, breaking relpath.
    norm = str.lower if sys.platform == "darwin" else str
    rel = os.path.relpath(
        norm(os.path.realpath(os.path.abspath(path))), norm(os.path.realpath(root))
    )

    if not rel.startswith("migrations" + os.sep):
        deny(
            "db-migration mode is active: schema changes go through NEW "
            "files under migrations/ (e.g. migrations/0002_short_name.sql), "
            "never through edits elsewhere. Create the next numbered "
            "migration, then run `make migrate` and `make test`."
        )
        return 0
    name = os.path.basename(rel)
    if not MIGRATION_NAME.match(name):
        deny(
            "migration files must be named NNNN_short_name.sql "
            "(four digits, ordered after the highest existing number)."
        )
        return 0
    if os.path.exists(os.path.join(root, rel)):
        deny(
            f"{name} already exists and applied migrations are immutable. "
            "Create the next numbered migration file instead."
        )
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
