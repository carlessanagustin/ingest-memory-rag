---
id: TASK-3
title: Add a Dockerfile and .dockerignore to run the app in a container
status: Done
assignee:
  - '@claude'
created_date: '2026-07-23 15:05'
updated_date: '2026-07-24 06:58'
labels: []
dependencies:
  - TASK-1
ordinal: 7000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Provide a container image so the ingestion service can run in Docker. The image installs dependencies reproducibly from `uv.lock` and runs the `ingest-memory-rag` console entry point. Scope is the image and build context only; wiring it into `docker-compose.yml` alongside Qdrant is a separate task.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A `Dockerfile` at the repo root builds a working image on a slim Python 3.12 base
- [x] #2 Dependencies install reproducibly from the committed `uv.lock` via `uv sync --frozen`, not re-resolved at build time
- [x] #3 The image default command runs the app entry point (`ingest-memory-rag` / `python -m ingest_memory_rag`)
- [x] #4 A `.dockerignore` excludes `.venv`, caches, `.git`, `raw/` data, and the local Qdrant storage folder to keep the build context small
- [x] #5 The container process runs as a non-root user
- [x] #6 `docker build` succeeds and the container starts, logging a clear error when Qdrant is unreachable
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add .dockerignore: exclude .git/.github, .venv, __pycache__ and tool caches, raw/, qdrant_storage/, tests/, backlog/, .env* and coverage; KEEP README.md (pyproject readme), pyproject.toml, uv.lock, src/.
2. Add Dockerfile: python:3.12-slim + uv binary from ghcr.io/astral-sh/uv; layer-cached deps install (uv sync --frozen --no-install-project --no-dev), then COPY . . and uv sync --frozen --no-dev; create non-root user (uid 10001), own /app and /app/raw; PATH=/app/.venv/bin; CMD ["ingest-memory-rag"].
3. docker build the image.
4. docker run without Qdrant reachable (default localhost:6333 is unreachable inside the container) and confirm it starts and logs a clear "cannot reach Qdrant" error; if the native failure hangs or is opaque, add a minimal startup connectivity check in run() (pragma-excluded, no coverage impact).
5. Verify non-root (id in container), entry point resolves, and .dockerignore keeps the context small.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented Dockerfile + .dockerignore, plus a small containerization refactor: IngestionEngine.verify_connection() and a startup Qdrant reachability check in watcher.run() (both in coverage-excluded paths).
Verified on Docker 29.6.2:
- AC#1 docker build succeeds on python:3.12-slim.
- AC#2 deps installed from uv.lock via 'uv sync --frozen --no-dev' (layer-cached deps step + project install); --frozen would fail on a stale lock.
- AC#3 entry point resolves to /app/.venv/bin/ingest-memory-rag; 'import ingest_memory_rag' ok.
- AC#4 image lacks tests/backlog/.git/raw; keeps README.md/pyproject.toml/uv.lock/src; /app/.venv is the container's own Linux venv (host .venv excluded from context).
- AC#5 container runs as non-root: id => uid=10001(appuser).
- AC#6 with Qdrant unreachable the container logs 'ERROR ... Cannot reach Qdrant at http://localhost:6333 — is it running? ([Errno 111] Connection refused)' and exits 1.
Local: ruff+mypy clean, 16 unit tests + 3 integration tests pass. Note: networking the app to Qdrant (so it can actually ingest) is TASK-5.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added a Dockerfile (python:3.12-slim + uv, deps installed reproducibly from uv.lock via 'uv sync --frozen --no-dev', non-root uid 10001, CMD ingest-memory-rag) and a .dockerignore that trims the build context (excludes .venv, caches, .git, raw/, qdrant_storage, tests/, backlog/). Added a startup Qdrant connectivity check so the container fails fast with a clear error when Qdrant is unreachable. Verified: docker build succeeds, container runs as non-root, and 'docker run' without Qdrant logs a clear connection error and exits 1. Compose networking to Qdrant is TASK-5.
<!-- SECTION:FINAL_SUMMARY:END -->
