---
id: TASK-26
title: Update the How it works diagram to include LobeChat and Ollama
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 09:10'
updated_date: '2026-07-29 09:16'
labels:
  - docs
dependencies: []
references:
  - docker-compose.yml
type: docs
ordinal: 28000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The "How it works" systems Mermaid diagram predates the LobeChat + Ollama compose services: it shows the ingest write-path and an MCP read-path for CLI clients (Claude Code/opencode/pi.dev) but omits the LobeChat UI and the Ollama model provider now in docker-compose.yml. Update the systems diagram so it reflects the running stack — add LobeChat as an MCP client of the mcp-qdrant bridge and Ollama as LobeChat local model provider — while keeping it systems-level (no code class names). Leave the collapsible detailed code-level diagram unchanged.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The systems diagram shows the LobeChat UI querying ingested data via the mcp-qdrant bridge (MCP), and the Ollama server as LobeChat local model provider
- [x] #2 The existing ingest write-path and the CLI MCP clients (Claude Code/opencode/pi.dev) remain represented
- [x] #3 The diagram stays systems-level (services + data flow, no code class names) and uses GitHub-compatible Mermaid that renders
- [x] #4 The collapsible "Detailed pipeline (code-level view)" diagram is left unchanged
- [x] #5 Only README.md is changed
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Replace the "How it works" systems Mermaid block: keep the ingest write-path (raw -> app -> embedding model + upsert to qdrant) and CLI MCP clients, and add a "Docker Compose stack" subgraph containing app/qdrant/mcp-qdrant/lobe-chat/ollama; show lobe-chat querying via mcp-qdrant (MCP) and chatting with ollama (local model).
2. Lightly update the intro sentence to mention the LobeChat chat path.
3. Leave the collapsible detailed diagram unchanged.
4. Verify with mermaid-cli (both diagrams render) and visually inspect the rendered systems PNG. README-only.
Handled inline (diagram design + visual render-verify is best done in the main loop, not a docker-ops subagent); backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Handled inline (diagram design + visual render-verify). Replaced the "How it works" systems Mermaid diagram: added a "Docker Compose stack" subgraph containing app/qdrant/mcp-qdrant/lobe-chat/ollama; kept the write-path (raw -> app -> embedding model + upsert to qdrant) and the CLI MCP clients; added lobe-chat -> mcp-qdrant (MCP query) and lobe-chat <-> ollama (chat). Lightly updated the intro sentence to mention the LobeChat chat path. Verified: mermaid-cli rendered BOTH charts from README (2 charts, both OK); rendered the systems diagram to PNG and visually confirmed the new nodes/edges (LobeChat via mcp-qdrant, Ollama as local model, write path intact, no code class names). git status shows only README.md changed; the collapsible detailed code-level diagram (flowchart TD) is unchanged.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Updated the "How it works" systems diagram to reflect the current compose stack: added a Docker Compose stack subgraph (app, qdrant, mcp-qdrant, lobe-chat, ollama) showing LobeChat querying ingested data via the mcp-qdrant MCP bridge and using the local Ollama model for chat, while keeping the ingest write-path and CLI MCP clients. Systems-level, GitHub-compatible Mermaid (verified rendering with mermaid-cli + visual PNG inspection); collapsible detailed diagram left unchanged; README-only.
<!-- SECTION:FINAL_SUMMARY:END -->
