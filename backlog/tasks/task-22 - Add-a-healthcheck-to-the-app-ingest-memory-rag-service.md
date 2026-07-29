---
id: TASK-22
title: Add a healthcheck to the app (ingest-memory-rag) service
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 08:33'
updated_date: '2026-07-29 08:55'
labels:
  - docker
  - ops
dependencies: []
references:
  - docker-compose.yml
type: enhancement
ordinal: 24000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The `app` (ingest-memory-rag) service is the only long-running service without a healthcheck. It is a background file-watcher with no HTTP port, so a port probe is not applicable. Add a lightweight healthcheck using tooling already in the app image (Python). Preferred, no code change: a small Python one-liner that checks readiness by reaching its hard dependency Qdrant (the app can only do useful work when Qdrant is reachable). If true process liveness is required instead, a minimal app change that emits a heartbeat file the healthcheck reads is acceptable — note which approach was used. The one-shot `ollama-pull` does not need a healthcheck.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The `app` service defines a `healthcheck` (test/interval/timeout/retries/start_period) using tooling available in the app image, with no new exposed ports
- [x] #2 The healthcheck reports healthy under normal operation — including when the watcher is idle waiting for file events — and fails when the app cannot function (process gone or Qdrant unreachable)
- [x] #3 `docker compose config` validates and `docker compose up -d qdrant app` shows `app` reaching `healthy`
- [x] #4 If any code change was required it is minimal and documented; otherwise the healthcheck is config-only
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Add a config-only healthcheck to the app service: a Python readiness probe that reaches the configured Qdrant (os.environ["QDRANT_URL"] + /healthz via urllib, timeout ~3s) — no new ports, no app code change. Sensible cadence (interval 30s, timeout 5s, retries 3, start_period 30s). Rationale: app has no HTTP server; Qdrant is its hard dependency, so reachability is a meaningful readiness signal.
Verify: docker compose config valid; docker compose up -d qdrant app -> app reaches (healthy); bonus negative test: stop qdrant -> app goes unhealthy -> restart qdrant -> healthy again; then down.
Delegated to sherpa:docky (background); backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by the sherpa:docky agent (config-only); runtime verified by the orchestrator. Added to the app service a healthcheck: test ["CMD","python","-c","import os,urllib.request; urllib.request.urlopen(os.environ[\"QDRANT_URL\"].rstrip(\"/\")+\"/healthz\", timeout=3)"], interval 30s / timeout 5s / retries 3 / start_period 30s. No new ports; no app source change (python is available in the app image). Rationale: app has no HTTP server, so readiness = can reach its hard dependency Qdrant at the configured URL. Verification (against the existing image, no rebuild): docker compose up -d qdrant app -> app reaches healthy (~20s); negative test: docker compose stop qdrant -> app transitions healthy->unhealthy at ~100s (3 failed checks); docker compose start qdrant -> app recovers to healthy (~40s); docker compose config VALID; teardown clean. (An earlier verify run was blocked by a leftover ingest-memory-rag container from a killed agents partial up --build; cleared with compose down --remove-orphans, then re-verified clean.)
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added a config-only healthcheck to the app (ingest-memory-rag) service: a Python urllib readiness probe against the configured Qdrant (QDRANT_URL/healthz), since the app has no HTTP server of its own. Verified end-to-end: app reaches healthy with Qdrant up, transitions to unhealthy when Qdrant is stopped (~100s, proving the probe is meaningful), and recovers to healthy when Qdrant returns; docker compose config valid.
<!-- SECTION:FINAL_SUMMARY:END -->
