---
id: TASK-55
title: Drop OpenWebUI from the Makefile reset/reset-hard text
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 14:02'
updated_date: '2026-07-30 14:06'
labels:
  - makefile
  - openwebui
  - cleanup
dependencies:
  - TASK-54
type: chore
ordinal: 57000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The reset and reset-hard targets describe the storage/ wipe by enumerating services including OpenWebUI. With OpenWebUI removed, update the ## help and WARNING text to drop the openwebui/OpenWebUI mentions. The wipe logic itself (rm -rf storage) is generic and stays unchanged.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The Makefile reset and reset-hard ## help and WARNING text no longer mention openwebui or OpenWebUI
- [x] #2 The remaining enumerated data (qdrant, ollama, opencode) is accurate
- [x] #3 make -n reset and make -n reset-hard still show the storage/ wipe (rm -rf storage / mkdir -p storage / touch storage/.gitkeep) without executing a real reset
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Makefile reset/reset-hard: remove openwebui/OpenWebUI from the ## help + WARNING text, keeping qdrant/ollama/opencode. 2. make -n reset/reset-hard still show the storage/ wipe.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Makefile reset and reset-hard ## help + WARNING text now enumerate storage/ (qdrant, ollama, opencode data) with no openwebui/OpenWebUI mentions; grep openwebui in Makefile == 0. The rm -rf storage / mkdir -p storage / touch storage/.gitkeep logic is unchanged; make -n reset and reset-hard still show the storage/ wipe.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Dropped OpenWebUI from the Makefile reset/reset-hard help and WARNING text (logic unchanged). Verified via grep (0 openwebui) and make -n dry-runs.
<!-- SECTION:FINAL_SUMMARY:END -->
