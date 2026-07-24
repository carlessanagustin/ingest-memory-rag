---
id: TASK-13
title: Merge the MCP docs into the README (condensed) and remove docs/mcp.md
status: To Do
assignee: []
created_date: '2026-07-24 12:23'
labels: []
dependencies:
  - TASK-9
ordinal: 15000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Fold the MCP documentation from docs/mcp.md into README.md as a single condensed section, then delete docs/mcp.md so the README is the one source. The current README MCP pointer (which links to docs/mcp.md) is replaced by the merged section, not duplicated. Keep only the essentials; drop the longer compatibility explanation.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 README has one MCP section with the essentials: the command to run the official mcp-server-qdrant over SSE against local Qdrant (QDRANT_URL=http://localhost:6333, COLLECTION_NAME=Document), the SSE endpoint (http://127.0.0.1:8000/sse), and pointers to the per-client setup (Claude Code, opencode, pi.dev)
- [ ] #2 The section is condensed (no long compatibility explanation) and replaces the previous README pointer-to-docs rather than duplicating it
- [ ] #3 docs/mcp.md is deleted, the docs/ folder is removed if it becomes empty, and no remaining links point to docs/mcp.md
- [ ] #4 README still renders correctly: valid Markdown, and the Mermaid diagram and other sections remain intact
<!-- AC:END -->
