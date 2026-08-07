---
id: TASK-104
title: Move compose/env to environments and rewire all code/config references
status: Done
assignee:
  - '@claude'
created_date: '2026-08-07 13:33'
updated_date: '2026-08-07 13:35'
labels:
  - docker
  - compose
  - infra
dependencies: []
ordinal: 106000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Relocate the per-environment resource-sizing profiles from ./compose/env to ./environments (repo root), preserving history with `git mv`, and update every non-documentation reference so the stack keeps working in one consistent change. In scope: move compose/env/{small,medium,large}.env to environments/; update the Makefile (the COMPOSE variable `--env-file compose/env/$(DEPLOY_ENV).env` and the explanatory comment) to point at environments/; update the four inline `# … see compose/env/*.env` comments in compose/app.yaml, compose/qdrant.yaml (two), compose/ollama.yaml, compose/opencode.yaml; update the header comments inside the moved *.env files that reference their own old path; and remove the now-obsolete .gitignore exceptions (`!compose/env/` and `!compose/env/**`) — they existed only because the broad `env/` virtualenv rule matched compose/env, and `environments/` is not matched by any ignore rule. Do NOT edit historical backlog task files. Recommended subagent: sherpa:docky.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The three files now live at environments/small.env, environments/medium.env, environments/large.env (moved via git mv so history is preserved); the compose/env/ directory no longer exists
- [x] #2 The Makefile COMPOSE variable loads environments/$(DEPLOY_ENV).env (not compose/env/…), and its explanatory comment matches
- [x] #3 The four inline resource comments in compose/app.yaml, compose/qdrant.yaml, compose/ollama.yaml, compose/opencode.yaml reference environments/*.env; the moved *.env header comments reference their new environments/<tier>.env path
- [x] #4 The obsolete .gitignore exceptions for compose/env are removed, and `git check-ignore` confirms environments/*.env are trackable without any exception
- [x] #5 `docker compose config` succeeds and `make -n up` emits `docker compose --env-file environments/medium.env --env-file .env up --build -d`
- [x] #6 No historical backlog task markdown files were modified
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. git mv compose/env/{small,medium,large}.env -> environments/; remove the now-empty compose/env/ dir.
2. Makefile: point COMPOSE var + comment at environments/$(DEPLOY_ENV).env.
3. compose/*.yaml: update the 4 inline "see compose/env/*.env" comments -> environments/*.env (app, qdrant x2, ollama, opencode).
4. Moved *.env header comments: update self-referential compose/env/<tier>.env -> environments/<tier>.env.
5. .gitignore: remove the obsolete !compose/env/ + !compose/env/** exceptions (and their comment).
6. Verify: git check-ignore shows environments/*.env trackable; docker compose config OK; make -n up shows environments/medium.env; compose/env gone; no historical backlog files touched.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Moved the three tier files to environments/ (they were untracked new files, so the move is a plain rename). Updated Makefile (COMPOSE var + comment) to environments/$(DEPLOY_ENV).env; updated the four inline comments in compose/app.yaml, compose/qdrant.yaml (x2), compose/ollama.yaml, compose/opencode.yaml to environments/*.env; updated the three moved *.env header comments to the new path AND fixed their stale --env-file order to match the Makefile (tier first, .env last). Removed the obsolete .gitignore !compose/env exceptions (+comment). Verified: git check-ignore reports environments/{small,medium,large}.env as trackable with no exception; compose/env/ is gone; `docker compose config` succeeds (ollama still commented in the include); `make -n up` emits `docker compose --env-file environments/medium.env --env-file .env up --build -d`; grep finds no compose/env in compose/ or environments/; no backlog task markdown was modified.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Relocated compose/env/{small,medium,large}.env to environments/ and rewired every code/config reference: Makefile COMPOSE var+comment, the four compose/*.yaml inline comments, the moved .env header comments (path + corrected --env-file order), and removed the now-dead .gitignore exceptions (environments/ needs none). Verified via git check-ignore, `docker compose config`, `make -n up`, and grep; historical backlog files untouched.
<!-- SECTION:FINAL_SUMMARY:END -->
