---
id: TASK-4
title: >-
  Store Qdrant data in a gitignored local folder instead of a named Docker
  volume
status: To Do
assignee: []
created_date: '2026-07-23 15:05'
labels: []
dependencies:
  - TASK-1
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Change the qdrant service in `docker-compose.yml` to persist storage in a local bind-mounted folder (for example `./qdrant_storage`) instead of the named `qdrant_storage` Docker volume, and ensure that folder is not committed. This makes the vector data visible and manageable on the host. Note: edits `docker-compose.yml`, which is shared with the containerization work.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The qdrant service bind-mounts a local folder (for example `./qdrant_storage`) to `/qdrant/storage` and no longer declares the named `qdrant_storage` volume
- [ ] #2 The local storage folder is ignored by git via `.gitignore`, with the folder kept in the repo through a placeholder if needed
- [ ] #3 After `docker compose up`, Qdrant data is written under the local folder and persists across `docker compose down` and restart
<!-- AC:END -->
