"""Runtime configuration, read from the environment with sensible defaults.

This module imports nothing heavy so it stays cheap to import from tests.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_WATCH_FOLDER = "./raw"
DEFAULT_QDRANT_URL = "http://localhost:6333"
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_EMBEDDING_DIM = 384  # matches all-MiniLM-L6-v2
PATTERNS: tuple[str, ...] = ("*.txt", "*.md")
MARKDOWN_SUFFIXES = frozenset({".md", ".markdown"})

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def _env_str(name: str, default: str) -> str:
    return os.environ.get(name, "").strip() or default


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    return int(raw) if raw else default


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name, "").strip()
    return float(raw) if raw else default


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    return raw in _TRUTHY if raw else default


def is_markdown(path: str | os.PathLike[str]) -> bool:
    """True when the path should be parsed as Markdown rather than plain text."""
    return Path(path).suffix.lower() in MARKDOWN_SUFFIXES


@dataclass(frozen=True)
class Settings:
    """Immutable, environment-driven configuration for the ingestion service."""

    watch_folder: Path
    qdrant_url: str
    index: str
    embedding_model: str
    embedding_dim: int
    patterns: tuple[str, ...]
    split_by: str
    split_length: int
    split_overlap: int
    debounce_seconds: float
    recreate_index: bool
    scan_on_start: bool

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            watch_folder=Path(_env_str("WATCH_FOLDER", DEFAULT_WATCH_FOLDER)).expanduser(),
            qdrant_url=_env_str("QDRANT_URL", DEFAULT_QDRANT_URL),
            index=_env_str("QDRANT_INDEX", "Document"),
            embedding_model=_env_str("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
            embedding_dim=_env_int("EMBEDDING_DIM", DEFAULT_EMBEDDING_DIM),
            patterns=PATTERNS,
            split_by=_env_str("SPLIT_BY", "word"),
            split_length=_env_int("SPLIT_LENGTH", 200),
            split_overlap=_env_int("SPLIT_OVERLAP", 30),
            debounce_seconds=_env_float("DEBOUNCE_SECONDS", 1.0),
            recreate_index=_env_bool("QDRANT_RECREATE_INDEX", default=False),
            scan_on_start=_env_bool("SCAN_ON_START", default=True),
        )
