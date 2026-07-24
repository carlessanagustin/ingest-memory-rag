---
id: TASK-13
title: Merge the MCP docs into the README (condensed) and remove docs/mcp.md
status: Done
assignee:
  - '@claude'
created_date: '2026-07-24 12:23'
updated_date: '2026-07-24 12:32'
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
- [x] #1 README has one MCP section with the essentials: the command to run the official mcp-server-qdrant over SSE against local Qdrant (QDRANT_URL=http://localhost:6333, COLLECTION_NAME=Document), the SSE endpoint (http://127.0.0.1:8000/sse), and pointers to the per-client setup (Claude Code, opencode, pi.dev)
- [x] #2 The section is condensed (no long compatibility explanation) and replaces the previous README pointer-to-docs rather than duplicating it
- [x] #3 docs/mcp.md is deleted, the docs/ folder is removed if it becomes empty, and no remaining links point to docs/mcp.md
- [x] #4 README still renders correctly: valid Markdown, and the Mermaid diagram and other sections remain intact
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Replace the README MCP pointer section with a condensed MCP section: one-line intro, the SSE run command (QDRANT_URL, COLLECTION_NAME=Document, EMBEDDING_MODEL, uvx mcp-server-qdrant --transport sse), the SSE endpoint http://127.0.0.1:8000/sse, and that Claude Code/opencode/pi.dev connect to it. Drop the long compatibility explanation. 2. Delete docs/mcp.md; remove docs/ if empty. 3. Verify no links to docs/mcp.md remain, README Markdown is valid, and the Mermaid diagram is intact.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Replaced the README MCP pointer with a condensed section (SSE run command + endpoint http://127.0.0.1:8000/sse + client pointers for Claude Code/opencode/pi.dev + the embedding-model caveat); dropped the long compatibility explanation. Deleted docs/mcp.md and removed the now-empty docs/ folder. Verified: grep shows 0 docs/mcp.md links in README, code-fence count is even (balanced), Mermaid diagram still present. Remaining docs/mcp.md mentions are only in TASK-9 historical notes.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Merged the MCP docs into a single condensed README section (SSE run command, endpoint http://127.0.0.1:8000/sse, and client pointers for Claude Code/opencode/pi.dev), replacing the previous pointer, and deleted docs/mcp.md plus the now-empty docs/ folder. Verified no README links to docs/mcp.md, balanced code fences, and an intact Mermaid diagram.
<!-- SECTION:FINAL_SUMMARY:END -->
