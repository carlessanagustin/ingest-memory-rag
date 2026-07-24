---
id: TASK-4
title: >-
  Store Qdrant data in a gitignored local folder instead of a named Docker
  volume
status: Done
assignee:
  - '@claude'
created_date: '2026-07-23 15:05'
updated_date: '2026-07-24 07:52'
labels: []
dependencies:
  - TASK-1
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Change the qdrant service in `docker-compose.yml` to persist storage in a local bind-mounted folder (for example `./qdrant_storage`) instead of the named `qdrant_storage` Docker volume, and ensure that folder is not committed. This makes the vector data visible and manageable on the host. Note: edits `docker-compose.yml`, which is shared with the containerization work.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The qdrant service bind-mounts a local folder (for example `./qdrant_storage`) to `/qdrant/storage` and no longer declares the named `qdrant_storage` volume
- [x] #2 The local storage folder is ignored by git via `.gitignore`, with the folder kept in the repo through a placeholder if needed
- [x] #3 After `docker compose up`, Qdrant data is written under the local folder and persists across `docker compose down` and restart
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. docker-compose.yml: change qdrant volume from the named volume "qdrant_storage" to a bind mount ./qdrant_storage:/qdrant/storage; remove the top-level volumes: declaration. 2. .gitignore: ignore qdrant_storage/* but keep qdrant_storage/.gitkeep. 3. Add qdrant_storage/.gitkeep placeholder. 4. Verify: docker compose up qdrant populates ./qdrant_storage on the host; create a collection; docker compose down; confirm data remains on host; up again; collection still present (persistence).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Verified: docker compose config has no top-level named volumes; ./qdrant_storage on the host is populated by Qdrant (aliases/, collections/, raft_state.json). Created collection persist_test, ran docker compose down, data remained on host, docker compose up again -> persist_test still present (persists across restart). git check-ignore confirms qdrant_storage/* is ignored while qdrant_storage/.gitkeep is kept.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Switched Qdrant storage from the named docker volume to a bind mount (./qdrant_storage:/qdrant/storage) and removed the top-level volumes: declaration; gitignored qdrant_storage/* with a .gitkeep placeholder. Verified via docker compose that Qdrant writes its storage to ./qdrant_storage on the host and a collection created before docker compose down survives a restart.
<!-- SECTION:FINAL_SUMMARY:END -->
