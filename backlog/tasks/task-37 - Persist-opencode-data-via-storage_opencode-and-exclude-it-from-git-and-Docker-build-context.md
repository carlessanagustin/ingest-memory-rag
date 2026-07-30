---
id: TASK-37
title: >-
  Persist opencode data via storage_opencode and exclude it from git and Docker
  build context
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 10:26'
updated_date: '2026-07-30 10:39'
labels:
  - docker
  - opencode
dependencies:
  - TASK-36
type: chore
ordinal: 39000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add the storage_opencode bind-mount folder used by the opencode service, following the storage_<service> convention already used for qdrant, ollama, and openwebui. Track only a .gitkeep placeholder; ignore its contents in git and exclude it from Docker build contexts so it never bloats an image.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 storage_opencode/.gitkeep exists and is tracked
- [x] #2 .gitignore ignores storage_opencode/* while keeping !storage_opencode/.gitkeep
- [x] #3 .dockerignore excludes storage_opencode/
- [x] #4 A fresh clone shows storage_opencode empty except for .gitkeep
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add storage_opencode/.gitkeep. 2. .gitignore: storage_opencode/* plus !storage_opencode/.gitkeep. 3. .dockerignore: storage_opencode/.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
storage_opencode/.gitkeep created. git add storage_opencode/.gitkeep stages as A (kept); git check-ignore matches storage_opencode/session.db against storage_opencode/*, and .gitkeep against the negation !storage_opencode/.gitkeep. .dockerignore excludes storage_opencode/. Same pattern as the sibling storage_ dirs.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added storage_opencode/.gitkeep plus .gitignore (storage_opencode/* + !.gitkeep) and .dockerignore (storage_opencode/). Verified: .gitkeep stages while data paths are ignored.
<!-- SECTION:FINAL_SUMMARY:END -->
