---
id: TASK-45
title: Wipe storage_opencode in the Makefile reset and reset-hard targets
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 11:41'
updated_date: '2026-07-30 11:45'
labels:
  - makefile
  - opencode
  - docker
dependencies: []
type: chore
ordinal: 47000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The Makefile reset and reset-hard targets rebuild a from-scratch dev environment by deleting and recreating the storage_<service> folders, but they were written before the opencode service existed and omit storage_opencode. Add storage_opencode to both targets so a reset also clears opencode data (auth, sessions, sqlite), consistent with the other storage folders, and update the WARNING and ## help text to mention it. Note: .gitignore and .dockerignore already include storage_opencode (added in TASK-37), so no change is needed there. Verify by dry-run only (make -n); never run a real reset, which would destroy live data.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 make reset deletes and recreates storage_opencode with a .gitkeep, alongside storage_qdrant, storage_ollama and storage_openwebui
- [x] #2 make reset-hard does the same for storage_opencode, in addition to its existing image/build-cache pruning
- [x] #3 The WARNING text and the ## help descriptions for reset and reset-hard mention storage_opencode (opencode auth/session state)
- [x] #4 make -n reset and make -n reset-hard (dry run) show storage_opencode in the rm -rf, mkdir -p and touch .gitkeep commands, without executing a real reset
- [x] #5 No other Makefile targets or storage folders are changed
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. reset target: add storage_opencode to the rm -rf, mkdir -p and touch .gitkeep lines; mention storage_opencode/opencode state in the ## help and WARNING echo. 2. reset-hard target: same additions to its rm/mkdir/touch lines and WARNING echo. 3. Validate with make -n reset and make -n reset-hard (dry-run only; never run a real reset).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Edited Makefile reset and reset-hard: added storage_opencode to rm -rf, mkdir -p and touch .gitkeep in both targets, and named storage_opencode + opencode state (auth/sessions) in the WARNING echoes; the reset ## help now lists storage_opencode (reset-hard ## help intentionally delegates via "Like reset" and enumerates no storage folder, but its WARNING names storage_opencode). Verified dry-run only: make -n reset and make -n reset-hard each show storage_opencode 4x (WARNING + rm + mkdir + touch). git diff limited to Makefile (9 insertions / 9 deletions, only reset/reset-hard lines). No real reset, docker, git or backlog commands executed against live data.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Extended Makefile reset and reset-hard to wipe/recreate storage_opencode (with .gitkeep) alongside the other storage folders, with updated WARNING/help text. Verified via make -n dry-runs (storage_opencode present in both) and a Makefile-only diff; no real reset run. .gitignore/.dockerignore already covered storage_opencode (TASK-37).
<!-- SECTION:FINAL_SUMMARY:END -->
