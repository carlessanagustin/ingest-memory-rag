---
id: TASK-77
title: Reload the ignore file live when it changes (watcher wiring)
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 08:28'
updated_date: '2026-08-04 08:44'
labels:
  - feature
dependencies:
  - TASK-76
ordinal: 79000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Make the running watcher detect changes to the ignore file and reload the shared matcher without a restart, so edits to the mounted .watchignore take effect live. The ingest handler only matches *.txt/*.md, so ignore-file events need their own handler. Must work with both the native and polling observers (polling is the docker default).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A dedicated handler detects create/modify/move of settings.ignore_file and triggers a reload of the shared matcher used by the live event handler (and subsequent scans)
- [x] #2 The reload-trigger decision lives in a unit-testable helper (not only inside the coverage-excluded run()); a unit test simulates an ignore-file change and asserts the matcher reloads
- [x] #3 run() schedules the observer to watch the ignore file location (its parent directory / within the watch tree) and reloads on change
- [x] #4 Rapid successive writes are debounced/coalesced so the matcher is not rebuilt repeatedly
- [x] #5 Behaviour holds whether WATCH_USE_POLLING is true or false
- [x] #6 A concise log line confirms when a reload occurs; ruff, mypy and pytest pass with coverage >=80%
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. watcher.py: add IgnoreFileEventHandler(ignore_file, on_change) filtering events by resolved path == ignore_file (created/modified + moved dest); this is the unit-testable dispatch helper.
2. run(): build one shared matcher; create a reload Debouncer whose action calls matcher.reload() + logs; schedule the ignore handler on settings.ignore_file.parent (reuse the main watch via add_handler_for_watch when parent == watch_folder, else a separate non-recursive schedule).
3. tests/test_watcher.py: handler calls on_change for the ignore-file path (create/modify/move), and NOT for other paths.
4. Works for polling + native observers; concise reload log line. ruff/mypy/pytest >=80%.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added IgnoreFileEventHandler(ignore_file, on_change) that fires only for the ignore file path on create/modify/moved-dest (the unit-testable dispatch helper). run() builds one shared matcher, a debounced reload (_reload_ignore logs each reload), and attaches the ignore handler to the main watch when the file is in the watch folder (else a separate non-recursive watch); reload_debouncer is cancelled in finally. Observer selection (polling vs native) is unchanged so it works either way. Verified: 2 handler-dispatch unit tests (fires for the ignore file across create/modify/move; ignores other paths) pass; ruff+mypy clean, 46 passed, watcher.py 100% coverage.
<!-- SECTION:FINAL_SUMMARY:END -->
