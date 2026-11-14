
# ==========================================
# Stage 1: Builder
# ==========================================
FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1

COPY pyproject.toml uv.lock ./

# Instala as dependências de produção
RUN uv sync --frozen --no-dev --no-install-project

# Copia o código
COPY src ./src

# ==========================================
# Stage 2: Runtime
# ==========================================
FROM python:3.14-slim AS runtime

WORKDIR /app

COPY --from=builder /bin/uv /bin/uv
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/pyproject.toml /app/pyproject.toml
COPY --from=builder /app/uv.lock /app/uv.lock
COPY --from=builder /app/src /app/src

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_HOST=0.0.0.0

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "src"]
