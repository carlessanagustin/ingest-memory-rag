---
id: TASK-1
title: Watch raw folder and ingest txt/md files into Qdrant via Haystack
status: Done
assignee:
  - '@claude'
created_date: '2026-07-23 14:04'
updated_date: '2026-07-23 15:15'
labels: []
dependencies: []
references:
  - 'https://docs.haystack.deepset.ai/docs/intro'
  - 'https://docs.haystack.deepset.ai/reference/integrations-qdrant'
  - 'https://qdrant.tech/documentation/'
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A long-running Python app watches a configurable folder (default ./raw) for filesystem changes cross-platform (inotify on Linux, FSEvents on macOS, ReadDirectoryChangesW on Windows via watchdog). When a *.txt or *.md file is created or modified, the app converts, splits, embeds, and writes its chunks into a Qdrant vector database (default http://localhost:6333) using a Haystack indexing pipeline. Updated files replace their previous chunks so the store never accumulates stale content.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Watch folder and Qdrant URL are configurable via environment variables with defaults ./raw and http://localhost:6333
- [x] #2 Creating or modifying a *.txt or *.md file under the watched folder triggers ingestion; other extensions are ignored
- [x] #3 Rapid repeated filesystem events for the same file are debounced into a single ingestion
- [x] #4 Re-ingesting a changed file deletes its previous chunks in Qdrant before writing new ones (no duplicates/stale chunks)
- [x] #5 File watching works on Linux, macOS, and Windows without code changes
- [x] #6 A fast unit test suite covers pattern-matching, debounce, and file-selection logic without touching the network or a live Qdrant
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Project scaffolding: pyproject.toml (uv-managed; runtime deps haystack-ai, qdrant-haystack, watchdog, sentence-transformers, markdown converters; dev group ruff/mypy/pytest/pytest-cov), .python-version=3.12, ruff+mypy+pytest config, README.
2. src/ingest_memory_rag/config.py: env-driven Settings (WATCH_FOLDER default ./raw, QDRANT_URL default http://localhost:6333, INDEX, EMBEDDING_MODEL=all-MiniLM-L6-v2, EMBEDDING_DIM=384, patterns *.txt/*.md, debounce seconds).
3. pipeline.py: build QdrantDocumentStore + Haystack indexing pipeline (Text/Markdown converter -> DocumentSplitter -> SentenceTransformersDocumentEmbedder -> DocumentWriter). Choose converter by extension; stamp meta.file_path.
4. ingest.py: ingest_file() deletes prior chunks for that file_path (filter_documents+delete_documents) then runs the pipeline; module-level singletons so the embedding model loads once.
5. watcher.py: watchdog PatternMatchingEventHandler (*.txt,*.md) with a Debouncer; Observer on the folder; optional initial scan of existing files. Pure helpers (should_ingest, Debouncer) kept import-light for testing.
6. __main__.py / console script: load settings, build pipeline, start watcher, block until Ctrl+C.
7. tests/: unit-test should_ingest pattern logic, Debouncer coalescing, and extension->converter selection with the pipeline mocked — no network/Qdrant.
8. Verify: ruff check/format, mypy, pytest; python -c import smoke.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented as a src-layout package (src/ingest_memory_rag): config.py (env-driven Settings), pipeline.py (QdrantDocumentStore + split->embed->write Haystack pipeline), ingest.py (IngestionEngine: convert-by-extension, delete prior chunks by meta.file_path, then write; shared warmed embedder), watcher.py (watchdog PatternMatchingEventHandler + Debouncer + initial_scan + run loop). Packaging via uv/hatchling; deps split runtime vs dev group; uv.lock committed (112 pkgs). Verified: ruff lint+format clean, mypy clean (src), 12 unit tests pass at 100% coverage on config/watcher (fast, no network/DB). Haystack/Qdrant layer (pipeline.py, ingest.py, __main__.py) excluded from the unit-coverage gate as it requires a live Qdrant + model download; docker-compose.yml provided to run Qdrant for end-to-end use.

AC verification (env: macOS, dev tools + watchdog only; no live Qdrant, no ML stack installed):
- AC#1 VERIFIED: tests/test_config.py (defaults + env overrides) and import smoke printed watch=raw, qdrant=http://localhost:6333, dim=384.
- AC#2 VERIFIED: tests/test_watch_integration.py::test_only_matching_files_trigger_ingestion drives a real watchdog Observer — note.md and data.txt ingested, ignore.log ignored.
- AC#3 VERIFIED: test_debouncer_coalesces_rapid_triggers (5 rapid triggers -> 1 call) plus real-event path.
- AC#6 VERIFIED: 14 tests pass in ~1.7s at 100% coverage on config/watcher, no network/DB.
- AC#4 NOT YET VERIFIED: delete-then-write logic is implemented in ingest.py (_delete_existing by meta.file_path, convert->delete->write ordering) but requires a live Qdrant + embedding model to prove end-to-end. Needs `docker compose up -d` + `uv sync`.
- AC#5 PARTIALLY VERIFIED: proven on macOS (FSEvents) via the real-Observer test; code has zero OS-specific branches (watchdog abstracts inotify/FSEvents/ReadDirectoryChangesW). Full Linux/Windows proof needs CI on those OSes.
Checks: ruff lint+format clean, mypy clean (src), pytest 14 passed / 100% cov. uv.lock committed (112 pkgs).

E2E verification (live Qdrant via docker compose + full uv sync, macOS/Python 3.12):
- Discovered Haystack 3.0.0 is installed (major release post-training): SentenceTransformersDocumentEmbedder moved out of core to the sentence-transformers-haystack integration (import haystack_integrations.components.embedders.sentence_transformers). Added that dep and fixed pipeline.py import.
- Fixed AC#4 bug found during E2E: the Haystack converters overwrite meta["file_path"] with the source basename, which broke delete-by-path. Switched to a dedicated meta key "source_file" (resolved absolute path, stamped AFTER conversion) and key deletions on meta.source_file.
- Made split_by a validated Literal in config (clear error on bad SPLIT_BY) to satisfy the DocumentSplitter type; bumped mypy python_version to 3.12 so it can parse numpy stubs.
- AC#4 VERIFIED: tests/test_qdrant_integration.py::test_update_replaces_previous_chunks — after updating a file, count==new chunk count, new token present, old token absent. Also added test_dropped_file_flows_through_watcher_into_qdrant (real Observer -> debounce -> ingest -> Qdrant) and a markdown ingest test.
- Full suite: 19 passed (16 unit + 3 integration), ruff+mypy clean, 100% coverage on config/watcher. Integration tests skip cleanly when Qdrant/Haystack are absent.
- AC#5 still pending full proof: verified on macOS; Linux/Windows to be confirmed by CI (TASK-2).

AC#5 progress — cross-platform watching verified on 2 of 3 OSes with real-Observer tests:
- macOS (FSEvents): verified earlier (test_watch_integration + live-Qdrant integration).
- Linux (inotify): verified now by running the watcher suite inside a python:3.12-slim container (docker run ... pytest -m "not integration"): 16 passed, 1 skipped (platform linux). The real Observer tests exercise inotify.
- Windows (ReadDirectoryChangesW): NOT verifiable locally; requires a Windows runner. The intended mechanism is the CI matrix in TASK-2 (unit tests on windows-latest). Code has zero OS-specific branches; watchdog selects the backend per OS.
AC#5 left unchecked pending objective Windows evidence.

Per user decision (2026-07-23): accept the macOS + Linux real-Observer verification plus watchdog documented Windows backend (no OS-specific code paths) as sufficient evidence for AC#5. CI on windows-latest (TASK-2) will confirm Windows as belt-and-suspenders.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented a cross-platform folder-watching ingestion service (src/ingest_memory_rag): a watchdog observer with event debouncing and a startup scan feeds a Haystack split->embed->write pipeline into Qdrant; updated files have their prior chunks deleted (keyed on meta.source_file, the resolved absolute path) before the new chunks are written, so the store never accumulates stale content. Config is environment-driven (defaults ./raw and http://localhost:6333). Verified end-to-end against live Qdrant on Haystack 3.0 with all-MiniLM-L6-v2: 19 tests pass (16 unit + 3 live-Qdrant integration), ruff and mypy clean, 100% coverage on config/watcher. Cross-platform watching proven on macOS (FSEvents) and Linux (inotify, via a python:3.12-slim container run); Windows accepted via watchdog documented backend and to be confirmed by the CI matrix in TASK-2.
<!-- SECTION:FINAL_SUMMARY:END -->
