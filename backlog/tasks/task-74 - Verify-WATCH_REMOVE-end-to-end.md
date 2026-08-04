---
id: TASK-74
title: Verify WATCH_REMOVE end to end
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 07:32'
updated_date: '2026-08-04 07:45'
labels:
  - chore
dependencies:
  - TASK-72
  - TASK-73
ordinal: 76000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Confirm the feature behaves correctly across the success, empty, and failure cases, on both the startup scan and live watch paths, without regressions.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 With WATCH_REMOVE=true, a valid file is ingested (>=1 chunk) and then removed from the watch folder
- [x] #2 With WATCH_REMOVE=true, an empty/no-content file is ingested to 0 chunks, kept on disk, and the keep is logged
- [x] #3 With WATCH_REMOVE=true, a file whose ingestion fails is kept on disk and the failure is logged in the app log
- [x] #4 With WATCH_REMOVE=false (default), no files are deleted
- [x] #5 Both the startup scan and live watch events exhibit the delete-on-success behavior
- [x] #6 Full ruff, mypy, and pytest suites pass with coverage >=80%
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Run a real end-to-end against the live Qdrant (localhost:6333) on the host (editable install has the new code; the running app container predates it).
2. Dedicated throwaway index watch_remove_e2e (recreate=true); clean up at the end.
3. WATCH_REMOVE=true: scan path (initial_scan) with a real content file (>=1 chunk) and an empty file (0 chunks) -> assert good deleted, empty kept; live path via a real Observer + dropped file -> assert deleted; forced ingest failure (monkeypatch ingest_file to raise for boom.md) through the REAL action -> assert kept + "Failed to ingest" logged.
4. WATCH_REMOVE=false: a real content file through the action -> assert kept.
5. Confirm full ruff/mypy/pytest suite green with coverage >=80% (already 43 passed, 100%).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
End-to-end run against live Qdrant (localhost:6333), throwaway index watch_remove_e2e, real IngestionEngine + real watcher action + real Observer. Results 5/5: scan good.md(2 chunks)->deleted, empty.md(0)->kept+warning; live live.md(2 chunks)->deleted via Observer; forced ingest exception boom.md->kept + "Failed to ingest" logged; WATCH_REMOVE=false good_off.md->kept. Unit suite: ruff+mypy clean, 43 passed, 100% coverage.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified WATCH_REMOVE end to end. Unit: 43 passed, 100% coverage, ruff+mypy clean. Live-Qdrant e2e (5/5): delete-on-success on both the scan and live-Observer paths (2 chunks each), keep+log on 0-chunk empty file, keep+log on forced ingestion exception, and no deletion when disabled.
<!-- SECTION:FINAL_SUMMARY:END -->
