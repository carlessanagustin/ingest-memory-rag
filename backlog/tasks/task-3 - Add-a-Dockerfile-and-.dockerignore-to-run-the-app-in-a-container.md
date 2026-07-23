---
id: TASK-3
title: Add a Dockerfile and .dockerignore to run the app in a container
status: To Do
assignee: []
created_date: '2026-07-23 15:05'
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
- [ ] #1 A `Dockerfile` at the repo root builds a working image on a slim Python 3.12 base
- [ ] #2 Dependencies install reproducibly from the committed `uv.lock` via `uv sync --frozen`, not re-resolved at build time
- [ ] #3 The image default command runs the app entry point (`ingest-memory-rag` / `python -m ingest_memory_rag`)
- [ ] #4 A `.dockerignore` excludes `.venv`, caches, `.git`, `raw/` data, and the local Qdrant storage folder to keep the build context small
- [ ] #5 The container process runs as a non-root user
- [ ] #6 `docker build` succeeds and the container starts, logging a clear error when Qdrant is unreachable
<!-- AC:END -->
