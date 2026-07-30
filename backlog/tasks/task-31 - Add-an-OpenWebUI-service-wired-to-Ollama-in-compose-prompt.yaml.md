---
id: TASK-31
title: Add an OpenWebUI service wired to Ollama (in compose/prompt.yaml)
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 15:34'
updated_date: '2026-07-29 15:47'
labels:
  - docker
  - openwebui
  - ollama
dependencies:
  - TASK-30
references:
  - 'https://github.com/open-webui/open-webui'
  - /Users/sanagu0000/repos/carles/app-pii/compose/lobe-chat.yml
type: feature
ordinal: 33000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add an OpenWebUI service to compose/prompt.yaml wired to the in-network Ollama server so its models (e.g. qwen3.5:9b) are usable for chat. Use image ghcr.io/open-webui/open-webui:main, expose the UI on a free host port (container listens on 8080; lobe-chat 3210 is disabled, so 3000 is a good host port), set OLLAMA_BASE_URL=http://ollama:11434, persist data via a gitignored bind mount ./openwebui_storage:/app/backend/data mirroring the qdrant_storage/ollama_storage convention (.gitignore entry + .gitkeep placeholder), depends_on ollama service_healthy, and add a healthcheck, restart policy, and resource limits in the existing repo style. This task covers Ollama-backed chat only; wiring the Qdrant MCP is a separate task.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 compose/prompt.yaml defines an openwebui service (ghcr.io/open-webui/open-webui:main) published on a free host port mapped to container 8080, with depends_on ollama service_healthy, restart unless-stopped, a healthcheck, and deploy resource limits in the existing style
- [x] #2 OLLAMA_BASE_URL=http://ollama:11434 is set and, from the openwebui container, the Ollama API is reachable by name (http://ollama:11434/api/tags returns 200)
- [x] #3 OpenWebUI data persists via a gitignored ./openwebui_storage:/app/backend/data bind mount; .gitignore excludes it with a .gitkeep exception like qdrant_storage/ollama_storage, and openwebui_storage/.gitkeep exists
- [x] #4 docker compose config is valid; docker compose up -d ollama openwebui brings openwebui to healthy; the UI is reachable on the host port and an Ollama model is listed/selectable
- [x] #5 No host port clash with other services, and changes are limited to compose/prompt.yaml, .gitignore, and openwebui_storage/.gitkeep
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add openwebui service to compose/prompt.yaml: image ghcr.io/open-webui/open-webui:main, ports 3000:8080, env OLLAMA_BASE_URL=http://ollama:11434 + WEBUI_AUTH handling as needed, volume ./openwebui_storage:/app/backend/data, depends_on ollama service_healthy, healthcheck (curl/python on :8080/health or /), restart unless-stopped, deploy limits in repo style.
2. .gitignore: add openwebui_storage/* + !openwebui_storage/.gitkeep (mirror qdrant_storage/ollama_storage); create openwebui_storage/.gitkeep.
3. Verify: docker compose config valid; up -d ollama openwebui -> openwebui healthy; from openwebui container reach http://ollama:11434/api/tags -> 200; UI reachable on host 3000; then down (no -v).
Delegated to sherpa:docky (sync); backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by sherpa:docky; verified. Added openwebui to compose/prompt.yaml: image ghcr.io/open-webui/open-webui:main, ports 3000:8080, OLLAMA_BASE_URL=http://ollama:11434, WEBUI_AUTH=False, volume ./openwebui_storage:/app/backend/data, depends_on ollama service_healthy, python3 /health healthcheck (start_period 120s), restart unless-stopped, deploy limits (2C/2G). .gitignore: openwebui_storage/* + !openwebui_storage/.gitkeep (mirrors qdrant/ollama); openwebui_storage/.gitkeep created. lobe-chat block left commented. Verified: python3 present in image; docker compose config VALID with openwebui listed and lobe-chat absent; up -d ollama openwebui -> both healthy; in-container openwebui->http://ollama:11434/api/tags = HTTP 200; host http://localhost:3000/health = 200; rendered volume source = repo-root/openwebui_storage. IMPORTANT environment note: a `make reset` had wiped ollama_storage (model) and qdrant_storage (Document collection) earlier (raw/ also empty) - likely during the OOM troubleshooting. To fully prove AC4 (model listed) and restore the env, re-ran ollama-pull: qwen3.5:9b (6.6GB) pulled exit 0, ollama list shows it, and OpenWebUI reports models: [qwen3.5:9b]. Data folders remain gitignored. Only compose/prompt.yaml, .gitignore, openwebui_storage/.gitkeep changed for this task.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added an openwebui service (ghcr.io/open-webui/open-webui:main) to compose/prompt.yaml wired to the in-network Ollama server (OLLAMA_BASE_URL=http://ollama:11434), published on host 3000->8080, with a gitignored ./openwebui_storage bind mount, depends_on ollama healthy, a /health healthcheck, restart policy, and resource limits; lobe-chat stays disabled. Verified: config valid, both containers healthy, OpenWebUI reaches Ollama by name (HTTP 200), host /health 200, and after re-pulling qwen3.5:9b (the env had been reset) OpenWebUI lists the model. MCP wiring is the follow-up task.
<!-- SECTION:FINAL_SUMMARY:END -->
