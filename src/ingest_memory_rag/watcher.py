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

import pathspec
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


def _build_spec(lines: list[str]) -> pathspec.PathSpec:
    """Compile ignore ``lines`` with full gitignore semantics when available."""
    spec_cls = getattr(pathspec, "GitIgnoreSpec", None)
    if spec_cls is not None:
        return spec_cls.from_lines(lines)
    return pathspec.PathSpec.from_lines("gitwildmatch", lines)


class IgnoreMatcher:
    """Match paths against gitignore-style rules relative to the watch folder."""

    def __init__(self, watch_folder: Path, spec: pathspec.PathSpec) -> None:
        self._watch_folder = Path(watch_folder).resolve()
        self._spec = spec

    def is_ignored(self, path: str | Path) -> bool:
        """True when ``path`` sits under the watch folder and matches a rule."""
        if not self._spec:
            return False
        resolved = Path(path).resolve()
        try:
            rel = resolved.relative_to(self._watch_folder)
        except ValueError:
            return False  # outside the watch folder — never our concern
        return self._spec.match_file(rel.as_posix())


def build_ignore_matcher(settings: Settings) -> IgnoreMatcher:
    """Build an :class:`IgnoreMatcher` from ``settings.ignore_file`` if it exists.

    The file is read once; an absent file yields an empty spec (nothing ignored).
    """
    if settings.ignore_file.is_file():
        lines = settings.ignore_file.read_text(encoding="utf-8").splitlines()
    else:
        lines = []
    return IgnoreMatcher(settings.watch_folder, _build_spec(lines))


def should_ingest(path: str | Path, patterns: tuple[str, ...]) -> bool:
    """True when ``path`` is a file whose name matches one of ``patterns``."""
    candidate = Path(path)
    if candidate.is_dir():
        return False
    return any(fnmatch.fnmatch(candidate.name, pattern) for pattern in patterns)


def iter_matching_files(
    folder: Path,
    patterns: tuple[str, ...],
    matcher: IgnoreMatcher | None = None,
) -> Iterator[Path]:
    """Yield existing files under ``folder`` matching ``patterns`` and not ignored."""
    seen: set[Path] = set()
    for pattern in patterns:
        for path in folder.rglob(pattern):
            if path.is_file() and path not in seen:
                seen.add(path)
                if matcher is not None and matcher.is_ignored(path):
                    continue
                yield path


def initial_scan(
    folder: Path,
    patterns: tuple[str, ...],
    action: Action,
    matcher: IgnoreMatcher | None = None,
) -> int:
    """Run ``action`` against every existing matching, non-ignored file.

    Returns the count.
    """
    count = 0
    for path in iter_matching_files(folder, patterns, matcher):
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

    def __init__(
        self,
        patterns: tuple[str, ...],
        debouncer: Debouncer,
        matcher: IgnoreMatcher | None = None,
    ) -> None:
        super().__init__(patterns=list(patterns), ignore_directories=True, case_sensitive=False)
        self._debouncer = debouncer
        self._matcher = matcher

    def on_created(self, event: FileSystemEvent) -> None:
        self._schedule(event.src_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        self._schedule(event.src_path)

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        # Atomic saves (write temp file, then rename into place) surface here.
        self._schedule(event.dest_path)

    def _schedule(self, raw_path: str | bytes) -> None:
        path = raw_path.decode() if isinstance(raw_path, bytes) else raw_path
        candidate = Path(path)
        if self._matcher is not None and self._matcher.is_ignored(candidate):
            logger.debug("Ignoring %s (matched an ignore rule)", candidate)
            return
        self._debouncer.trigger(candidate)


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

    # Loaded once at startup; editing the ignore file takes effect on restart.
    matcher = build_ignore_matcher(settings)

    if settings.scan_on_start:
        logger.info("Scanning existing files under %s", folder)
        initial_scan(folder, settings.patterns, action, matcher)

    debouncer = Debouncer(settings.debounce_seconds, action)
    handler = IngestEventHandler(settings.patterns, debouncer, matcher)
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
