---
id: TASK-93
title: 'Align MCP section transports, dedupe opencode, and remove pi.dev'
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 14:39'
updated_date: '2026-08-04 14:54'
labels:
  - docs
dependencies:
  - TASK-92
ordinal: 95000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Make the MCP client instructions consistent and non-redundant: one coherent transport story aligned with the compose bridge (Streamable HTTP /mcp) and the standalone SSE where applicable, merge the two opencode subsections into one, and remove the pi.dev subsection plus its stray mentions (MCP intro, client lists).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The MCP client docs use a consistent, accurate transport story (no contradictory /mcp vs /sse for the same client); Claude Code (stdio) and opencode paths retained and correct
- [x] #2 The two opencode subsections are merged into a single coherent one
- [x] #3 The pi.dev subsection is removed, and pi.dev is removed from the MCP intro and any client lists
- [x] #4 Changes limited to README.md
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
MCP align to streamable-http /mcp; merge two opencode subsections; remove pi.dev + stray mentions. part of one coherent README.md refactor pass
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
MCP aligned to Streamable HTTP /mcp everywhere (standalone example uses --transport streamable-http; clients use http://localhost:8000/mcp or http://mcp-qdrant:8000/mcp); all /sse guidance removed (Claude Code stays stdio, remote note uses --transport http). The two opencode subsections merged into one "opencode (web coding agent + CLI)". pi.dev subsection + all stray mentions removed (grep clean).
<!-- SECTION:FINAL_SUMMARY:END -->
