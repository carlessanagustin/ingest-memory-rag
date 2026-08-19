---
id: TASK-113
title: Verify the Python 3.14 Docker build and quality gate
status: Done
assignee:
  - '@claude'
created_date: '2026-08-19 10:41'
updated_date: '2026-08-19 10:50'
labels:
  - build
  - verification
  - python
dependencies:
  - TASK-111
  - TASK-112
ordinal: 115000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Confirm the original failure is fixed and the project is healthy on 3.14. Rebuild the app image (docker compose build app) and confirm the "No interpreter found for Python >=3.11,<3.13" error is gone and `uv sync --frozen` installs cleanly on the 3.14 base; run the local quality gate (make check: ruff lint + format-check + mypy + unit tests) on 3.14. Recommended subagent: sherpa:docky (Docker build).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `docker compose build app` completes successfully; the previous interpreter/uv-sync error no longer appears in the build log
- [x] #2 The in-image `uv sync --frozen` step does not re-resolve (lockfile is consistent with pyproject) and installs all deps from wheels (no source-build failures)
- [x] #3 `make check` (ruff lint, ruff format --check, mypy, unit tests) passes on Python 3.14
- [x] #4 Any residual risk (e.g. a missing 3.14 wheel on a non-linux CI runner) is documented in the task notes
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Rebuild the app image (docker compose build app) — confirm the "No interpreter found for Python >=3.11,<3.13" error is gone and uv sync --frozen installs from wheels on the 3.14 base.
2. Confirm the in-image uv sync --frozen does not re-resolve (lock consistent).
3. Run make check (ruff lint, ruff format --check, mypy, unit tests) on 3.14 locally.
4. Record any residual non-linux wheel risk.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Verified on the real toolchain. `docker compose build app` now completes successfully on the python:3.14-slim base: the originally failing stage (uv sync --frozen --no-install-project --no-dev) installs all deps from wheels, the "No interpreter found for Python >=3.11,<3.13" error is gone, and the second uv sync --frozen --no-dev builds/installs the project with no re-resolution (frozen lock consistent). Image ingest-memory-rag-app:latest built.

`make check` passes on Python 3.14.7: ruff check (All checks passed), ruff format --check (pass after one reformat, see below), mypy (Success: no issues found in 6 source files), pytest (46 passed, 3 deselected, 100% coverage, >=80% gate met).

One code change was required to keep the gate green: the relock pulled ruff 0.15.22, whose formatter — with target-version py314 — applies PEP 758 (Python 3.14) and strips the now-redundant parentheses in tests/test_qdrant_integration.py (except (A, B): -> except A, B:). Applied via `ruff format .`; confirmed the file still parses on 3.14. This is valid 3.14-only syntax, consistent with the 3.14-only move.

Residual risks / follow-ups (non-blocking):
- CI unit matrix keeps os=[ubuntu, macos, windows] on py3.14. 3.14 wheels verified on x86_64 linux (Docker) and macOS-arm64 (local); onnxruntime is the most likely to lag on Windows/macos GitHub runners. If a job fails on a missing wheel, drop the non-linux OSes or wait for the wheel; the Docker/linux path is unaffected.
- pytest emits 2 DeprecationWarnings from the newer pathspec: GitWildMatchPattern ('gitwildmatch') is deprecated in favour of 'gitignore'. Tests still pass; a small follow-up could switch watcher.py to the 'gitignore' factory.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified the 3.14 upgrade: docker compose build app succeeds (original "No interpreter found" error gone, deps install from wheels, frozen lock does not re-resolve), and make check passes on Python 3.14.7 (ruff+mypy clean, 46 tests, 100% coverage). Applied one ruff-format change (PEP 758 paren strip in a test file, required by the newer locked ruff at target py314). Documented residual risks: non-linux 3.14 wheels (onnxruntime) on the CI matrix and a non-blocking pathspec deprecation warning.
<!-- SECTION:FINAL_SUMMARY:END -->
