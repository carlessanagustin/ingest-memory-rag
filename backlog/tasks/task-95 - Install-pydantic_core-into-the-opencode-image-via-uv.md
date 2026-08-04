---
id: TASK-95
title: Install pydantic_core into the opencode image via uv
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 15:38'
updated_date: '2026-08-04 15:43'
labels:
  - docker
dependencies: []
ordinal: 97000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add a build step to compose/opencode/Dockerfile that installs pydantic_core using uv (the ubuntu:26.04 base has no system pip). This bakes the pydantic_core wheel into the image / uv cache ahead of runtime, so mcp-server-qdrant does not have to fetch or build it on first use. Change is limited to the Dockerfile.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 compose/opencode/Dockerfile installs pydantic_core at build time using uv (e.g. uv pip install into a uv-managed Python/venv — the base image has no system pip, so a plain `pip install` is not available)
- [x] #2 The opencode image builds successfully with the new step (docker compose build opencode)
- [x] #3 pydantic_core is present in the built image (its wheel is cached / importable), verifiable inside the container
- [x] #4 Change limited to compose/opencode/Dockerfile
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Add a uv-based pydantic_core install to compose/opencode/Dockerfile (after the uv install + PATH line). No system pip on ubuntu:26.04, so use a uv venv or a uv-managed Python (e.g. uv venv /opt/… && uv pip install --python …/bin/python pydantic_core, or uv pip install --system after providing an interpreter). Goal: pydantic_core installed + wheel cached; build succeeds.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Dockerfile installs pydantic_core via uv into a pinned Python 3.12 venv (uv venv /opt/uv-venv --python 3.12 && uv pip install --python …/bin/python pydantic_core). --system was impossible (no system Python on ubuntu:26.04) and the default uv Python (3.14) has no pydantic_core wheel and failed to build from source (no Rust), so 3.12 was pinned. Verified: image builds; pydantic_core 2.47.0 imports in the venv. Only the Dockerfile changed.
<!-- SECTION:FINAL_SUMMARY:END -->
