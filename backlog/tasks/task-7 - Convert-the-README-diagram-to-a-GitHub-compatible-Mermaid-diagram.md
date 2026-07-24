---
id: TASK-7
title: Convert the README diagram to a GitHub-compatible Mermaid diagram
status: To Do
assignee: []
created_date: '2026-07-23 15:54'
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
- [ ] #1 The ASCII diagram in README.md is replaced by a Mermaid diagram inside a fenced `mermaid` code block
- [ ] #2 The diagram uses valid Mermaid syntax of a GitHub-supported type (e.g. flowchart) and renders on github.com
- [ ] #3 The diagram conveys the same flow: watched file -> watchdog event -> debounce -> convert (text/markdown) -> delete prior chunks by source_file -> split -> embed -> write to Qdrant
- [ ] #4 No surrounding README content is lost and the section still reads correctly
<!-- AC:END -->
