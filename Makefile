# Переменные
PYTHON = uv run python
APP_DIR = app
# Переменная для сообщения миграции, по умолчанию "auto"
msg ?= auto

.PHONY: lint format check test migrate upgrade downgrade history status

# --- Линтинг и форматирование ---
lint:
	uv run ruff check $(APP_DIR) --fix
	uv run mypy $(APP_DIR)

format:
	uv run ruff format $(APP_DIR)
	uv run ruff check $(APP_DIR) --fix

# --- База данных (Alembic) ---

# Создать новую миграцию: make migrate msg="add_users_table"
migrate:
	uv run alembic revision --autogenerate -m "$(msg)"

# Применить все миграции до последней
upgrade:
	uv run alembic upgrade head

# Откатить последнюю миграцию
downgrade:
	uv run alembic downgrade -1

# Посмотреть историю миграций
history:
	uv run alembic history --verbose

# Посмотреть текущий статус БД относительно миграций
status:
	uv run alembic current

# --- Тестирование ---
test:
	uv run pytest tests/
