---
id: TASK-47
title: Update .gitignore and .dockerignore for the storage/ layout
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 11:57'
updated_date: '2026-07-30 12:01'
labels:
  - docker
  - storage
dependencies:
  - TASK-46
type: chore
ordinal: 49000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Switch the ignore rules from the four storage_<service> entries to the single storage/ tree. .gitignore should ignore everything under storage/ except the top-level .gitkeep; .dockerignore should exclude storage/ from the build context.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 .gitignore ignores storage/* and keeps !storage/.gitkeep; the four storage_<service> blocks are removed
- [x] #2 .dockerignore excludes storage/; the four storage_<service> lines are removed
- [x] #3 git check-ignore confirms runtime paths like storage/qdrant are ignored while storage/.gitkeep stays tracked
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. .gitignore: replace the four storage_<service> blocks with storage/* + !storage/.gitkeep. 2. .dockerignore: replace the four storage_<service> lines with storage/. 3. Verify via git check-ignore (main loop).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
.gitignore now: storage/* + !storage/.gitkeep (four storage_<svc> blocks removed). .dockerignore now: storage/ (four lines removed). Verified: git check-ignore storage/qdrant -> ignored; git add -n storage/.gitkeep -> trackable.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Switched ignore rules to the single storage/ tree (.gitignore keeps only storage/.gitkeep; .dockerignore excludes storage/). Verified with git check-ignore / add --dry-run.
<!-- SECTION:FINAL_SUMMARY:END -->
