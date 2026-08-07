---
id: TASK-99
title: Wire the interpolated env include and centralize deploy.resources
status: Done
assignee:
  - '@claude'
created_date: '2026-08-07 12:42'
updated_date: '2026-08-07 12:55'
labels:
  - docker
  - compose
  - infra
dependencies:
  - TASK-98
ordinal: 101000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Make the tier selection live. Add an interpolated include entry to docker-compose.yml (verbose form, matching the existing style): a path of `compose/env/${DEPLOY_ENV:-medium}.yaml` with `project_directory: .`. Then REMOVE the now-duplicated `deploy.resources` blocks from the four base service files (compose/app.yaml, compose/qdrant.yaml which holds both qdrant and mcp-qdrant, compose/ollama.yaml, compose/opencode.yaml) so the env tier files are the single source of truth for resources. This is what prevents a conflicting cross-include merge and was verified to resolve cleanly with `docker compose config`. Everything else in the base files (image, build, ports, environment, volumes, healthcheck, restart, and the Ollama GPU guidance comment) stays untouched. Recommended subagent: sherpa:docky.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 docker-compose.yml has an include entry for compose/env/${DEPLOY_ENV:-medium}.yaml using the verbose path/project_directory form
- [x] #2 No `deploy.resources` block remains in compose/app.yaml, compose/qdrant.yaml, compose/ollama.yaml, or compose/opencode.yaml
- [x] #3 With DEPLOY_ENV unset, `docker compose config` succeeds and resolves resources equal to the medium tier (i.e. the previous behaviour) for all five services
- [x] #4 `DEPLOY_ENV=small docker compose config` resolves the small numbers and `DEPLOY_ENV=large docker compose config` resolves the large numbers, for all five services
- [x] #5 All non-resource service config (image/build, ports, environment, volumes, healthcheck, restart, GPU comment) is byte-for-byte unchanged from before
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. docker-compose.yml: add a verbose include entry `compose/env/${DEPLOY_ENV:-medium}.yaml` (project_directory: .) after the opencode include, with an explanatory comment.
2. Remove the deploy.resources block from each base file so env tiers are the single source: compose/app.yaml (app), compose/qdrant.yaml (qdrant + mcp-qdrant), compose/ollama.yaml (ollama, incl. the now-relocated GPU comment), compose/opencode.yaml (opencode).
3. Keep all other keys (image/build, ports, environment, volumes, healthcheck, restart) untouched.
4. Verify at repo root: `docker compose config` (unset->medium), and DEPLOY_ENV=small/large resolve the right numbers for all 5 services; confirm no deploy.resources remains in the base files.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added `- path: compose/env/${DEPLOY_ENV:-medium}.yaml` (project_directory: .) to docker-compose.yml and removed all five deploy.resources blocks from the base files. Verified at repo root with `docker compose config --format json`: DEPLOY_ENV unset (reads .env) resolves medium == current byte-for-byte; DEPLOY_ENV=small and =large resolve the intended numbers for app/qdrant/mcp-qdrant/ollama/opencode. `git diff` of the four base files shows only deletions of the deploy blocks (48 lines, 0 additions; Ollama GPU comment relocated to the env files in TASK-98), so image/build, ports, environment, volumes, healthcheck, and restart are untouched. grep confirms no deploy:/resources: remain in the base files.

Post-verification defect + fix: the broad `env/` virtualenv rule in .gitignore also matched compose/env/, so the tier files would NOT have been committed — which would break the include (compose/env/${DEPLOY_ENV}.yaml) on any fresh clone / other VPS, defeating the feature. Fixed by adding `!compose/env/` and `!compose/env/**` exceptions (kept the virtualenv rule intact). Verified: `git check-ignore` now reports the three tier files as trackable, a top-level env/ virtualenv is still ignored, and `git status` lists compose/env/ as untracked.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Wired per-environment sizing: docker-compose.yml now interpolates compose/env/${DEPLOY_ENV:-medium}.yaml, and the deploy.resources blocks were removed from the four base service files so the env tiers are the single source of truth. Verified via `docker compose config` that unset->medium (== prior behaviour, byte-for-byte), small, and large each resolve the correct limits/reservations for all five services, and via `git diff` that only the deploy blocks changed.
<!-- SECTION:FINAL_SUMMARY:END -->
