---
id: TASK-72
title: Delete the source file after successful ingestion when WATCH_REMOVE is on
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 07:31'
updated_date: '2026-08-04 07:40'
labels:
  - feature
dependencies:
  - TASK-71
ordinal: 74000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
When WATCH_REMOVE is enabled, delete a source file once it is correctly ingested; otherwise keep it and log why. "Correctly ingested" means at least one chunk was written to Qdrant. A 0-chunk result (empty/no-content file) or any ingestion exception must keep the file and log it in the app log. The behavior applies to both the startup scan and live watch events, since both run through the same per-file action.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 When WATCH_REMOVE is on and ingest_file returns >=1 chunk, the source file is deleted and an info line is logged
- [x] #2 When WATCH_REMOVE is on and ingest_file returns 0 chunks, the file is kept and a log message explains nothing was stored
- [x] #3 When ingestion raises, the file is kept and the failure is logged in the app log (existing logger.exception path preserved)
- [x] #4 When WATCH_REMOVE is off (default), no file is ever deleted
- [x] #5 A failed delete (e.g. permission/OS error) is caught and logged without crashing the watcher
- [x] #6 Removal applies to both the SCAN_ON_START scan and live create/modify/move events (shared action path)
- [x] #7 The delete/keep decision lives in a unit-testable helper (not only inside the coverage-excluded action closure); tests cover delete-on-success, keep-on-0-chunks, keep-when-off, and delete-error handling
- [x] #8 ruff, mypy and pytest pass with coverage staying >=80%
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add a module-level, unit-testable helper in watcher.py, e.g. `maybe_remove_ingested(path: Path, written: int, *, enabled: bool) -> None`:
   - enabled and written>=1: path.unlink(); log info "deleted ... after ingesting N chunk(s)"; catch OSError -> log exception, do not raise.
   - enabled and written==0: keep file; log warning "kept ... (0 chunks written, nothing stored)".
   - not enabled: no-op.
2. Wire into `_build_default_action`.action: on success call the helper with enabled=settings.watch_remove; on exception keep existing logger.exception and return (no removal). Shared action => applies to both scan and live paths.
3. tests/test_watcher.py: delete-on-success (>=1, enabled) removes file + info; keep-on-0-chunks (enabled) keeps + warning; enabled=False never deletes; unlink OSError (e.g. missing file) is caught + logged, no raise.
4. Run ruff, mypy, pytest; coverage >=80%.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added module-level maybe_remove_ingested(path, written, *, enabled) in watcher.py (outside the coverage-excluded closure) and wired it into the shared action after a successful ingest: deletes on written>=1 (info log), keeps+warns on written==0, no-op when disabled, and catches OSError on unlink (logged, no crash). Ingest-exception branch unchanged (kept + logger.exception). Same action serves both scan and live paths. Verified: 4 new watcher unit tests cover all four branches; full suite 43 passed, watcher.py 100% coverage; ruff + mypy clean.
<!-- SECTION:FINAL_SUMMARY:END -->
