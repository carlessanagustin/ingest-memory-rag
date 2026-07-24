"""Qdrant client, fastembed embedder, and splitter construction.

The collection is written in the layout the official mcp-server-qdrant reads:
a named vector (``fast-<model>``) and a payload of ``{"document", "metadata"}``.
Embeddings come from fastembed with the same model the MCP server uses to embed
queries, so store and query align. Parsing/splitting still use Haystack.
"""

from __future__ import annotations

from fastembed import TextEmbedding
from haystack.components.preprocessors import DocumentSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from ingest_memory_rag.config import Settings, fastembed_vector_name


def create_qdrant_client(settings: Settings) -> QdrantClient:
    return QdrantClient(url=settings.qdrant_url)


def create_embedder(settings: Settings) -> TextEmbedding:
    return TextEmbedding(model_name=settings.embedding_model)


def create_splitter(settings: Settings) -> DocumentSplitter:
    splitter = DocumentSplitter(
        split_by=settings.split_by,
        split_length=settings.split_length,
        split_overlap=settings.split_overlap,
    )
    splitter.warm_up()
    return splitter


def ensure_collection(client: QdrantClient, settings: Settings) -> None:
    """Create the collection with the fastembed-compatible named vector if absent."""
    name = settings.index
    if settings.recreate_index and client.collection_exists(name):
        client.delete_collection(name)
    if not client.collection_exists(name):
        client.create_collection(
            name,
            vectors_config={
                fastembed_vector_name(settings.embedding_model): VectorParams(
                    size=settings.embedding_dim, distance=Distance.COSINE
                )
            },
        )
