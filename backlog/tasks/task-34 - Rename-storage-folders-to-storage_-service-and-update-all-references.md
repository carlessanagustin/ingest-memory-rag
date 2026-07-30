---
id: TASK-34
title: Rename storage folders to storage_<service> and update all references
status: Done
assignee:
  - '@carles'
created_date: '2026-07-30 06:36'
updated_date: '2026-07-30 06:51'
labels:
  - docker
  - ops
dependencies:
  - TASK-33
references:
  - .gitignore
  - .dockerignore
  - Makefile
type: chore
ordinal: 36000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Rename the three gitignored data bind-mount folders to a storage_<service name> convention, preserving their contents: qdrant_storage -> storage_qdrant, ollama_storage -> storage_ollama, openwebui_storage -> storage_openwebui. These hold real data (the pulled ~6.6GB qwen3.5:9b Ollama model and the Qdrant collection), so rename on disk with mv (stack down first) and do NOT re-download. Then update every reference: the bind-mount paths in compose/qdrant.yaml, compose/ollama.yaml, and compose/openwebui.yaml (openwebui lives there after TASK-33); the .gitignore entries and the .gitkeep placeholders; the .dockerignore entries (which currently list only qdrant and ollama - add storage_openwebui too, per the request to add those folders to .dockerignore); the Makefile reset and reset-hard targets (which reference the old names and would otherwise break, and should also wipe storage_openwebui now that OpenWebUI persists state); and the README mention. A repo-wide grep for the old names (excluding backlog history) must come back empty.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The folders are renamed on disk to storage_qdrant, storage_ollama, storage_openwebui with contents preserved (the Ollama model and Qdrant data survive; no re-download); the old-named folders no longer exist
- [x] #2 Bind-mount paths are updated in compose/qdrant.yaml (./storage_qdrant), compose/ollama.yaml (./storage_ollama), and compose/openwebui.yaml (./storage_openwebui), and docker compose config resolves each to repo-root/storage_<service>
- [x] #3 .gitignore lists storage_qdrant/*, storage_ollama/*, storage_openwebui/* each with a !.../.gitkeep exception; each storage_<service>/.gitkeep exists; no stale qdrant_storage/ollama_storage/openwebui_storage entries remain
- [x] #4 .dockerignore excludes all three folders (storage_qdrant/, storage_ollama/, storage_openwebui/) - including storage_openwebui which was previously absent - with no stale old names
- [x] #5 Makefile reset and reset-hard reference the new folder names (and clear storage_openwebui too); make -n reset shows the correct sequence and no old names remain in the Makefile
- [x] #6 README and any other non-backlog reference updated; a repo-wide grep for qdrant_storage/ollama_storage/openwebui_storage (excluding backlog/ and .git/) returns nothing
- [x] #7 docker compose config is valid and bringing up qdrant + ollama uses the renamed folders with data intact (e.g. ollama list still shows qwen3.5:9b without a re-pull)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Stack DOWN first (no -v). Rename on disk with mv (preserve data): qdrant_storage->storage_qdrant, ollama_storage->storage_ollama, openwebui_storage->storage_openwebui. Ensure each storage_<svc>/.gitkeep exists.
2. Update bind mounts: compose/qdrant.yaml ./storage_qdrant, compose/ollama.yaml ./storage_ollama (+comment), compose/openwebui.yaml ./storage_openwebui.
3. .gitignore: rename all six lines to storage_*; .dockerignore: rename qdrant/ollama + ADD storage_openwebui.
4. Makefile reset + reset-hard: update names, add storage_openwebui to the wipe set.
5. README:272 ./ollama_storage -> ./storage_ollama.
6. Verify: docker compose config valid, volume sources = repo-root/storage_*; repo-wide grep (excl backlog/,.git/) for old names is empty; up qdrant+ollama with data intact -> ollama list shows qwen3.5:9b WITHOUT re-pull, qdrant collections present; make -n reset shows new names; down (no -v).
Delegated to sherpa:docky (sync); backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by sherpa:docky; verified with data preserved. Renamed on disk with mv (stack was down): ollama_storage->storage_ollama (6.1G, sha256 blobs present), qdrant_storage->storage_qdrant (3.2M, collections/Document present), openwebui_storage->storage_openwebui (977M); .gitkeep moved with each. Updated: compose bind mounts (qdrant.yaml ./storage_qdrant, ollama.yaml ./storage_ollama + comment, openwebui.yaml ./storage_openwebui); .gitignore (six storage_* lines + .gitkeep exceptions); .dockerignore (storage_qdrant/, storage_ollama/, and newly-added storage_openwebui/); Makefile reset + reset-hard (warning text, rm -rf, mkdir -p, touch .gitkeep all use the three new names incl. storage_openwebui); README:272 ./storage_ollama. Independently verified: old folders gone / new present with data; .gitignore + .dockerignore + compose + Makefile (9 storage_* refs, 0 old names) + README all updated; repo-wide grep for old names OUTSIDE backlog/ is CLEAN (only backlog history retains them, expected); docker compose config VALID with resolved volume sources repo-root/storage_qdrant|storage_ollama|storage_openwebui; up -d qdrant ollama -> healthy, ollama list shows qwen3.5:9b WITHOUT a re-pull, GET /collections shows Document; make -n reset shows new names; git check-ignore confirms storage_*/* ignored while .gitkeep kept; down without -v.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Renamed the three data bind-mount folders to the storage_<service> convention (qdrant_storage->storage_qdrant, ollama_storage->storage_ollama, openwebui_storage->storage_openwebui) with contents preserved (the 6.6GB qwen3.5:9b model and the Qdrant Document collection survived, no re-download), and updated every reference: the three compose bind mounts, .gitignore + .gitkeep placeholders, .dockerignore (now including storage_openwebui, previously missing), the Makefile reset/reset-hard targets (also clearing storage_openwebui), and the README. Verified: config valid with resolved sources at repo-root/storage_*, a clean repo-wide grep for old names outside backlog history, and qdrant+ollama coming up with data intact (ollama list still shows qwen3.5:9b without a re-pull).
<!-- SECTION:FINAL_SUMMARY:END -->
