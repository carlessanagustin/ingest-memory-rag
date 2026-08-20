---
id: TASK-118
title: Document the PGID setting in .env.example and README
status: Done
assignee:
  - '@claude'
created_date: '2026-08-20 13:38'
updated_date: '2026-08-20 13:47'
labels: []
dependencies:
  - TASK-117
type: docs
ordinal: 120000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Once TASK-117 makes the app containers GID configurable via PGID, document it so users hitting the WATCH_REMOVE PermissionError (delete fails on the bind-mounted ./raw folder because the container GID does not match the host groups that owns ./raw) know how to fix it themselves, without digging through compose internals.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 .env.example has a `PGID=` entry near the other WATCH_* vars, with a short inline comment pointing at `id -g`
- [x] #2 README Configuration table includes a PGID row (default 10001) explaining its purpose
- [x] #3 README has a short note near the existing WATCH_REMOVE explanation stating that deletion requires the containers group to match the group owning the host ./raw directory, and how to find/set that value
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add `PGID=` to .env.example near WATCH_* vars with a comment pointing at `id -g`. 2. Add a PGID row to the README Configuration table (default 10001). 3. Add a short note in the WATCH_REMOVE paragraph explaining the bind-mount GID requirement, mirroring the existing Docker Desktop bind-mount caveat callout style.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added `PGID=10001` to .env.example with a comment pointing at `id -g`. Added a PGID row to the README Configuration table, and a blockquote callout after the WATCH_REMOVE paragraph (README.md ~line 261) explaining the bind-mount group requirement, matching the style of the existing Docker Desktop caveat callout. Verified with grep that PGID appears in both files as expected.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Documented PGID (added in TASK-117) in .env.example and README: a PGID= entry with comment, a Configuration table row, and an explanatory callout next to WATCH_REMOVE covering the bind-mount PermissionError and how to fix it via id -g.
<!-- SECTION:FINAL_SUMMARY:END -->
