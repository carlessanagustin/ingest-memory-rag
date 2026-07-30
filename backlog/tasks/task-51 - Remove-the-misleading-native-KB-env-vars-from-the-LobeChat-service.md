---
id: TASK-51
title: Remove the misleading native-KB env vars from the LobeChat service
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 13:00'
updated_date: '2026-07-30 13:07'
labels:
  - docker
  - lobechat
  - mcp
dependencies: []
type: chore
ordinal: 53000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
compose/lobechat.yaml carries LobeChat native knowledge-base env vars (VECTOR_DB, QDRANT_URL, QDRANT_URI, QDRANT_COLLECTION_NAME, COLLECTION_NAME) that read from .env via the ${VAR:-} default. That native KB is the wrong path for querying the ingested Document collection (it manages its own collection/embeddings and typically needs the server-DB edition); the intended path is the qdrant-find MCP plugin added in the LobeChat UI. If .env sets VECTOR_DB=qdrant these would activate the native path on the PGlite community image. Remove them from the lobe-chat service (keep the Ollama wiring, provider-key vars and ACCESS_CODE) and add a short comment that Qdrant RAG is via the qdrant-find MCP plugin. Also remove any VECTOR_DB/QDRANT_URI/QDRANT_COLLECTION_NAME lines from the local .env.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The lobe-chat service no longer sets VECTOR_DB, QDRANT_URL, QDRANT_URI, QDRANT_COLLECTION_NAME or COLLECTION_NAME
- [x] #2 The Ollama wiring (ENABLED_OLLAMA, OLLAMA_PROXY_URL), provider-key env and ACCESS_CODE remain intact
- [x] #3 A brief comment notes that Qdrant RAG is via the qdrant-find MCP plugin, not LobeChat native KB
- [x] #4 The local .env no longer sets VECTOR_DB/QDRANT_URI/QDRANT_COLLECTION_NAME
- [x] #5 docker compose config validates
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. compose/lobechat.yaml: remove the # Qdrant block (VECTOR_DB, QDRANT_URL, QDRANT_URI, QDRANT_COLLECTION_NAME, COLLECTION_NAME); keep ACCESS_CODE, provider keys, ENABLED_OLLAMA, OLLAMA_PROXY_URL; add a comment that Qdrant RAG is via the qdrant-find MCP plugin. 2. .env: remove VECTOR_DB/QDRANT_URI/QDRANT_COLLECTION_NAME lines; keep QDRANT_URL and QDRANT_INDEX. 3. docker compose config validates.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Removed the # Qdrant block (VECTOR_DB, QDRANT_URL, QDRANT_URI, QDRANT_COLLECTION_NAME, COLLECTION_NAME) from the lobe-chat environment; added a comment that Qdrant RAG is via the qdrant-find MCP plugin. Kept ACCESS_CODE, provider keys, ENABLED_OLLAMA, OLLAMA_PROXY_URL. Removed VECTOR_DB/QDRANT_URI/QDRANT_COLLECTION_NAME (+ the # lobe-chat header) from .env; kept QDRANT_URL/QDRANT_INDEX. Verified: grep of lobechat.yaml for native-KB vars == 0; the resolved lobe-chat service in docker compose config has no VECTOR_DB/QDRANT/COLLECTION vars (the remaining COLLECTION_NAME=Document belongs to mcp-qdrant); docker compose config -> CONFIG_OK.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Removed the misleading native-KB env vars from the lobe-chat service and local .env (kept Ollama wiring). Verified the lobe-chat service in docker compose config carries no Qdrant/native-KB vars and config validates.
<!-- SECTION:FINAL_SUMMARY:END -->
