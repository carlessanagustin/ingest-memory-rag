"""Console entry point: ``python -m ingest_memory_rag`` / ``ingest-memory-rag``."""

from __future__ import annotations

import logging

from ingest_memory_rag.config import Settings
from ingest_memory_rag.watcher import run


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    settings = Settings.from_env()
    run(settings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
