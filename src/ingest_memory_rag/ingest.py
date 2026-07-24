"""Convert a single file and (re)write its chunks into Qdrant.

Chunks are stored in the layout the official mcp-server-qdrant reads: a named
vector (``fast-<model>``), payload ``{"document": <text>, "metadata": {...}}``,
with fastembed producing the vectors. Parsing and splitting use Haystack.
"""

from __future__ import annotations

import logging
import uuid
from pathlib import Path

from haystack.components.converters import MarkdownToDocument, TextFileToDocument
from haystack.dataclasses import Document
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue, PointStruct

from ingest_memory_rag.config import Settings, fastembed_vector_name, is_markdown
from ingest_memory_rag.pipeline import (
    create_embedder,
    create_qdrant_client,
    create_splitter,
    ensure_collection,
)

logger = logging.getLogger(__name__)

# Stored at payload["metadata"][FILE_PATH_META]; used to replace a file's chunks.
FILE_PATH_META = "source_file"


class IngestionEngine:
    """Converts, splits, embeds (fastembed) and writes chunks to Qdrant."""

    def __init__(self, settings: Settings, client: QdrantClient | None = None) -> None:
        self.settings = settings
        self.client = client or create_qdrant_client(settings)
        self.embedder = create_embedder(settings)
        self.splitter = create_splitter(settings)
        self.text_converter = TextFileToDocument()
        self.markdown_converter = MarkdownToDocument()
        self.vector_name = fastembed_vector_name(settings.embedding_model)
        ensure_collection(self.client, settings)

    def verify_connection(self) -> None:
        """Force a round-trip to Qdrant so an unreachable backend fails fast."""
        self.client.get_collections()

    def _convert(self, path: Path) -> list[Document]:
        if is_markdown(path):
            result = self.markdown_converter.run(sources=[path])
        else:
            result = self.text_converter.run(sources=[path])
        return list(result["documents"])

    def _split(self, documents: list[Document]) -> list[Document]:
        return list(self.splitter.run(documents=documents)["documents"])

    def _delete_existing(self, path: Path) -> None:
        self.client.delete(
            collection_name=self.settings.index,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key=f"metadata.{FILE_PATH_META}",
                        match=MatchValue(value=str(path)),
                    )
                ]
            ),
        )

    def ingest_file(self, path: str | Path) -> int:
        """Ingest one file, replacing any previously stored chunks for it.

        Conversion/splitting happen before the delete so a failure leaves the
        existing chunks intact. Returns the number of chunks written.
        """
        path = Path(path).resolve()
        chunks = self._split(self._convert(path))
        self._delete_existing(path)
        if not chunks:
            logger.warning("No content extracted from %s; wrote 0 chunks", path)
            return 0
        texts = [chunk.content or "" for chunk in chunks]
        embeddings = list(self.embedder.embed(texts))
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector={self.vector_name: embedding.tolist()},
                payload={
                    "document": text,
                    "metadata": {FILE_PATH_META: str(path), "file_name": path.name},
                },
            )
            for text, embedding in zip(texts, embeddings, strict=True)
        ]
        self.client.upsert(collection_name=self.settings.index, points=points)
        return len(points)
