# Project conventions

- Stack: FastAPI + SQLite/Postgres.
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
