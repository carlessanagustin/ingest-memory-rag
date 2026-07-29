---
id: TASK-19
title: 'Auto-provision the qwen3.6:27b model into Ollama on startup'
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 08:01'
updated_date: '2026-07-29 08:16'
labels:
  - docker
  - ollama
dependencies:
  - TASK-18
references:
  - 'https://ollama.com/library/qwen3.6'
type: feature
ordinal: 21000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Ollama does not download models on its own, so add a one-shot companion service (e.g. `ollama-pull`) that runs `ollama pull qwen3.6:27b` against the ollama server once it is healthy, then exits. This makes the model available automatically after `docker compose up` without a manual step. The pull is idempotent (a no-op if the model is already present in the persisted volume from TASK-18). Heads-up: qwen3.6:27b is a large download (~tens of GB) and first startup will take a while.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 docker-compose.yml defines a one-shot service that pulls `qwen3.6:27b` into the ollama server after it is healthy (`depends_on` ollama `service_healthy`) and does not stay running (`restart: "no"`)
- [x] #2 The pull targets the in-network server (e.g. `OLLAMA_HOST=http://ollama:11434`), not a separate embedded server, so the model lands in the persisted volume
- [x] #3 After `docker compose up`, `qwen3.6:27b` appears in `GET http://localhost:11434/api/tags` (and `ollama list`)
- [x] #4 Re-running `docker compose up` does not re-download the model (idempotent; served from the persisted volume)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add a one-shot `ollama-pull` service to docker-compose.yml: image ollama/ollama:latest, depends_on ollama service_healthy, OLLAMA_HOST=http://ollama:11434, command ["pull","qwen3.6:27b"] (ollama image ENTRYPOINT is /bin/ollama), restart "no".
2. Verify: docker compose up ollama + ollama-pull -> pull completes against the in-network server; qwen3.6:27b appears in GET /api/tags and `ollama list`; second `up` is idempotent (no re-download); tear down.
Implementation + real pull delegated to sherpa:docky (background); backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by the sherpa:docky agent; verified with a real pull. Added one-shot `ollama-pull` (ollama/ollama:latest, depends_on ollama service_healthy, OLLAMA_HOST=http://ollama:11434, command ["pull","qwen3.6:27b"], restart "no"). Agent evidence: first run downloaded a single ~17GB blob (qwen3.6:27b, 27.8B, Q4_K_M) and exited 0; GET /api/tags and `ollama list` both show qwen3.6:27b (17GB); second `docker compose up ollama-pull` completed in <1s with all layers already present (no re-download) and model still present; docker compose down clean. Independently confirmed: compose VALID with ollama-pull listed; service block correct; ./ollama_storage persisted 16G with manifest models/manifests/registry.ollama.ai/library/qwen3.6/27b. Model data is gitignored (won't be committed).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added a one-shot `ollama-pull` compose service that pulls qwen3.6:27b into the ollama server over the network (OLLAMA_HOST=http://ollama:11434) once it is healthy, then exits (restart "no"), so the model is provisioned automatically on `docker compose up` and persists in the gitignored ./ollama_storage volume. Verified with a real ~17GB pull: model appears in /api/tags and `ollama list`, and a second run is a <1s no-op (idempotent).
<!-- SECTION:FINAL_SUMMARY:END -->
