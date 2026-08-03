---
id: TASK-65
title: Update docs for the opencode.json-driven ollama-pull
status: Done
assignee:
  - '@claude'
created_date: '2026-08-03 14:22'
updated_date: '2026-08-03 15:18'
labels:
  - docs
  - ollama
dependencies:
  - TASK-64
type: docs
ordinal: 67000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Reflect that ollama-pull now pulls the models listed in compose/opencode/opencode.json (provider.ollama.models) rather than a single hardcoded model. Update the README services-table ollama-pull row and any Ollama section text that names a single pulled model. In compose/ollama.yaml, drop the now-obsolete "# options: nemotron-3-nano:4b, qwen3.5:9b, qwen3:8b" comment and fix the stale "must fit qwen3.6:27b" comment on the ollama deploy block (that model is not used; make it model-agnostic).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The README ollama-pull row says it pulls the models defined in compose/opencode/opencode.json (provider.ollama.models), not a single model
- [x] #2 No stale single-model or qwen3.6:27b references remain in compose/ollama.yaml or the README Ollama docs
- [x] #3 The docs note that editing provider.ollama.models changes what ollama-pull fetches
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. README ollama-pull services-table row + Ollama section text: models come from compose/opencode/opencode.json (provider.ollama.models), not a single model. 2. compose/ollama.yaml: fix stale "must fit qwen3.6:27b" comment (make model-agnostic); confirm the # options comment is gone.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
README: services-table ollama-pull row now says it pulls the models in compose/opencode/opencode.json (provider.ollama.models); the setup text and the Ollama section fetch line say models come from opencode.json; the LobeChat "Pick model" step generalized (e.g. qwen3.5:9b) and notes ollama-pull fetches every model in opencode.json. compose/ollama.yaml: the # options comment was removed during the TASK-64 refactor; the stale "must fit qwen3.6:27b" deploy comment is now model-agnostic ("size to the largest model you pull"). Verified: 0 qwen3.6:27b in README/compose; 0 "# options" in ollama.yaml.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Updated README (services table + setup/Ollama text) and compose/ollama.yaml comments to reflect ollama-pull pulling every model in compose/opencode/opencode.json; removed the stale qwen3.6:27b/options references.
<!-- SECTION:FINAL_SUMMARY:END -->
