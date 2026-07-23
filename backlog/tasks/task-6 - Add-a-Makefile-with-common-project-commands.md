---
id: TASK-6
title: Add a Makefile with common project commands
status: To Do
assignee: []
created_date: '2026-07-23 15:06'
updated_date: '2026-07-23 15:07'
labels: []
dependencies:
  - TASK-1
  - TASK-5
ordinal: 8000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Provide a `Makefile` that wraps the most-used commands so they do not need to be memorized: environment setup, running the app, testing, linting, type-checking, and the Docker lifecycle. Running `make` with no target (or `make help`) lists the available targets with short descriptions.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 `make help` is the default target and lists every target with a one-line description
- [ ] #2 Targets exist for dependency sync and lockfile update (wrapping `uv sync` and `uv lock`)
- [ ] #3 Targets exist to run the app, run unit tests, run integration tests, lint (`ruff check`), format (`ruff format`), and type-check (`mypy`), plus an aggregate `check` target
- [ ] #4 Targets exist for the Docker lifecycle (build, up, down, logs) matching the compose setup
- [ ] #5 The commands invoked by the targets match the checks enforced in CI so local and CI behavior stay consistent
<!-- AC:END -->
