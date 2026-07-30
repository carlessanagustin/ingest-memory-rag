---
id: TASK-42
title: Wire the Qdrant MCP server into the opencode config
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 10:47'
updated_date: '2026-07-30 10:55'
labels:
  - docker
  - opencode
  - mcp
dependencies: []
references:
  - 'https://opencode.ai/docs'
type: feature
ordinal: 44000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add the Qdrant MCP bridge to the opencode service so opencode can query the ingested Document collection via the qdrant-find tool. Add an mcp entry to the committed opencode config (compose/opencode/opencode.json) pointing at http://mcp-qdrant:8000/mcp using the opencode remote MCP schema (type remote, enabled), alongside the existing Ollama provider. Because opencode loads MCP servers at startup and connects server-side inside the compose network, also make the opencode service wait for mcp-qdrant to be healthy so the tool loads reliably on first boot.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 compose/opencode/opencode.json contains an mcp entry named qdrant with type remote, url http://mcp-qdrant:8000/mcp, and enabled true, with the existing Ollama provider block intact
- [x] #2 compose/opencode.yaml declares depends_on mcp-qdrant with condition service_healthy (in addition to ollama)
- [x] #3 docker compose config validates and shows the opencode dependency on mcp-qdrant
- [x] #4 The opencode config remains valid JSON with no secrets
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. compose/opencode/opencode.json: add top-level mcp.qdrant { type: remote, url: http://mcp-qdrant:8000/mcp, enabled: true }, keep the provider block; valid JSON. 2. compose/opencode.yaml: add mcp-qdrant to depends_on with condition service_healthy (alongside ollama). 3. Validate with docker compose config.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added top-level mcp.qdrant (type remote, url http://mcp-qdrant:8000/mcp, enabled true) to compose/opencode/opencode.json alongside the Ollama provider; added mcp-qdrant: condition service_healthy to compose/opencode.yaml depends_on. Verified: python3 json.load -> JSON_OK; docker compose config -> CONFIG_OK; the opencode depends_on shows both mcp-qdrant and ollama service_healthy.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Wired the Qdrant MCP into opencode (remote MCP at http://mcp-qdrant:8000/mcp) and made opencode wait for mcp-qdrant to be healthy. Verified valid JSON and docker compose config.
<!-- SECTION:FINAL_SUMMARY:END -->
