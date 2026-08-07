---
id: TASK-102
title: Verify per-environment resource sizing end to end
status: Done
assignee:
  - '@claude'
created_date: '2026-08-07 12:42'
updated_date: '2026-08-07 12:53'
labels:
  - docker
  - compose
  - infra
  - verification
dependencies:
  - TASK-99
  - TASK-100
ordinal: 104000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Non-destructive verification that DEPLOY_ENV actually changes effective resource limits, with no container start required (use `docker compose config`). Confirm each tier resolves the intended numbers, the default is unchanged from before, and an unknown tier fails fast rather than silently falling back. Recommended subagent: sherpa:docky.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 For each of small, medium, large, `DEPLOY_ENV=<tier> docker compose config` shows the correct cpus/memory for both limits and reservations on all five services
- [x] #2 Default (DEPLOY_ENV unset) resolves to medium and matches the pre-change effective config — no behavioural regression
- [x] #3 An invalid value (e.g. DEPLOY_ENV=bogus) fails fast with a clear missing-file error, confirming there is no silent fallback
- [x] #4 The value set in .env is honoured by the normal `docker compose up` path (verified via `docker compose config`, without actually starting containers)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Resolve each tier (small/medium/large) via `DEPLOY_ENV=<t> docker compose config --format json` and assert cpus/memory for limits+reservations on all 5 services.
2. Prove no regression: create a temporary git worktree at HEAD (pre-change: inline deploy.resources), render its config, and diff the 5 core services deploy.resources against the new default — expect identical.
3. Assert invalid DEPLOY_ENV=bogus fails fast (non-zero, missing compose/env/bogus.yaml), i.e. no silent fallback.
4. Confirm the .env value (DEPLOY_ENV=medium) is honored by the plain `docker compose config` path.
5. Clean up the temp worktree.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
End-to-end verification via `docker compose config --format json` (no containers started). AC1: small/medium/large each resolve the intended cpus/memory for both limits and reservations across app/qdrant/mcp-qdrant/ollama/opencode. AC2: rendered a temporary git worktree at HEAD (pre-change, inline deploy.resources) and diffed all five services deploy.resources against the new default — MATCH on every field (no regression). AC3: `DEPLOY_ENV=bogus docker compose config` exits 1 with "open .../compose/env/bogus.yaml: no such file or directory" — fails fast, no silent fallback. AC4: with .env DEPLOY_ENV=medium, the plain `docker compose config` path resolves ollama to the medium limits. Temp worktree removed; `git worktree list` clean.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified per-environment sizing end to end with `docker compose config`: each tier resolves the intended limits/reservations for all five services; the default is byte-identical to the pre-change HEAD config (no regression, proven via a HEAD worktree diff); an unknown DEPLOY_ENV fails fast with a missing-file error; and the .env value is honored on the normal up path. No containers were started; the temp worktree was cleaned up.
<!-- SECTION:FINAL_SUMMARY:END -->
