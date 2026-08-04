---
id: TASK-88
title: Refactor the first Mermaid diagram into a Docker Compose architecture view
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 14:39'
updated_date: '2026-08-04 14:53'
labels:
  - docs
dependencies:
  - TASK-87
ordinal: 90000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Rework the How it works top diagram to clearly present the Docker Compose architecture with explicit inputs and outputs: what goes in (raw files, user queries), the services, and what comes out (stored vectors, chat/search answers). Remove pi.dev from it.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The diagram shows the Docker Compose services (qdrant, app, mcp-qdrant, ollama, lobe-chat, opencode) and their relationships
- [x] #2 Inputs (./raw .txt/.md files, user queries via clients) and outputs (vectors stored in Qdrant, chat/search answers) are explicitly represented
- [x] #3 No pi.dev reference in the diagram; CLI clients shown accurately (e.g. Claude Code / opencode)
- [x] #4 Valid Mermaid that renders (mermaid-cli) without errors; changes limited to README.md
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
First mermaid -> Docker Compose architecture with explicit inputs/outputs; drop pi.dev. part of one coherent README.md refactor pass
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
First Mermaid reworked into a Docker Compose architecture: explicit inputs (./raw files, user queries) on the left, the six services in the middle, outputs (vectors to Qdrant, chat/search answers) on the right. pi.dev removed; CLI clients = Claude Code / opencode. Renders via mermaid-cli (115KB SVG).
<!-- SECTION:FINAL_SUMMARY:END -->
