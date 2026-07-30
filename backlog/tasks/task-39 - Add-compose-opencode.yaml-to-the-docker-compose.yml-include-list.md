---
id: TASK-39
title: Add compose/opencode.yaml to the docker-compose.yml include list
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 10:27'
updated_date: '2026-07-30 10:39'
labels:
  - docker
  - opencode
dependencies:
  - TASK-36
type: chore
ordinal: 41000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Aggregate the new opencode service into the top-level stack so docker compose up starts it alongside the other services, using the same include long-syntax with project_directory: . as the sibling compose files.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 docker-compose.yml include lists compose/opencode.yaml with project_directory: .
- [x] #2 docker compose config shows the opencode service and the existing services are unchanged
- [x] #3 Any commented-out entries (for example openwebui) remain as-is
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add compose/opencode.yaml to docker-compose.yml include with project_directory: . 2. Keep openwebui commented. 3. Validate docker compose config lists opencode.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
docker-compose.yml include lists compose/opencode.yaml with project_directory: . ; docker compose config shows the opencode service; the openwebui entry stays commented; other services unchanged.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added compose/opencode.yaml to the docker-compose.yml include list. Verified with docker compose config (opencode present; openwebui still commented).
<!-- SECTION:FINAL_SUMMARY:END -->
