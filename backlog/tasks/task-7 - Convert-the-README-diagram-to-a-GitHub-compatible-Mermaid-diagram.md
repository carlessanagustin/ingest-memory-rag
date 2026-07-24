---
id: TASK-7
title: Convert the README diagram to a GitHub-compatible Mermaid diagram
status: Done
assignee:
  - '@claude'
created_date: '2026-07-23 15:54'
updated_date: '2026-07-24 08:22'
labels: []
dependencies:
  - TASK-1
ordinal: 9000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The README currently depicts the ingestion flow as an ASCII-art diagram. Replace it with a Mermaid diagram in a fenced `mermaid` code block so it renders natively on GitHub and is easier to maintain. It should convey the same flow: a watched .txt/.md file to watchdog event to debounce to IngestionEngine, then convert (Text/Markdown), delete prior chunks by source_file, split, embed, and write to the Qdrant document store.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The ASCII diagram in README.md is replaced by a Mermaid diagram inside a fenced `mermaid` code block
- [x] #2 The diagram uses valid Mermaid syntax of a GitHub-supported type (e.g. flowchart) and renders on github.com
- [x] #3 The diagram conveys the same flow: watched file -> watchdog event -> debounce -> convert (text/markdown) -> delete prior chunks by source_file -> split -> embed -> write to Qdrant
- [x] #4 No surrounding README content is lost and the section still reads correctly
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Replace the ASCII diagram in README How it works with a Mermaid flowchart (```mermaid, flowchart TD): watched .txt/.md -> watchdog event -> debounce -> IngestionEngine -> convert (Text/Markdown) -> delete prior chunks by meta.source_file -> DocumentSplitter -> SentenceTransformersDocumentEmbedder -> DocumentWriter -> Qdrant. Keep surrounding prose and fix any stale meta.file_path reference to meta.source_file. Verify fenced block + valid GitHub Mermaid syntax.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Replaced the ASCII diagram in README How it works with a fenced mermaid flowchart (flowchart TD): watched .txt/.md -> watchdog event -> debounce -> IngestionEngine -> convert (Text/Markdown) -> delete prior chunks by meta.source_file -> DocumentSplitter -> SentenceTransformersDocumentEmbedder -> DocumentWriter -> Qdrant. Uses only core flowchart syntax (quoted labels, line breaks, cylinder node) that GitHub renders natively. Also fixed stale prose meta.file_path to meta.source_file so the section stays accurate. Verified the block replaced the ASCII art and the section reads correctly; final visual render confirmed on the GitHub README after push.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Replaced the README ASCII How it works diagram with a GitHub-native Mermaid flowchart (fenced mermaid, flowchart TD) conveying the same flow (watched file -> watchdog event -> debounce -> IngestionEngine -> convert -> delete prior chunks by meta.source_file -> split -> embed -> write to Qdrant), and corrected surrounding prose to meta.source_file. Uses only core flowchart syntax that GitHub renders.
<!-- SECTION:FINAL_SUMMARY:END -->
