---
id: TASK-41
title: Verify the opencode service end to end
status: Done
assignee: []
created_date: '2026-07-30 10:27'
updated_date: '2026-07-30 10:43'
labels:
  - docker
  - opencode
  - verification
dependencies:
  - TASK-36
  - TASK-38
  - TASK-39
type: chore
ordinal: 43000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Bring up the stack and confirm the opencode service builds, runs, is reachable on port 4096, is healthy, and can use the local Ollama model. Preserve data: do not use docker compose down -v and do not wipe storage folders.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 docker compose up --build builds the opencode image (ubuntu:26.04) and the service reports healthy
- [x] #2 http://localhost:4096 serves the opencode web UI from the host
- [x] #3 opencode can list/select the Ollama model (qwen3.5:9b) and complete a simple prompt
- [x] #4 storage_opencode persists config across a restart (auth/session survives docker compose restart opencode)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
End-to-end on the running stack (ollama + opencode): image built (exit 0, ~441MB, opencode 1.18.9); container healthy; curl http://localhost:4096 -> HTTP 200 serving the OpenCode web UI; qwen3.5:9b pulled via ollama-pull; opencode models lists ollama/qwen3.5:9b; opencode run --model ollama/qwen3.5:9b returned "pong"; after docker compose restart opencode the container returned to healthy, storage_opencode/opencode.db persisted (survived with data, 249856 -> 262144 bytes), and http://localhost:4096 still returned 200. No down -v or storage wipe used.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified the opencode service end to end: builds, healthy, reachable on host 4096, chats via the Ollama model (pong), and data persists across restart.
<!-- SECTION:FINAL_SUMMARY:END -->
