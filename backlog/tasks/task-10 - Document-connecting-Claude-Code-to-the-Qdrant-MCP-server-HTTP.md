---
id: TASK-10
title: Document connecting Claude Code to the Qdrant MCP server (HTTP)
status: Done
assignee:
  - '@claude'
created_date: '2026-07-24 11:08'
updated_date: '2026-07-24 13:00'
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
- [x] #1 Docs show adding the Qdrant MCP server to Claude Code as an HTTP/SSE server (claude mcp add with an sse/http transport and/or a .mcp.json entry using the remote server type and URL)
- [x] #2 Both project-scoped (.mcp.json committed to the repo) and user-scoped configuration options are described
- [x] #3 Docs show how to confirm the server and its tools are available (the /mcp view) and include a sample query against the ingested data
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Add a Claude Code subsection under the README MCP section: the claude mcp add command for an SSE server, a project-scoped .mcp.json entry (type sse, url), a note on user vs project scope, and how to confirm via /mcp + a sample query. Verify the claude mcp add flags against claude mcp add --help.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added a Claude Code subsection to the README MCP section. Verified the command against claude mcp add --help and by running add/get/remove: claude mcp add --transport sse qdrant http://127.0.0.1:8000/sse registers a Type: sse server (get showed Type: sse + URL; removed cleanly). Documented --scope project (shared .mcp.json) vs --scope user, the equivalent .mcp.json (type sse + url), and verifying via /mcp + a sample query.

Post-completion correction: switched the README Claude Code subsection from SSE to stdio. Claude Code runs an OAuth handshake for HTTP/SSE MCP servers, but mcp-server-qdrant has no auth, so an SSE entry stalls at "not authenticated" and fails to connect. The stdio form (claude mcp add qdrant -e QDRANT_URL=... -e COLLECTION_NAME=Document -e EMBEDDING_MODEL=... -- uvx mcp-server-qdrant) has Claude Code spawn the server locally with no auth; verified claude mcp get qdrant reports Status: Connected. SSE remains documented for remote/shared use (needs an auth layer).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added a Claude Code subsection to the README MCP section: claude mcp add --transport sse for the SSE server, an equivalent project-scoped .mcp.json (type sse + url), a note on --scope project vs user, and verifying via /mcp + a sample query. Verified the command registers an SSE server (add/get/remove).
<!-- SECTION:FINAL_SUMMARY:END -->
