---
id: TASK-12
title: Document connecting pi.dev (Pi coding agent) to the Qdrant MCP server (HTTP)
status: To Do
assignee: []
created_date: '2026-07-24 11:08'
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
- [ ] #1 Docs note that Pi has no built-in MCP support and that MCP is provided via the pi MCP extension/adapter
- [ ] #2 Docs show installing the pi MCP extension/adapter and adding the Qdrant MCP server to its config (e.g. ~/.pi/agent/mcp.json) as an SSE/StreamableHTTP server with the URL
- [ ] #3 Docs show how to confirm the tools are available in Pi and include a sample query against the ingested data
<!-- AC:END -->
