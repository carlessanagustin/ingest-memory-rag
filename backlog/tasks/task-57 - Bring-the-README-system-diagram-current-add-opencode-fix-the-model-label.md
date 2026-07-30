---
id: TASK-57
title: 'Bring the README system diagram current (add opencode, fix the model label)'
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 14:02'
updated_date: '2026-07-30 14:12'
labels:
  - docs
  - diagram
dependencies:
  - TASK-54
type: docs
ordinal: 59000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update the systems-level mermaid diagram in the How it works section so it reflects the stack after the OpenWebUI removal: add the opencode service (queries mcp-qdrant for RAG and uses ollama for its model) and correct the model label from qwen3.6:27b to qwen3.5:9b. Also fix the same qwen3.6:27b drift elsewhere in the README (setup text and the ollama-pull services-table row). Confirm the diagram contains no openwebui/mcpo.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The system diagram includes the opencode service with edges to mcp-qdrant and ollama
- [x] #2 The diagram labels the Ollama model as qwen3.5:9b (not qwen3.6:27b) and contains no openwebui/mcpo nodes
- [x] #3 No qwen3.6:27b string remains anywhere in README.md
- [x] #4 The mermaid diagram is syntactically valid (renders)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. System diagram: add opencode service node (edges to mcp-qdrant for RAG and ollama for model); fix qwen3.6:27b -> qwen3.5:9b. 2. Fix qwen3.6:27b elsewhere in README (setup text + ollama-pull table row). 3. Confirm no openwebui/mcpo in the diagram; valid mermaid.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
System diagram: added opencode service node with edges opencode -->|MCP query| mcp and opencode <-->|chat| ollama; model label changed to qwen3.5:9b; removed opencode from the external CLI-clients label to avoid duplication; no openwebui/mcpo nodes. Fixed all 4 qwen3.6:27b occurrences -> qwen3.5:9b (setup text, ollama-pull table row, Ollama section x2) and revised the CPU caveat (no longer describes a 27B/tens-of-GB model). Verified: grep qwen3.6:27b == 0; mmdc rendered the diagram to a 24KB SVG (parses/renders).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Brought the system diagram current: added the opencode service (edges to mcp-qdrant and ollama), fixed the model label to qwen3.5:9b, removed all qwen3.6:27b drift across the README, and revised the CPU caveat. Verified the diagram renders via mermaid-cli.
<!-- SECTION:FINAL_SUMMARY:END -->
