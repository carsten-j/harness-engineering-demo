# Project conventions

- Stack: FastAPI + SQLite (stdlib sqlite3).
- Python tooling: uv. Never pip install.
- Tests: pytest, not unittest.
- HTTP clients: httpx, not requests.

## Commands

make test      # unit tests
make check     # ruff format + lint + pytest
make migrate   # create the SQLite schema

## Iron laws

- Never git push --force.
- Never touch the prod database (DATABASE_URL=postgres://prod-db.internal/invoices).
- Never hand-edit invoices.sqlite3.
