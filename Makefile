PYTHON = uv run python
APP_DIR = app

.PHONY: lint format check test

lint:
	uv run ruff check $(APP_DIR) --fix
	uv run mypy $(APP_DIR)

format:
	uv run ruff format $(APP_DIR)
	uv run ruff check $(APP_DIR) --fix

check:
	uv run ruff check $(APP_DIR)
	uv run mypy $(APP_DIR)

test:
	uv run pytest tests/
