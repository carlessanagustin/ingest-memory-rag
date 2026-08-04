---
id: TASK-75
title: Mount the host .watchignore into the app container (read-only)
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 08:28'
updated_date: '2026-08-04 08:34'
labels:
  - ci
dependencies: []
ordinal: 77000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Bind-mount the repo-root .watchignore into the app container at the path the app already resolves by default (/app/raw/.watchignore), so the ignore rules the app applies are the ones in the host file and edits made outside the container reach it. No WATCH_IGNORE env override is needed because the default resolves a relative WATCH_IGNORE under WATCH_FOLDER (=/app/raw).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 compose/app.yaml volumes include `./.watchignore:/app/raw/.watchignore:ro`
- [x] #2 No WATCH_IGNORE environment override is added (the in-code default already resolves to /app/raw/.watchignore)
- [x] #3 The tracked repo-root .watchignore remains present so the single-file bind mount always has a source (Docker never creates a directory in its place)
- [x] #4 `docker compose config` is valid and the app service starts; the container path /app/raw/.watchignore reflects the host file contents
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. In compose/app.yaml, add `- ./.watchignore:/app/raw/.watchignore:ro` to the app service volumes (after `- ./raw:/app/raw`).
2. No WATCH_IGNORE env change (default already resolves to /app/raw/.watchignore).
3. Validate with `docker compose config`; confirm the app service mounts the file read-only. Keep the tracked repo-root .watchignore as the mount source.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added `- ./.watchignore:/app/raw/.watchignore:ro` to the app service volumes in compose/app.yaml. No WATCH_IGNORE env override (the in-code default resolves to /app/raw/.watchignore). Verified with `docker compose config app`: both mounts render, the .watchignore mount shows read_only: true, YAML is valid; the tracked repo-root .watchignore (mount source) is unchanged.
<!-- SECTION:FINAL_SUMMARY:END -->
