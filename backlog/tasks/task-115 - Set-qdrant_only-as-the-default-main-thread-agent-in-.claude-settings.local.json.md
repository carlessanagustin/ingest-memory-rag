---
id: TASK-115
title: >-
  Set qdrant_only as the default main-thread agent in
  .claude/settings.local.json
status: Done
assignee:
  - '@claude'
created_date: '2026-08-20 11:38'
updated_date: '2026-08-20 11:40'
labels:
  - claude
  - agent
  - config
dependencies:
  - TASK-114
ordinal: 117000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Translate opencode.json's default_agent: qdrant_only into Claude Code by adding the top-level "agent" key to the repo-root .claude/settings.local.json, and grant the Qdrant MCP tools via permissions.allow. The settings schema documents agent as: 'Name of an agent (built-in or custom) to use for the main thread. Applies the agent's system prompt, tool restrictions, and model.' The earlier compose/claude/settings.json used opencode's schema for permissions (a "permission" map of pattern->allow), which Claude Code silently ignores; the correct shape is permissions.allow as an array of rule strings. MCP permission rules take the server name optionally followed by a tool, so mcp__qdrant matches every tool from the qdrant server. Add mcp__qdrant, mcp__qdrant_remote and mcp__qdrant_local. Only mcp__qdrant resolves today (user-scope stdio server); the other two are inert until a .mcp.json defining them is in scope, and inert allow rules produce no startup warning. CRITICAL: this is a MERGE, not a rewrite. The existing permissions.allow array holds ~50 entries that must all survive. Target settings.local.json (gitignored via ~/.gitignore_global) rather than settings.json so the default never reaches a fresh clone. Apply this task only after TASK-114 exists, so the default never points at a missing agent. Recommended subagent: general-purpose (careful read-then-edit JSON merge; the risk is clobbering the existing allowlist).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 jq parses .claude/settings.local.json as valid JSON
- [x] #2 Top-level .agent equals qdrant_only
- [x] #3 permissions.allow contains mcp__qdrant, mcp__qdrant_remote and mcp__qdrant_local
- [x] #4 The permissions.allow entry count is greater than or equal to the pre-change count, and every pre-existing entry is still present
- [x] #5 No settings.json is created at the repo root and no unrelated settings keys are invented
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Back up .claude/settings.local.json to the scratchpad for before/after comparison.
2. Merge with jq (never a hand-rewrite): set .agent = "qdrant_only" and append only the missing rules via .permissions.allow += ($new - .permissions.allow), which preserves existing order and cannot duplicate.
3. Validate the result with jq -e on .agent and on the mcp__qdrant* rules.
4. Prove no entry was lost: compare the backup's allow array against the new one and require the set difference to be empty, and the count to be >= 46 (pre-change baseline).
5. Confirm no .claude/settings.json was created.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Merged with jq rather than hand-editing, and used '.permissions.allow += ($new - .permissions.allow)' so the append is idempotent and preserves the original array order. The candidate was validated with 'jq -e .' before it replaced the live file; a backup was kept in the session scratchpad for the before/after diff.

Verification evidence:
- jq -e . => valid JSON.
- jq -e '.agent == "qdrant_only"' => true.
- permissions.allow now contains mcp__qdrant, mcp__qdrant_remote, mcp__qdrant_local (alongside the pre-existing mcp__qdrant__qdrant-find).
- Count 46 -> 49. Set difference (backup allow) - (new allow) = [] => no pre-existing entry dropped.
- Top-level keys went from [permissions] to [agent, permissions] => nothing else invented or removed.
- No .claude/settings.json was created; the change is confined to the gitignored settings.local.json.

Left mcp__qdrant__qdrant-find in place. It is now redundant (mcp__qdrant subsumes it) but removing it is pure churn.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added "agent": "qdrant_only" and the three server-level rules mcp__qdrant / mcp__qdrant_remote / mcp__qdrant_local to permissions.allow in the gitignored .claude/settings.local.json, replacing the opencode-shaped 'permission' map that Claude Code silently ignores. Done as a jq merge validated before overwrite: verified .agent resolves, all three rules are present, the allowlist grew 46 -> 49 with an empty set difference against the backup (nothing dropped), top-level keys changed only by adding 'agent', and no settings.json was created.
<!-- SECTION:FINAL_SUMMARY:END -->
