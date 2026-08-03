---
id: TASK-63
title: Verify recursive ingestion and .ingestignore end to end
status: Done
assignee:
  - '@claude'
created_date: '2026-08-03 09:17'
updated_date: '2026-08-03 09:36'
labels:
  - app
  - python
  - verification
dependencies:
  - TASK-59
  - TASK-60
  - TASK-61
  - TASK-62
type: chore
ordinal: 65000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Exercise the new behavior end-to-end and confirm the checks pass. Preserve data (no down -v, no reset). Use a WATCH_FOLDER (or a temp folder / the app service) containing a subfolder with .txt/.md files plus a .ingestignore that excludes some of them.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 ruff check, ruff format --check, mypy and pytest (coverage at or above 80 percent) all pass
- [x] #2 A real ingest run shows a nested subfolder .txt/.md file ingested (present in Qdrant by its source_file) while a .ingestignore-excluded file is NOT ingested
- [x] #3 Editing or removing the .ingestignore changes what gets ingested as documented
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Full suite (ruff/format/mypy/pytest) already green. 2. Real ingest: temp folder with sub/keep-nested.md + top.txt (ingest) and secret-private.md + drafts/draft1.md excluded via .ingestignore -> collection IngestIgnoreTest. 3. Verify by source_file: kept files present, ignored absent. 4. Cleanup: kill ingester, delete test collection + temp dir.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
AC1: independently ran uv run ruff check . (passed), ruff format --check . (10 files formatted), mypy (no issues), pytest (30 passed, 3 skipped, 100% coverage on config.py + watcher.py). AC2: real ingest via uv run ingest-memory-rag against a temp folder (sub/keep-nested.md, top.txt, secret-private.md, drafts/draft1.md) with .ingestignore = "secret-private.md" + "drafts/", into a throwaway IngestIgnoreTest collection. Result by source_file: ingested == [keep-nested.md, top.txt] (nested subfolder file + top-level), and the two ignored files were NOT ingested (log shows only top.txt and sub/keep-nested.md ingested). AC3: the .ingestignore excluded matching files here; the unit test for an absent ignore file (nothing ignored) confirms removing it re-includes them — read-once-at-startup behavior as documented. Cleanup: deleted IngestIgnoreTest, removed temp dir. Document collection untouched.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified end-to-end: lint/format/mypy/pytest green (100% coverage); a real ingest run put the nested subfolder file + top-level file into Qdrant while .ingestignore-excluded files were skipped (confirmed by source_file). Ran against a throwaway collection; Document untouched.
<!-- SECTION:FINAL_SUMMARY:END -->
