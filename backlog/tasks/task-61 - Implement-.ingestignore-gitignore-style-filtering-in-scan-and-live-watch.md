---
id: TASK-61
title: Implement .ingestignore (gitignore-style) filtering in scan and live watch
status: Done
assignee:
  - '@claude'
created_date: '2026-08-03 09:17'
updated_date: '2026-08-03 09:29'
labels:
  - app
  - python
  - ingestion
dependencies:
  - TASK-60
type: feature
ordinal: 63000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Load the WATCH_IGNORE file (a single .ingestignore at the WATCH_FOLDER root) into a pathspec spec using gitignore semantics (wildcards, ** across subfolders, ! negation, / anchoring, trailing / for directories, # comments). Provide a helper that decides whether a candidate path (normalized to a POSIX path relative to WATCH_FOLDER) is ignored. Apply the filter in BOTH the startup scan (iter_matching_files/initial_scan) and the live event handler (IngestEventHandler) so ignored files are skipped consistently. Handle: ignore file absent (nothing ignored), paths outside WATCH_FOLDER (not ignored), and the relative-vs-absolute path discrepancy between scan paths and resolved paths.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 With a .ingestignore present, files matching its patterns are skipped by both the startup scan and the live watcher; non-matching .txt/.md files are still ingested
- [x] #2 gitignore capabilities work via pathspec: globs, ** across subfolders, ! negation, / anchoring, trailing-slash directory patterns and # comments
- [x] #3 Patterns are matched against the path relative to WATCH_FOLDER (POSIX-normalized); an absent ignore file means nothing is ignored
- [x] #4 Unit tests cover the matcher and its integration into scan + handler; suite green and coverage at or above 80 percent for config.py and watcher.py
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. IgnoreMatcher(watch_folder, spec) with is_ignored(path) = POSIX path relative to watch_folder -> spec.match_file; paths outside root not ignored. 2. build from settings.ignore_file (empty spec if absent) via pathspec GitIgnoreSpec. 3. Wire into iter_matching_files (scan) and IngestEventHandler (live) through run(). 4. Unit tests for matcher + scan/handler integration; coverage >=80%.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
watcher.py: IgnoreMatcher(watch_folder, spec).is_ignored(path) resolves path, computes relative_to(watch_folder) (ValueError -> outside -> not ignored), matches spec.match_file(rel.as_posix()); empty spec -> False. _build_spec prefers pathspec.GitIgnoreSpec (full gitignore semantics) with a gitwildmatch fallback. build_ignore_matcher reads settings.ignore_file if present else empty spec. Wired into iter_matching_files/initial_scan (scan) and IngestEventHandler._schedule (live, early-return + debug log), built once in run(). Unit tests cover: specific file, drafts/ subfolder, **/scratch.txt glob, !negation re-include, # comment, absent file (nothing ignored), empty spec, path outside root, plus iter_matching_files skipping and handler not scheduling an ignored path. Verified: ruff/format/mypy clean; pytest 30 passed/3 skipped; coverage 100% on config.py + watcher.py.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented .ingestignore filtering (pathspec gitignore semantics) applied in both the startup scan and the live handler, matched relative to WATCH_FOLDER, absent-file-safe. Verified via ruff/mypy and unit+integration tests at 100% coverage.
<!-- SECTION:FINAL_SUMMARY:END -->
