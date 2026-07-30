---
id: TASK-30
title: Split docker-compose.yml into compose/ files aggregated with include
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 15:33'
updated_date: '2026-07-29 15:38'
labels:
  - docker
  - ops
dependencies: []
references:
  - docker-compose.yml
  - 'https://docs.docker.com/reference/compose-file/include/'
type: chore
ordinal: 32000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Refactor the monolithic docker-compose.yml into per-concern files under a new compose/ folder, aggregated from the top-level docker-compose.yml via Compose include. This is a pure refactor: move existing service definitions verbatim (images, env, healthchecks, deploy limits, volumes, ports). Layout: compose/qdrant.yaml (qdrant + mcp-qdrant), compose/app.yaml (app), compose/ollama.yaml (ollama + ollama-pull), compose/prompt.yaml (lobe-chat; openwebui is added later in a separate task). The top-level docker-compose.yml keeps only an include list of the four files and defines no services itself. Disable lobe-chat for now by commenting out its service block (it lives in compose/prompt.yaml after the split, so that is where the comment goes). CRITICAL RISK: Compose include can change how relative paths resolve, so the build context (.) and the bind mounts (./qdrant_storage, ./ollama_storage, ./raw) must still resolve to the repo root, not to compose/. Verify the resolved config is unchanged and use project_directory or adjusted paths if needed.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A new compose/ folder contains qdrant.yaml, app.yaml, ollama.yaml, prompt.yaml, each a valid standalone compose file; top-level docker-compose.yml contains only an include list of those four and defines no services of its own
- [x] #2 Service-to-file mapping matches: qdrant+mcp-qdrant in qdrant.yaml, app in app.yaml, ollama+ollama-pull in ollama.yaml, lobe-chat in prompt.yaml
- [x] #3 lobe-chat is commented out (disabled) and does not appear in docker compose config --services
- [x] #4 docker compose config is valid and, for the still-active services (qdrant, app, mcp-qdrant, ollama, ollama-pull), the effective config equals the pre-split file: same images, env, ports, healthchecks, deploy limits, and RESOLVED bind-mount/build paths pointing at the repo root (not compose/)
- [x] #5 docker compose up -d for the active services still works from the repo root with no relative-path breakage (spot-check a service reaching healthy)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Capture baseline: docker compose config (current monolith, with the users qwen3.5:9b edit) -> baseline file.
2. Create compose/ with qdrant.yaml (qdrant+mcp-qdrant), app.yaml (app), ollama.yaml (ollama+ollama-pull), prompt.yaml (lobe-chat, commented out). Move service blocks verbatim.
3. Rewrite top-level docker-compose.yml to only: include: [compose/qdrant.yaml, compose/app.yaml, compose/ollama.yaml, compose/prompt.yaml].
4. Fix include path resolution so ./qdrant_storage, ./ollama_storage, ./raw and build context resolve to repo root (use project_directory or ../ paths as needed).
5. Verify: docker compose config valid; diff active-service config vs baseline shows ONLY lobe-chat removed (all resolved volume/build paths identical); a service still comes up healthy.
Delegated to sherpa:docky (sync); backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by sherpa:docky; verified by before/after config diff. Top-level docker-compose.yml now contains only an include list (long syntax with project_directory: . on each entry to pin relative-path resolution to repo root); no top-level services key. Files: compose/qdrant.yaml (qdrant+mcp-qdrant), compose/app.yaml (app), compose/ollama.yaml (ollama+ollama-pull), compose/prompt.yaml (lobe-chat entirely commented out). Services moved verbatim, preserving current working-tree state (ollama-pull pulls qwen3.5:9b). Verification: docker compose config VALID; diff of pre-split baseline vs post-split shows ONLY lobe-chat removed (43 lines) - all other resolved config identical, including volume source abs paths (repo-root/qdrant_storage, /ollama_storage, /raw) and app build.context (repo root), none under compose/; docker compose config --services = qdrant/app/mcp-qdrant/ollama/ollama-pull (no lobe-chat); qdrant spot-check up -> healthy with mount source repo-root/qdrant_storage, down without -v (data intact). Independently re-confirmed structure, no top-level services:, config valid. NOTE: an unrelated uncommitted Makefile edit (docker-build target renamed to build) is present in the working tree - made by the user, not this task; left untouched.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Split the monolithic docker-compose.yml into compose/qdrant.yaml (qdrant+mcp-qdrant), compose/app.yaml, compose/ollama.yaml (ollama+ollama-pull), and compose/prompt.yaml (lobe-chat, commented out/disabled), aggregated from a top-level docker-compose.yml that is now just an include list. Used include long-syntax with project_directory: . so bind mounts and build context still resolve to the repo root. Verified as a pure refactor: docker compose config diff shows only lobe-chat removed, all other services identical incl. resolved paths, and qdrant still comes up healthy from the repo root.
<!-- SECTION:FINAL_SUMMARY:END -->
