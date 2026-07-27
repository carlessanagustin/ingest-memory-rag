---
id: TASK-14
title: >-
  Refactor the How it works Mermaid diagram in README into a systems-oriented
  view
status: Done
assignee:
  - '@carles'
created_date: '2026-07-27 09:17'
updated_date: '2026-07-27 10:34'
labels: []
dependencies: []
ordinal: 16000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The current Mermaid diagram under the `## How it works` section in README.md is code-level: its nodes name concrete Haystack/pipeline components. Add a higher-level, systems-oriented diagram that shows the moving parts and data flow (watched folder -> watcher/debounce -> ingestion service -> embedding -> Qdrant vector store, plus the MCP query path) without code-level class names, so a first-time reader understands the architecture at a glance. The existing detailed diagram is still valuable for implementers, so keep it — moved into a collapsible detailed subsection below the new one. Scope is README.md ONLY; do not touch source, other docs, or the code path.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The `## How it works` section opens with a new systems-oriented Mermaid diagram showing components/services and data flow (watched folder, watcher/debounce, ingestion service, embedding, Qdrant store, and the MCP read path), with no code-level class names
- [x] #2 The existing code-level diagram is preserved verbatim and kept below the new one inside a collapsible `<details>` block labelled as the detailed pipeline view
- [x] #3 Both diagrams use GitHub-compatible Mermaid syntax and render correctly on GitHub
- [x] #4 Surrounding prose still reads correctly (the `meta.source_file` delete-on-update note remains accurate and in place)
- [x] #5 Only README.md is modified; no changes to source code or other files
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. In README.md `## How it works`, add a new systems-oriented Mermaid flowchart at the top: watched ./raw folder -> file watcher/debounce -> ingestion service (chunk+embed) -> embedding model -> Qdrant; plus the MCP read path (MCP clients -> mcp-server-qdrant -> Qdrant -> results). No code-level class names.
2. Move the existing code-level diagram verbatim into a collapsible <details> block titled as the detailed pipeline view, placed below the new diagram.
3. Keep the `meta.source_file` delete-on-update note in place.
4. Verify GitHub-compatible Mermaid syntax (flowchart, subgraphs, cylinder/subroutine node shapes, <br/> labels) and that mermaid renders inside <details>.
5. Confirm only README.md changed (git status).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implementation blocked: file-write tools (Edit/Write and file-writing Bash) are denied in the current permission mode. Diagram content is ready to apply; awaiting write permission or user-run edit.

Applied the README change via Edit (write access granted on re-run). Verified: `git diff --stat` shows only README.md changed. Rendered both diagrams with mermaid-cli (mmdc) against README.md -> 2 charts, both render OK (installed chrome-headless-shell for puppeteer). Rendered the new systems diagram to PNG and visually confirmed it shows the watched folder, watcher/debounce, ingestion service, embedding model, Qdrant, and the MCP read path with no code-level class names. Confirmed the detailed code-level diagram is preserved verbatim inside a collapsible <details> block, and the meta.source_file delete-on-update note remains in place.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Refactored the README `## How it works` section: added a new systems-oriented Mermaid diagram (components + write/read data flow, MCP query path, no code-level class names) and moved the original code-level diagram verbatim into a collapsible <details> "Detailed pipeline (code-level view)" block below it. README.md only. Verified by rendering both diagrams with mermaid-cli (both parse/render) and visually inspecting the systems diagram PNG; git diff confirms no other files changed.
<!-- SECTION:FINAL_SUMMARY:END -->
