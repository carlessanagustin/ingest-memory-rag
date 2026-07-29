---
id: TASK-24
title: Reclaim disk from the bloated app image and stale build cache
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 08:59'
updated_date: '2026-07-29 09:07'
labels:
  - docker
  - ops
dependencies:
  - TASK-23
type: chore
ordinal: 26000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The earlier builds (before the .dockerignore fix) left a bloated `ingest-memory-rag-app` image (~70GB) plus dangling images and stale Docker build cache on the local machine. After TASK-23 produces a slim rebuild, remove the stale/dangling image layers and prune the build cache to reclaim the disk. This is a local Docker environment cleanup only — no repository files change. Note it forces the next build to run without the old cache.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 After a slim rebuild (TASK-23), stale/dangling `ingest-memory-rag-app` image layers from the bloated builds are removed
- [x] #2 Docker build cache entries from the bloated builds are pruned
- [x] #3 Reclaimed disk is reported (e.g. `docker system df` before/after), and `ingest-memory-rag-app:latest` is the new slim image
- [x] #4 No repository files are changed (local environment cleanup only)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. docker system df (before).
2. Prune dangling images (the old ~70GB ingest-memory-rag layers, now untagged after the slim rebuild) with docker image prune -f, and stale build cache with docker builder prune -f.
3. Do NOT touch tagged images (keep ingest-memory-rag-app:latest 1.03GB, qdrant/ollama/lobe-chat) or any running containers (unrelated workloads are running).
4. docker system df (after); confirm slim image intact; report reclaimed disk.
Local ops only, no repo change. Delegated to sherpa:docky (synchronous); backlog in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Done by the sherpa:docky agent (targeted, safe). docker system df BEFORE: Images 33.57GB (28.87GB reclaimable); AFTER: 31.23GB. docker image prune -f removed 5 dangling images -> 2.341GB reclaimed; docker builder prune -f -> 2.286MB (remaining cache showed 0B reclaimable, left in place). Combined ~2.343GB reclaimed. Slim ingest-memory-rag-app:latest (1.03GB) intact; all other tagged images (qdrant/ollama/lobe-chat/uv/python) preserved; unrelated running containers (bold_elgamal, peaceful_matsumoto) untouched; no docker system prune -a, no volume prune, no repo changes. NOTE: the earlier "~70GB" was Docker per-image LOGICAL size (overcounts shared layers) — actual on-disk dangling reclaim was ~2.34GB. Remaining ~26.5GB "reclaimable" is TAGGED but currently-unused images from other projects, intentionally not pruned (out of scope / could disrupt unrelated work). The durable fix is TASK-23 (.dockerignore) which stops the bloat recurring.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Reclaimed local Docker disk after the bloated builds: pruned dangling images (2.34GB) and stale build cache, leaving the slim ingest-memory-rag-app:latest (1.03GB) and all tagged images/running containers untouched. Reported via docker system df before/after. The headline ~70GB was Docker logical per-image size (shared-layer overcount); real on-disk dangling reclaim was ~2.34GB, and TASK-23 prevents recurrence. Local-env cleanup only, no repo changes.
<!-- SECTION:FINAL_SUMMARY:END -->
