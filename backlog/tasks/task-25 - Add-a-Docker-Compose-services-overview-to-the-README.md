---
id: TASK-25
title: Add a Docker Compose services overview to the README
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 09:10'
updated_date: '2026-07-29 09:14'
labels:
  - docs
dependencies: []
references:
  - docker-compose.yml
type: docs
ordinal: 27000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The README documents the LobeChat and Ollama additions in prose but has no single place that mirrors the full docker-compose.yml topology. Add a concise "Compose services" overview table to the README listing every service, its image, published host port (if any), and one-line purpose, and note that the long-running services now have healthchecks and resource limits (added in TASK-18..22) while ollama-pull is a one-shot model puller. This gives readers an at-a-glance map of the running stack that matches docker-compose.yml.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 README contains a compose-services overview table covering all six services: qdrant, app, mcp-qdrant, ollama, ollama-pull, lobe-chat — each with its image, published host port (or none/one-shot), and a one-line purpose
- [x] #2 Published ports match docker-compose.yml exactly: qdrant 6333 (REST/UI) + 6334 (gRPC), mcp-qdrant 8000 (/mcp), ollama 11434, lobe-chat 3210; app and ollama-pull expose no host port
- [x] #3 The overview notes that long-running services have healthchecks and resource limits, and that ollama-pull is a one-shot job that pulls qwen3.6:27b
- [x] #4 The overview is consistent with the existing Setup and MCP/LobeChat/Ollama sections (no contradictions) and placed sensibly (e.g. under Setup)
- [x] #5 Only README.md is changed
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Add a "Compose services" overview table to the README (under Setup / Run the full stack) listing all six services with image, published host port, and purpose, and noting healthchecks + resource limits on long-running services and the one-shot puller. Ports from compose: qdrant 6333/6334, mcp-qdrant 8000, ollama 11434, lobe-chat 3210; app + ollama-pull none. README-only. Delegated to sherpa:docky (sync); verify content vs compose + only README changed; backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by the sherpa:docky agent; verified. Added a **Compose services** table under Setup > Run the full stack (README lines ~95-106, before Run locally), as a bold-label block (no new heading, so no duplicate anchor). Covers all six services with image, host port(s), and purpose; ports verified against docker-compose.yml (qdrant 6333/6334, mcp-qdrant 8000, ollama 11434, lobe-chat 3210; app + ollama-pull none). Follow-up note states long-running services have healthchecks + CPU/memory limits and ollama-pull is a one-shot with none. Independently confirmed: docker compose config --services lists the six; the table region renders as valid GFM; only README.md changed.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added a "Compose services" overview table to the README (under Setup) mirroring docker-compose.yml: all six services with image, published host port, and purpose, plus a note that long-running services have healthchecks + resource limits and ollama-pull is a one-shot puller. Ports/images verified against the compose file; README-only change.
<!-- SECTION:FINAL_SUMMARY:END -->
