---
id: TASK-17
title: Connect LobeChat to the Qdrant RAG data via MCP and document it
status: Done
assignee:
  - '@carles'
created_date: '2026-07-27 12:16'
updated_date: '2026-07-27 12:49'
labels:
  - docs
  - lobechat
  - mcp
dependencies:
  - TASK-15
  - TASK-16
references:
  - 'https://lobehub.com/docs/usage/plugins/mcp'
  - README.md
type: docs
ordinal: 19000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Wire LobeChat to the ingested RAG data through the MCP bridge and document the end-to-end flow in the README. In LobeChat, register the MCP bridge as a custom MCP plugin pointing at the in-network SSE endpoint (e.g. http://mcp-qdrant:8000/sse), then document: bring up the stack, open http://localhost:3210, configure an LLM provider, add the qdrant MCP plugin, and ask a question that retrieves from ingested files via the qdrant-find tool. Make clear that Qdrant is reached through MCP and that LobeChat native pgvector knowledge base is not used here.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 README documents running LobeChat with the stack and connecting it to the Qdrant RAG data via the MCP bridge: the custom MCP plugin registration steps, the Streamable HTTP endpoint URL, and LLM provider setup
- [x] #2 The docs include a concrete verification step: a LobeChat chat query returns results derived from ingested files through the `qdrant-find` MCP tool
- [x] #3 The docs state that Qdrant is reached via MCP and that LobeChat built-in knowledge base (pgvector) is intentionally not used
- [x] #4 Changes in this task are limited to documentation (README and/or .env.example); the compose service definitions come from TASK-15 and TASK-16
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added a "LobeChat (chat UI, via Docker Compose)" subsection to the README MCP section, updated the "Run the full stack" Setup blurb to list all four services, and added LobeChat to the MCP client list. Documented: start the stack + open http://localhost:3210; configure an LLM provider (tool-calling capable) via .env keys the lobe-chat service reads or the in-app AI Service Provider settings; add a custom MCP plugin Type=Streamable HTTP, URL=http://mcp-qdrant:8000/mcp (server-side in-network name, with the host-published http://localhost:8000/mcp noted as the external alternative); a concrete verify step invoking qdrant-find. States Qdrant is reached via MCP and pgvector KB is not used. Verified the documented facts against the running stack: compose starts qdrant/app/mcp-qdrant/lobe-chat; lobe-chat /health -> 200; lobe-chat container reaches http://mcp-qdrant:8000/mcp (HTTP 307, FastMCP redirect the client follows); LobeChat only supports stdio|Streamable HTTP for custom MCP (source: packages/types/src/plugins/mcp.ts); qdrant-find works over Streamable HTTP (real results). The final in-chat query is documented as a user-run step (executing it needs a live LLM provider key, which is not available here); every connectivity layer beneath it was verified. Only README.md changed in this task.
<!-- SECTION:NOTES:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @carles
created: 2026-07-27 12:34
---
Blocker/finding: LobeChat 1.143.3 custom-MCP connection type is `stdio | http` where http = Streamable HTTP (source: packages/types/src/plugins/mcp.ts, StreamableHTTPAuthSchema). No SSE option in the UI. The TASK-16 bridge serves SSE, which LobeChat cannot consume. To make LobeChat actually connect, the bridge must serve streamable-http (mcp-server-qdrant supports it; endpoint http://mcp-qdrant:8000/mcp). This requires changing TASK-16 (currently Done with SSE). Paused for user decision on transport.
---
<!-- COMMENTS:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Documented connecting LobeChat to the ingested Qdrant RAG data via the mcp-qdrant Streamable HTTP bridge: added a README subsection (start the compose stack, configure a tool-calling LLM provider via .env or the UI, add a custom MCP plugin of Type Streamable HTTP at http://mcp-qdrant:8000/mcp, and a qdrant-find verification query), updated the Setup section to reflect all four services, and clarified that Qdrant is reached via MCP (not LobeChat pgvector). Verified every documented layer against the live stack (services start, UI healthy, lobe-chat container reaches the bridge by name, qdrant-find returns real results over Streamable HTTP); the in-chat query is left as a documented user step since it requires an LLM API key. README-only change.
<!-- SECTION:FINAL_SUMMARY:END -->
