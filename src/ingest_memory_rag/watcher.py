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
    FileSystemEventHandler,
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
    """Match paths against gitignore-style rules relative to the watch folder.

    The compiled spec can be rebuilt from disk at runtime via :meth:`reload`. A
    lock guards the spec because it is read on the observer thread while being
    swapped from an event-callback thread.
    """

    def __init__(
        self,
        watch_folder: Path,
        spec: pathspec.PathSpec,
        ignore_file: Path | None = None,
    ) -> None:
        self._watch_folder = Path(watch_folder).resolve()
        self._spec = spec
        self._ignore_file = ignore_file
        self._lock = threading.Lock()

    def reload(self) -> None:
        """Re-read the ignore file and swap in a freshly compiled spec.

        A no-op when no ignore file was configured; an absent file yields an
        empty spec (nothing ignored).
        """
        if self._ignore_file is None:
            return
        if self._ignore_file.is_file():
            lines = self._ignore_file.read_text(encoding="utf-8").splitlines()
        else:
            lines = []
        spec = _build_spec(lines)
        with self._lock:
            self._spec = spec

    def is_ignored(self, path: str | Path) -> bool:
        """True when ``path`` sits under the watch folder and matches a rule."""
        with self._lock:
            spec = self._spec
        if not spec:
            return False
        resolved = Path(path).resolve()
        try:
            rel = resolved.relative_to(self._watch_folder)
        except ValueError:
            return False  # outside the watch folder — never our concern
        return spec.match_file(rel.as_posix())


def build_ignore_matcher(settings: Settings) -> IgnoreMatcher:
    """Build an :class:`IgnoreMatcher` from ``settings.ignore_file`` if it exists.

    An absent file yields an empty spec (nothing ignored). The file path is kept
    so :meth:`IgnoreMatcher.reload` can re-read it after it changes on disk.
    """
    if settings.ignore_file.is_file():
        lines = settings.ignore_file.read_text(encoding="utf-8").splitlines()
    else:
        lines = []
    return IgnoreMatcher(
        settings.watch_folder,
        _build_spec(lines),
        ignore_file=settings.ignore_file,
    )


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


class IgnoreFileEventHandler(FileSystemEventHandler):
    """Calls ``on_change`` when the ignore file itself is created/modified/moved.

    A :class:`PatternMatchingEventHandler` matching ``*.txt``/``*.md`` never sees
    the ignore file, so it gets a dedicated handler that fires only for that one
    path — letting the watcher reload its rules without a restart.
    """

    def __init__(self, ignore_file: Path, on_change: Callable[[], None]) -> None:
        self._ignore_file = Path(ignore_file).resolve()
        self._on_change = on_change

    def on_created(self, event: FileSystemEvent) -> None:
        self._maybe_fire(event.src_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        self._maybe_fire(event.src_path)

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        # Atomic saves (write temp file, then rename into place) surface here.
        self._maybe_fire(event.dest_path)

    def _maybe_fire(self, raw_path: str | bytes) -> None:
        path = raw_path.decode() if isinstance(raw_path, bytes) else raw_path
        if Path(path).resolve() == self._ignore_file:
            self._on_change()


def maybe_remove_ingested(path: Path, written: int, *, enabled: bool) -> None:
    """Delete ``path`` after a successful ingest when ``WATCH_REMOVE`` is on.

    Only removes when ``written >= 1``; a file that stored nothing is kept and a
    warning logged. A failed unlink is logged and swallowed so the watcher
    survives permission/missing-file errors.
    """
    if not enabled:
        return
    if written < 1:
        logger.warning("Kept %s: nothing was stored (0 chunk(s))", path)
        return
    try:
        path.unlink()
        logger.info("Deleted %s after ingesting %d chunk(s)", path, written)
    except OSError:
        logger.exception("Failed to delete %s", path)


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
            maybe_remove_ingested(path, written, enabled=settings.watch_remove)
        except Exception:  # noqa: BLE001 - keep the watcher alive on any file error
            logger.exception("Failed to ingest %s", path)

    return action


def _reload_ignore(matcher: IgnoreMatcher, settings: Settings) -> None:  # pragma: no cover
    """Re-read the ignore file into ``matcher`` and log it."""
    matcher.reload()
    logger.info("Reloaded ignore rules from %s", settings.ignore_file)


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

    # Shared between the ingest handler and the live reload below.
    matcher = build_ignore_matcher(settings)

    if settings.scan_on_start:
        logger.info("Scanning existing files under %s", folder)
        initial_scan(folder, settings.patterns, action, matcher)

    debouncer = Debouncer(settings.debounce_seconds, action)
    handler = IngestEventHandler(settings.patterns, debouncer, matcher)

    # Reload the ignore rules live when the file changes, debounced like ingests.
    reload_debouncer = Debouncer(
        settings.debounce_seconds, lambda _p: _reload_ignore(matcher, settings)
    )
    ignore_handler = IgnoreFileEventHandler(
        settings.ignore_file, lambda: reload_debouncer.trigger(settings.ignore_file)
    )

    # Native FS events (inotify/FSEvents) are not delivered across bind mounts
    # on Docker Desktop; polling reliably picks up changes there.
    observer = PollingObserver() if settings.use_polling else Observer()
    main_watch = observer.schedule(handler, str(folder), recursive=True)
    # The ignore file usually lives inside the watch folder — reuse that watch;
    # a custom WATCH_IGNORE elsewhere needs its own (non-recursive) one.
    if settings.ignore_file.parent.resolve() == folder.resolve():
        observer.add_handler_for_watch(ignore_handler, main_watch)
    else:
        observer.schedule(ignore_handler, str(settings.ignore_file.parent), recursive=False)
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
        reload_debouncer.cancel_all()
        observer.join()
