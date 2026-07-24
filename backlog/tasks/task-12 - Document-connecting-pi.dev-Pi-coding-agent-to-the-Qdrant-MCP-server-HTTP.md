---
id: TASK-12
title: Document connecting pi.dev (Pi coding agent) to the Qdrant MCP server (HTTP)
status: Done
assignee:
  - '@claude'
created_date: '2026-07-24 11:08'
updated_date: '2026-07-24 12:41'
labels: []
dependencies:
  - TASK-9
references:
  - 'https://pi.dev'
  - 'https://github.com/0xKobold/pi-mcp'
ordinal: 14000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Document how to configure pi.dev (the Pi coding agent at https://pi.dev) to use the HTTP/SSE Qdrant MCP server (from TASK-9). Note that Pi has no built-in MCP support; MCP is enabled via a community extension/adapter (pi-mcp / pi-mcp-adapter). Cover installing the extension and connecting it to the Qdrant MCP server over SSE/StreamableHTTP.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Docs note that Pi has no built-in MCP support and that MCP is provided via the pi MCP extension/adapter
- [x] #2 Docs show installing the pi MCP extension/adapter and adding the Qdrant MCP server to its config (e.g. ~/.pi/agent/mcp.json) as an SSE/StreamableHTTP server with the URL
- [x] #3 Docs show how to confirm the tools are available in Pi and include a sample query against the ingested data
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Add a pi.dev subsection to the README MCP section: note Pi has no built-in MCP (use the pi-mcp extension/adapter), show the ~/.pi/agent/mcp.json entry for the SSE/StreamableHTTP Qdrant server, and how to confirm the tools + a sample query. Verify the config format against the pi-mcp docs.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added a pi.dev subsection to the README MCP section. Verified config against the pi-mcp repo (0xKobold/pi-mcp): Pi has no built-in MCP, so a community adapter is used; registered the SSE Qdrant server in the adapter config (~/.0xkobold/mcp.json) with servers[].transport {type sse, url}, enabled, autoReconnect. Documented confirming via /mcp discover (or /mcp status) + a sample query, and noted config path/format follow the chosen adapter. Note: the ecosystem has multiple pi MCP adapters; documented pi-mcp concretely.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added a pi.dev subsection to the README MCP section: notes Pi has no built-in MCP and uses a community adapter (pi-mcp), shows registering the SSE Qdrant server in the adapter config (~/.0xkobold/mcp.json), and confirming via /mcp discover + a sample query. Config format verified against the pi-mcp repo.
<!-- SECTION:FINAL_SUMMARY:END -->
