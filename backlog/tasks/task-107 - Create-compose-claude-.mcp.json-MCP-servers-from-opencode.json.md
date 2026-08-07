---
id: TASK-107
title: Create compose/claude/.mcp.json (MCP servers) from opencode.json
status: Done
assignee:
  - '@claude'
created_date: '2026-08-07 14:21'
updated_date: '2026-08-07 14:22'
labels:
  - claude
  - mcp
  - config
dependencies: []
ordinal: 109000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Translate the mcp section of compose/opencode/opencode.json into a Claude Code .mcp.json at compose/claude/.mcp.json (Claude Code uses the mcpServers key; there is no single claude.json holding mcp+agent+default_agent — confirmed via the claude-code-guide). Include BOTH servers. qdrant_remote: OpenCode type "remote" becomes Claude type "http" with url http://mcp-qdrant:8000/mcp. qdrant_local: OpenCode local/command-array becomes stdio with command "uvx" and args ["mcp-server-qdrant"], environment becomes env, and OpenCode {env:VAR} interpolation becomes Claude ${VAR}. Drop the OpenCode-only "enabled" field. Recommended subagent: general-purpose (schema already confirmed via claude-code-guide).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 compose/claude/.mcp.json is valid JSON (jq parses it) with a top-level mcpServers object containing qdrant_remote and qdrant_local
- [x] #2 qdrant_remote has type http and url http://mcp-qdrant:8000/mcp
- [x] #3 qdrant_local has command uvx, args [mcp-server-qdrant], and an env object with keys QDRANT_URL, COLLECTION_NAME, EMBEDDING_MODEL
- [x] #4 env uses Claude ${VAR} interpolation: QDRANT_URL=${QDRANT_URL}, COLLECTION_NAME=${QDRANT_INDEX}; EMBEDDING_MODEL is the literal sentence-transformers/all-MiniLM-L6-v2
- [x] #5 No OpenCode-only keys remain (no "enabled", no "type":"remote"/"local")
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Create compose/claude/.mcp.json with mcpServers { qdrant_remote (type http, url http://mcp-qdrant:8000/mcp), qdrant_local (type stdio, command uvx, args [mcp-server-qdrant], env QDRANT_URL=${QDRANT_URL}, COLLECTION_NAME=${QDRANT_INDEX}, EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2) }.
2. Translations: opencode remote->http, local command-array->command+args, environment->env, {env:X}->${X}; drop enabled.
3. Verify jq parses it and the keys/values are as specified.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Created compose/claude/.mcp.json. jq validates it; mcpServers has qdrant_remote (type http, url http://mcp-qdrant:8000/mcp) and qdrant_local (type stdio, command uvx, args [mcp-server-qdrant], env QDRANT_URL=${QDRANT_URL}, COLLECTION_NAME=${QDRANT_INDEX}, EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2). Applied translations: opencode remote->http, command-array->command+args, environment->env, {env:X}->${X}; dropped the opencode-only enabled field. grep confirms no enabled/type:remote/type:local remain.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added compose/claude/.mcp.json translating the opencode.json mcp section to Claude Code mcpServers (qdrant_remote as http, qdrant_local as stdio uvx with ${VAR} env interpolation). Verified valid via jq and field-by-field against the source.
<!-- SECTION:FINAL_SUMMARY:END -->
