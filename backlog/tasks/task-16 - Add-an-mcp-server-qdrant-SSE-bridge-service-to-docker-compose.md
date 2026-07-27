---
id: TASK-16
title: Add an mcp-server-qdrant (Streamable HTTP) bridge service to docker-compose
status: Done
assignee:
  - '@carles'
created_date: '2026-07-27 12:16'
updated_date: '2026-07-27 12:49'
labels:
  - docker
  - mcp
  - lobechat
dependencies: []
references:
  - 'https://github.com/qdrant/mcp-server-qdrant'
  - README.md
type: feature
ordinal: 18000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
LobeChat has no native Qdrant vector-store integration (its built-in knowledge base uses PostgreSQL + pgvector), but its plugin system speaks the Model Context Protocol. LobeChat 1.143.3 only supports `stdio` and Streamable HTTP for custom MCP servers (no SSE), so to let LobeChat query the ingested RAG data, add a compose service that runs the official mcp-server-qdrant over the Streamable HTTP transport, on the same network as qdrant, reachable by name. Point it at the existing collection using the same embedding model as ingestion so query vectors match stored vectors. This is the bridge TASK-17 wires LobeChat to.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 docker-compose.yml defines an MCP service that runs `mcp-server-qdrant` over the Streamable HTTP transport, configured with `QDRANT_URL=http://qdrant:6333`, `COLLECTION_NAME=Document`, and an embedding model matching ingestion (`sentence-transformers/all-MiniLM-L6-v2`)
- [x] #2 The Streamable HTTP endpoint binds to all interfaces so it is reachable from other compose services by name (e.g. `http://mcp-qdrant:8000/mcp`)
- [x] #3 The service uses `depends_on` with qdrant `service_healthy` and has a restart policy
- [x] #4 `docker compose config` validates, and after `docker compose up` the endpoint serves a working `qdrant-find` tool (verified with an MCP client)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Change the mcp-qdrant service command to `uvx mcp-server-qdrant@0.8.1 --transport streamable-http`.
2. Keep FASTMCP_SERVER_HOST=0.0.0.0 / FASTMCP_SERVER_PORT=8000 so the endpoint (http://mcp-qdrant:8000/mcp) binds all interfaces; update the port comment from /sse to /mcp.
3. Keep depends_on qdrant service_healthy, restart unless-stopped, TCP healthcheck on 8000, publish 8000.
4. Verify: docker compose config valid; bring up qdrant+mcp-qdrant; logs show Uvicorn on 0.0.0.0:8000; a Streamable HTTP MCP client (mcp SDK streamablehttp_client -> http://localhost:8000/mcp) lists tools and calls qdrant-find successfully; in-network reachability http://mcp-qdrant:8000/mcp from the qdrant peer container.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Transport changed from SSE to Streamable HTTP after discovering LobeChat 1.143.3 only supports stdio|http (Streamable HTTP), no SSE (source: packages/types/src/plugins/mcp.ts). Service: ghcr.io/astral-sh/uv:python3.12-bookworm-slim running `uvx mcp-server-qdrant@0.8.1 --transport streamable-http`, FASTMCP_SERVER_HOST=0.0.0.0/PORT=8000 (FastMCP 2.7.0 ignores FASTMCP_HOST), depends_on qdrant service_healthy, restart unless-stopped, TCP healthcheck, port 8000 published. Verified: docker compose config VALID; logs "Uvicorn running on http://0.0.0.0:8000"; Streamable HTTP MCP client (mcp SDK streamablehttp_client -> http://localhost:8000/mcp) initialize -> mcp-server-qdrant, list_tools -> [qdrant-find, qdrant-store], call qdrant-find(query="agentic coding") -> isError False with real ingested content; in-network by-name test from qdrant container GET http://mcp-qdrant:8000/mcp -> HTTP/1.1 307 (FastMCP /mcp -> /mcp/ redirect; client follows). Endpoint path is /mcp.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added an `mcp-qdrant` compose service running mcp-server-qdrant (pinned 0.8.1) over Streamable HTTP against qdrant, exposing qdrant-find/qdrant-store to in-network MCP clients at http://mcp-qdrant:8000/mcp (also published on host). Streamable HTTP chosen because LobeChat only supports stdio|Streamable HTTP for custom MCP (no SSE). Configured QDRANT_URL/COLLECTION_NAME=Document/EMBEDDING_MODEL to match ingestion, and FASTMCP_SERVER_HOST=0.0.0.0 to bind all interfaces (FastMCP 2.7.0 ignores FASTMCP_HOST). Verified via docker compose config, a Streamable HTTP MCP client that listed and successfully called qdrant-find (real results), and a by-name reachability test from the qdrant peer container.
<!-- SECTION:FINAL_SUMMARY:END -->
