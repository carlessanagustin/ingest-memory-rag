---
id: TASK-89
title: Update the detailed pipeline Mermaid diagram if needed
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 14:39'
updated_date: '2026-08-04 14:53'
labels:
  - docs
dependencies:
  - TASK-88
ordinal: 91000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Review the code-level pipeline diagram (watchdog -> debounce -> IngestionEngine -> convert -> delete prior chunks -> split -> embed -> upsert -> Qdrant) against ingest.py/watcher.py and update only if inaccurate or incomplete (e.g. WATCH_REMOVE delete-on-success, ignore filtering).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The detailed diagram accurately reflects the current ingestion pipeline in the code
- [x] #2 If already accurate it is left unchanged (noted as verified); if not, it is corrected
- [x] #3 Valid Mermaid that renders without errors; changes limited to README.md
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Verify/adjust detailed pipeline mermaid vs ingest.py/watcher.py. part of one coherent README.md refactor pass
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Detailed pipeline diagram was INACCURATE (showed convert->delete->split; code splits before deleting). Corrected to convert->split->delete-prior-chunks->(chunks>0?)->embed->upsert, and added the .watchignore skip branch and the WATCH_REMOVE delete-on-success branch. Matches ingest.py/watcher.py; renders via mermaid-cli.
<!-- SECTION:FINAL_SUMMARY:END -->
