---
id: TASK-46
title: >-
  Consolidate storage_<service> folders under a single storage/ and update
  compose mounts
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 11:57'
updated_date: '2026-07-30 12:01'
labels:
  - docker
  - storage
dependencies: []
type: chore
ordinal: 48000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Replace the four top-level storage_<service> bind-mount folders with a single storage/ folder holding one subfolder per service (storage/qdrant, storage/ollama, storage/openwebui, storage/opencode). Update the four compose bind mounts to ./storage/<service>. Per the chosen layout, track only storage/.gitkeep; service subfolders are created at runtime by Docker/compose. The current folders are empty (only .gitkeep), so no data migration is needed; remove the old empty storage_<service> folders.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 compose/qdrant.yaml mounts ./storage/qdrant:/qdrant/storage
- [x] #2 compose/ollama.yaml mounts ./storage/ollama:/root/.ollama
- [x] #3 compose/openwebui.yaml mounts ./storage/openwebui:/app/backend/data
- [x] #4 compose/opencode.yaml mounts ./storage/opencode:/root/.local/share/opencode
- [x] #5 storage/.gitkeep exists and is tracked; the old storage_qdrant, storage_ollama, storage_openwebui and storage_opencode folders are removed
- [x] #6 docker compose config validates with the new mount paths
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Update 4 compose bind mounts to ./storage/<service> (qdrant.yaml, ollama.yaml + its comment on line ~36, openwebui.yaml, opencode.yaml). 2. mkdir storage; touch storage/.gitkeep. 3. rm -rf the old empty storage_<service> dirs. 4. docker compose config validates.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Compose mounts updated: qdrant -> ./storage/qdrant, ollama -> ./storage/ollama (+comment), openwebui -> ./storage/openwebui, opencode -> ./storage/opencode. Created storage/.gitkeep; removed the four old empty storage_<svc> folders (git shows their tracked .gitkeep as deleted). docker compose config -> CONFIG_OK and grep -c storage_ == 0.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Consolidated the four storage_<service> bind-mount folders into a single storage/ tree; updated all four compose mounts to ./storage/<service>, added storage/.gitkeep, removed the old folders. Verified via docker compose config (valid, zero storage_).
<!-- SECTION:FINAL_SUMMARY:END -->
