---
id: TASK-9
title: >-
  Make ingestion fastembed-compatible and serve it via the official Qdrant MCP
  server over local Qdrant
status: Done
assignee:
  - '@claude'
created_date: '2026-07-24 11:08'
updated_date: '2026-07-24 12:15'
labels: []
dependencies:
  - TASK-1
references:
  - 'https://github.com/qdrant/mcp-server-qdrant'
ordinal: 11000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
To let the official mcp-server-qdrant serve semantic search over the ingested data via the local Qdrant at http://localhost:6333, the collection must be written in the format that server expects. We confirmed a mismatch: Haystack writes an UNNAMED 384-dim vector with payload keys content and meta, whereas the official server (fastembed) queries a NAMED vector fast-all-minilm-l6-v2 with payload keys document and metadata (a 400 Not existing vector name error). This task changes the app embed and write path to produce a fastembed-compatible collection (named vector plus document/metadata payload, embeddings from fastembed all-MiniLM-L6-v2 so store and query align), then runs and documents the official mcp-server-qdrant over HTTP/SSE against the local Qdrant, verified end to end. The watcher, converters, splitter, and delete-then-write behavior are preserved; only the embed and write step changes.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The ingestion writes the collection in the official mcp-server-qdrant format: a named vector fast-all-minilm-l6-v2 (384-dim, cosine), chunk text under the document payload key, and metadata under metadata
- [x] #2 Document embeddings are produced with fastembed all-MiniLM-L6-v2 so they align with the query embeddings the official server computes
- [x] #3 Update behavior is preserved: re-ingesting a changed file replaces its prior chunks (keyed on the source file); watcher, converters and splitter are unchanged
- [x] #4 The official mcp-server-qdrant runs over HTTP/SSE pointed at the local Qdrant (QDRANT_URL=http://localhost:6333, COLLECTION_NAME=Document)
- [x] #5 End-to-end sanity check: the server find tool returns a known ingested document for a relevant query, with no vector-name or payload errors
- [x] #6 docs/mcp.md or a README section documents running the server against local Qdrant and the compatible ingestion format; existing data is re-ingested into the compatible collection
- [x] #7 Tests are updated for the new write path and remain green (unit suite stays network-free; integration verifies the fastembed-compatible store)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Replace the embed+write path: use qdrant-client + fastembed to store chunks under named vector fast-all-minilm-l6-v2 with document/metadata payload (retire Haystack QdrantDocumentStore + SentenceTransformersDocumentEmbedder for writing; keep converters/splitter/watcher). Preserve delete-then-write via the source-file key. 2. Recreate and re-ingest the Document collection in the new format. 3. Run official mcp-server-qdrant (uvx or docker) in SSE mode against QDRANT_URL=http://localhost:6333, COLLECTION_NAME=Document, EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2. 4. Verify qdrant-find returns the ingested governing-ai document. 5. Update tests and docs/mcp.md. 6. Finalize.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented the fastembed-compatible write path. Probed the official mcp-server-qdrant format (QdrantConnector.store): NAMED vector fast-all-minilm-l6-v2 + payload {document, metadata}. Reworked the app embed+write to qdrant-client + fastembed producing exactly that layout; kept Haystack converters + DocumentSplitter and delete-then-write (keyed on metadata.source_file). Dropped qdrant-haystack, sentence-transformers, sentence-transformers-haystack (and transitively torch); added fastembed + qdrant-client.
Verification (live Qdrant at http://localhost:6333):
- Integration tests (3) pass: compatible store, delete-then-write replacement, watcher to ingest to Qdrant.
- AC#5: the official server find logic (mcp_server_qdrant QdrantConnector.search) returned an ingested document from the Document collection with content + metadata, no vector/payload errors.
- AC#4: launched mcp-server-qdrant --transport sse (QDRANT_URL=http://localhost:6333, COLLECTION_NAME=Document); SSE endpoint http://127.0.0.1:8000/sse returned 200 OK.
- docs/mcp.md + README pointer added; app image rebuilt torch-free.
- Unit+integration: 20 passed, 100% coverage on units; ruff+mypy clean.
Note: the previously-ingested file had been removed from raw/, so there was no existing data to re-ingest; Document was recreated empty in the compatible format. Verification used a temporary sample that was then cleaned up.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Reworked ingestion to write a Qdrant collection the official mcp-server-qdrant can read: qdrant-client + fastembed store chunks under the named vector fast-all-minilm-l6-v2 with a document/metadata payload (Haystack still parses/splits; delete-then-write preserved). Removed qdrant-haystack/sentence-transformers/torch; added fastembed/qdrant-client. Verified against local Qdrant: the official server search returns ingested docs, and mcp-server-qdrant runs over SSE (200 on /sse) pointed at http://localhost:6333 with COLLECTION_NAME=Document. Added docs/mcp.md + README pointer. 20 tests pass (100% coverage on units), ruff+mypy clean, app image rebuilt torch-free.
<!-- SECTION:FINAL_SUMMARY:END -->
