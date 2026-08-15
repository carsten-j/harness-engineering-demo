"""The migration runner applies numbered files once and is idempotent."""

import sqlite3

from api import db


def test_migrate_applies_and_is_idempotent(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.sqlite3")
    db.migrate()
    first = capsys.readouterr().out
    assert "applied 0001_initial.sql" in first

    db.migrate()  # second run: no-op
    assert "applied" not in capsys.readouterr().out

    with sqlite3.connect(db.DB_PATH) as conn:
        names = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
    assert {"invoices", "schema_migrations"} <= names
