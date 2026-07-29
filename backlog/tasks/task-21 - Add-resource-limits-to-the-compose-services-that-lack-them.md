---
id: TASK-21
title: Add resource limits to the compose services that lack them
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 08:33'
updated_date: '2026-07-29 08:38'
labels:
  - docker
  - ops
dependencies: []
references:
  - 'https://docs.docker.com/reference/compose-file/deploy/#resources'
  - docker-compose.yml
type: enhancement
ordinal: 23000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Only the `lobe-chat` service currently declares `deploy.resources`; `qdrant`, `app`, `mcp-qdrant`, and `ollama` have none, so a runaway container could starve the host. Add `deploy.resources` (limits + reservations) to those four services, matching the style already used by `lobe-chat`. Size `ollama` generously: it must be able to load and run qwen3.6:27b, and a memory limit below the model working set (~18-24GB) would OOM it — prefer a high memory ceiling (or leave memory uncapped and cap CPU only), and note that the Docker Desktop VM must actually be allocated that much RAM. The one-shot `ollama-pull` is short-lived, so limits there are optional. Keep chosen values in tunable comments.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `qdrant`, `app`, `mcp-qdrant`, and `ollama` each declare `deploy.resources` with `limits` (cpus + memory) and `reservations`, in the same style as the existing `lobe-chat` service
- [x] #2 The `ollama` memory limit is high enough not to constrain loading qwen3.6:27b (documented), or memory is intentionally left uncapped with only CPU limited
- [x] #3 The existing `lobe-chat` limits remain intact
- [x] #4 `docker compose config` validates and the rendered config shows limits + reservations for each of the four services
- [x] #5 `docker compose up -d` brings every long-running service to healthy under the applied limits — no container is capped so low it fails to start or crashes
- [x] #6 Chosen values are documented with comments and easy to tune
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Add deploy.resources (limits + reservations) to the four services lacking them, mirroring lobe-chat style:
- qdrant: limits cpus "2"/memory 2G; reservations cpus "0.5"/memory 512M
- app: limits cpus "2"/memory 1.5G; reservations cpus "0.5"/memory 512M (runs fastembed on startup scan)
- mcp-qdrant: limits cpus "2"/memory 1.5G; reservations cpus "0.5"/memory 512M (runs fastembed for queries)
- ollama: limits cpus "8"/memory 24G; reservations cpus "1"/memory 2G (must fit qwen3.6:27b; comment that the Docker Desktop VM must have the RAM)
Leave lobe-chat + ollama-pull as-is. Add tunable-value comments.
Verify: docker compose config valid + rendered limits for the four; docker compose up -d -> healthchecked services healthy and app running (no OOMKilled/crash) under limits; then down.
Delegated to sherpa:docky (background); backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by the sherpa:docky agent; verified. Added deploy.resources (limits+reservations, tunable comments) to qdrant (2C/2G, res 0.5C/512M), app (2C/1.5G, res 0.5C/512M), mcp-qdrant (2C/1.5G, res 0.5C/512M), ollama (memory 24G, res 1C/2G). lobe-chat and ollama-pull left unchanged. Adaptation: ollama cpus lowered 8->6 because this Docker Desktop VM only exposes 6 vCPUs (docker compose up errored at container creation with cpus:8: "range of CPUs is from 0.01 to 6.00"); documented inline. Agent verification: docker compose config exit 0; rendered limits correct for all four; docker compose up -d -> qdrant/mcp-qdrant/ollama/lobe-chat (healthy), app Up (no healthcheck yet, expected), ollama-pull Exited 0 (cache no-op); none Restarting/OOMKilled; docker inspect confirms per-container Memory/NanoCpus applied (e.g. ollama mem=25769803776 nanocpus=6000000000); docker compose down clean. Independently re-confirmed the four deploy blocks in source + config VALID.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added deploy.resources (limits + reservations, tunable) to the four compose services that lacked them — qdrant (2C/2G), app (2C/1.5G), mcp-qdrant (2C/1.5G), and ollama (6C/24G, sized to fit qwen3.6:27b) — leaving lobe-chat and the one-shot ollama-pull unchanged. ollama CPU was capped at 6 to match this Docker Desktop VM (documented). Verified: docker compose config valid, all services start healthy/running under the limits with none OOM-killed, and docker inspect confirms the cgroup limits are applied.
<!-- SECTION:FINAL_SUMMARY:END -->
