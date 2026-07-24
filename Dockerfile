# Slim Python 3.12 base (matches .python-version / requires-python).
FROM python:3.12-slim

# uv binary from the official image — no network install needed.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# 1) Install ONLY dependencies first, from the committed lockfile, so this
#    layer is cached across source-only changes. --frozen fails if uv.lock is
#    out of date (no resolution at build time); --no-dev skips dev tooling.
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# 2) Copy the project and install it (builds the wheel from src/, needs README.md).
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Run as a non-root user; own /app (venv) and the default watch folder.
RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /app/raw \
    && chown -R appuser:appuser /app
USER appuser

# Watches WATCH_FOLDER (default ./raw) and ingests into QDRANT_URL.
CMD ["ingest-memory-rag"]
