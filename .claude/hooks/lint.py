#!/usr/bin/env python3
"""PostToolUse sensor: format + lint any edited Python file.

Silent on success. On lint failure, prints ruff's output to stderr and
exits 2 so the error signal flows back into the agent's context.
"""

import json
import os
import subprocess
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    path = (payload.get("tool_input") or {}).get("file_path", "")
    if not path.endswith(".py"):
        return 0

    root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    subprocess.run(
        ["uv", "run", "ruff", "format", "--quiet", path],
        cwd=root,
        capture_output=True,
    )
    check = subprocess.run(
        ["uv", "run", "ruff", "check", path],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if check.returncode != 0:
        sys.stderr.write(check.stdout + check.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
