---
id: TASK-11
title: Document connecting opencode to the Qdrant MCP server (HTTP)
status: Done
assignee:
  - '@claude'
created_date: '2026-07-24 11:08'
updated_date: '2026-07-24 12:40'
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
- [x] #1 Docs show adding the Qdrant MCP server to the opencode config (opencode.json) as a remote MCP server with its type and URL
- [x] #2 Any opencode-specific fields (enabled flag, remote vs local type) are documented
- [x] #3 Docs show how to confirm the tools are available in opencode and include a sample query against the ingested data
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Add an opencode subsection to the README MCP section: an opencode.json mcp entry for a remote SSE server (type remote, url, enabled), and how to confirm the tools + a sample query. Verify the config format against the opencode MCP docs.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added an opencode subsection to the README MCP section. Config format verified against the opencode MCP docs: opencode.json mcp entry with type "remote", url, and enabled. Documented pointing it at http://127.0.0.1:8000/sse and confirming via the loaded qdrant-find tool + a sample query.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added an opencode subsection to the README MCP section: an opencode.json mcp entry (type: remote, url, enabled) pointing at the SSE endpoint, plus confirming via the loaded qdrant-find tool and a sample query. Config format verified against the opencode MCP docs.
<!-- SECTION:FINAL_SUMMARY:END -->
