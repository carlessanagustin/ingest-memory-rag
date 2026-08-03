from pathlib import Path

import pytest

from ingest_memory_rag.config import (
    DEFAULT_QDRANT_URL,
    DEFAULT_WATCH_IGNORE,
    Settings,
    fastembed_vector_name,
    is_markdown,
)


def test_defaults(monkeypatch):
    for var in (
        "WATCH_FOLDER",
        "QDRANT_URL",
        "QDRANT_INDEX",
        "EMBEDDING_MODEL",
        "EMBEDDING_DIM",
        "SPLIT_LENGTH",
        "DEBOUNCE_SECONDS",
        "QDRANT_RECREATE_INDEX",
        "SCAN_ON_START",
        "WATCH_USE_POLLING",
        "WATCH_IGNORE",
    ):
        monkeypatch.delenv(var, raising=False)

    settings = Settings.from_env()

    assert settings.watch_folder == Path("./raw")
    assert settings.ignore_file == Path("./raw") / DEFAULT_WATCH_IGNORE
    assert settings.qdrant_url == DEFAULT_QDRANT_URL
    assert settings.embedding_dim == 384
    assert settings.patterns == ("*.txt", "*.md")
    assert settings.recreate_index is False
    assert settings.scan_on_start is True
    assert settings.use_polling is False


def test_env_overrides(monkeypatch):
    monkeypatch.setenv("WATCH_FOLDER", "/data/docs")
    monkeypatch.setenv("QDRANT_URL", "http://qdrant:6333")
    monkeypatch.setenv("EMBEDDING_DIM", "768")
    monkeypatch.setenv("DEBOUNCE_SECONDS", "2.5")
    monkeypatch.setenv("QDRANT_RECREATE_INDEX", "true")
    monkeypatch.setenv("SCAN_ON_START", "no")
    monkeypatch.setenv("WATCH_USE_POLLING", "true")

    settings = Settings.from_env()

    assert settings.watch_folder == Path("/data/docs")
    assert settings.qdrant_url == "http://qdrant:6333"
    assert settings.embedding_dim == 768
    assert settings.debounce_seconds == 2.5
    assert settings.recreate_index is True
    assert settings.scan_on_start is False
    assert settings.use_polling is True


def test_ignore_file_defaults_inside_watch_folder(monkeypatch):
    monkeypatch.setenv("WATCH_FOLDER", "/data/docs")
    monkeypatch.delenv("WATCH_IGNORE", raising=False)

    settings = Settings.from_env()

    assert settings.ignore_file == Path("/data/docs") / DEFAULT_WATCH_IGNORE


def test_ignore_file_relative_override_resolves_against_watch_folder(monkeypatch):
    monkeypatch.setenv("WATCH_FOLDER", "/data/docs")
    monkeypatch.setenv("WATCH_IGNORE", "skip.list")

    settings = Settings.from_env()

    assert settings.ignore_file == Path("/data/docs/skip.list")


def test_ignore_file_absolute_override_is_used_verbatim(monkeypatch):
    monkeypatch.setenv("WATCH_FOLDER", "/data/docs")
    monkeypatch.setenv("WATCH_IGNORE", "/etc/ingest/global.ignore")

    settings = Settings.from_env()

    assert settings.ignore_file == Path("/etc/ingest/global.ignore")


def test_valid_split_by_override(monkeypatch):
    monkeypatch.setenv("SPLIT_BY", "sentence")
    assert Settings.from_env().split_by == "sentence"


def test_invalid_split_by_raises(monkeypatch):
    monkeypatch.setenv("SPLIT_BY", "bogus")
    with pytest.raises(ValueError, match="SPLIT_BY"):
        Settings.from_env()


def test_is_markdown():
    assert is_markdown("notes.md") is True
    assert is_markdown("README.MARKDOWN") is True
    assert is_markdown("data.txt") is False
    assert is_markdown("script.py") is False


def test_fastembed_vector_name():
    assert (
        fastembed_vector_name("sentence-transformers/all-MiniLM-L6-v2") == "fast-all-minilm-l6-v2"
    )
    assert fastembed_vector_name("BAAI/bge-small-en-v1.5") == "fast-bge-small-en-v1.5"
