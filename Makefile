.PHONY: install sync format lint test test-parallel test-report clean help

# Переменные
PYTHON := uv run
PYTEST := $(PYTHON) pytest
REPORTS_DIR := reports
msg ?= auto

help: ## Показать справку по командам
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

sync: ## Синхронизировать зависимости через uv
	uv sync

format: ## Автоматическое форматирование кода (Ruff)
	$(PYTHON) ruff format .
	$(PYTHON) ruff check --fix .

lint: ## Запуск проверок (Ruff + MyPy)
	$(PYTHON) ruff check .
	$(PYTHON) mypy .

test: ## Запуск тестов (в один поток)
	$(PYTEST) tests/

test-parallel: ## Запуск тестов параллельно (pytest-xdist)
	$(PYTEST) -n auto --dist loadscope tests/

test-report: ## Запуск тестов с генерацией HTML-отчета
	@mkdir -p $(REPORTS_DIR)
	$(PYTEST) -n auto --dist loadscope --html=$(REPORTS_DIR)/report.html --self-contained-html tests/

clean: ## Удалить временные файлы и кэш
	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist *.egg-info
	rm -rf $(REPORTS_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} +

# --- База данных (Alembic) ---
migrate: ## Создать новую миграцию: make migrate msg="add_users_table"
	uv run alembic revision --autogenerate -m "$(msg)"

upgrade: ## Применить все миграции до последней
	uv run alembic upgrade head

downgrade: ## Откатить последнюю миграцию
	uv run alembic downgrade -1

history: ## Посмотреть историю миграций
	uv run alembic history --verbose

status: ## Посмотреть текущий статус БД относительно миграций
	uv run alembic current

