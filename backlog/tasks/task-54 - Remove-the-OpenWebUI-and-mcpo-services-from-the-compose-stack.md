---
id: TASK-54
title: Remove the OpenWebUI and mcpo services from the compose stack
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 14:02'
updated_date: '2026-07-30 14:06'
labels:
  - docker
  - openwebui
  - cleanup
dependencies: []
type: chore
ordinal: 56000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Remove the OpenWebUI web UI and its mcpo (MCP-to-OpenAPI) bridge completely. mcpo exists solely to feed OpenWebUI and has no other consumer; mcp-qdrant stays because LobeChat and opencode use it directly. Delete compose/openwebui.yaml (both services) and compose/mcpo.config.json, remove the commented compose/openwebui.yaml entry from the docker-compose.yml include list, and remove the orphaned storage/openwebui data folder. The rest of the stack (qdrant, app, mcp-qdrant, ollama, ollama-pull, lobe-chat, opencode) must be unaffected.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 compose/openwebui.yaml and compose/mcpo.config.json are deleted
- [x] #2 The docker-compose.yml include list no longer references compose/openwebui.yaml (the commented lines are removed)
- [x] #3 The orphaned storage/openwebui data folder is removed
- [x] #4 docker compose config validates and contains no openwebui or mcpo service; mcp-qdrant and all other services remain
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Delete compose/openwebui.yaml and compose/mcpo.config.json. 2. Remove the commented #- path: compose/openwebui.yaml (+ its project_directory line) from docker-compose.yml include. 3. rm -rf storage/openwebui (orphaned, if present). 4. docker compose config validates; no openwebui/mcpo; mcp-qdrant + rest intact.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Deleted compose/openwebui.yaml and compose/mcpo.config.json; removed the two commented compose/openwebui.yaml include lines from docker-compose.yml; rm -rf storage/openwebui (did not exist). Verified: docker compose config -> CONFIG_OK; grep openwebui|mcpo in config == 0; mcp-qdrant retained (3 matches); compose services = app lobe-chat mcp-qdrant ollama ollama-pull opencode qdrant (no openwebui/mcpo).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Removed the openwebui + mcpo services (deleted compose/openwebui.yaml, compose/mcpo.config.json, the commented include line, and orphaned storage/openwebui). Verified docker compose config is valid with no openwebui/mcpo and mcp-qdrant + all other services retained.
<!-- SECTION:FINAL_SUMMARY:END -->
