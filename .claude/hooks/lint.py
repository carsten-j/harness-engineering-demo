#!/usr/bin/env python3
"""PostToolUse sensor: format + lint any edited Python file.

On lint failure, prints ruff's output to stderr behind a banner and exits 2
so the error signal flows back into the agent's context. Silent to the agent
on success — but every invocation, pass or fail, appends a line to
.claude/lint-hook.log so the presenter can show the sensor ran at all.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

BANNER = "── PostToolUse hook: .claude/hooks/lint.py ──"
LOG = ".claude/lint-hook.log"


def log(root: str, verdict: str, path: str) -> None:
    """Append one audit line. Never let logging break the hook."""
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        with open(os.path.join(root, LOG), "a") as fh:
            fh.write(f"{stamp}\t{verdict}\t{path}\n")
    except OSError:
        pass


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    path = (payload.get("tool_input") or {}).get("file_path", "")
    root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    rel = os.path.relpath(path, root) if path else ""
    if rel.startswith(".."):  # outside the repo — keep the log line readable
        rel = path

    if not path.endswith(".py"):
        if rel:
            log(root, "SKIP", rel)
        return 0

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
        output = check.stdout + check.stderr
        rule = re.search(r"\b([A-Z]{1,4}\d{3,4})\b", output)
        log(root, f"FAIL {rule.group(1)}" if rule else "FAIL", rel)
        sys.stderr.write(f"{BANNER}\n{output}")
        return 2

    log(root, "PASS", rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
