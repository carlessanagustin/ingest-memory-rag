---
id: TASK-97
title: Verify the opencode image bakes in the MCP server deps
status: Done
assignee: []
created_date: '2026-08-04 15:38'
updated_date: '2026-08-04 15:43'
labels:
  - chore
dependencies:
  - TASK-95
  - TASK-96
ordinal: 99000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Build the opencode image and confirm pydantic_core and mcp-server-qdrant are baked in, and that `uvx mcp-server-qdrant` starts from cache without a runtime download (removing the first-run download that made qdrant_local time out). qdrant_local also reaching Qdrant depends on QDRANT_URL/Qdrant and is out of scope here.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 docker compose build opencode completes with no hang (the server is never started during build)
- [x] #2 In the built image, pydantic_core imports successfully and `uvx mcp-server-qdrant --help` (or equivalent) runs from the baked-in packages with no network access (offline)
- [x] #3 The existing image behaviour still works (opencode web serves on port 4096; opencode --version succeeds)
- [x] #4 Documented evidence that the first-run download is eliminated (e.g. the cached tool resolves offline)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Independent build + verification (docker compose build opencode, then docker run in the built image): build completes with no hang; uv tool list -> mcp-server-qdrant v0.8.1; uv tool run --offline mcp-server-qdrant --help -> usage printed, exit 0 (no network, proving the first-run download is eliminated); /opt/uv-venv pydantic_core 2.47.0 imports; opencode --version -> 1.18.12. Key build fix: ubuntu:26.04 uv defaults to Python 3.14 (no pydantic_core wheel -> source build fails without Rust), so the Dockerfile pins Python 3.12.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified the opencode image bakes in the MCP deps: build succeeds with no hang, mcp-server-qdrant@0.8.1 + pydantic_core are baked in, `uvx mcp-server-qdrant` resolves fully offline (no first-run download), and opencode still works. The download that made qdrant_local time out is eliminated.
<!-- SECTION:FINAL_SUMMARY:END -->
