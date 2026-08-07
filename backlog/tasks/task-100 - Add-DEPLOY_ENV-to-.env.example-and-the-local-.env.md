---
id: TASK-100
title: Add DEPLOY_ENV to .env.example and the local .env
status: Done
assignee:
  - '@claude'
created_date: '2026-08-07 12:42'
updated_date: '2026-08-07 12:50'
labels:
  - docker
  - compose
  - infra
dependencies:
  - TASK-99
ordinal: 102000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Expose and default the tier selector. Add `DEPLOY_ENV=medium` to .env.example with a comment that lists the allowed values (small|medium|large) and explains it selects the compose/env/<tier>.yaml resource profile that Docker Compose interpolates into its include path. Set `DEPLOY_ENV=medium` in the local .env as well (gitignored, holds real secrets — edit only, do not commit). Recommended subagent: sherpa:docky.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 .env.example contains a DEPLOY_ENV entry defaulting to medium, with a comment naming the allowed values small|medium|large and describing its effect
- [x] #2 The local .env contains DEPLOY_ENV=medium
- [x] #3 With no shell override present, `docker compose config` picks up the tier from the .env value (medium)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add a Deployment sizing section to .env.example with DEPLOY_ENV=medium and a comment naming allowed values (small|medium|large), default, and its effect on compose/env/${DEPLOY_ENV}.yaml.
2. Add DEPLOY_ENV=medium to the local .env (gitignored; edit only, do not commit).
3. Verify: `docker compose config` with no shell override resolves medium from .env; prove the .env mechanism is authoritative (not just the compose default) via a throwaway --env-file setting a different tier.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added a "Deployment sizing" section with DEPLOY_ENV=medium (comment: allowed small|medium|large, default medium, selects compose/env/${DEPLOY_ENV}.yaml) to .env.example, and DEPLOY_ENV=medium to the local .env. Verified: `docker compose config` with no shell override resolves medium from .env; a throwaway `--env-file` with DEPLOY_ENV=small resolved ollama to 4cpu/8G (small) rather than 6cpu/24G (medium), proving the env-file value drives the include-path interpolation, not merely the compose default.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Exposed the tier selector: DEPLOY_ENV=medium documented in .env.example (with allowed values and effect) and set in the local .env. Verified via `docker compose config` that .env drives the tier (medium by default; a --env-file override to small changed the resolved limits), confirming the .env-based selection works.
<!-- SECTION:FINAL_SUMMARY:END -->
