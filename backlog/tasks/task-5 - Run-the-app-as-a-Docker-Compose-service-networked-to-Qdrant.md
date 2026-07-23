---
id: TASK-5
title: Run the app as a Docker Compose service networked to Qdrant
status: To Do
assignee: []
created_date: '2026-07-23 15:06'
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
- [ ] #1 docker-compose.yml defines an `app` service built from the `Dockerfile` that depends on the `qdrant` service
- [ ] #2 The app connects to Qdrant via compose networking using `QDRANT_URL=http://qdrant:6333`, set through the environment with no code change required
- [ ] #3 The host `./raw` folder is mounted into the app container so files added or updated on the host are ingested
- [ ] #4 File create and update events are reliably detected inside the container for the mounted folder, including on Docker Desktop where native inotify/FSEvents may not cross the bind mount (for example via a polling observer selectable by environment variable)
- [ ] #5 `docker compose up` brings up the full stack and the app starts watching once Qdrant is ready
- [ ] #6 The README documents running the full stack in Docker
<!-- AC:END -->
