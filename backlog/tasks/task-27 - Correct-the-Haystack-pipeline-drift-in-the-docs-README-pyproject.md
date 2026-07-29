---
id: TASK-27
title: Correct the Haystack-pipeline drift in the docs (README + pyproject)
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 09:24'
updated_date: '2026-07-29 09:25'
labels:
  - docs
dependencies: []
references:
  - src/ingest_memory_rag/pipeline.py
  - src/ingest_memory_rag/ingest.py
type: docs
ordinal: 29000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The docs describe ingestion as a Haystack indexing pipeline, but the code only uses Haystack for parsing and splitting (TextFileToDocument/MarkdownToDocument + DocumentSplitter). Embeddings are produced by fastembed (TextEmbedding) and storage is via qdrant-client (upsert) — not Haystack SentenceTransformersDocumentEmbedder/DocumentWriter. Correct the drift in three spots: (a) the README intro sentence, (b) the collapsible detailed diagram embed/write nodes, and (c) the pyproject.toml description string. Docs/metadata only — no source or dependency changes; haystack-ai stays because it is still used for parsing/splitting.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The README intro no longer implies Haystack runs the whole pipeline; it accurately states Haystack parses/splits while fastembed embeds and qdrant-client stores
- [x] #2 In the detailed code-level diagram, the embed node reflects fastembed (TextEmbedding) and the write node reflects qdrant-client upsert (no SentenceTransformersDocumentEmbedder/DocumentWriter); the convert/split/delete nodes are unchanged (already accurate)
- [x] #3 The pyproject.toml `description` no longer claims "via Haystack" and accurately reflects the fastembed + qdrant-client reality
- [x] #4 The detailed diagram still renders as valid GitHub-compatible Mermaid
- [x] #5 Changes are limited to README.md and pyproject.toml; no source-code or dependency changes (haystack-ai remains, still used for parsing/splitting)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. README intro: rewrite the "through a Haystack indexing pipeline" sentence to describe the hybrid accurately (Haystack parse/split, fastembed embed, qdrant-client store).
2. Detailed diagram: node H SentenceTransformersDocumentEmbedder -> "embed / fastembed TextEmbedding"; node I DocumentWriter -> "upsert / qdrant-client".
3. pyproject.toml description: drop "via Haystack"; state Haystack parsing + fastembed embeddings.
4. Verify: mermaid-cli renders both diagrams; git shows only README.md + pyproject.toml; haystack-ai dependency untouched.
Handled inline; backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Handled inline; verified. Grounded in code (pipeline.py/ingest.py): Haystack does convert (TextFileToDocument/MarkdownToDocument) + split (DocumentSplitter); fastembed TextEmbedding does embeddings; qdrant-client upsert does storage. Edits: (1) README intro rewritten to the accurate hybrid (Haystack parse/split, fastembed embed, qdrant-client upsert), with fastembed + qdrant-client links; (2) detailed diagram node H -> "embed / fastembed TextEmbedding", node I -> "upsert / qdrant-client" (convert/split/delete nodes left as-is, already accurate); (3) pyproject.toml description changed from "via Haystack" to "(Haystack parsing, fastembed embeddings)". Verified: mermaid-cli rendered both README charts OK; rendered the detailed diagram to PNG and visually confirmed the new fastembed/qdrant-client nodes; git status shows only README.md + pyproject.toml changed; haystack-ai>=2.6 dependency untouched (still used for parsing/splitting). Note (out of scope, not changed): the detailed diagram still draws delete before split, whereas the code splits then deletes — a minor ordering nit unrelated to the Haystack drift.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Corrected the Haystack-pipeline doc drift. The code only uses Haystack for parsing/splitting; embeddings are fastembed (TextEmbedding) and storage is qdrant-client (upsert). Updated the README intro sentence, the detailed diagram embed/write nodes (fastembed / qdrant-client instead of SentenceTransformersDocumentEmbedder / DocumentWriter), and the pyproject.toml description. Docs/metadata only — haystack-ai remains a dependency (still used for parsing/splitting); verified both diagrams still render.
<!-- SECTION:FINAL_SUMMARY:END -->
