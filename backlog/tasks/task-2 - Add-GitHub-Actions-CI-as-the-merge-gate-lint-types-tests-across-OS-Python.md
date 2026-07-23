---
id: TASK-2
title: 'Add GitHub Actions CI as the merge gate (lint, types, tests across OS/Python)'
status: In Progress
assignee:
  - '@claude'
created_date: '2026-07-23 14:56'
updated_date: '2026-07-23 15:00'
labels: []
dependencies:
  - TASK-1
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Enforce the project standards in CI on every push and pull request: ruff lint+format, mypy, and pytest with coverage. Run the unit suite across the supported OS (Linux/macOS/Windows) and Python (3.11/3.12) matrix to prove cross-platform file watching (closes TASK-1 AC#5), and run the live-Qdrant integration tests against a Qdrant service container on Linux.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 CI runs on push and pull_request and is the merge gate
- [ ] #2 ruff check, ruff format --check, and mypy run in CI and must pass
- [ ] #3 Unit tests (pytest -m "not integration") run on Linux, macOS, and Windows for Python 3.11 and 3.12, enforcing the 80% coverage floor
- [ ] #4 Integration tests (pytest -m integration) run against a Qdrant service container on Linux
- [ ] #5 Dependencies are installed reproducibly from uv.lock (uv sync --frozen)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. .github/workflows/ci.yml with three jobs, triggered on push + pull_request.
2. lint job (ubuntu, 3.12): setup-uv, uv sync --frozen, ruff check, ruff format --check, mypy.
3. test job (matrix: ubuntu/macos/windows x 3.11/3.12): uv sync --frozen, pytest -m "not integration" (enforces 80% coverage; proves cross-OS watching -> TASK-1 AC#5).
4. integration job (ubuntu, 3.12): Qdrant service container on 6333, wait for /readyz, uv sync --frozen, pytest -m integration --no-cov.
5. Use astral-sh/setup-uv with caching; pin fetch-depth. Validate YAML parses locally; confirm uv sync --frozen matches the committed lock.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added .github/workflows/ci.yml with 3 jobs (push + pull_request):
- lint (ubuntu, 3.12): uv sync --frozen; ruff check; ruff format --check; mypy.
- test (matrix ubuntu/macos/windows x py3.11/3.12): uv sync --frozen; pytest -m "not integration" (80% coverage floor enforced via pyproject addopts).
- integration (ubuntu, Qdrant service container on 6333): wait for /readyz; uv sync --frozen; pytest -m integration --no-cov.
Uses astral-sh/setup-uv@v6 with caching; concurrency cancels superseded runs.
Validated locally: YAML parses (jobs lint/test/integration); uv lock --check passes so --frozen installs match the committed lock; pytest -m "not integration" => 16 passed / 100% cov; pytest -m integration => 3 passed against live Qdrant.
Runtime verification of the workflow itself (matrix + service container) is pending a push that triggers Actions; ACs to be checked once CI runs green.
<!-- SECTION:NOTES:END -->
