---
id: TASK-110
title: Verify the compose/claude Claude Code config mirrors opencode.json
status: Done
assignee:
  - '@claude'
created_date: '2026-08-07 14:21'
updated_date: '2026-08-07 14:25'
labels:
  - claude
  - config
  - verification
dependencies:
  - TASK-107
  - TASK-108
  - TASK-109
ordinal: 112000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Non-destructive verification that the new compose/claude/ config is well-formed and faithfully mirrors the mcp / default_agent / agent parts of opencode.json using the correct Claude Code schema. Recommended subagent: general-purpose.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 .mcp.json and settings.json parse as valid JSON (jq); agents/qdrant_only.md frontmatter parses as valid YAML
- [x] #2 The two MCP servers (names, transports, url/command/args/env) correspond to opencode.json with the documented Claude deltas (remote->http, command array->command+args, {env:X}->${X})
- [x] #3 settings.json "agent" equals opencode.json default_agent (qdrant_only); the agent file name matches
- [x] #4 The agent is provably restricted to only the qdrant MCP tools (tools allowlist = mcp__qdrant_remote, mcp__qdrant_local) and no other tools are permitted
- [x] #5 The delivered file set is exactly compose/claude/{.mcp.json, settings.json, agents/qdrant_only.md}
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Validate: jq parses .mcp.json + settings.json; YAML-parse qdrant_only.md frontmatter.
2. Cross-check against opencode.json with a script: server names/transports/url/command/args/env mapping (remote->http, command-array->command+args, {env:X}->${X}); default_agent==settings.agent==qdrant_only; agent tools allowlist == only the two qdrant servers.
3. Confirm the delivered file set is exactly compose/claude/{.mcp.json, settings.json, agents/qdrant_only.md}.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Verified with jq (both JSON files) and a scripted cross-check against opencode.json: server set {qdrant_remote, qdrant_local} matches; qdrant_remote transport remote->http with url preserved; qdrant_local command-array split into command+args, environment->env with {env:QDRANT_URL}->${QDRANT_URL}, {env:QDRANT_INDEX}->${QDRANT_INDEX}, EMBEDDING_MODEL literal preserved; opencode default_agent==settings.json agent==qdrant_only; agent frontmatter name qdrant_only; tools allowlist == exactly {mcp__qdrant_remote, mcp__qdrant_local} and none of the 13 opencode-denied tools appear in the allowlist. Delivered file set is exactly compose/claude/{.mcp.json, settings.json, agents/qdrant_only.md}.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified the compose/claude/ Claude Code config is well-formed (jq + YAML frontmatter) and faithfully mirrors the mcp/default_agent/agent parts of opencode.json with the documented Claude deltas, and that the agent is provably restricted to only the two qdrant MCP servers. Evidence: jq validation + a field-by-field cross-check script against opencode.json.
<!-- SECTION:FINAL_SUMMARY:END -->
