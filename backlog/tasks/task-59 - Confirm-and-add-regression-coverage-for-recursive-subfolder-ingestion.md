---
id: TASK-59
title: Confirm and add regression coverage for recursive subfolder ingestion
status: Done
assignee:
  - '@claude'
created_date: '2026-08-03 09:16'
updated_date: '2026-08-03 09:29'
labels:
  - app
  - python
  - ingestion
  - tests
dependencies: []
type: feature
ordinal: 61000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The app is already recursive: the live watcher schedules with recursive=True and the startup scan uses folder.rglob, and the ingestion engine keys on resolved absolute paths, so nested .txt/.md files ingest correctly. Add explicit regression coverage proving a file in a subfolder is picked up end-to-end (startup scan and the live PatternMatchingEventHandler path), so the recursive requirement is locked in. No production code change is expected unless a gap is found.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A test asserts a .txt or .md file in a nested subfolder of WATCH_FOLDER is discovered by the startup scan and triggers the ingest action
- [x] #2 A test asserts the live watch path (recursive observer / handler) triggers on a nested subfolder file
- [x] #3 If any gap in recursion is found it is fixed; otherwise the tests lock in the existing recursive behavior
- [x] #4 The fast unit suite stays green and coverage stays at or above 80 percent
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add tests: startup scan (iter_matching_files/initial_scan) discovers a nested subfolder .txt/.md and runs the action; live handler/observer triggers on a nested file. 2. Confirm existing recursive=True + rglob; fix only if a gap surfaces.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Confirmed recursion is already implemented (observer.schedule recursive=True; iter_matching_files uses folder.rglob). Added regression tests: initial_scan discovers a deeply nested a/b/c/deep.md (test_watcher.py); a live recursive Observer ingests a file created in a new nested subfolder (test_watch_integration.py test_nested_subfolder_file_is_ingested). No production change needed for recursion. Independently verified: pytest 30 passed / 3 skipped, coverage 100% (config.py + watcher.py).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Locked in recursive subfolder ingestion with scan-level and live-observer regression tests (recursion was already implemented via recursive=True + rglob). Suite green at 100% coverage.
<!-- SECTION:FINAL_SUMMARY:END -->
