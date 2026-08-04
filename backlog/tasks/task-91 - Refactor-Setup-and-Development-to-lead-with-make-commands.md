---
id: TASK-91
title: Refactor Setup and Development to lead with make commands
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 14:39'
updated_date: '2026-08-04 14:53'
labels:
  - docs
dependencies:
  - TASK-90
ordinal: 93000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Rewrite Setup and Development to use the Makefile shortcuts as the primary commands (make up/down/logs/build/reset for the stack; make check/lint/format/typecheck/test for dev), keeping the underlying raw docker/uv command only as a brief clarifying note where useful.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Setup leads with make commands (e.g. make up, make logs, make down, make reset) for running the stack
- [x] #2 Development leads with make commands (e.g. make check, make test, make lint, make format, make typecheck)
- [x] #3 Commands shown match real Makefile targets; any raw docker/uv command is kept only as a short note
- [x] #4 Changes limited to README.md
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Setup+Development lead with make commands. part of one coherent README.md refactor pass
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Setup leads with make up/logs/down/build/reset (raw docker compose kept only as a note + the single-service qdrant case); Development leads with make check/test/lint/format/typecheck (uv run as a note). All commands match real Makefile targets.
<!-- SECTION:FINAL_SUMMARY:END -->
