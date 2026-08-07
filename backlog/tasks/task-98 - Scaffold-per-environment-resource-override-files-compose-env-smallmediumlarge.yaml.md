---
id: TASK-98
title: >-
  Scaffold per-environment resource override files
  (compose/env/{small,medium,large}.yaml)
status: Done
assignee:
  - '@claude'
created_date: '2026-08-07 12:41'
updated_date: '2026-08-07 12:46'
labels:
  - docker
  - compose
  - infra
dependencies: []
ordinal: 100000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Enable per-VPS resource sizing by creating three Compose override files, one per environment tier, that carry ONLY `deploy.resources`. Each file defines limits + reservations for all five services that currently have a resources block: `app`, `qdrant`, `mcp-qdrant`, `ollama`, `opencode`. `medium` reproduces the CURRENT hardcoded sizings exactly so default behaviour is unchanged; `small` scales down for a tight VPS and `large` scales up for a beefy VPS. These files are standalone here and get wired into `docker-compose.yml` in a follow-up task. Chosen mechanism (confirmed with the user): an interpolated `include:` path in `docker-compose.yml` selecting the tier via `DEPLOY_ENV`. Keeping `deploy.resources` in exactly one place (these files) avoids conflicting cross-include merges (verified working with `docker compose config`). Recommended subagent: sherpa:docky. Proposed starting values (tunable): small = app 1cpu/768M, qdrant 1cpu/1G, mcp-qdrant 1cpu/768M, ollama 4cpu/8G, opencode 1cpu/1G; large = app 4cpu/3G, qdrant 4cpu/6G, mcp-qdrant 4cpu/3G, ollama 12cpu/48G, opencode 4cpu/4G; reservations scaled proportionally.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Three files exist and are valid YAML with a top-level `services:` map: compose/env/small.yaml, compose/env/medium.yaml, compose/env/large.yaml
- [x] #2 Each file defines deploy.resources (both limits and reservations) for all five services: app, qdrant, mcp-qdrant, ollama, opencode
- [x] #3 medium values equal the current hardcoded sizings exactly: app 2cpu/1.5G, qdrant 2cpu/2G, mcp-qdrant 2cpu/1.5G, ollama 6cpu/24G, opencode 2cpu/2G, with the existing reservations preserved
- [x] #4 For every service, small <= medium <= large on both the cpus limit and the memory limit
- [x] #5 The Ollama GPU reservation guidance currently commented in compose/ollama.yaml is preserved as a comment in the env files (so it is not lost when the resources block moves)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Create compose/env/medium.yaml with deploy.resources for all 5 services matching the current hardcoded values byte-for-byte (app 2/1.5G, qdrant 2/2G, mcp-qdrant 2/1.5G, ollama 6/24G, opencode 2/2G; existing reservations).
2. Create compose/env/small.yaml (scaled down) and compose/env/large.yaml (scaled up), keeping small<=medium<=large on cpus and memory for every service.
3. Carry the Ollama GPU reservation guidance across as a comment in each env file (adapted to sit under the existing reservations block).
4. Add a header comment to each file explaining the DEPLOY_ENV selection and single-source-of-truth intent.
5. Verify all three parse as valid Compose via `docker compose config` in a scratch harness (standalone, not yet wired into the repo).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Created compose/env/{small,medium,large}.yaml. Verified by merging each onto a 5-service scratch base and reading `docker compose config --format json`: medium resolves byte-for-byte to the current sizings (app 2/1.5G, qdrant 2/2G, mcp-qdrant 2/1.5G, ollama 6/24G, opencode 2/2G + existing reservations); small<=medium<=large holds for cpus and memory on all five services; each file retains the Ollama NVIDIA GPU reservation guidance as a comment. Files are standalone (not yet wired into docker-compose.yml).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added three deploy.resources sizing profiles under compose/env/ (small/medium/large) covering app, qdrant, mcp-qdrant, ollama, opencode. medium reproduces the original fixed limits exactly (zero default-behaviour change); small/large scale down/up monotonically. Verified via `docker compose config --format json` on a scratch merge (medium == current byte-for-byte; monotonicity asserted; GPU comment preserved).
<!-- SECTION:FINAL_SUMMARY:END -->
