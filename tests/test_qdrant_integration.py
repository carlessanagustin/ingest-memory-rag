"""End-to-end ingestion against a live Qdrant (skipped when unavailable).

Proves AC#4: re-ingesting a changed file deletes its previous chunks before
writing the new ones, so the store never accumulates stale content.

Requires a reachable Qdrant (``QDRANT_URL``, default http://localhost:6333) and
the Haystack ML stack. Both absences ``skip`` rather than fail, so the fast unit
suite stays green without any services. Run explicitly with:

    uv run pytest -m integration
"""

from __future__ import annotations

import time
import urllib.error
import urllib.request
from dataclasses import replace

import pytest

from ingest_memory_rag.config import Settings

# The heavy Haystack import is optional; skip the whole module if it is absent.
pytest.importorskip("haystack")
pytest.importorskip("haystack_integrations.document_stores.qdrant")

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


def _by_source(path):
    from ingest_memory_rag.ingest import FILE_PATH_META

    return {
        "field": f"meta.{FILE_PATH_META}",
        "operator": "==",
        "value": str(path.resolve()),
    }


@pytest.fixture
def engine():
    from ingest_memory_rag.ingest import IngestionEngine

    # Dedicated, freshly recreated collection so the test is isolated.
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

    # Large first version → several chunks, tagged with a distinctive token.
    doc.write_text("ALPHATOKEN " + " ".join(["lorem"] * 300))
    written_a = engine.ingest_file(doc)
    assert written_a > 1
    assert engine.document_store.count_documents() == written_a

    # Small second version → a single chunk with a different token.
    doc.write_text("BRAVOTOKEN just a short replacement body")
    written_b = engine.ingest_file(doc)

    total = engine.document_store.count_documents()
    assert total == written_b, f"stale chunks left behind: {total} != {written_b}"

    stored = engine.document_store.filter_documents(filters=_by_source(doc))
    contents = " ".join(d.content or "" for d in stored)
    assert "BRAVOTOKEN" in contents
    assert "ALPHATOKEN" not in contents  # old content fully removed


def test_markdown_file_is_ingested(engine, tmp_path):
    note = tmp_path / "note.md"
    note.write_text("# Heading\n\nSome **markdown** body text for embedding.")

    written = engine.ingest_file(note)

    assert written >= 1
    stored = engine.document_store.filter_documents(filters=_by_source(note))
    assert stored
    assert any("markdown" in (d.content or "").lower() for d in stored)


def test_dropped_file_flows_through_watcher_into_qdrant(engine, tmp_path):
    """Full chain: watchdog event → debounce → ingest → Qdrant."""
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
        count = 0
        while time.monotonic() < deadline:
            count = engine.document_store.count_documents()
            if count > 0:
                break
            time.sleep(0.3)
        assert count > 0, "file dropped into the watched folder never reached Qdrant"
    finally:
        observer.stop()
        debouncer.cancel_all()
        observer.join()
