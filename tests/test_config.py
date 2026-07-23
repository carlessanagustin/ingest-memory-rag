from pathlib import Path

import pytest

from ingest_memory_rag.config import (
    DEFAULT_QDRANT_URL,
    Settings,
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
    ):
        monkeypatch.delenv(var, raising=False)

    settings = Settings.from_env()

    assert settings.watch_folder == Path("./raw")
    assert settings.qdrant_url == DEFAULT_QDRANT_URL
    assert settings.embedding_dim == 384
    assert settings.patterns == ("*.txt", "*.md")
    assert settings.recreate_index is False
    assert settings.scan_on_start is True


def test_env_overrides(monkeypatch):
    monkeypatch.setenv("WATCH_FOLDER", "/data/docs")
    monkeypatch.setenv("QDRANT_URL", "http://qdrant:6333")
    monkeypatch.setenv("EMBEDDING_DIM", "768")
    monkeypatch.setenv("DEBOUNCE_SECONDS", "2.5")
    monkeypatch.setenv("QDRANT_RECREATE_INDEX", "true")
    monkeypatch.setenv("SCAN_ON_START", "no")

    settings = Settings.from_env()

    assert settings.watch_folder == Path("/data/docs")
    assert settings.qdrant_url == "http://qdrant:6333"
    assert settings.embedding_dim == 768
    assert settings.debounce_seconds == 2.5
    assert settings.recreate_index is True
    assert settings.scan_on_start is False


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
