---
id: TASK-60
title: Add pathspec dependency and a WATCH_IGNORE setting
status: Done
assignee:
  - '@claude'
created_date: '2026-08-03 09:16'
updated_date: '2026-08-03 09:29'
labels:
  - app
  - python
  - config
dependencies: []
type: feature
ordinal: 62000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Prepare for .ingestignore support. Add pathspec as a runtime dependency (it currently exists only transitively via mypy) and lock it. Add a WATCH_IGNORE setting to Settings.from_env() (default .ingestignore) representing the ignore-file path, resolved relative to WATCH_FOLDER when relative so the default file is WATCH_FOLDER/.ingestignore. Do not yet apply any filtering (that is the next task).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 pathspec is declared in [project.dependencies] in pyproject.toml and present in uv.lock as a direct dependency
- [x] #2 Settings has an ignore-file field; from_env() reads WATCH_IGNORE (default .ingestignore) and resolves it relative to WATCH_FOLDER for relative values
- [x] #3 A unit test covers the WATCH_IGNORE default and an override, including the relative-to-WATCH_FOLDER resolution
- [x] #4 uv sync --frozen installs cleanly and lint/type-check pass
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. uv add pathspec (runtime dep, lock). 2. config.py: DEFAULT_WATCH_IGNORE=.ingestignore; Settings.ignore_file: Path; from_env reads WATCH_IGNORE, resolves relative to watch_folder. 3. Unit tests: default, relative override, absolute override.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
uv add pathspec -> pathspec>=1.1.1 in [project.dependencies] and uv.lock (verified: grep pyproject shows pathspec>=1.1.1; uv sync --frozen -> Checked 77 packages, clean). config.py: added DEFAULT_WATCH_IGNORE=.ingestignore and Settings.ignore_file: Path; from_env computes watch_folder then reads WATCH_IGNORE (default .ingestignore), expanduser, and resolves relative values against watch_folder (default -> watch_folder/.ingestignore), absolute verbatim. Unit tests cover default + relative + absolute. ruff/mypy clean.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added pathspec as a runtime dependency and a WATCH_IGNORE setting (Settings.ignore_file, default .ingestignore resolved relative to WATCH_FOLDER). Verified via uv sync --frozen, config unit tests, ruff and mypy.
<!-- SECTION:FINAL_SUMMARY:END -->
