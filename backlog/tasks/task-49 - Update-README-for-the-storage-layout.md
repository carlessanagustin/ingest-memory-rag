---
id: TASK-49
title: Update README for the storage/ layout
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 11:57'
updated_date: '2026-07-30 12:02'
labels:
  - docs
  - storage
dependencies:
  - TASK-46
type: docs
ordinal: 51000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update all README references from storage_<service> to the new storage/<service> paths, including the ollama and opencode persistence mentions and any reset documentation, so the docs match the compose mounts and Makefile.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 README no longer references storage_qdrant, storage_ollama, storage_openwebui or storage_opencode; it uses storage/<service> paths
- [x] #2 The ollama and opencode persistence mentions point at storage/ollama and storage/opencode
- [x] #3 Any reset-related docs reflect the single storage/ tree
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Replace every storage_<service> reference in README with storage/<service>. 2. Focus points: the ollama persistence mention and the opencode Data & auth mention; any make reset docs. 3. Confirm no storage_ remains in README.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Updated the two README storage references: ./storage_ollama -> ./storage/ollama (Ollama persistence) and ./storage_opencode -> ./storage/opencode (opencode Data & auth). grep storage_ in README == 0. No make reset docs exist in README, so no reset-doc changes were needed.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Updated README to the storage/<service> layout (ollama + opencode persistence mentions). No storage_ references remain.
<!-- SECTION:FINAL_SUMMARY:END -->
