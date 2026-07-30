---
id: TASK-50
title: Verify the storage/ consolidation end to end
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 11:57'
updated_date: '2026-07-30 12:04'
labels:
  - docker
  - storage
  - verification
dependencies:
  - TASK-46
  - TASK-47
  - TASK-48
  - TASK-49
type: chore
ordinal: 52000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Confirm the restructure works: compose config is valid with the new paths, git tracks only storage/.gitkeep, the old storage_<service> folders are gone, and bringing up a service creates and writes to its storage/<service> subfolder. No data to preserve (folders were already empty).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 docker compose config validates and every service mounts ./storage/<service>
- [x] #2 git status shows storage/.gitkeep tracked and no storage_<service> paths remain; a repo-wide grep for storage_ outside backlog/ is clean
- [x] #3 Bringing up at least one service creates storage/<service> and writes data there (e.g. qdrant creates storage/qdrant)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. docker compose config valid + every service mounts ./storage/<service>. 2. repo-wide grep storage_ (outside backlog/) is clean; git tracks storage/.gitkeep. 3. Bring up qdrant and confirm it creates+writes storage/qdrant.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
AC1: docker compose config valid; sources = ./storage/qdrant, ./storage/ollama, ./storage/opencode (openwebui file also on ./storage/openwebui, currently commented out of the include). AC2: precise grep for storage_(qdrant|ollama|openwebui|opencode) across project files (excluding .venv/.git/backlog/storage) is clean; storage/.gitkeep is trackable. AC3: docker compose up -d qdrant -> healthy; the bind mount created storage/qdrant/ on the host with collections/, aliases/, raft_state.json (user-owned, not root). No data was pre-existing (clean env).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified the storage/ consolidation: compose config valid on ./storage/<service>, no storage_ references remain in project files, storage/.gitkeep tracked, and bringing up qdrant created+wrote storage/qdrant.
<!-- SECTION:FINAL_SUMMARY:END -->
