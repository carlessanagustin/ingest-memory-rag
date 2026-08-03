---
id: TASK-66
title: Verify ollama-pull pulls all opencode.json models end to end
status: Done
assignee:
  - '@claude'
created_date: '2026-08-03 14:22'
updated_date: '2026-08-03 15:30'
labels:
  - docker
  - ollama
  - verification
dependencies:
  - TASK-64
  - TASK-65
type: chore
ordinal: 68000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Bring up ollama + ollama-pull and confirm the refactor works. Preserve data (no down -v / no reset). Note: pulling every model in provider.ollama.models (currently qwen3.5:9b, nemotron-3-nano:4b, qwen3:8b) downloads several GB.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 ollama-pull installs jq and runs ollama pull for each key in provider.ollama.models; the job exits 0
- [x] #2 After the run, ollama list shows every model from provider.ollama.models
- [x] #3 Re-running ollama-pull is a no-op (already-present models), and docker compose config validates
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Bring up ollama, wait healthy; list models before. 2. Run ollama-pull (docker compose up ollama-pull) - apt-installs jq, reads the 3 keys, pulls each; capture exit code + logs. 3. ollama list shows all 3. 4. Idempotent re-run is a fast no-op. 5. docker compose config valid. No down -v / no reset.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Brought up ollama (healthy); models before = none. Ran docker compose up ollama-pull: the script apt-installed jq, logged "Models to pull: nemotron-3-nano:4b qwen3.5:9b qwen3:8b" (jq extracted all 3 keys from opencode.json), ran ollama pull for each, printed "All models pulled successfully", and compose reported "ollama-pull exited with code 0". ollama list AFTER shows all three: qwen3:8b (5.2GB), qwen3.5:9b (6.6GB), nemotron-3-nano:4b (2.8GB). Idempotent re-run reprocessed the same 3 keys with no re-download and exited 0. docker compose config validated in TASK-64. No down -v / no reset.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified end-to-end: ollama-pull apt-installs jq, reads every provider.ollama.models key from opencode.json, and pulls each (ollama list shows all three); the job exits 0 and re-running is an idempotent no-op.
<!-- SECTION:FINAL_SUMMARY:END -->
