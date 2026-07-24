---
id: TASK-6
title: Add a Makefile with common project commands
status: Done
assignee:
  - '@claude'
created_date: '2026-07-23 15:06'
updated_date: '2026-07-24 07:53'
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
- [x] #1 `make help` is the default target and lists every target with a one-line description
- [x] #2 Targets exist for dependency sync and lockfile update (wrapping `uv sync` and `uv lock`)
- [x] #3 Targets exist to run the app, run unit tests, run integration tests, lint (`ruff check`), format (`ruff format`), and type-check (`mypy`), plus an aggregate `check` target
- [x] #4 Targets exist for the Docker lifecycle (build, up, down, logs) matching the compose setup
- [x] #5 The commands invoked by the targets match the checks enforced in CI so local and CI behavior stay consistent
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add Makefile: .DEFAULT_GOAL=help, .PHONY targets. 2. help (default) auto-lists targets from ## comments. 3. Targets: sync, lock, run, test, test-integration, lint, format, format-check, typecheck, check (aggregate = lint+format-check+typecheck+test to match the CI gate), docker-build, up, down, logs, clean. 4. Verify: make help lists targets with descriptions; make check runs the CI gate locally and passes.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Verified: make help (default) lists all targets with descriptions; make check ran the CI gate (ruff check + ruff format --check + mypy + pytest -m 'not integration') and passed with 100% coverage. Docker targets (docker-build/up/down/logs) wrap docker compose. Tabs correct (make executed without 'missing separator').
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added a Makefile with a self-documenting default help target and targets for sync/lock, run, test, test-integration, lint, format, format-check, typecheck, an aggregate check (lint+format-check+typecheck+test matching the CI gate), Docker lifecycle (docker-build/up/down/logs), and clean. Verified make help lists targets and make check passes.
<!-- SECTION:FINAL_SUMMARY:END -->
