---
id: TASK-62
title: Document recursive ingestion and the .ingestignore feature
status: Done
assignee:
  - '@claude'
created_date: '2026-08-03 09:17'
updated_date: '2026-08-03 09:32'
labels:
  - docs
  - app
dependencies:
  - TASK-60
  - TASK-61
type: docs
ordinal: 64000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update the README and .env.example so the new behavior is documented: WATCH_FOLDER is ingested recursively (subfolders included), and files can be excluded via a gitignore-style .ingestignore (configurable with WATCH_IGNORE, default .ingestignore at the WATCH_FOLDER root). Add WATCH_IGNORE to the Configuration table and .env.example with a short .ingestignore example.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The README Configuration section documents recursive ingestion and the WATCH_IGNORE/.ingestignore feature with a short pattern example
- [x] #2 The README Configuration table includes a WATCH_IGNORE row (default .ingestignore)
- [x] #3 .env.example includes WATCH_IGNORE=.ingestignore
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. README Configuration: note recursive ingestion (subfolders); add a WATCH_IGNORE row (default .ingestignore) to the table; short .ingestignore example. 2. .env.example: add WATCH_IGNORE=.ingestignore.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
README Configuration: WATCH_FOLDER row now says watched recursively (subfolders); added a WATCH_IGNORE row (default .ingestignore); added a note explaining recursive ingestion and the .ingestignore (gitignore syntax: globs, **, ! negation, / anchoring, dir/, # comments; matched relative to WATCH_FOLDER; read once at startup) with a fenced example. .env.example: added WATCH_IGNORE=.ingestignore with a comment.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Documented recursive ingestion and the .ingestignore/WATCH_IGNORE feature in the README (config table + note with example) and .env.example.
<!-- SECTION:FINAL_SUMMARY:END -->
