"""End-to-end ingestion against a live Qdrant (skipped when unavailable).

Verifies the fastembed-compatible store: chunks land under the named vector with
a document/metadata payload, and re-ingesting a changed file replaces its prior
chunks (no stale content).

Requires a reachable Qdrant (``QDRANT_URL``, default http://localhost:6333) and
the ingestion deps (fastembed, qdrant-client, haystack). Absences ``skip`` so the
fast unit suite stays green without services. Run explicitly with:

    uv run pytest -m integration
"""

from __future__ import annotations

import time
import urllib.error
import urllib.request
from dataclasses import replace

import pytest

from ingest_memory_rag.config import Settings

pytest.importorskip("fastembed")
pytest.importorskip("qdrant_client")
pytest.importorskip("haystack")

from qdrant_client.models import FieldCondition, Filter, MatchValue  # noqa: E402

QDRANT_URL = Settings.from_env().qdrant_url


def _qdrant_reachable(url: str) -> bool:
    try:
        with urllib.request.urlopen(f"{url}/readyz", timeout=2) as resp:
            return resp.status == 200
    except (urllib.error.URLError, OSError):
        return False


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not _qdrant_reachable(QDRANT_URL),
        reason=f"no Qdrant reachable at {QDRANT_URL}",
    ),
]


def _source_filter(path):
    return Filter(
        must=[
            FieldCondition(
                key="metadata.source_file",
                match=MatchValue(value=str(path.resolve())),
            )
        ]
    )


def _total(engine):
    return engine.client.count(collection_name=engine.settings.index, exact=True).count


def _count_for(engine, path):
    return engine.client.count(
        collection_name=engine.settings.index,
        count_filter=_source_filter(path),
        exact=True,
    ).count


def _documents_for(engine, path):
    points, _ = engine.client.scroll(
        collection_name=engine.settings.index,
        scroll_filter=_source_filter(path),
        with_payload=True,
        limit=100,
    )
    return " ".join((p.payload or {}).get("document", "") for p in points)


@pytest.fixture
def engine():
    from ingest_memory_rag.ingest import IngestionEngine

    settings = replace(
        Settings.from_env(),
        index="e2e_ingest_test",
        recreate_index=True,
        split_length=50,
        split_overlap=0,
    )
    return IngestionEngine(settings)


def test_update_replaces_previous_chunks(engine, tmp_path):
    doc = tmp_path / "doc.txt"

    doc.write_text("ALPHATOKEN " + " ".join(["lorem"] * 300))
    written_a = engine.ingest_file(doc)
    assert written_a > 1
    assert _total(engine) == written_a
    assert _count_for(engine, doc) == written_a

    doc.write_text("BRAVOTOKEN just a short replacement body")
    written_b = engine.ingest_file(doc)

    assert _total(engine) == written_b, "stale chunks left behind"
    assert _count_for(engine, doc) == written_b
    contents = _documents_for(engine, doc)
    assert "BRAVOTOKEN" in contents
    assert "ALPHATOKEN" not in contents


def test_markdown_file_is_ingested(engine, tmp_path):
    note = tmp_path / "note.md"
    note.write_text("# Heading\n\nSome markdown body text for embedding.")

    written = engine.ingest_file(note)

    assert written >= 1
    assert "markdown" in _documents_for(engine, note).lower()


def test_dropped_file_flows_through_watcher_into_qdrant(engine, tmp_path):
    """Full chain: watchdog event -> debounce -> ingest -> Qdrant."""
    from watchdog.observers import Observer

    from ingest_memory_rag.config import PATTERNS
    from ingest_memory_rag.watcher import Debouncer, IngestEventHandler

    debouncer = Debouncer(delay=0.3, action=engine.ingest_file)
    handler = IngestEventHandler(PATTERNS, debouncer)
    observer = Observer()
    observer.schedule(handler, str(tmp_path), recursive=True)
    observer.start()
    try:
        (tmp_path / "dropped.txt").write_text("end to end ingestion " * 20)
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            if _total(engine) > 0:
                break
            time.sleep(0.3)
        assert _total(engine) > 0, "dropped file never reached Qdrant"
    finally:
        observer.stop()
        debouncer.cancel_all()
        observer.join()
