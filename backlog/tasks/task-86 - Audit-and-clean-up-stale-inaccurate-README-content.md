---
id: TASK-86
title: Audit and clean up stale/inaccurate README content
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 14:38'
updated_date: '2026-08-04 14:53'
labels:
  - docs
dependencies: []
ordinal: 88000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Cross-check README.md against the actual code, compose files, and Makefile, and fix content describing non-existent features, removed services, or wrong details (ports, models, paths, env vars). Scope: everything NOT owned by the dedicated tasks below (intro, the two Mermaid diagrams, Requirements, the make-command refactor of Setup/Development, Project board, and the MCP align/dedupe/pi.dev removal).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Features/behaviour described in the README (outside the sections owned by TASK-87..93) match the current code/compose/Makefile; no references to removed features/services remain
- [x] #2 The Compose services table and Configuration table are accurate (services, images, host ports, env var names/defaults match compose + config.py)
- [x] #3 How it works / Setup prose is factually correct (URLs, model names, paths, transports mentioned there)
- [x] #4 Dead or duplicated content found outside the owned sections is removed or corrected; changes limited to README.md
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Cross-check README vs code/compose/Makefile; fix stale facts (opencode agent model is deepseek-v4-flash:cloud; verify services table, config table, lobe-chat 1.143.3, mcp-server-qdrant@0.8.1). part of one coherent README.md refactor pass
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Fixed stale facts: OLLAMA_PROXY_URL now http://localhost:11434 (matches compose/lobechat.yaml), mcp-qdrant image full tag + mcp-server-qdrant@0.8.1, metadata.source_file, removed the false claim that opencode uses qwen3.5:9b (its default_agent qdrant_only uses deepseek-v4-flash:cloud). Services + Configuration tables verified against compose/config.py. Only README.md changed.
<!-- SECTION:FINAL_SUMMARY:END -->
