---
id: TASK-38
title: Wire the opencode service to the local Ollama provider
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 10:27'
updated_date: '2026-07-30 10:43'
labels:
  - docker
  - opencode
  - ollama
dependencies:
  - TASK-36
references:
  - 'https://opencode.ai/docs'
type: feature
ordinal: 40000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Configure opencode so the local Ollama service (http://ollama:11434) is available as a model provider, so the web UI can chat without an external API key. Ollama exposes an OpenAI-compatible endpoint; provide a reproducible opencode config (committed or mounted, not manual UI-only) that registers Ollama and exposes the already-pulled model qwen3.5:9b. Keep it local-only with no secrets.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 opencode is configured with an Ollama provider targeting http://ollama:11434 via its OpenAI-compatible endpoint
- [x] #2 The pulled Ollama model qwen3.5:9b is selectable in opencode (appears in opencode models and/or the web UI model picker)
- [x] #3 The configuration contains no hardcoded secrets and is reproducible from the repo (committed or volume-mounted config, not manual UI-only steps)
- [x] #4 With ollama healthy, an opencode chat backed by the Ollama model returns a response
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Committed opencode config compose/opencode/opencode.json registering Ollama via @ai-sdk/openai-compatible at http://ollama:11434/v1 with model qwen3.5:9b. 2. Mount it read-only into the container global config path and/or set OPENCODE_CONFIG. 3. No secrets.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Reproducible config compose/opencode/opencode.json mounted read-only at /root/.config/opencode/opencode.json (OPENCODE_CONFIG set). Provider ollama via @ai-sdk/openai-compatible, baseURL http://ollama:11434/v1, model qwen3.5:9b. Verified: docker exec opencode opencode models lists ollama/qwen3.5:9b; docker exec opencode opencode run --model ollama/qwen3.5:9b returned "pong". No secrets.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Wired opencode to the local Ollama via a committed OpenAI-compatible provider config (qwen3.5:9b). Verified: opencode models lists the model and opencode run returned a response (pong).
<!-- SECTION:FINAL_SUMMARY:END -->
