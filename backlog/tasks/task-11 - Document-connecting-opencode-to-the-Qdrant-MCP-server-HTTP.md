---
id: TASK-11
title: Document connecting opencode to the Qdrant MCP server (HTTP)
status: To Do
assignee: []
created_date: '2026-07-24 11:08'
labels: []
dependencies:
  - TASK-9
references:
  - 'https://opencode.ai/docs/mcp-servers/'
ordinal: 13000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Document how to configure opencode (the opencode.ai coding agent) to use the HTTP/SSE Qdrant MCP server (from TASK-9) so it can query the ingested knowledge base.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Docs show adding the Qdrant MCP server to the opencode config (opencode.json) as a remote MCP server with its type and URL
- [ ] #2 Any opencode-specific fields (enabled flag, remote vs local type) are documented
- [ ] #3 Docs show how to confirm the tools are available in opencode and include a sample query against the ingested data
<!-- AC:END -->
