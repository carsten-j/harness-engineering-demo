# Project conventions

- Stack: FastAPI + SQLite (stdlib sqlite3).
- Python tooling: uv. Never pip install.
- Tests: pytest, not unittest.
- HTTP clients: httpx, not requests.

## Databases

- Test: local sqlite
- Prod: postgres://prod-db.internal/invoices

## Commands

make test      # unit tests
make check     # ruff format + lint + pytest
make migrate   # apply numbered SQL migrations from migrations/

## Iron laws

- Never git push --force.
- Never hand-edit invoices.sqlite3.
- Schema changes only via new numbered files in migrations/ (invoke the db-migration skill).
