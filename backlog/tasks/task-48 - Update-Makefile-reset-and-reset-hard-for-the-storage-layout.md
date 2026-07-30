---
id: TASK-48
title: Update Makefile reset and reset-hard for the storage/ layout
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 11:57'
updated_date: '2026-07-30 12:01'
labels:
  - makefile
  - storage
dependencies:
  - TASK-46
type: chore
ordinal: 50000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The reset and reset-hard targets currently rm/mkdir/touch four storage_<service> folders. Update them to operate on the single storage/ tree: wipe storage/ and recreate it with storage/.gitkeep. Update the WARNING and ## help text to refer to storage/. Verify by dry-run only; never run a real reset.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 make reset removes storage/ and recreates it with storage/.gitkeep (one tree instead of four folders)
- [x] #2 make reset-hard does the same, in addition to its image/build-cache pruning
- [x] #3 The WARNING and ## help text refer to storage/ and its qdrant/ollama/openwebui/opencode data
- [x] #4 make -n reset and make -n reset-hard (dry run) show the storage/ operations without executing a real reset
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Makefile reset + reset-hard: change rm -rf/mkdir -p/touch to operate on a single storage/ tree (rm -rf storage; mkdir -p storage; touch storage/.gitkeep); update WARNING + ## help to reference storage/. 2. Validate make -n reset / reset-hard (dry run only; never a real reset).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
reset and reset-hard now do rm -rf storage && mkdir -p storage && touch storage/.gitkeep. WARNING and reset ## help updated to "storage/ (qdrant, ollama, openwebui, opencode data)". Verified dry-run only: make -n reset and make -n reset-hard both show the three storage/ operations; no real reset executed.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Updated Makefile reset/reset-hard to wipe/recreate the single storage/ tree with storage/.gitkeep, plus WARNING/help text. Verified via make -n dry-runs (both targets).
<!-- SECTION:FINAL_SUMMARY:END -->
