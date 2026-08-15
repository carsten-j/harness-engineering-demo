"""SQLite schema management for the demo invoice service."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "invoices.sqlite3"

SCHEMA = """
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY,
    customer TEXT NOT NULL,
    total_cents INTEGER NOT NULL,
    due_date TEXT NOT NULL,
    reminded INTEGER NOT NULL DEFAULT 0
);
"""


def migrate() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)
    print(f"schema ready at {DB_PATH}")


if __name__ == "__main__":
    migrate()
