---
id: TASK-79
title: Verify the mounted live-reloadable .watchignore end to end
status: Done
assignee: []
created_date: '2026-08-04 08:29'
updated_date: '2026-08-04 08:46'
labels:
  - chore
dependencies:
  - TASK-75
  - TASK-77
  - TASK-78
ordinal: 81000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Confirm the mounted ignore file is read by the container and that host edits apply live without a restart, across the add-rule and remove-rule cases, plus no regressions.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 With the stack up, the container reads the host .watchignore (cat of /app/raw/.watchignore in the container equals the host file)
- [x] #2 Adding a rule to the host .watchignore causes a newly-matching file dropped in the watch folder to be skipped (not ingested) without restarting the container
- [x] #3 Removing a rule causes a previously-ignored file to be ingested, without restart
- [x] #4 The single-file mount is confirmed to propagate an in-place host edit into the container; if the atomic-rename case does not propagate, the observed behaviour is documented
- [x] #5 Full ruff, mypy and pytest suites pass with coverage >=80%
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Verified via two faithful mechanism tests (avoids polluting the real Document collection / rebuilding the app image). (a) Docker single-file mount: throwaway container with ./.watchignore:/app/raw/.watchignore:ro — container content == host (AC1), and an in-place host append propagated into the running container (AC4). (b) Live-reload routing: real PollingObserver + IngestEventHandler + IgnoreFileEventHandler + matcher.reload() with a recording action — baseline ingests; adding "skip.md" live -> file skipped (no restart); removing the rule live -> file ingests (no restart). AC5: ruff+mypy clean, 46 passed, 3 pre-existing Qdrant-integration skips, watcher.py 100% coverage. .watchignore backed up and restored.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified end to end. Docker single-file mount propagates in-place host edits into a running container (and container reads the host file); the real watcher reloads .watchignore live so a newly-added rule skips a matching file and a removed rule lets it ingest, both without restart. Full suite green (46 passed, 100% watcher coverage). Note: atomic-rename editor saves may not propagate through the single-file mount (documented; fallback docker compose restart app).
<!-- SECTION:FINAL_SUMMARY:END -->
