---
id: TASK-44
title: Verify opencode loads the Qdrant MCP and queries the Document collection
status: Done
assignee:
  - '@claude'
created_date: '2026-07-30 10:48'
updated_date: '2026-07-30 11:36'
labels:
  - docker
  - opencode
  - mcp
  - verification
dependencies:
  - TASK-42
type: chore
ordinal: 46000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Bring up the stack and confirm the opencode service connects to the Qdrant MCP bridge and can retrieve from the ingested Document collection via qdrant-find. Preserve data: no docker compose down -v and no storage wipe.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 With qdrant, mcp-qdrant and opencode healthy, opencode shows the qdrant MCP connected and the qdrant-find tool available
- [x] #2 A live opencode query using qdrant-find returns content from the ingested Document collection
- [x] #3 opencode starts only after mcp-qdrant is healthy (startup ordering works) and the Ollama model still responds
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Bring up qdrant + mcp-qdrant; wait healthy; confirm Document collection populated. 2. Recreate opencode (up -d) so it loads the new mounted config and waits for mcp-qdrant; wait healthy. 3. Confirm opencode connected the qdrant MCP / qdrant-find tool available (opencode mcp listing or logs). 4. Live opencode run using qdrant-find returns ingested content from Document. 5. Confirm Ollama model still responds. No down -v / no storage wipe.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Verified on the running stack. opencode mcp list -> "qdrant  connected  http://mcp-qdrant:8000/mcp" (1 server). Recreated opencode waited for mcp-qdrant AND ollama to become healthy before starting (depends_on ordering confirmed via the Waiting->Healthy sequence). A prior reset had emptied storage_qdrant and ./raw, so ingested a smoke-test doc raw/opencode-mcp-smoke-test.md via the app service (Document collection status green, points=1). Live: docker exec opencode opencode run --model ollama/qwen3.5:9b invoking qdrant-find; opencode session DB storage_opencode/opencode.db contains the returned Document content ("blue reset button", "Nimbus appliance"), proving qdrant-find retrieved ingested content into opencode. Independent cross-check via mcp qdrant-find returned the same chunk. Caveat: qwen3.5:9b reliably CALLS qdrant-find but does not reliably synthesize a final natural-language answer from the result; the MCP wiring and retrieval are correct. A stronger tool-calling model gives better final prose. No down -v / no storage wipe used.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified opencode loads the Qdrant MCP (mcp list: qdrant connected) and that a live opencode qdrant-find call returns Document content (ingested chunk stored in opencode session DB; cross-checked via mcp qdrant-find). Startup waits for mcp-qdrant healthy; Ollama responds. Note: the 9B model is weak at final-answer synthesis though it does invoke the tool.
<!-- SECTION:FINAL_SUMMARY:END -->
