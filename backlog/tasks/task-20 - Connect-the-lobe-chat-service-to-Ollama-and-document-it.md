---
id: TASK-20
title: Connect the lobe-chat service to Ollama and document it
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 08:02'
updated_date: '2026-07-29 08:20'
labels:
  - docker
  - ollama
  - lobechat
dependencies:
  - TASK-18
references:
  - /Users/sanagu0000/repos/carles/app-pii/compose/lobe-chat.yml
  - 'https://lobehub.com/docs'
type: feature
ordinal: 22000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Wire the existing lobe-chat compose service to the new ollama server so Ollama models (e.g. qwen3.6:27b from TASK-19) are selectable in LobeChat alongside the OpenAI/Anthropic providers. Add the Ollama provider env (enable Ollama + point it at the in-network server), make lobe-chat depend on ollama, and document how to select and use the Ollama model in the README. This does not replace the existing providers; it adds Ollama as another option.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The `lobe-chat` service enables the Ollama provider and points it at the in-network server (`ENABLED_OLLAMA=1`, `OLLAMA_PROXY_URL=http://ollama:11434`), keeping the existing OpenAI/Anthropic env intact
- [x] #2 The `lobe-chat` service `depends_on` the ollama service so it starts after it
- [x] #3 From the lobe-chat container, the ollama API is reachable by name (`http://ollama:11434/api/tags` returns 200)
- [x] #4 The README documents that LobeChat can use the local Ollama model: how to select the `qwen3.6:27b` model in the UI, that the model is provided by the ollama service (TASK-18/19), and the CPU/RAM caveat
- [x] #5 `docker compose config` validates and the change is limited to docker-compose.yml, README, and (if needed) .env.example
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. lobe-chat service: add ENABLED_OLLAMA="1" and OLLAMA_PROXY_URL=http://ollama:11434 (keep existing OpenAI/Anthropic env); add depends_on ollama (condition: service_healthy).
2. README: extend the LobeChat section to document the local Ollama option (select the Ollama provider + qwen3.6:27b model in the UI; model is provided by the ollama + ollama-pull services; CPU-only/RAM caveat), and update the "whole stack" service list to include ollama + ollama-pull.
3. Verify: docker compose config valid; up ollama + lobe-chat; from the lobe-chat container reach http://ollama:11434/api/tags -> 200 with qwen3.6:27b listed; rendered config shows the new env + depends_on.
Implementation + verification delegated to sherpa:docky; backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by the sherpa:docky agent; verified. lobe-chat: added ENABLED_OLLAMA="1" and OLLAMA_PROXY_URL=http://ollama:11434 (OpenAI/Anthropic/ACCESS_CODE env kept), plus depends_on ollama condition: service_healthy. README: extended the "Run the full stack" blurb + code comment to include ollama/ollama-pull, added a "#### Local model via Ollama" subsection (pick Ollama provider + qwen3.6:27b in Settings -> AI Service Provider; model provided by ollama/ollama-pull; CPU-only + high-RAM caveat). No .env.example change needed. Agent verification: docker compose config exit 0; rendered lobe-chat config shows the env + depends_on; docker compose up -d ollama lobe-chat -> both Up (healthy); in-container check from lobe-chat `node http.get(http://ollama:11434/api/tags)` -> "HTTP 200 model-present"; docker compose down clean. Independently re-confirmed: compose VALID, rendered lobe-chat env/depends_on correct, README subsection + anchor present; TASK-20 touched only docker-compose.yml and README.md.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Wired the lobe-chat compose service to the local Ollama server: added ENABLED_OLLAMA=1 + OLLAMA_PROXY_URL=http://ollama:11434 (keeping OpenAI/Anthropic) and depends_on ollama (service_healthy), and documented it in the README (select the Ollama provider + qwen3.6:27b in the UI, provided by the ollama/ollama-pull services, with a CPU-only/high-RAM caveat; stack service list updated). Verified: compose config valid, both containers come up healthy, and from inside the lobe-chat container http://ollama:11434/api/tags returns HTTP 200 with qwen3.6:27b present.
<!-- SECTION:FINAL_SUMMARY:END -->
