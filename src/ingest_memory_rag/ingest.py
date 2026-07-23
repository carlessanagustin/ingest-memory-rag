"""Convert a single file and (re)write its chunks into Qdrant."""

from __future__ import annotations

import logging
from pathlib import Path

from haystack.components.converters import MarkdownToDocument, TextFileToDocument
from haystack.dataclasses import Document
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore

from ingest_memory_rag.config import Settings, is_markdown
from ingest_memory_rag.pipeline import create_document_store, create_indexing_pipeline

logger = logging.getLogger(__name__)

# Meta key used to associate every chunk with its source file so that an
# updated file can have its stale chunks deleted before the new ones land.
FILE_PATH_META = "file_path"


class IngestionEngine:
    """Holds the warmed-up pipeline and converters for repeated ingestion."""

    def __init__(
        self,
        settings: Settings,
        document_store: QdrantDocumentStore | None = None,
    ) -> None:
        self.settings = settings
        self.document_store = document_store or create_document_store(settings)
        self.pipeline = create_indexing_pipeline(settings, self.document_store)
        self.text_converter = TextFileToDocument()
        self.markdown_converter = MarkdownToDocument()

    def _convert(self, path: Path) -> list[Document]:
        meta = {FILE_PATH_META: str(path)}
        if is_markdown(path):
            result = self.markdown_converter.run(sources=[path], meta=meta)
        else:
            result = self.text_converter.run(sources=[path], meta=meta)
        return list(result["documents"])

    def _delete_existing(self, path: Path) -> int:
        filters = {"field": f"meta.{FILE_PATH_META}", "operator": "==", "value": str(path)}
        existing = self.document_store.filter_documents(filters=filters)
        if existing:
            self.document_store.delete_documents([doc.id for doc in existing])
        return len(existing)

    def ingest_file(self, path: str | Path) -> int:
        """Ingest one file, replacing any previously stored chunks for it.

        Returns the number of chunks written. Conversion happens before the
        delete so that a conversion failure leaves the existing chunks intact.
        """
        path = Path(path)
        documents = self._convert(path)
        removed = self._delete_existing(path)
        if removed:
            logger.info("Removed %d stale chunk(s) for %s", removed, path)
        if not documents:
            logger.warning("No content extracted from %s; wrote 0 chunks", path)
            return 0
        result = self.pipeline.run({"splitter": {"documents": documents}})
        written = int(result["writer"]["documents_written"])
        return written
