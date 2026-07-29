---
id: TASK-23
title: Exclude ollama_storage from the Docker build context (fix .dockerignore)
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 08:59'
updated_date: '2026-07-29 09:04'
labels:
  - docker
  - ops
dependencies: []
references:
  - Dockerfile
  - .dockerignore
type: bug
ordinal: 25000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The Dockerfile copies the whole build context into the app image (`COPY . .`), and the later `chown -R /app` duplicates it into a second layer. `.dockerignore` excludes `raw/` and `qdrant_storage/` but NOT `ollama_storage/` (the gitignored local Ollama model store added in TASK-18), so the ~16GB of pulled model data is copied into the image twice, bloating `ingest-memory-rag-app` to tens of GB. Add `ollama_storage/` to `.dockerignore` (mirroring the existing `qdrant_storage/` entry) so model data never enters the build context or image. No application behaviour change.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `.dockerignore` excludes `ollama_storage/`, grouped with the existing `raw/` and `qdrant_storage/` local-data entries
- [x] #2 Rebuilding the app image contains no ollama_storage/model data and is dramatically smaller than the bloated image (target on the order of a few hundred MB, well under ~1.5GB)
- [x] #3 The build context transferred to the daemon no longer includes the ~16GB ollama_storage (much smaller "transferring context" size on build)
- [x] #4 The app still builds and runs: `docker compose up -d qdrant app` brings `app` to healthy (TASK-22 healthcheck)
- [x] #5 Change is limited to `.dockerignore`
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add `ollama_storage/` to .dockerignore, grouped with raw/ and qdrant_storage/.
2. Rebuild the app image (foreground) and verify it is now small (no model data, well under ~1.5GB) with a small build context; app still comes up healthy.
Change limited to .dockerignore. Delegated to sherpa:docky (synchronous, foreground build); backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by the sherpa:docky agent (foreground build, no stall); verified. Added `ollama_storage/` to .dockerignore in the local-data group (line 23, next to raw/ and qdrant_storage/). Evidence: build "transferring context" dropped from ~16GB to 262.57kB; image ingest-memory-rag-app:latest 69.7GB -> 1.03GB; in-image check du -sh /app = 280M and NO_OLLAMA_STORAGE_IN_IMAGE; docker compose up -d qdrant app -> app (healthy); torn down. Independently re-confirmed: .dockerignore has ollama_storage/, image is 1.03GB, only .dockerignore changed for this task.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added `ollama_storage/` to .dockerignore so the 16GB local Ollama model store no longer enters the Docker build context (which COPY . . + chown -R had been duplicating into the app image). Build context dropped from ~16GB to ~262kB and the app image from ~70GB to 1.03GB, with no model data baked in and the app still building/running healthy. One-line, .dockerignore-only change.
<!-- SECTION:FINAL_SUMMARY:END -->
