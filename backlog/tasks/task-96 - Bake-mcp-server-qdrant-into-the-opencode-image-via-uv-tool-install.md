---
id: TASK-96
title: Bake mcp-server-qdrant into the opencode image via uv tool install
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 15:38'
updated_date: '2026-08-04 15:43'
labels:
  - docker
dependencies:
  - TASK-95
ordinal: 98000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add `uv tool install mcp-server-qdrant` to compose/opencode/Dockerfile so the MCP server and all its dependencies are installed at build time. The qdrant_local stdio server in opencode.json runs `uvx mcp-server-qdrant`, which then reuses the baked-in install and starts without any runtime download. Do NOT run the server itself during build — `uvx mcp-server-qdrant` is a long-running stdio server and would hang the build. Optionally pin the version to match the compose mcp-qdrant bridge (mcp-server-qdrant@0.8.1) for consistency.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 compose/opencode/Dockerfile runs `uv tool install mcp-server-qdrant` (packages baked in); it does NOT start the server, so the build does not hang
- [x] #2 The opencode image builds successfully
- [x] #3 In the built image, `uvx mcp-server-qdrant` resolves from the baked-in install with no network download (reuses the installed tool)
- [x] #4 Change limited to compose/opencode/Dockerfile
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Add `RUN uv tool install mcp-server-qdrant@0.8.1` (pin to match the compose mcp-qdrant bridge) after the uv install. Do NOT run the server (no blocking uvx). Baked-in tool -> runtime `uvx mcp-server-qdrant` reuses it with no download. Build to confirm no hang.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Dockerfile runs `uv tool install --python 3.12 mcp-server-qdrant@0.8.1` (pinned to match the compose mcp-qdrant bridge; Python 3.12 pinned for pydantic_core wheels). The server is never started at build (no hang). Verified in the built image: `uv tool list` shows mcp-server-qdrant v0.8.1, and `uv tool run --offline mcp-server-qdrant --help` resolves with NO network (exit 0) — the exact path runtime `uvx mcp-server-qdrant` (qdrant_local) takes, so it now starts from cache without a download. Only the Dockerfile changed.
<!-- SECTION:FINAL_SUMMARY:END -->
