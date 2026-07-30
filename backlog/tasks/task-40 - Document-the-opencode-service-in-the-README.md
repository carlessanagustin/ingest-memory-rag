---
id: TASK-40
title: Document the opencode service in the README
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 10:27'
updated_date: '2026-07-30 10:39'
labels:
  - docs
  - opencode
dependencies:
  - TASK-36
type: docs
ordinal: 42000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Document the opencode web service so a new user can find and use it: what it is, that it is built on ubuntu:26.04, the host port 4096 (http://localhost:4096), that it uses the local Ollama provider, and its local-only no-auth posture with a note on OPENCODE_SERVER_PASSWORD for network exposure. Add it to the Compose services overview table alongside the other services.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The README Compose-services overview table includes the opencode service (image/build, host port 4096, purpose)
- [x] #2 A subsection explains how to open http://localhost:4096 and that opencode uses the local Ollama provider
- [x] #3 The docs note the local-only/no-auth posture and the OPENCODE_SERVER_PASSWORD option for network access
- [x] #4 Any command shown matches the actual bind flags (--hostname 0.0.0.0 --port 4096)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add an opencode row to the Compose services table (build compose/opencode/, host port 4096, purpose). 2. Add opencode to the has-healthcheck/limits sentence. 3. New subsection documenting: open http://localhost:4096, wired to local Ollama via compose/opencode/opencode.json (qwen3.5:9b), storage_opencode persistence, local no-auth + OPENCODE_SERVER_PASSWORD note, bind flags --hostname 0.0.0.0 --port 4096.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
README: added an opencode row to the Compose services table (build compose/opencode/, host 4096, purpose); added opencode to the healthcheck/limits sentence; new subsection opencode (web coding agent, via Docker Compose) covering http://localhost:4096, the Ollama provider via compose/opencode/opencode.json (qwen3.5:9b), storage_opencode persistence, local no-auth plus OPENCODE_SERVER_PASSWORD, and the exact bind flags --hostname 0.0.0.0 --port 4096.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Documented the opencode service in README (services table row + dedicated subsection: URL, Ollama provider, persistence, security note, correct bind flags).
<!-- SECTION:FINAL_SUMMARY:END -->
