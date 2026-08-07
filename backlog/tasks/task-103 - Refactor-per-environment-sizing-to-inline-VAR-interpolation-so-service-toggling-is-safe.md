---
id: TASK-103
title: >-
  Refactor per-environment sizing to inline ${VAR} interpolation so service
  toggling is safe
status: Done
assignee:
  - '@claude'
created_date: '2026-08-07 13:21'
updated_date: '2026-08-07 13:28'
labels:
  - docker
  - compose
  - infra
dependencies: []
ordinal: 105000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The tier-file approach (TASK-98/99) defines each service in a separate compose fragment (compose/env/<tier>.yaml) carrying only deploy.resources. When a service is toggled off by commenting its base include (e.g. ollama for a VPS that does not run a local model server), the tier fragment still introduces that service with no image/build, so Compose fails: "service \"ollama\" has neither an image nor a build context specified". Refactor so a service and its resource sizing travel together: put deploy.resources back INLINE in each base service file using ${VAR:-default} interpolation (medium values as the inline defaults), replace the compose/env/<tier>.yaml fragments with dotenv value files compose/env/<tier>.env (per-service CPU/memory variables), and select the tier by loading .env + the chosen tier file via `docker compose --env-file` from the Makefile targets. DEPLOY_ENV (from .env, default medium) picks the tier. Commenting a service include then removes both the service and its interpolated resources with no orphan. Supersedes the fragment mechanism; keeps small/medium/large and the .gitignore exception. Recommended subagent: sherpa:docky.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 deploy.resources is defined inline in every base service file (app, qdrant, mcp-qdrant, ollama, opencode) using ${VAR:-default} interpolation, with the medium values as the inline defaults
- [x] #2 The compose/env/${DEPLOY_ENV}.yaml fragment include is removed from docker-compose.yml and the old compose/env/{small,medium,large}.yaml fragments are deleted
- [x] #3 compose/env/{small,medium,large}.env dotenv value files exist (per-service CPU/memory vars) and are tracked by git (gitignore exception retained); they contain no secrets
- [x] #4 make up/down/build/logs/reset/reset-hard invoke Compose with `--env-file .env --env-file compose/env/$(DEPLOY_ENV).env`, DEPLOY_ENV read from .env (default medium), overridable via `make <t> DEPLOY_ENV=<tier>`
- [x] #5 With ollama commented out of the include list, `docker compose config` succeeds (no orphaned-service error) — the original bug is fixed
- [x] #6 With all base services enabled, each tier (small/medium/large) resolves the intended limits+reservations for all five services via the tier .env file, and the inline defaults (no tier file) equal medium
- [x] #7 An invalid DEPLOY_ENV fails fast (missing compose/env/<tier>.env)
- [x] #8 README updated to describe the inline + --env-file mechanism; Ollama GPU reservation comment restored in compose/ollama.yaml; .env/.env.example DEPLOY_ENV comment updated
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Base files: add inline deploy.resources with ${VAR:-default} interpolation (medium defaults) to app.yaml, qdrant.yaml (qdrant + mcp-qdrant), ollama.yaml (restore GPU comment), opencode.yaml. Vars: <SVC>_{CPU_LIMIT,MEM_LIMIT,CPU_RES,MEM_RES}.
2. docker-compose.yml: remove the compose/env/${DEPLOY_ENV}.yaml fragment include (leave the user-commented ollama include as-is).
3. Delete compose/env/*.yaml fragments; create compose/env/{small,medium,large}.env dotenv value files (20 vars each; medium == defaults).
4. Makefile: add DEPLOY_ENV (from .env, default medium) + COMPOSE := docker compose [--env-file .env] --env-file compose/env/$(DEPLOY_ENV).env; route build/up/down/logs/reset/reset-hard through $(COMPOSE).
5. Update .env/.env.example DEPLOY_ENV comment; keep .gitignore !compose/env exceptions.
6. Update README Per-environment resource sizing section to the inline + --env-file mechanism and note toggling is now safe.
7. Verify: real config (ollama off) succeeds; scratch harness with all base files proves each tier resolves per-service numbers and defaults==medium; --env-file layering (.env then tier) confirmed; invalid tier fails fast; `make -n up` shows correct command; git tracks the .env tier files.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented the inline refactor. deploy.resources is now inline in each base file (app/qdrant/mcp-qdrant/ollama/opencode) via ${VAR:-default} with medium defaults; the compose/env/${DEPLOY_ENV}.yaml fragment include was removed and the .yaml fragments replaced by compose/env/{small,medium,large}.env dotenv files (tracked; no secrets). Makefile: DEPLOY_ENV read from .env (default medium, overridable via `make <t> DEPLOY_ENV=<tier>`), COMPOSE := docker compose --env-file compose/env/$(DEPLOY_ENV).env [--env-file .env].

NOTE on ordering: I load the tier file FIRST and .env LAST (opposite of the AC text) because `docker compose --env-file` gives the LAST file precedence. This makes the tier the base and lets .env override a single value ad hoc — the intended and documented behaviour.

Verified with `docker compose config --format json` (no containers started):
(a) real repo with ollama commented out now configs cleanly with no orphan — the reported bug;
(b) inline defaults == medium byte-for-byte;
(c) small/medium/large each resolve the intended limits+reservations for all five services via the tier .env;
(d) .env (last) overrides a single tier value (OLLAMA_MEM_LIMIT=32G beats small 8G), and a .env with no resource vars leaves the tier intact;
(e) invalid DEPLOY_ENV fails fast (couldn't find env file .../bogus.env, exit 1);
(f) `make -n up` emits: docker compose --env-file compose/env/medium.env --env-file .env up --build -d, and DEPLOY_ENV=large override works.

GPU reservation comment restored in compose/ollama.yaml. .env/.env.example had their DEPLOY_ENV comments trimmed by the user; the bare DEPLOY_ENV=medium is consistent with the make-driven mechanism and no stale include-path comment remains. README section rewritten for the inline + --env-file mechanism (toggling a service now removes it and its limits together).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Refactored per-environment sizing from separate tier-file includes to inline ${VAR:-default} interpolation in each base service file, with tiers as compose/env/{small,medium,large}.env dotenv files selected by DEPLOY_ENV and loaded by the Makefile via --env-file (tier first, .env last so .env can override). Fixes the orphaned-service error when a service include is commented out (the size now travels with the service), while preserving named tiers, byte-for-byte medium defaults, and per-service ad-hoc overrides. Verified end-to-end with `docker compose config` (bug fixed, all tiers correct, defaults==medium, override + fail-fast semantics) and `make -n` dry-runs. Supersedes the fragment mechanism from TASK-98/99.
<!-- SECTION:FINAL_SUMMARY:END -->
