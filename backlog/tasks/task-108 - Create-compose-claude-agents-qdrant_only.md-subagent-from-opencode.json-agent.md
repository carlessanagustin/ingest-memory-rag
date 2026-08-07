---
id: TASK-108
title: Create compose/claude/agents/qdrant_only.md subagent from opencode.json agent
status: Done
assignee:
  - '@claude'
created_date: '2026-08-07 14:21'
updated_date: '2026-08-07 14:23'
labels:
  - claude
  - agent
  - config
dependencies: []
ordinal: 110000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Translate agent.qdrant_only from opencode.json into a Claude Code subagent Markdown file at compose/claude/agents/qdrant_only.md (Claude Code agents are Markdown + YAML frontmatter, not JSON). Frontmatter: name qdrant_only; a description of the strict knowledge-base agent; tools as an ALLOWLIST containing only the two qdrant MCP servers (mcp__qdrant_remote, mcp__qdrant_local) which denies every other tool (read/edit/bash/webfetch/etc.), mirroring the OpenCode permission deny-list; model haiku (OpenCode used deepseek-v4-flash:cloud, which Claude Code cannot run); maxTurns 6 (mirrors OpenCode steps:6). The Markdown body is the system prompt: strictly answer from the qdrant_* tools and reply that it does not know when the answer is not present. OpenCode temperature and mode have no Claude frontmatter equivalent and are dropped (record this in the task notes). Recommended subagent: general-purpose.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 compose/claude/agents/qdrant_only.md exists with valid YAML frontmatter followed by a Markdown body
- [x] #2 Frontmatter: name is qdrant_only and model is haiku
- [x] #3 tools is an allowlist of exactly mcp__qdrant_remote and mcp__qdrant_local (no read/edit/glob/grep/bash/webfetch/websearch/task/etc.)
- [x] #4 maxTurns is 6 (mirrors OpenCode steps)
- [x] #5 The body instructs the agent to answer strictly from the qdrant_* tools and to reply that it does not know when the answer is absent
- [x] #6 Dropped/changed OpenCode fields are recorded in the task notes (temperature and mode dropped; permission deny-list expressed as a tools allowlist; model deepseek-v4-flash:cloud changed to haiku)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Create compose/claude/agents/qdrant_only.md with YAML frontmatter (name qdrant_only; description; tools allowlist mcp__qdrant_remote, mcp__qdrant_local; model haiku; maxTurns 6) and the strict single-source-of-truth prompt as the body.
2. Deltas from opencode: temperature and mode dropped (no Claude equivalent); permission deny-list -> tools allowlist; model deepseek-v4-flash:cloud -> haiku.
3. Verify frontmatter parses as YAML and the allowlist/model/maxTurns are exactly as specified.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Created compose/claude/agents/qdrant_only.md. Verified with a YAML parse: name=qdrant_only, model=haiku, maxTurns=6, tools allowlist = exactly {mcp__qdrant_remote, mcp__qdrant_local} (so Read/Edit/Bash/Write/WebFetch/WebSearch/Grep/Glob and every other non-qdrant tool are denied by allowlist semantics), and the body carries the strict single-source-of-truth prompt (answer only from qdrant_* tools; otherwise reply that it does not know). Documented deltas from opencode.json: temperature (0) and mode (primary) have no Claude subagent frontmatter equivalent and were dropped; the permission deny-list was expressed as the tools allowlist; model deepseek-v4-flash:cloud was changed to haiku (Claude Code runs Anthropic models); OpenCode steps:6 mapped to maxTurns:6.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added compose/claude/agents/qdrant_only.md, the Claude Code subagent mirroring opencode agent.qdrant_only: tools allowlist restricted to the two qdrant MCP servers, model haiku, maxTurns 6, and the strict answer-only-from-Qdrant prompt. Verified frontmatter/allowlist via a YAML parse; documented the dropped/changed fields (temperature, mode, model).
<!-- SECTION:FINAL_SUMMARY:END -->
