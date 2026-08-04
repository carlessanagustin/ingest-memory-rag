---
id: TASK-78
title: 'Document the mounted, live-reloadable .watchignore'
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 08:29'
updated_date: '2026-08-04 08:44'
labels:
  - docs
dependencies:
  - TASK-75
  - TASK-77
ordinal: 80000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Document that the app reads a bind-mounted .watchignore that is edited from the host and applies live, including the Docker Desktop single-file-mount caveat.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 README explains .watchignore is bind-mounted read-only into the app container at /app/raw/.watchignore and is edited from the host repo root
- [x] #2 README states edits apply live without a container restart
- [x] #3 README documents the Docker Desktop single-file-mount caveat: edit the file in place (append/overwrite); editors that replace it via atomic rename may not propagate through a single-file bind mount, in which case `docker compose restart app` is the fallback
- [x] #4 Any WATCH_IGNORE notes in .env.example / the config table are consistent with the mounted in-container path
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. README: document .watchignore is bind-mounted read-only at /app/raw/.watchignore, edited from the host repo root, applies live (no restart).
2. Document the Docker Desktop single-file-mount caveat (edit in place; atomic-rename editors may not propagate; fallback docker compose restart app).
3. Keep .env.example / config-table WATCH_IGNORE notes consistent with the in-container path.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
README documents that .watchignore is bind-mounted read-only at /app/raw/.watchignore, edited from the host repo root, and reloaded live (within DEBOUNCE_SECONDS, no restart), plus the Docker Desktop single-file-mount caveat (edit in place; atomic-rename may not propagate; fallback docker compose restart app). .env.example WATCH_IGNORE comment notes the in-container path and live reload. Verified by reviewing rendered diffs.
<!-- SECTION:FINAL_SUMMARY:END -->
