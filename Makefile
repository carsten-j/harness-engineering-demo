.PHONY: test check migrate

test:
	uv run pytest -q

check:
	uv run ruff format --check .
	uv run ruff check .
	uv run pytest -q

migrate:
	uv run python -m api.db
