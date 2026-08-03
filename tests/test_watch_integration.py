"""End-to-end watch test using a real watchdog Observer (no network / no Qdrant).

Proves that native filesystem events on this OS flow through the handler and
debouncer to the per-file action, that non-matching extensions are ignored, and
that an update re-triggers ingestion. The action is a plain recorder, so no
Haystack or Qdrant is involved.
"""

import threading
import time
from pathlib import Path

from watchdog.observers import Observer

from ingest_memory_rag.config import PATTERNS
from ingest_memory_rag.watcher import Debouncer, IngestEventHandler


class _Recorder:
    def __init__(self) -> None:
        self.paths: list[Path] = []
        self._event = threading.Event()
        self._lock = threading.Lock()

    def __call__(self, path: Path) -> None:
        with self._lock:
            self.paths.append(path)
        self._event.set()

    def wait_for(self, count: int, timeout: float = 5.0) -> bool:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with self._lock:
                if len(self.paths) >= count:
                    return True
            self._event.wait(0.1)
            self._event.clear()
        with self._lock:
            return len(self.paths) >= count

    def names(self) -> set[str]:
        with self._lock:
            return {p.name for p in self.paths}


def _start(tmp_path: Path, recorder: _Recorder) -> tuple[Observer, Debouncer]:
    debouncer = Debouncer(delay=0.1, action=recorder)
    handler = IngestEventHandler(PATTERNS, debouncer)
    observer = Observer()
    observer.schedule(handler, str(tmp_path), recursive=True)
    observer.start()
    return observer, debouncer


def test_only_matching_files_trigger_ingestion(tmp_path):
    recorder = _Recorder()
    observer, debouncer = _start(tmp_path, recorder)
    try:
        (tmp_path / "note.md").write_text("# hello")
        (tmp_path / "data.txt").write_text("hello")
        (tmp_path / "ignore.log").write_text("nope")

        assert recorder.wait_for(2), f"expected 2 ingestions, got {recorder.names()}"
        # Give any erroneous extra event time to arrive.
        time.sleep(0.3)
        assert recorder.names() == {"note.md", "data.txt"}
    finally:
        observer.stop()
        debouncer.cancel_all()
        observer.join()


def test_nested_subfolder_file_is_ingested(tmp_path):
    recorder = _Recorder()
    observer, debouncer = _start(tmp_path, recorder)
    try:
        nested = tmp_path / "deep" / "nested"
        nested.mkdir(parents=True)
        time.sleep(0.2)  # let the recursive watch register the new subtree
        (nested / "buried.md").write_text("# buried")

        assert recorder.wait_for(1), f"nested file not ingested, got {recorder.names()}"
        assert "buried.md" in recorder.names()
    finally:
        observer.stop()
        debouncer.cancel_all()
        observer.join()


def test_update_retriggers_ingestion(tmp_path):
    recorder = _Recorder()
    observer, debouncer = _start(tmp_path, recorder)
    try:
        target = tmp_path / "doc.txt"
        target.write_text("v1")
        assert recorder.wait_for(1), "create was not observed"

        time.sleep(0.3)  # let the first debounce fire and clear
        target.write_text("v2 updated content")
        assert recorder.wait_for(2), "update was not observed"
    finally:
        observer.stop()
        debouncer.cancel_all()
        observer.join()
