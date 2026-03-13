# Этап 1: Сборка зависимостей
FROM python:3.14-slim-bookworm AS builder

# Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Настройки для оптимизации сборки
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

WORKDIR /project

# Сначала копируем только файлы зависимостей для кэширования слоев
COPY uv.lock pyproject.toml /project/

# Синхронизируем зависимости без dev-пакетов
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Этап 2: Финальный образ
FROM python:3.14-slim-bookworm

WORKDIR /project

# Копируем установленное окружение из билдера
COPY --from=builder /project/.venv /project/.venv
COPY . /project

# Добавляем виртуальное окружение в PATH
ENV PATH="/project/.venv/bin:$PATH" \
    PYTHONPATH=/project \
    PYTHONUNBUFFERED=1

# Права на запуск скриптов
RUN chmod +x ./app/prestart.sh

WORKDIR /project/app

ENTRYPOINT ["./prestart.sh"]

# Используем uvicorn напрямую через venv для скорости
CMD ["python", "run_main.py"]
