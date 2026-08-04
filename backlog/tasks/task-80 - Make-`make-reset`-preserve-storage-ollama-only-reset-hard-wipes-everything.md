---
id: TASK-80
title: Make `make reset` preserve storage/ollama (only reset-hard wipes everything)
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 08:55'
updated_date: '2026-08-04 08:59'
labels:
  - chore
dependencies: []
ordinal: 82000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Change the reset target so it no longer deletes the downloaded Ollama models, avoiding a multi-GB re-download after a routine reset. reset should wipe all other storage state (qdrant, opencode, and any future service dir) but keep storage/ollama. reset-hard keeps its current behaviour of deleting the entire storage/ tree (models included). The Makefile `##` help text is the only user-facing documentation for these targets, so update it too (README does not document them).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `make reset` no longer deletes storage/ollama; pulled models persist across a reset
- [x] #2 `make reset` still removes every other top-level entry under storage/ (e.g. storage/qdrant, storage/opencode) plus any future non-ollama dir, using a generic rule (find ... ! -name ollama ! -name .gitkeep), not a hardcoded per-service list
- [x] #3 After `make reset`, storage/ and storage/.gitkeep still exist and storage/ollama (when present) is untouched; a missing storage/ollama causes no error
- [x] #4 The reset WARNING and `##` help text are updated to say Ollama models are preserved (no longer deletes the ~17GB model) and that reset-hard is what removes everything including models
- [x] #5 `make reset-hard` still deletes the entire storage/ tree (behaviour unchanged); its message makes the reset-vs-reset-hard difference clear
- [x] #6 The existing confirmation prompt (read -p) and `docker compose down` step are preserved in reset
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. In the reset recipe, replace `rm -rf storage && mkdir -p storage && touch storage/.gitkeep` with a selective wipe that spares ollama:
   `mkdir -p storage && find storage -mindepth 1 -maxdepth 1 ! -name ollama ! -name .gitkeep -exec rm -rf {} + && touch storage/.gitkeep`.
2. Update reset `##` help text + WARNING: models are preserved (reset no longer deletes the Ollama model); reset-hard is what removes everything incl. models.
3. reset-hard delete logic unchanged (still rm -rf storage); tweak its message to contrast with reset.
4. Keep the read -p confirmation and `docker compose down` step in reset.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
reset now runs `mkdir -p storage && find storage -mindepth 1 -maxdepth 1 ! -name ollama ! -name .gitkeep -exec rm -rf {} + && touch storage/.gitkeep` instead of `rm -rf storage`, so the Ollama models are preserved while qdrant/opencode (and any other dir) are wiped; the read -p prompt and `docker compose down` are kept. Help text + WARNING updated to say models are preserved and that reset-hard removes everything. reset-hard delete logic unchanged (still rm -rf storage), message tweaked to contrast. Verified: git diff; `make -n reset` shows the find line and no `rm -rf storage`; `make -n reset-hard` still shows `rm -rf storage`; `make help` renders updated text; throwaway-tree simulation confirmed reset keeps ollama+.gitkeep and removes qdrant+opencode, reset-hard removes all.
<!-- SECTION:FINAL_SUMMARY:END -->
