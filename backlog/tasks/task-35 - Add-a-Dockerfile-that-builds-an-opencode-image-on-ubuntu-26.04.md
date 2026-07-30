---
id: TASK-35
title: 'Add a Dockerfile that builds an opencode image on ubuntu:26.04'
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 10:26'
updated_date: '2026-07-30 10:39'
labels:
  - docker
  - opencode
dependencies: []
references:
  - 'https://opencode.ai/docs'
type: feature
ordinal: 37000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Provide a build for the opencode agentic coding tool. A dedicated Dockerfile at compose/opencode/Dockerfile (kept in its own folder so the build context stays tiny) starts from ubuntu:26.04, installs curl, runs the official opencode install script, and puts the opencode binary on PATH. This image is the base for the compose service that serves the opencode web UI. The install script places the binary at /root/.opencode/bin/opencode.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A Dockerfile exists at compose/opencode/Dockerfile and is based on ubuntu:26.04
- [x] #2 It installs curl and runs the official installer (curl -fsSL https://opencode.ai/install | bash) non-interactively
- [x] #3 /root/.opencode/bin is on PATH so the opencode command resolves; opencode --version succeeds in the built image
- [x] #4 The build context is minimal (scoped to compose/opencode/), not the whole repository
- [x] #5 No API keys or secrets are baked into the image
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Create compose/opencode/Dockerfile FROM ubuntu:26.04. 2. apt-get update + install curl ca-certificates; run official installer (curl -fsSL https://opencode.ai/install | bash) non-interactively. 3. ENV PATH=/root/.opencode/bin:$PATH so opencode resolves. 4. Context scoped to compose/opencode/. 5. Runtime opencode --version verified during end-to-end (TASK-41).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Built via docker compose build opencode -> exit 0; ubuntu:26.04 base, RUN opencode --version succeeded. Image ingest-memory-rag-opencode:latest ~441MB. opencode --version = 1.18.9. Build context scoped to ./compose/opencode (Dockerfile does not COPY the repo). No secrets baked in.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added compose/opencode/Dockerfile (ubuntu:26.04 + official opencode installer, PATH set, build-time opencode --version). Verified by building the image (exit 0) and opencode --version = 1.18.9.
<!-- SECTION:FINAL_SUMMARY:END -->
