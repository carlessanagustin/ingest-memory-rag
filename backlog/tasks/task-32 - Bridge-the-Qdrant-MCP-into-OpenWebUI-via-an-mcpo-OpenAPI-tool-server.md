---
id: TASK-32
title: Bridge the Qdrant MCP into OpenWebUI via an mcpo OpenAPI tool server
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 15:34'
updated_date: '2026-07-29 15:54'
labels:
  - docker
  - openwebui
  - mcp
dependencies:
  - TASK-31
references:
  - 'https://github.com/open-webui/mcpo'
  - docker-compose.yml
type: feature
ordinal: 34000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
OpenWebUI has no native MCP client; it consumes external tools as OpenAPI tool servers. To let OpenWebUI query the app-ingested Document collection, add an mcpo (MCP-to-OpenAPI proxy, image ghcr.io/open-webui/mcpo:main) service that fronts the existing mcp-qdrant streamable-http server and exposes it as an OpenAPI endpoint, then document registering that endpoint in OpenWebUI as a tool server so a tool-calling Ollama model can invoke qdrant-find. Put mcpo in compose/prompt.yaml alongside openwebui. Clarify in docs that this MCP path reads the app-ingested data, and that OpenWebUI native RAG (VECTOR_DB=qdrant) is a different feature that is not used here (also remove the stray VECTOR_DB/QDRANT_URI env that was mistakenly left on the disabled lobe-chat service).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 compose/prompt.yaml defines an mcpo service (ghcr.io/open-webui/mcpo:main) that fronts the qdrant MCP (connecting to the existing mcp-qdrant streamable-http endpoint http://mcp-qdrant:8000/mcp via mcpo config, or running its own mcp-server-qdrant), exposing an OpenAPI endpoint on a stable in-network URL, with appropriate depends_on and a restart policy
- [x] #2 The mcpo OpenAPI endpoint exposes the qdrant-find operation (its generated openapi.json/docs list a qdrant-find path) and a call returns results from the ingested Document collection
- [x] #3 README documents registering the mcpo OpenAPI server in OpenWebUI (Settings tool-server URL) and a verification chat query that uses qdrant-find over the ingested files, noting this is the MCP path to the app-ingested data and that OpenWebUI native RAG (VECTOR_DB) is intentionally not used
- [x] #4 docker compose config is valid; bringing up qdrant + mcp-qdrant + mcpo + openwebui works and the qdrant-find tool is callable end to end (connectivity verified even if the final in-chat step needs a tool-calling model)
- [x] #5 Changes are limited to compose/prompt.yaml, README.md, and (if needed) .env.example; the stray VECTOR_DB/QDRANT_URI env on the commented lobe-chat service is removed
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add mcpo service (ghcr.io/open-webui/mcpo:main) to compose/prompt.yaml fronting the existing mcp-qdrant streamable-http endpoint (http://mcp-qdrant:8000/mcp) via an mcpo config file (compose/mcpo.config.json mounted in), exposing an OpenAPI endpoint on a stable in-network URL (e.g. http://mcpo:8000). depends_on mcp-qdrant; restart policy; verify exact mcpo flags via --help in the image.
2. Remove the stray VECTOR_DB/QDRANT_URI lines from the commented lobe-chat block.
3. README: document registering the mcpo OpenAPI tool server in OpenWebUI (Settings) + a qdrant-find verification query; clarify this is the MCP path to app-ingested data and that OpenWebUI native RAG (VECTOR_DB) is not used.
4. Verify: mcpo OpenAPI exposes a qdrant-find path; seed a tiny doc into raw + run app to ingest into the Document collection; call qdrant-find through mcpo -> returns that content; clean up the seed doc; down (no -v).
Delegated to sherpa:docky (sync); backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by sherpa:docky; verified end-to-end. Added mcpo (ghcr.io/open-webui/mcpo:main) to compose/prompt.yaml, command --config /config/mcpo.config.json, mounting compose/mcpo.config.json (streamable-http -> http://mcp-qdrant:8000/mcp), depends_on mcp-qdrant service_healthy, host port 8001:8000 (mcp-qdrant owns 8000), curl /docs healthcheck, restart + limits. mcpo mounts the server under /qdrant, exposing /qdrant/openapi.json + /qdrant/docs and POST tool routes /qdrant/qdrant-find and /qdrant/qdrant-store (body {"query": ...}). Removed the stray VECTOR_DB/QDRANT_URI lines from the commented lobe-chat block. README: added "### OpenWebUI (tool server via mcpo)" documenting registration (Settings -> Tools; URL http://mcpo:8000/qdrant server-side / http://localhost:8001/qdrant from host), a qdrant-find verification chat prompt + equivalent curl, and a note that this is the MCP path to app-ingested data and OpenWebUI native RAG (VECTOR_DB) is not used. Verification: mcpo --help confirmed --config multi-server mode + streamable-http type; docker compose config VALID, services include mcpo (not lobe-chat); up qdrant+mcp-qdrant+mcpo -> healthy; /qdrant/openapi.json lists /qdrant-find + /qdrant-store; END-TO-END: seeded raw/_mcpo_smoketest.md (pineapple lighthouse), ran app until Document points_count=1, POST http://localhost:8001/qdrant/qdrant-find {"query":"pineapple lighthouse"} returned the seeded content; seed file deleted; down without -v (data folders untouched). Extra file created beyond the AC list: compose/mcpo.config.json (necessary for mcpo). Env note: the Document collection had been emptied by an earlier make reset; the smoke test repopulated one point then removed the source file.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Bridged the Qdrant MCP into OpenWebUI via an mcpo (MCP-to-OpenAPI) service in compose/prompt.yaml, fronting the existing mcp-qdrant streamable-http server (compose/mcpo.config.json) and re-exposing qdrant-find/qdrant-store as an OpenAPI tool server on host 8001 (in-network http://mcpo:8000/qdrant). Documented registering it in OpenWebUI plus a verification query, and clarified this MCP path reads the app-ingested Document collection while OpenWebUI native RAG (VECTOR_DB) is not used; also removed the stray VECTOR_DB/QDRANT_URI env from the disabled lobe-chat. Verified end-to-end: OpenAPI exposes qdrant-find and a seeded document was retrieved through app -> Qdrant -> mcp-qdrant -> mcpo.
<!-- SECTION:FINAL_SUMMARY:END -->
