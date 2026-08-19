---
id: TASK-111
title: >-
  Bump project to Python 3.14 (requires-python, .python-version, mypy,
  Dockerfile comment) and relock
status: Done
assignee:
  - '@claude'
created_date: '2026-08-19 10:41'
updated_date: '2026-08-19 10:45'
labels:
  - python
  - build
  - deps
dependencies: []
ordinal: 113000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Fix the build failure caused by FROM python:3.14-slim while the project still requires >=3.11,<3.13. Move the project to Python 3.14 only (user decision). Changes: pyproject.toml requires-python to ">=3.14" and [tool.mypy] python_version to "3.14" (and update the now-stale comment near it that says runtime support still includes 3.11); .python-version from 3.12 to 3.14; the stale Dockerfile line-1 comment ("Slim Python 3.12 base ...") to reflect 3.14; then regenerate uv.lock with `uv lock` so the locked resolution targets >=3.14. Dependency wheels for 3.14 are available (verified: tokenizers via cp310-abi3; onnxruntime/pydantic-core/numpy/grpcio via cp314), so no source builds are expected. Recommended subagent: general-purpose (Python packaging / uv).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 pyproject.toml requires-python is ">=3.14" and [tool.mypy] python_version is "3.14"; the stale "still includes 3.11" comment is updated/removed
- [x] #2 .python-version contains 3.14; the Dockerfile line-1 comment no longer claims a 3.12 base
- [x] #3 uv.lock is regenerated with `uv lock` and its requires-python is ">=3.14"
- [x] #4 `uv sync --frozen --no-dev` succeeds on a Python 3.14 interpreter (no "No interpreter found" error, no re-resolution)
- [x] #5 No touched file still asserts 3.11/3.12 support
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. pyproject.toml: requires-python -> ">=3.14"; [tool.mypy] python_version -> "3.14"; update the stale "still includes 3.11" comment.
2. .python-version -> 3.14; Dockerfile line-1 comment -> 3.14.
3. Ensure a 3.14 interpreter (uv python install 3.14 if needed), then `uv lock` to relock.
4. Verify uv.lock requires-python ">=3.14" and `uv sync --frozen --no-dev` resolves/install on 3.14 with no re-resolution.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Set pyproject requires-python=">=3.14", [tool.mypy] python_version="3.14" (replaced the stale 3.11/3.12 rationale comment), and also bumped [tool.ruff] target-version "py311"->"py314". .python-version 3.12->3.14; Dockerfile line-1 comment now says 3.14. Regenerated uv.lock with `uv lock` (CPython 3.14.7): requires-python is ">=3.14", 80 packages resolved, tomli removed (only needed on <3.11). Verified `UV_PYTHON_DOWNLOADS=never uv sync --frozen --no-dev` installs all runtime deps from wheels on Python 3.14.7 with no re-resolution and no source builds; the native deps pydantic_core, tokenizers (0.22.2), numpy, onnxruntime, qdrant_client and fastembed all import successfully on 3.14. grep confirms no 3.11/3.12/py311/py312 remains in pyproject.toml, .python-version, or Dockerfile.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Moved the project to Python 3.14-only: pyproject requires-python=">=3.14" (+ mypy python_version and ruff target-version to 3.14/py314), .python-version=3.14, corrected the Dockerfile comment, and relocked (uv.lock requires-python=">=3.14"). Verified uv sync --frozen installs from wheels on 3.14 and all native deps (incl. onnxruntime/fastembed) import.
<!-- SECTION:FINAL_SUMMARY:END -->
