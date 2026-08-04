---
id: TASK-90
title: Update Requirements to cover all Makefile targets
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 14:39'
updated_date: '2026-08-04 14:53'
labels:
  - docs
dependencies:
  - TASK-89
ordinal: 92000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update the Requirements section so it lists everything needed to run every Makefile command: Docker + Docker Compose (up/down/build/reset/logs) and Python 3.11/3.12 + uv (run/test/lint/format/typecheck/check). Add a pointer to `make help`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Requirements lists Docker + Docker Compose and Python 3.11/3.12 + uv as prerequisites, tied to the make targets they enable
- [x] #2 A line points readers to `make help` to list all available commands
- [x] #3 No prerequisite required by a make target is missing; changes limited to README.md
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Requirements = Docker+Compose, Python 3.11/3.12+uv, + make help pointer. part of one coherent README.md refactor pass
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Requirements now lists Docker + Docker Compose (up/down/build/logs/reset) and Python 3.11/3.12 + uv (run/test/lint/format/typecheck/check), with make run needing a live Qdrant, plus a "run make help" pointer.
<!-- SECTION:FINAL_SUMMARY:END -->
