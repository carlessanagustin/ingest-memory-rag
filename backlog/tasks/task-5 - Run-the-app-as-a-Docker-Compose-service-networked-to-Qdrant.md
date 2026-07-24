---
id: TASK-5
title: Run the app as a Docker Compose service networked to Qdrant
status: Done
assignee:
  - '@claude'
created_date: '2026-07-23 15:06'
updated_date: '2026-07-24 07:30'
labels: []
dependencies:
  - TASK-1
  - TASK-3
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add the containerized app to `docker-compose.yml` so `docker compose up` starts both Qdrant and the ingestion app together. The app reaches Qdrant over the compose network and watches a host folder mounted into the container. Include any refactoring needed for reliable file-change detection inside a container.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 docker-compose.yml defines an `app` service built from the `Dockerfile` that depends on the `qdrant` service
- [x] #2 The app connects to Qdrant via compose networking using `QDRANT_URL=http://qdrant:6333`, set through the environment with no code change required
- [x] #3 The host `./raw` folder is mounted into the app container so files added or updated on the host are ingested
- [x] #4 File create and update events are reliably detected inside the container for the mounted folder, including on Docker Desktop where native inotify/FSEvents may not cross the bind mount (for example via a polling observer selectable by environment variable)
- [x] #5 `docker compose up` brings up the full stack and the app starts watching once Qdrant is ready
- [x] #6 The README documents running the full stack in Docker
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Code (containerization refactor): add WATCH_USE_POLLING env -> config.use_polling; in watcher.run() use watchdog PollingObserver when set (bind-mounted host dirs on Docker Desktop do not deliver native inotify/FSEvents). Keep default Observer for local use.
2. docker-compose.yml: add an app service built from the Dockerfile, depends_on qdrant (service_healthy if the qdrant image supports a healthcheck, else service_started + app-side retry), environment QDRANT_URL=http://qdrant:6333 and WATCH_USE_POLLING=true, and bind-mount ./raw -> /app/raw.
3. Qdrant healthcheck: add one if the image has curl/wget/bash TCP; else fall back to app connection retry so the app waits for Qdrant to be ready.
4. README: document running the full stack with docker compose.
5. Verify: docker compose up -d, drop/edit a file in ./raw, confirm it is ingested into Qdrant (count/logs); ruff+mypy+unit locally.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Verified full stack with docker compose (Docker 29.6.2, macOS host): compose up brought qdrant to Healthy (bash /dev/tcp healthcheck) then started the app (depends_on condition service_healthy). App connected over the compose network via QDRANT_URL=http://qdrant:6333 (no code change). A .md file created on the HOST in ./raw was detected across the bind mount by the PollingObserver (WATCH_USE_POLLING=true) and ingested: 'Ingested /app/raw/compose-e2e.md -> 1 chunk(s)'; Qdrant points_count=1. Code change: added config.use_polling (WATCH_USE_POLLING env) and PollingObserver selection in watcher.run(). ruff+mypy clean, 16 unit tests pass (added use_polling assertions).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added an app service to docker-compose.yml (built from the Dockerfile; depends_on qdrant with a bash /dev/tcp healthcheck gated on condition: service_healthy; QDRANT_URL=http://qdrant:6333 over the compose network; ./raw bind-mounted to /app/raw; WATCH_USE_POLLING=true). Added an env-selectable PollingObserver (config.use_polling / WATCH_USE_POLLING) so bind-mounted host changes are detected on Docker Desktop where native FS events are not delivered. Documented the Docker full-stack workflow in the README. Verified end-to-end: compose up -> qdrant healthy -> app watches; a host-side .md file was ingested and appeared in Qdrant (points_count=1).
<!-- SECTION:FINAL_SUMMARY:END -->
