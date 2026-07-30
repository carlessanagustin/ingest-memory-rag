---
id: TASK-33
title: >-
  Split compose/prompt.yaml into compose/openwebui.yaml and
  compose/lobechat.yaml
status: Done
assignee:
  - '@carles'
created_date: '2026-07-30 06:35'
updated_date: '2026-07-30 06:47'
labels:
  - docker
  - ops
dependencies:
  - TASK-32
references:
  - compose/prompt.yaml
  - docker-compose.yml
type: chore
ordinal: 35000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
compose/prompt.yaml currently defines the openwebui service and its mcpo tool bridge (both active) plus a commented-out lobe-chat block. Split it into two files: compose/openwebui.yaml (openwebui + mcpo, since mcpo is openwebui tool bridge) and compose/lobechat.yaml (the commented-out lobe-chat block). Remove compose/prompt.yaml and update the top-level docker-compose.yml include list to reference the two new files in place of prompt.yaml (keeping the include long-syntax with project_directory: . on each). This is a pure refactor with no behavior change: the same services must render. Keep lobechat.yaml body commented (re-enabling lobe-chat stays a matter of uncommenting its block); its include entry stays active like prompt.yaml was.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 compose/openwebui.yaml contains the openwebui service and the mcpo service (moved verbatim); compose/lobechat.yaml contains the commented-out lobe-chat block; compose/prompt.yaml no longer exists
- [x] #2 Top-level docker-compose.yml include list references compose/openwebui.yaml and compose/lobechat.yaml in place of compose/prompt.yaml, each with project_directory: .
- [x] #3 docker compose config is valid and the effective config is unchanged versus before the split: docker compose config --services still lists qdrant, app, mcp-qdrant, ollama, ollama-pull, openwebui, mcpo (and NOT lobe-chat), with all resolved paths identical
- [x] #4 Bringing up a prompt service still works from the new file (spot-check openwebui or mcpo reaches healthy from the repo root)
- [x] #5 Changes are limited to files under compose/ and the top-level docker-compose.yml
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Baseline: docker compose config (current) -> baseline.txt.
2. Create compose/openwebui.yaml (openwebui + mcpo, verbatim) and compose/lobechat.yaml (commented lobe-chat block, verbatim). Remove compose/prompt.yaml.
3. Update docker-compose.yml include: replace the prompt.yaml entry with openwebui.yaml + lobechat.yaml (project_directory: . each).
4. Verify: docker compose config valid; diff baseline vs after == identical (same services incl. openwebui+mcpo, no lobe-chat, same resolved paths); spot-check openwebui or mcpo config renders; changes limited to compose/ + docker-compose.yml.
Delegated to sherpa:docky (sync); backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by sherpa:docky; verified by empty config diff. Created compose/openwebui.yaml (openwebui + mcpo, verbatim) and compose/lobechat.yaml (commented lobe-chat block + re-enable header); deleted compose/prompt.yaml. Top-level docker-compose.yml include list now: qdrant, app, ollama, openwebui, lobechat (each project_directory: .). Verification: docker compose config VALID; diff of pre-split baseline vs post-split config is EMPTY (pure refactor, nothing changed); docker compose config --services = qdrant, app, mcp-qdrant, mcpo, ollama, ollama-pull, openwebui (no lobe-chat; the all-commented lobechat.yaml includes cleanly); prompt.yaml gone, both new files present; spot-check up -d qdrant mcp-qdrant mcpo -> mcpo reached healthy from the new openwebui.yaml, down without -v. Independently re-confirmed include list, file contents, config valid, service list.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Split compose/prompt.yaml into compose/openwebui.yaml (openwebui + its mcpo tool bridge) and compose/lobechat.yaml (commented-out lobe-chat), removed prompt.yaml, and updated the top-level include list to reference the two new files. Pure refactor: the rendered docker compose config is byte-identical before/after (empty diff), the same seven services render (lobe-chat still disabled), and mcpo still comes up healthy from the new file.
<!-- SECTION:FINAL_SUMMARY:END -->
