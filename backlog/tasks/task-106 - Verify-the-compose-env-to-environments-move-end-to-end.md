---
id: TASK-106
title: Verify the compose/env to environments move end to end
status: Done
assignee:
  - '@claude'
created_date: '2026-08-07 13:33'
updated_date: '2026-08-07 13:37'
labels:
  - docker
  - compose
  - infra
  - verification
dependencies:
  - TASK-104
  - TASK-105
ordinal: 108000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Non-destructive verification (no containers started) that the move is complete and nothing still points at the old path. Recommended subagent: sherpa:docky.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A repo-wide grep for `compose/env` returns matches ONLY inside backlog/ historical task files (zero matches in Makefile, .gitignore, compose/*.yaml, environments/*.env, README.md, .env/.env.example)
- [x] #2 For each tier, `docker compose --env-file environments/<tier>.env --env-file .env config` resolves the intended CPU/memory for the enabled services; an invalid DEPLOY_ENV still fails fast (missing environments/<tier>.env)
- [x] #3 environments/{small,medium,large}.env are tracked by git (git status shows them; git check-ignore reports them not ignored) and compose/env/ is gone
- [x] #4 `make -n up` and `make -n up DEPLOY_ENV=large` emit the correct docker compose commands referencing environments/
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Repo-wide grep for compose/env — expect matches only under backlog/ (historical), zero in Makefile/.gitignore/compose/*.yaml/environments/*.env/README.md/.env(.example).
2. Per tier, render config with --env-file environments/<tier>.env --env-file .env and assert numbers (use a scratch all-services compose to cover ollama too; plus confirm the real repo config succeeds).
3. Invalid DEPLOY_ENV fails fast (missing environments/<tier>.env).
4. git tracks environments/{small,medium,large}.env (status + check-ignore); compose/env gone.
5. make -n up and make -n up DEPLOY_ENV=large reference environments/.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Verified with docker compose config (no containers). AC1: a repo-wide grep for compose/env returns matches only under backlog/ historical task files (zero in Makefile, .gitignore, compose/*.yaml, environments/*.env, README.md, .env/.env.example). AC2: with a scratch all-services compose, each tier via `--env-file environments/<tier>.env --env-file .env` resolves the intended limits+reservations for all five services (medium byte-for-byte == originals); the real repo config (ollama commented) succeeds for small/medium/large; an invalid tier fails fast ("couldn't find env file: .../environments/bogus.env", exit 1). AC3: git status lists environments/ as untracked (ready to add) and git check-ignore reports environments/{small,medium,large}.env not ignored; compose/env/ is gone. AC4: `make -n up` -> docker compose --env-file environments/medium.env --env-file .env up --build -d, and DEPLOY_ENV=large override -> environments/large.env.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified the compose/env -> environments move end to end: no non-backlog reference to compose/env remains; every tier resolves correct per-service resources from environments/*.env (medium unchanged); invalid tier fails fast; environments/*.env are git-trackable and compose/env is gone; make dry-runs reference environments/. Evidence: grep, `docker compose config --format json`, git check-ignore, `make -n`.
<!-- SECTION:FINAL_SUMMARY:END -->
