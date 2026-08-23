"""The migration runner applies numbered files once and is idempotent."""

import logging
import sqlite3

from api import db


def test_migrate_applies_and_is_idempotent(tmp_path, monkeypatch, caplog):
    caplog.set_level(logging.INFO, logger="api.db")
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.sqlite3")
    db.migrate()
    assert "applied 0001_initial.sql" in caplog.text

    caplog.clear()
    db.migrate()  # second run: no-op
    assert "applied" not in caplog.text

    with sqlite3.connect(db.DB_PATH) as conn:
        names = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
    assert {"invoices", "schema_migrations"} <= names
