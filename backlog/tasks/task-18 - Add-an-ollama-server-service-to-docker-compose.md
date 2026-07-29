---
id: TASK-18
title: Add an ollama server service to docker-compose
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 08:01'
updated_date: '2026-07-29 08:10'
labels:
  - docker
  - ollama
dependencies: []
references:
  - 'https://hub.docker.com/r/ollama/ollama'
  - /Users/sanagu0000/repos/carles/app-pii/compose/lobe-chat.yml
type: feature
ordinal: 20000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add an `ollama` service to docker-compose.yml so the stack can serve local LLMs. It runs the official ollama/ollama image on the shared default compose network, exposes the API on 11434, and persists downloaded models to a gitignored local folder (matching the existing ./qdrant_storage bind-mount convention) so models survive restarts and are not re-downloaded. This service is the LLM backend that TASK-19 pulls a model into and TASK-20 wires lobe-chat to. Note: a 27B model needs substantial RAM and, on Docker Desktop (macOS/Windows), runs CPU-only (no GPU passthrough); GPU acceleration applies only on a Linux host with a supported GPU.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 docker-compose.yml defines an `ollama` service using the official `ollama/ollama` image, on the same default network as the other services, with the API published on host port 11434 and reachable in-network at `http://ollama:11434`
- [x] #2 Downloaded models persist across restarts via a gitignored local bind-mount folder (e.g. `./ollama_storage:/root/.ollama`), added to `.gitignore` like `./qdrant_storage`
- [x] #3 The service has a healthcheck that only reports healthy once the Ollama API is serving, plus `restart: unless-stopped`
- [x] #4 `docker compose config` validates and `docker compose up -d ollama` brings the service healthy; `GET http://localhost:11434/api/tags` returns 200
- [x] #5 A short comment documents the CPU-only behaviour on Docker Desktop and where to enable GPU reservations on a Linux host
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add an `ollama` service to docker-compose.yml: image ollama/ollama, container_name ollama, ports 11434:11434, models persisted to gitignored ./ollama_storage:/root/.ollama, healthcheck that only passes once the API serves, restart unless-stopped, on the default network. Comment on CPU-only (Docker Desktop) vs GPU (Linux+NVIDIA).
2. Add ./ollama_storage to .gitignore and a .gitkeep placeholder, mirroring ./qdrant_storage.
3. Verify: docker compose config valid; docker compose up -d ollama -> healthy; GET http://localhost:11434/api/tags -> 200.
Implementation + verification delegated to the sherpa:docky agent; backlog + git handled in the main loop.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by the sherpa:docky agent; verified. Added `ollama` (ollama/ollama:latest) on the default network, port 11434 (in-network http://ollama:11434), models persisted to gitignored ./ollama_storage:/root/.ollama (.gitignore mirrors qdrant_storage: `ollama_storage/*` + `!ollama_storage/.gitkeep`; .gitkeep created), healthcheck `ollama list` (healthy only once API serves), restart unless-stopped, plus a comment on CPU-only Docker Desktop and a commented-out Linux+NVIDIA GPU reservations block. Agent verification: docker compose config VALID with ollama listed; docker compose up -d ollama -> Up (healthy); curl http://localhost:11434/api/tags -> 200; container on network ingest-memory-rag_default; docker compose down clean; no models pulled. Independently re-confirmed static config: compose VALID, services {app,lobe-chat,mcp-qdrant,ollama,qdrant}, service block + .gitignore + .gitkeep all present.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added an `ollama` server service to docker-compose.yml (official image, host+in-network port 11434, gitignored ./ollama_storage model persistence mirroring qdrant_storage, API-serving healthcheck, restart policy, CPU-only note + commented GPU block). Verified via docker compose config, a healthy container, and http://localhost:11434/api/tags returning 200.
<!-- SECTION:FINAL_SUMMARY:END -->
