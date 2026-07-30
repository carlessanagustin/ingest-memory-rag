---
id: TASK-52
title: >-
  Document the LobeChat to Qdrant qdrant-find quickstart and the local-model
  caveat
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 13:00'
updated_date: '2026-07-30 13:08'
labels:
  - docs
  - lobechat
  - mcp
dependencies:
  - TASK-51
type: docs
ordinal: 54000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The README LobeChat section documents adding the Qdrant MCP plugin. Add a short quickstart that ties it to querying the Document collection via prompts, and note the local-model caveat: the local Ollama qwen3.5:9b emits tool calls but is only moderately reliable at using MCP tool results, so prompts should explicitly say to use qdrant-find and may need a retry; a cloud provider key gives more reliable tool-calling.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The README LobeChat section shows the plugin URL http://mcp-qdrant:8000/mcp (Streamable HTTP, server-side via the mcp-qdrant service name) and an example qdrant-find prompt against the Document collection
- [x] #2 It notes the qwen3.5:9b tool-calling caveat and that a cloud provider key is a more reliable alternative
- [x] #3 It clarifies Qdrant is queried via the MCP plugin, not LobeChat native KB
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. In the README LobeChat section, add a short note on the qwen3.5:9b tool-calling caveat (emits the call but is only moderately reliable at using results; say "use qdrant-find" explicitly and retry) and that a cloud provider key is more reliable. 2. Confirm the plugin URL + example prompt + native-KB-not-used note are present.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
README LobeChat section: added a provider-step note that local Ollama qwen3.5:9b is enabled by default but only moderately reliable at tool-calling (may emit the qdrant-find call without acting on the result) — prompt explicitly with "use qdrant-find" and retry; cloud models (OpenAI/Anthropic) are more reliable. Confirmed the section already shows the plugin URL http://mcp-qdrant:8000/mcp (Streamable HTTP, server-side via the mcp-qdrant service name), an example qdrant-find prompt against the ingested files, and the note that LobeChat native KB (pgvector) is intentionally not used.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Documented the local qwen3.5:9b tool-calling caveat (with the cloud-key alternative) in the README LobeChat section; the plugin URL, example qdrant-find prompt, and native-KB-not-used note were already present.
<!-- SECTION:FINAL_SUMMARY:END -->
