---
id: TASK-29
title: Add a Makefile `reset-hard` target (also remove built image + prune)
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 09:31'
updated_date: '2026-07-29 09:38'
labels:
  - docker
  - ops
dependencies:
  - TASK-28
references:
  - Makefile
type: chore
ordinal: 31000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Recommended companion to `reset`: a `reset-hard` target that does everything `reset` does and ALSO removes the locally-built app image and prunes dangling images + build cache, so the next build/up is truly from scratch (fresh image build + fresh model pull + empty Qdrant). Same destructive-confirmation and warning. Scope strictly to this projects artifacts: do NOT run `docker system prune -a` or `docker volume prune`, and do not remove unrelated images/containers.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A new phony target (e.g. `reset-hard`) exists with a `## ...` help description and appears in `make help`
- [x] #2 It performs the `reset` cleanup (stack down + wipe qdrant_storage/ and ollama_storage/ down to just .gitkeep) AND removes the locally-built app image (e.g. ingest-memory-rag-app) and prunes dangling images + build cache
- [x] #3 It is guarded by confirmation and does NOT remove unrelated images/containers, nor run docker system prune -a / docker volume prune
- [x] #4 It modifies no git-tracked files and preserves ./raw
- [x] #5 After running, the built app image is gone and the data folders contain only .gitkeep, so the next `make up` rebuilds the image, re-pulls the model, and starts Qdrant empty
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add a phony `reset-hard` target + ## help, self-contained (own confirm, not chained to reset to avoid a double prompt).
2. Recipe: warn + interactive [y/N]; on y -> docker compose down --rmi local --remove-orphans (--rmi local removes only the locally-built app image, not pulled images like qdrant/ollama/lobe-chat), then wipe qdrant_storage/ollama_storage to just .gitkeep, then docker image prune -f (dangling) + docker builder prune -f (unused cache). Scoped: NO docker system prune -a, NO volume prune, no unrelated images. Leave ./raw.
3. Verify SAFELY: make help lists it; make -n reset-hard shows the full sequence (incl. --rmi local + prunes); abort path (printf n | make reset-hard) leaves the real 16GB model + app image intact; folder-wipe logic already proven in TASK-28 sandbox. Do NOT run the real proceed-path.
Delegated to sherpa:docky; backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by the sherpa:docky agent; verified SAFELY (real model + app image preserved). Added phony `reset-hard` (self-contained, own [y/N] confirm): warns, then on y -> docker compose down --rmi local --remove-orphans (removes only the locally-built app image, not pulled images) && wipe qdrant_storage/ollama_storage to .gitkeep && docker image prune -f && docker builder prune -f && "Hard reset complete"; else "Aborted." Scope guard verified: no docker system prune -a and no docker volume prune anywhere in the Makefile; ./raw untouched. Verification: make help lists reset-hard; make -n reset-hard shows the full sequence (down --rmi local, folder wipe, image prune, builder prune); abort path (printf n | make reset-hard) printed the warning + Aborted and did nothing (ollama_storage/models still 16G, ingest-memory-rag-app:latest still 1.03GB). Folder-wipe logic already proven in the TASK-28 sandbox. The destructive proceed-path was intentionally NOT executed against real state (would remove the model + app image + prune). Independently re-confirmed .PHONY, target block, scope guard, intact real state, and only Makefile changed.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added a `make reset-hard` target: everything `reset` does (stack down + wipe qdrant_storage/ollama_storage to .gitkeep) plus `docker compose down --rmi local` to drop the locally-built app image and `docker image prune -f` + `docker builder prune -f` for a fully-from-scratch rebuild — guarded by confirmation, scoped to project artifacts (no system prune -a / volume prune / unrelated images), ./raw preserved. Verified safely (make help, make -n, abort path) without destroying the real 16GB model or app image. Makefile-only change.
<!-- SECTION:FINAL_SUMMARY:END -->
