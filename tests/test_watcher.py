import logging
import threading
from pathlib import Path

import pathspec
from watchdog.events import FileCreatedEvent, FileModifiedEvent, FileMovedEvent

from ingest_memory_rag.config import PATTERNS, Settings
from ingest_memory_rag.watcher import (
    Debouncer,
    IgnoreFileEventHandler,
    IgnoreMatcher,
    IngestEventHandler,
    _build_spec,
    build_ignore_matcher,
    initial_scan,
    iter_matching_files,
    maybe_remove_ingested,
    should_ingest,
)


def _matcher(watch_folder: Path, lines: list[str]) -> IgnoreMatcher:
    return IgnoreMatcher(watch_folder, pathspec.GitIgnoreSpec.from_lines(lines))


def _settings(monkeypatch, tmp_path: Path, ignore: str | None = None) -> Settings:
    monkeypatch.setenv("WATCH_FOLDER", str(tmp_path))
    if ignore is None:
        monkeypatch.delenv("WATCH_IGNORE", raising=False)
    else:
        monkeypatch.setenv("WATCH_IGNORE", ignore)
    return Settings.from_env()


def test_should_ingest_matches_txt_and_md(tmp_path):
    txt = tmp_path / "a.txt"
    md = tmp_path / "b.md"
    other = tmp_path / "c.py"
    for f in (txt, md, other):
        f.write_text("x")

    assert should_ingest(txt, PATTERNS) is True
    assert should_ingest(md, PATTERNS) is True
    assert should_ingest(other, PATTERNS) is False


def test_should_ingest_ignores_directories(tmp_path):
    sub = tmp_path / "nested.txt"  # a directory that happens to match the glob
    sub.mkdir()
    assert should_ingest(sub, PATTERNS) is False


def test_iter_matching_files_finds_only_txt_and_md(tmp_path):
    (tmp_path / "keep1.txt").write_text("x")
    (tmp_path / "keep2.md").write_text("x")
    (tmp_path / "skip.log").write_text("x")
    nested = tmp_path / "sub"
    nested.mkdir()
    (nested / "keep3.md").write_text("x")

    found = {p.name for p in iter_matching_files(tmp_path, PATTERNS)}

    assert found == {"keep1.txt", "keep2.md", "keep3.md"}


def test_debouncer_coalesces_rapid_triggers():
    calls: list[Path] = []
    done = threading.Event()

    def action(path: Path) -> None:
        calls.append(path)
        done.set()

    debouncer = Debouncer(delay=0.05, action=action)
    target = Path("/tmp/file.txt")
    for _ in range(5):
        debouncer.trigger(target)  # burst faster than the delay

    assert done.wait(timeout=2.0), "debounced action never fired"
    # A tiny grace period to catch any erroneous extra firings.
    done.clear()
    assert done.wait(timeout=0.2) is False
    assert calls == [target]


def test_debouncer_fires_per_distinct_path():
    fired: list[Path] = []
    lock = threading.Lock()
    both = threading.Event()

    def action(path: Path) -> None:
        with lock:
            fired.append(path)
            if len(fired) == 2:
                both.set()

    debouncer = Debouncer(delay=0.05, action=action)
    debouncer.trigger(Path("/tmp/a.txt"))
    debouncer.trigger(Path("/tmp/b.md"))

    assert both.wait(timeout=2.0), "expected both paths to fire"
    assert set(fired) == {Path("/tmp/a.txt"), Path("/tmp/b.md")}


def test_debouncer_cancel_all_prevents_firing():
    fired: list[Path] = []
    done = threading.Event()

    def action(path: Path) -> None:
        fired.append(path)
        done.set()

    debouncer = Debouncer(delay=0.1, action=action)
    debouncer.trigger(Path("/tmp/x.txt"))
    debouncer.cancel_all()

    assert done.wait(timeout=0.3) is False
    assert fired == []


class _RecordingDebouncer:
    def __init__(self) -> None:
        self.triggered: list[Path] = []

    def trigger(self, path: Path) -> None:
        self.triggered.append(path)


def test_handler_schedules_created_modified_and_moved():
    recorder = _RecordingDebouncer()
    handler = IngestEventHandler(PATTERNS, recorder)  # type: ignore[arg-type]

    handler.on_created(FileCreatedEvent("/tmp/new.txt"))
    handler.on_modified(FileModifiedEvent("/tmp/changed.md"))
    handler.on_moved(FileMovedEvent("/tmp/.tmp-abc", "/tmp/saved.md"))

    assert recorder.triggered == [
        Path("/tmp/new.txt"),
        Path("/tmp/changed.md"),
        Path("/tmp/saved.md"),  # move uses the destination path
    ]


def test_handler_decodes_bytes_paths():
    recorder = _RecordingDebouncer()
    handler = IngestEventHandler(PATTERNS, recorder)  # type: ignore[arg-type]

    handler.on_created(FileCreatedEvent(b"/tmp/bytes.txt"))

    assert recorder.triggered == [Path("/tmp/bytes.txt")]


def test_initial_scan_invokes_action_per_matching_file(tmp_path):
    (tmp_path / "one.txt").write_text("x")
    (tmp_path / "two.md").write_text("x")
    (tmp_path / "skip.log").write_text("x")
    seen: list[Path] = []

    count = initial_scan(tmp_path, PATTERNS, seen.append)

    assert count == 2
    assert {p.name for p in seen} == {"one.txt", "two.md"}


# --- Recursive ingestion regression (TASK-59) -------------------------------


def test_initial_scan_discovers_deeply_nested_file(tmp_path):
    nested = tmp_path / "a" / "b" / "c"
    nested.mkdir(parents=True)
    (nested / "deep.md").write_text("x")
    (tmp_path / "top.txt").write_text("x")
    seen: list[Path] = []

    count = initial_scan(tmp_path, PATTERNS, seen.append)

    assert count == 2
    assert {p.name for p in seen} == {"deep.md", "top.txt"}
    assert any(p.parent == nested for p in seen), "nested file was not discovered"


# --- .watchignore matcher (TASK-61) ----------------------------------------


def test_ignore_matcher_applies_gitignore_rules(tmp_path):
    matcher = _matcher(
        tmp_path,
        [
            "# a comment line — ignored by the parser",
            "notes-private.md",
            "drafts/",
            "**/scratch.txt",
            "report-*.md",
            "!report-keep.md",  # negation re-includes a file the glob would ignore
        ],
    )

    assert matcher.is_ignored(tmp_path / "notes-private.md") is True
    assert matcher.is_ignored(tmp_path / "drafts" / "wip.md") is True
    assert matcher.is_ignored(tmp_path / "sub" / "scratch.txt") is True
    assert matcher.is_ignored(tmp_path / "report-secret.md") is True
    assert matcher.is_ignored(tmp_path / "report-keep.md") is False
    assert matcher.is_ignored(tmp_path / "keep.md") is False
    assert matcher.is_ignored(tmp_path / "notes-public.md") is False


def test_ignore_matcher_ignores_paths_outside_watch_folder(tmp_path):
    matcher = _matcher(tmp_path, ["*.md"])
    outside = tmp_path.parent / "elsewhere" / "notes.md"

    assert matcher.is_ignored(outside) is False


def test_ignore_matcher_empty_spec_ignores_nothing(tmp_path):
    matcher = _matcher(tmp_path, [])

    assert matcher.is_ignored(tmp_path / "anything.md") is False


def test_build_ignore_matcher_reads_ignore_file(monkeypatch, tmp_path):
    (tmp_path / ".watchignore").write_text("notes-private.md\ndrafts/\n")
    settings = _settings(monkeypatch, tmp_path)

    matcher = build_ignore_matcher(settings)

    assert matcher.is_ignored(tmp_path / "notes-private.md") is True
    assert matcher.is_ignored(tmp_path / "drafts" / "wip.md") is True
    assert matcher.is_ignored(tmp_path / "keep.md") is False


def test_build_ignore_matcher_absent_file_ignores_nothing(monkeypatch, tmp_path):
    settings = _settings(monkeypatch, tmp_path)  # no .watchignore on disk

    matcher = build_ignore_matcher(settings)

    assert matcher.is_ignored(tmp_path / "notes-private.md") is False


def test_build_spec_falls_back_without_gitignorespec(monkeypatch, tmp_path):
    monkeypatch.delattr(pathspec, "GitIgnoreSpec", raising=False)

    spec = _build_spec(["notes-private.md"])
    matcher = IgnoreMatcher(tmp_path, spec)

    assert matcher.is_ignored(tmp_path / "notes-private.md") is True
    assert matcher.is_ignored(tmp_path / "keep.md") is False


# --- Live-reloadable ignore file (TASK-76 / TASK-77) -----------------------


def test_reload_picks_up_added_rule(monkeypatch, tmp_path):
    ignore = tmp_path / ".watchignore"
    ignore.write_text("")  # present but rule-less at build time
    matcher = build_ignore_matcher(_settings(monkeypatch, tmp_path))
    assert matcher.is_ignored(tmp_path / "notes-private.md") is False

    ignore.write_text("notes-private.md\n")
    matcher.reload()

    assert matcher.is_ignored(tmp_path / "notes-private.md") is True


def test_reload_drops_removed_rule(monkeypatch, tmp_path):
    ignore = tmp_path / ".watchignore"
    ignore.write_text("notes-private.md\n")
    matcher = build_ignore_matcher(_settings(monkeypatch, tmp_path))
    assert matcher.is_ignored(tmp_path / "notes-private.md") is True

    ignore.write_text("")  # rule removed
    matcher.reload()

    assert matcher.is_ignored(tmp_path / "notes-private.md") is False


def test_reload_absent_file_keeps_empty_spec(monkeypatch, tmp_path):
    matcher = build_ignore_matcher(_settings(monkeypatch, tmp_path))  # no file on disk

    matcher.reload()  # file still absent

    assert matcher.is_ignored(tmp_path / "notes-private.md") is False


def test_reload_without_configured_file_is_noop(tmp_path):
    matcher = _matcher(tmp_path, ["notes-private.md"])  # ignore_file defaults to None

    matcher.reload()  # nothing to re-read; keeps the compiled spec

    assert matcher.is_ignored(tmp_path / "notes-private.md") is True


def test_ignore_file_handler_fires_only_for_the_ignore_file(tmp_path):
    ignore = tmp_path / ".watchignore"
    calls: list[None] = []
    handler = IgnoreFileEventHandler(ignore, lambda: calls.append(None))

    handler.on_created(FileCreatedEvent(str(ignore)))
    handler.on_modified(FileModifiedEvent(str(ignore)))
    handler.on_moved(FileMovedEvent(str(tmp_path / ".tmp-abc"), str(ignore)))

    assert len(calls) == 3


def test_ignore_file_handler_ignores_other_paths(tmp_path):
    ignore = tmp_path / ".watchignore"
    calls: list[None] = []
    handler = IgnoreFileEventHandler(ignore, lambda: calls.append(None))

    handler.on_created(FileCreatedEvent(str(tmp_path / "notes.md")))
    handler.on_modified(FileModifiedEvent(str(tmp_path / "other.txt")))
    handler.on_moved(FileMovedEvent(str(tmp_path / "a"), str(tmp_path / "b")))

    assert calls == []


def test_iter_matching_files_skips_ignored(tmp_path):
    (tmp_path / "keep.md").write_text("x")
    (tmp_path / "notes-private.md").write_text("x")
    drafts = tmp_path / "drafts"
    drafts.mkdir()
    (drafts / "wip.md").write_text("x")
    matcher = _matcher(tmp_path, ["notes-private.md", "drafts/"])

    found = {p.name for p in iter_matching_files(tmp_path, PATTERNS, matcher)}

    assert found == {"keep.md"}


def test_handler_does_not_schedule_ignored_path(tmp_path):
    recorder = _RecordingDebouncer()
    matcher = _matcher(tmp_path, ["notes-private.md"])
    handler = IngestEventHandler(PATTERNS, recorder, matcher)  # type: ignore[arg-type]

    handler.on_created(FileCreatedEvent(str(tmp_path / "notes-private.md")))
    handler.on_created(FileCreatedEvent(str(tmp_path / "keep.md")))

    assert recorder.triggered == [tmp_path / "keep.md"]


# --- WATCH_REMOVE (delete source after successful ingest) -------------------


def test_maybe_remove_ingested_deletes_after_chunks(tmp_path, caplog):
    target = tmp_path / "done.txt"
    target.write_text("x")

    with caplog.at_level(logging.INFO, logger="ingest_memory_rag.watcher"):
        maybe_remove_ingested(target, 3, enabled=True)

    assert not target.exists()
    assert any(r.levelno == logging.INFO and "Deleted" in r.getMessage() for r in caplog.records)


def test_maybe_remove_ingested_keeps_file_on_zero_chunks(tmp_path, caplog):
    target = tmp_path / "empty.txt"
    target.write_text("x")

    with caplog.at_level(logging.WARNING, logger="ingest_memory_rag.watcher"):
        maybe_remove_ingested(target, 0, enabled=True)

    assert target.exists()
    assert any(r.levelno == logging.WARNING for r in caplog.records)


def test_maybe_remove_ingested_disabled_keeps_file(tmp_path):
    target = tmp_path / "keep.txt"
    target.write_text("x")

    maybe_remove_ingested(target, 5, enabled=False)

    assert target.exists()


def test_maybe_remove_ingested_swallows_delete_error(tmp_path, caplog):
    missing = tmp_path / "gone.txt"  # never created → unlink raises FileNotFoundError

    with caplog.at_level(logging.ERROR, logger="ingest_memory_rag.watcher"):
        maybe_remove_ingested(missing, 1, enabled=True)  # must not raise

    assert any(
        r.levelno == logging.ERROR and "Failed to delete" in r.getMessage() for r in caplog.records
    )
