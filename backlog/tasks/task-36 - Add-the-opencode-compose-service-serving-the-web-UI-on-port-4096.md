---
id: TASK-36
title: Add the opencode compose service serving the web UI on port 4096
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 10:26'
updated_date: '2026-07-30 10:39'
labels:
  - docker
  - opencode
dependencies:
  - TASK-35
type: feature
ordinal: 38000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create compose/opencode.yaml defining an opencode service that builds from compose/opencode/Dockerfile and runs the opencode web server reachable from the host on port 4096. Because opencode web defaults to binding 127.0.0.1 on a random port, the command must bind explicitly to 0.0.0.0:4096. Follow the repo per-service conventions (container_name, restart, deploy limits, healthcheck). Persist the opencode data directory so auth and sessions survive restarts; mount the volume at the opencode data dir (for example /root/.local/share/opencode), NOT over /root/.opencode which holds the installed binary.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 compose/opencode.yaml defines a service named opencode that builds from compose/opencode/Dockerfile
- [x] #2 The command runs: opencode web --hostname 0.0.0.0 --port 4096 (using /root/.opencode/bin/opencode if opencode is not on PATH); the web UI is reachable at http://localhost:4096
- [x] #3 Publishes host port 4096:4096; sets container_name opencode and restart unless-stopped
- [x] #4 Includes a deploy.resources limits/reservations block consistent with the other services
- [x] #5 Has a healthcheck that confirms the server is listening on port 4096 (TCP probe)
- [x] #6 Declares depends_on ollama with condition service_healthy
- [x] #7 Persists opencode data to ./storage_opencode mounted at the opencode data dir without shadowing the binary at /root/.opencode/bin
- [x] #8 docker compose config validates with the service present
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. compose/opencode.yaml service opencode; build context compose/opencode, dockerfile Dockerfile. 2. command: opencode web --hostname 0.0.0.0 --port 4096. 3. ports 4096:4096; container_name opencode; restart unless-stopped. 4. deploy limits/reservations like siblings. 5. TCP healthcheck on 4096 (bash /dev/tcp). 6. depends_on ollama service_healthy. 7. Mount ./storage_opencode at the XDG data dir /root/.local/share/opencode (NOT over /root/.opencode). 8. Validate docker compose config.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
docker compose config validates. Brought the service up: container healthy (TCP 4096 healthcheck), curl http://localhost:4096 -> HTTP 200 serving the OpenCode web UI. command opencode web --hostname 0.0.0.0 --port 4096; ports 4096:4096; container_name opencode; restart unless-stopped; deploy limits present; depends_on ollama service_healthy (ollama went healthy first). storage_opencode mounted at /root/.local/share/opencode without shadowing the binary at /root/.opencode/bin (opencode runs), and now holds opencode.db/log/repos.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added compose/opencode.yaml serving opencode web on host 4096, wired to ollama, persisted at storage_opencode. Verified: compose config valid, container healthy, http://localhost:4096 returns HTTP 200 with the OpenCode UI.
<!-- SECTION:FINAL_SUMMARY:END -->
