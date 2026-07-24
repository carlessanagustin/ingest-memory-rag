---
id: TASK-10
title: Document connecting Claude Code to the Qdrant MCP server (HTTP)
status: To Do
assignee: []
created_date: '2026-07-24 11:08'
labels: []
dependencies:
  - TASK-9
references:
  - 'https://github.com/qdrant/mcp-server-qdrant'
ordinal: 12000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Document how to configure Claude Code to use the HTTP/SSE Qdrant MCP server (from the shared setup in TASK-9) so it can query the ingested knowledge base. Cover adding the server and confirming the tools are available.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Docs show adding the Qdrant MCP server to Claude Code as an HTTP/SSE server (claude mcp add with an sse/http transport and/or a .mcp.json entry using the remote server type and URL)
- [ ] #2 Both project-scoped (.mcp.json committed to the repo) and user-scoped configuration options are described
- [ ] #3 Docs show how to confirm the server and its tools are available (the /mcp view) and include a sample query against the ingested data
<!-- AC:END -->
