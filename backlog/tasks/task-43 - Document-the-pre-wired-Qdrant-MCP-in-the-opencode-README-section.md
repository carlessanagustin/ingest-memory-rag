---
id: TASK-43
title: Document the pre-wired Qdrant MCP in the opencode README section
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 10:47'
updated_date: '2026-07-30 10:56'
labels:
  - docs
  - opencode
  - mcp
dependencies:
  - TASK-42
type: docs
ordinal: 45000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update the README so the containerized opencode service documents that the Qdrant MCP is already wired in via http://mcp-qdrant:8000/mcp (server-side, using the compose service name mcp-qdrant, not localhost), and how to use the qdrant-find tool from the opencode web UI to search the ingested Document collection. Keep the existing host-run opencode MCP example intact or cross-reference it.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The opencode service subsection (Docker Compose) states the Qdrant MCP is pre-wired at http://mcp-qdrant:8000/mcp and that opencode connects server-side using the compose service name mcp-qdrant
- [x] #2 The docs explain how to use qdrant-find from the opencode web UI to query the Document collection
- [x] #3 The existing host-run opencode MCP example is preserved or clearly cross-referenced
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. In the opencode service subsection, add a RAG bullet: Qdrant MCP pre-wired in compose/opencode/opencode.json at http://mcp-qdrant:8000/mcp, server-side via service name mcp-qdrant (not localhost), qdrant-find loaded at startup, example query against the Document collection, waits for mcp-qdrant healthy. 2. Preserve the existing host-run opencode MCP example (line ~357).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
README opencode subsection: added an Ingested-docs search (RAG) bullet stating the Qdrant MCP is pre-wired at http://mcp-qdrant:8000/mcp, opencode connects server-side using the service name mcp-qdrant (not localhost), waits for mcp-qdrant healthy, loads qdrant-find at startup, with an example query against the Document collection. The existing host-run opencode MCP example (127.0.0.1:8000/sse) is preserved.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Documented the pre-wired Qdrant MCP in the opencode service subsection (server-side via mcp-qdrant, qdrant-find usage against the Document collection); host-run example left intact.
<!-- SECTION:FINAL_SUMMARY:END -->
