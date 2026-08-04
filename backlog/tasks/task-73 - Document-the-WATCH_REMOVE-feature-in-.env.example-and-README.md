---
id: TASK-73
title: Document the WATCH_REMOVE feature in .env.example and README
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 07:32'
updated_date: '2026-08-04 07:40'
labels:
  - docs
dependencies:
  - TASK-72
ordinal: 75000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Document the new opt-in, destructive WATCH_REMOVE behavior so operators understand exactly when files are deleted vs kept.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 .env.example includes WATCH_REMOVE (default false) with a short comment noting it deletes files after successful ingestion
- [x] #2 README configuration table has a WATCH_REMOVE row describing the default and effect
- [x] #3 README documents the exact rule: deletes only on >=1 chunk written; keeps and logs on 0 chunks or ingestion failure; applies to both the startup scan and live events
- [x] #4 The docs flag it clearly as opt-in and destructive (files are permanently removed from disk)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. .env.example: add `WATCH_REMOVE=false` near WATCH_FOLDER/WATCH_IGNORE with a one-line comment (deletes source file after successful ingestion; opt-in/destructive).
2. README configuration table: add a WATCH_REMOVE row (default false, effect).
3. README note documenting the exact rule: deletes only when >=1 chunk written; keeps + logs on 0 chunks or ingestion failure; applies to both startup scan and live events; opt-in and destructive.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Documented WATCH_REMOVE in .env.example (WATCH_REMOVE=false with an opt-in/destructive comment) and README (config-table row + a note stating the exact rule: deletes only on >=1 chunk written; keeps+logs on 0 chunks or failure; applies to startup scan and live events; failed delete logged, not fatal; opt-in and destructive). Verified by reviewing the rendered diffs.
<!-- SECTION:FINAL_SUMMARY:END -->
