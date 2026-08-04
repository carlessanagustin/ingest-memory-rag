---
id: TASK-76
title: Make the ignore matcher reloadable at runtime
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 08:28'
updated_date: '2026-08-04 08:44'
labels:
  - feature
dependencies: []
ordinal: 78000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Refactor the ignore-matching layer so the compiled gitignore-style spec can be rebuilt from settings.ignore_file while the app is running. This is the pure-logic foundation for live reload (no observer involved here). The matcher is read from the observer thread, so reloads must swap the spec safely.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The ignore matcher exposes a way to reload its rules from settings.ignore_file at runtime (e.g. IgnoreMatcher.reload() or an equivalent reloadable wrapper)
- [x] #2 After the ignore file changes on disk and a reload runs, is_ignored reflects the new rules: an added rule causes a matching path to become ignored; a removed rule causes it to stop being ignored
- [x] #3 An absent or empty ignore file reloads to an empty spec (nothing ignored), matching current behaviour
- [x] #4 The spec swap is thread-safe so a reload cannot corrupt a concurrent is_ignored call
- [x] #5 Unit tests cover reload adding a rule, removing a rule, and the absent-file case; ruff, mypy and pytest pass with coverage >=80%
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. watcher.py IgnoreMatcher: store the ignore_file path + a threading.Lock; add reload() that re-reads settings.ignore_file (empty list if absent) via _build_spec and swaps self._spec under the lock; is_ignored reads the spec under the lock.
2. build_ignore_matcher passes ignore_file=settings.ignore_file so reload() works.
3. tests/test_watcher.py: reload adds a rule (path becomes ignored), removes a rule (stops being ignored), absent file stays empty.
4. ruff/mypy/pytest >=80%.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
IgnoreMatcher now stores its ignore_file + a threading.Lock and gains reload(): it re-reads the file (empty list if absent), builds a fresh spec, and swaps it under the lock; is_ignored reads the spec under the lock. build_ignore_matcher passes ignore_file so reload works. Verified: 4 reload unit tests (add rule -> ignored, remove rule -> not ignored, absent-file empty, unconfigured no-op) pass; full suite ruff+mypy clean, 46 passed, watcher.py 100% coverage.
<!-- SECTION:FINAL_SUMMARY:END -->
