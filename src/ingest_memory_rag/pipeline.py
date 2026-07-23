"""Haystack document store and indexing pipeline construction.

The indexing pipeline is deliberately split → embed → write. File conversion is
done per-file (see :mod:`ingest_memory_rag.ingest`) so a single, warmed-up
embedder is shared across every ingested file regardless of its format.
"""

from __future__ import annotations

from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore

from ingest_memory_rag.config import Settings


def create_document_store(settings: Settings) -> QdrantDocumentStore:
    return QdrantDocumentStore(
        url=settings.qdrant_url,
        index=settings.index,
        embedding_dim=settings.embedding_dim,
        recreate_index=settings.recreate_index,
    )


def create_indexing_pipeline(settings: Settings, document_store: QdrantDocumentStore) -> Pipeline:
    """Build split → embed → write. Entry point is the ``splitter`` component."""
    pipeline = Pipeline()
    pipeline.add_component(
        "splitter",
        DocumentSplitter(
            split_by=settings.split_by,
            split_length=settings.split_length,
            split_overlap=settings.split_overlap,
        ),
    )
    pipeline.add_component(
        "embedder", SentenceTransformersDocumentEmbedder(model=settings.embedding_model)
    )
    pipeline.add_component(
        "writer",
        DocumentWriter(document_store=document_store, policy=DuplicatePolicy.OVERWRITE),
    )
    pipeline.connect("splitter.documents", "embedder.documents")
    pipeline.connect("embedder.documents", "writer.documents")
    return pipeline
