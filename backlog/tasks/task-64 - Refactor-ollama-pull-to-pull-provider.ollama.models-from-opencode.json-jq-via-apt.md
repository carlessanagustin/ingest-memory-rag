---
id: TASK-64
title: >-
  Refactor ollama-pull to pull provider.ollama.models from opencode.json (jq via
  apt)
status: Done
assignee:
  - '@claude'
created_date: '2026-08-03 14:21'
updated_date: '2026-08-03 15:16'
labels:
  - docker
  - ollama
  - opencode
dependencies: []
type: feature
ordinal: 66000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Replace the hardcoded single-model ollama-pull (command: pull nemotron-3-nano:4b) with one that pulls every model listed under provider.ollama.models in compose/opencode/opencode.json. Keep the ollama/ollama image and use the native ollama CLI. Since that image has no JSON parser, apt-install the requirement (jq) at container start (Ubuntu 24.04 base, runs as root, apt network is available because it must download models anyway). Provide the logic as a small mounted script (e.g. compose/pull_models.sh) or an inline command: apt-get install jq, then jq -r ".provider.ollama.models | keys[]" over the mounted opencode.json, looping ollama pull for each key (the ollama model tags, not the .name labels). Mount opencode.json read-only; keep OLLAMA_HOST=http://ollama:11434, depends_on ollama service_healthy, restart no. Idempotent; empty/missing models map is a graceful no-op.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 ollama-pull keeps the ollama/ollama image and apt-installs its requirements (jq) at startup; no other base image is introduced
- [x] #2 It reads provider.ollama.models KEYS from the mounted compose/opencode/opencode.json and runs ollama pull for each
- [x] #3 Adding/removing a model key in opencode.json changes what gets pulled with no compose edit; an empty or missing models map is a graceful no-op
- [x] #4 The job exits non-zero if any pull fails and 0 when all succeed; re-running is idempotent (present models are no-ops)
- [x] #5 depends_on ollama service_healthy and restart no are preserved; docker compose config validates
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add compose/pull_models.sh (bash, set -euo pipefail): apt-get install jq; jq -r ".provider.ollama.models // {} | keys[]" on /config/opencode.json; graceful no-op if config missing/empty; loop ollama pull per key. 2. Rewrite ollama-pull in compose/ollama.yaml: entrypoint bash + run the script; mount ./compose/opencode/opencode.json:/config/opencode.json:ro and ./compose/pull_models.sh:/scripts/pull_models.sh:ro; keep OLLAMA_HOST, depends_on ollama service_healthy, restart no; drop the old pull command + # options comment. 3. Validate docker compose config + jq key extraction; do NOT run the pull.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
compose/pull_models.sh (bash, set -euo pipefail): apt-get install jq; graceful exit 0 if config missing or provider.ollama.models empty; mapfile jq -r ".provider.ollama.models // {} | keys[]"; loop ollama pull per key. compose/ollama.yaml ollama-pull: keeps ollama/ollama:latest; entrypoint /bin/bash + command /scripts/pull_models.sh; mounts opencode.json + the script read-only; env OLLAMA_HOST + OPENCODE_CONFIG; depends_on ollama service_healthy + restart no; old hardcoded command and # options comment removed. Verified: docker compose config -> CONFIG_OK with the wiring; jq keys[] on opencode.json yields nemotron-3-nano:4b, qwen3.5:9b, qwen3:8b; only ollama/ollama image used (no new base). Runtime pull is exercised in TASK-66.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Refactored ollama-pull to pull every provider.ollama.models key from compose/opencode/opencode.json via a mounted bash script that apt-installs jq and loops ollama pull (ollama image kept). Verified config validity and key extraction; graceful no-op + non-zero-on-failure by construction.
<!-- SECTION:FINAL_SUMMARY:END -->
