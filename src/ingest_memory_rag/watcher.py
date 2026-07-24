"""Cross-platform folder watching.

``watchdog`` picks the best native backend per OS: inotify on Linux, FSEvents
(or kqueue) on macOS, and ReadDirectoryChangesW on Windows. The same code runs
unchanged on all three.
"""

from __future__ import annotations

import fnmatch
import logging
import threading
from collections.abc import Callable, Iterator
from pathlib import Path

from watchdog.events import (
    DirMovedEvent,
    FileMovedEvent,
    FileSystemEvent,
    PatternMatchingEventHandler,
)
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

from ingest_memory_rag.config import Settings

logger = logging.getLogger(__name__)

Action = Callable[[Path], None]


def should_ingest(path: str | Path, patterns: tuple[str, ...]) -> bool:
    """True when ``path`` is a file whose name matches one of ``patterns``."""
    candidate = Path(path)
    if candidate.is_dir():
        return False
    return any(fnmatch.fnmatch(candidate.name, pattern) for pattern in patterns)


def iter_matching_files(folder: Path, patterns: tuple[str, ...]) -> Iterator[Path]:
    """Yield existing files under ``folder`` matching any of ``patterns``."""
    seen: set[Path] = set()
    for pattern in patterns:
        for path in folder.rglob(pattern):
            if path.is_file() and path not in seen:
                seen.add(path)
                yield path


def initial_scan(folder: Path, patterns: tuple[str, ...], action: Action) -> int:
    """Run ``action`` against every existing matching file. Returns the count."""
    count = 0
    for path in iter_matching_files(folder, patterns):
        action(path)
        count += 1
    return count


class Debouncer:
    """Coalesce bursts of events for the same path into a single call.

    Editors and copy tools emit several create/modify events per save; the
    timer resets on every trigger so ``action`` runs once, once the file has
    been quiet for ``delay`` seconds.
    """

    def __init__(self, delay: float, action: Action) -> None:
        self._delay = delay
        self._action = action
        self._timers: dict[Path, threading.Timer] = {}
        self._lock = threading.Lock()

    def trigger(self, path: Path) -> None:
        with self._lock:
            existing = self._timers.get(path)
            if existing is not None:
                existing.cancel()
            timer = threading.Timer(self._delay, self._fire, args=(path,))
            self._timers[path] = timer
            timer.start()

    def _fire(self, path: Path) -> None:
        with self._lock:
            self._timers.pop(path, None)
        self._action(path)

    def cancel_all(self) -> None:
        with self._lock:
            for timer in self._timers.values():
                timer.cancel()
            self._timers.clear()


class IngestEventHandler(PatternMatchingEventHandler):
    """Routes matching create/modify/move events to the debouncer."""

    def __init__(self, patterns: tuple[str, ...], debouncer: Debouncer) -> None:
        super().__init__(patterns=list(patterns), ignore_directories=True, case_sensitive=False)
        self._debouncer = debouncer

    def on_created(self, event: FileSystemEvent) -> None:
        self._schedule(event.src_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        self._schedule(event.src_path)

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        # Atomic saves (write temp file, then rename into place) surface here.
        self._schedule(event.dest_path)

    def _schedule(self, raw_path: str | bytes) -> None:
        path = raw_path.decode() if isinstance(raw_path, bytes) else raw_path
        self._debouncer.trigger(Path(path))


def _build_default_action(settings: Settings) -> Action:  # pragma: no cover
    """Create the real ingestion callback.

    Excluded from unit coverage: it imports the Haystack layer lazily and needs
    a live Qdrant, so it is exercised by integration runs rather than the fast
    unit suite.
    """
    from ingest_memory_rag.ingest import IngestionEngine

    engine = IngestionEngine(settings)
    engine.verify_connection()  # fail fast if Qdrant is unreachable

    def action(path: Path) -> None:
        try:
            written = engine.ingest_file(path)
            logger.info("Ingested %s → %d chunk(s)", path, written)
        except Exception:  # noqa: BLE001 - keep the watcher alive on any file error
            logger.exception("Failed to ingest %s", path)

    return action


def run(settings: Settings, action: Action | None = None) -> None:  # pragma: no cover
    """Start watching ``settings.watch_folder`` and block until interrupted.

    ``action`` is the per-file callback; when omitted a real
    :class:`~ingest_memory_rag.ingest.IngestionEngine` is used.
    """
    folder = settings.watch_folder
    folder.mkdir(parents=True, exist_ok=True)

    if action is None:
        try:
            action = _build_default_action(settings)
        except Exception as exc:  # noqa: BLE001 - surface a clear startup error
            logger.error(
                "Cannot reach Qdrant at %s — is it running? (%s)",
                settings.qdrant_url,
                exc,
            )
            raise SystemExit(1) from exc

    if settings.scan_on_start:
        logger.info("Scanning existing files under %s", folder)
        initial_scan(folder, settings.patterns, action)

    debouncer = Debouncer(settings.debounce_seconds, action)
    handler = IngestEventHandler(settings.patterns, debouncer)
    # Native FS events (inotify/FSEvents) are not delivered across bind mounts
    # on Docker Desktop; polling reliably picks up changes there.
    observer = PollingObserver() if settings.use_polling else Observer()
    observer.schedule(handler, str(folder), recursive=True)
    observer.start()
    logger.info("Watching %s for %s (Ctrl+C to stop)", folder, list(settings.patterns))
    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        logger.info("Stopping...")
    finally:
        observer.stop()
        debouncer.cancel_all()
        observer.join()
