---
id: TASK-117
title: >-
  Make the app container's GID configurable via PGID so it can delete files in
  the bind-mounted ./raw folder
status: Done
assignee:
  - '@claude'
created_date: '2026-08-20 13:38'
updated_date: '2026-08-20 13:46'
labels: []
dependencies: []
type: bug
ordinal: 119000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
WATCH_REMOVE=true fails to delete ingested files: PermissionError: [Errno 13] Permission denied at watcher.py maybe_remove_ingested -> path.unlink(). Root cause: the app container runs as appuser, hardcoded uid=10001 gid=10001 in the Dockerfile. The host ./raw directory (bind-mounted in compose/app.yaml) is owned by the host user, typically mode drwxrwxr-x - owner and group have rwx, "other" only has r-x. From the containers point of view appuser is "other", so reads succeed (files are 0664) but unlink() fails because it needs write+execute on the *containing directory*, which appuser lacks as "other". This is a Docker bind-mount UID/GID mismatch, not a bug in the deletion logic itself (maybe_remove_ingested already correctly catches and logs OSError instead of crashing).

Fix: make the containers effective GID configurable via a new PGID env var (default 10001, matching current baked-in behavior, so nothing changes for anyone who does not set it), following the same ${VAR:-default} convention already used for WATCH_REMOVE/WATCH_USE_POLLING/etc. in compose/app.yaml. Keep the UID pinned at the existing appuser (10001) so HOME/passwd resolution (used for the sentence-transformers model cache under ~/.cache) is untouched - only the GID becomes configurable. Users then set PGID to the GID that already owns their host ./raw directory (typically their own primary group, via `id -g`); since a normal users directories are usually created owner:group rwxrwxr-x, the group already has write access, so matching the GID alone fixes deletion with no host filesystem permission changes and no Dockerfile/entrypoint changes needed.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 compose/app.yaml sets `user: "10001:${PGID:-10001}"` on the app service
- [x] #2 With PGID unset, the containers effective uid:gid is unchanged from before this fix (10001:10001)
- [x] #3 With PGID set in .env to the GID that owns the host ./raw directory, `docker compose exec app id` reports that GID as the containers effective group
- [x] #4 No changes are made to watcher.py or any other Python source - this is a compose-config-only fix
- [x] #5 `make check` (lint, format-check, typecheck, unit tests) passes unchanged
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add `user: "10001:${PGID:-10001}"` to the app service in compose/app.yaml, next to the environment/volumes keys. 2. Verify `docker compose config` renders the expected default (10001:10001) with PGID unset, and the override value when PGID is set. 3. Run `make check` to confirm no regressions (compose-only change, no source touched).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added `user: "10001:${PGID:-10001}"` to compose/app.yaml with a short comment. Verified via `docker compose config`: PGID unset -> user: 10001:10001 (unchanged); PGID=1001 -> user: 10001:1001. `make check` passes (ruff, ruff format --check, mypy, pytest, 100% coverage). No Python source touched.

Live-verified AC#3: `PGID=1001 docker compose run --rm --no-deps --entrypoint id app` -> "uid=10001(appuser) gid=1001 groups=1001". Cleaned up the one-off run container afterward.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added `user: "10001:${PGID:-10001}"` to the app service in compose/app.yaml. Verified statically (`docker compose config`, PGID unset -> 10001:10001, PGID=1001 -> 10001:1001) and live (`docker compose run --rm --no-deps --entrypoint id app` with PGID=1001 -> uid=10001(appuser) gid=1001 groups=1001). `make check` (ruff, ruff format --check, mypy, pytest w/ 100% coverage) passes unchanged; no Python source touched.
<!-- SECTION:FINAL_SUMMARY:END -->
