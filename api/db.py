"""SQLite schema management: apply numbered migrations from migrations/ in order."""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "invoices.sqlite3"
MIGRATIONS_DIR = ROOT / "migrations"


def migrate() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            "  filename TEXT PRIMARY KEY,"
            "  applied_at TEXT NOT NULL DEFAULT (datetime('now'))"
            ")"
        )
        applied = {
            row[0] for row in conn.execute("SELECT filename FROM schema_migrations")
        }
        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            if path.name in applied:
                continue
            conn.executescript(path.read_text())
            conn.execute(
                "INSERT INTO schema_migrations (filename) VALUES (?)", (path.name,)
            )
            conn.commit()
            print(f"applied {path.name}")
    print(f"schema ready at {DB_PATH}")


if __name__ == "__main__":
    migrate()
