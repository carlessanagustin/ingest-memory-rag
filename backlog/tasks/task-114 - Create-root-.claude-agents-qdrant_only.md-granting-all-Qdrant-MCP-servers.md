---
id: TASK-114
title: Create root .claude/agents/qdrant_only.md granting all Qdrant MCP servers
status: Done
assignee:
  - '@claude'
created_date: '2026-08-20 11:38'
updated_date: '2026-08-20 11:40'
labels:
  - claude
  - agent
  - config
dependencies: []
ordinal: 116000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Copy compose/.claude/agents/qdrant_only.md to the repo root at .claude/agents/qdrant_only.md so Claude Code actually loads it (project agents and settings resolve from the git root; compose/.claude is a subdirectory and is never loaded, and nothing mounts it into a container). Two deliberate changes from the compose copy: widen tools to the three server-level MCP patterns mcp__qdrant, mcp__qdrant_remote and mcp__qdrant_local (subagent frontmatter accepts mcp__<server> to grant every tool from that server, so full tool names are not needed); and remove maxTurns: 6, because as a MAIN-THREAD agent maxTurns caps the whole session and would halt it mid-conversation. model: haiku and the system-prompt body are carried over verbatim. The tools allowlist is what denies Read/Edit/Bash/Grep/WebFetch, mirroring the opencode.json permission deny-list without enumerating it. Leave compose/.claude untouched. Recommended subagent: general-purpose (single-file authoring, no codebase search needed).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 File .claude/agents/qdrant_only.md exists at the repo root with valid YAML frontmatter followed by a Markdown body
- [x] #2 Frontmatter tools lists all three of mcp__qdrant, mcp__qdrant_remote, mcp__qdrant_local
- [x] #3 Frontmatter has model: haiku and name: qdrant_only, and no maxTurns key
- [x] #4 The Markdown body (system prompt) is byte-identical to the body in compose/.claude/agents/qdrant_only.md
- [x] #5 compose/.claude/ is unmodified
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Create .claude/agents/ at the repo root.
2. Write .claude/agents/qdrant_only.md from the compose/.claude copy, changing only: tools -> mcp__qdrant, mcp__qdrant_remote, mcp__qdrant_local; and dropping maxTurns: 6.
3. Keep name, description, model: haiku and the system-prompt body verbatim.
4. Verify YAML frontmatter parses and the body matches the compose copy byte-for-byte.
5. Confirm compose/.claude is untouched (git status).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Built the root file by piping the compose copy through sed (tools line rewritten, maxTurns line deleted) rather than retyping it, which guarantees the system-prompt body is preserved exactly.

Verification evidence:
- PyYAML (.venv/bin/python) parsed the frontmatter: {name: qdrant_only, model: haiku, tools: 'mcp__qdrant, mcp__qdrant_remote, mcp__qdrant_local'}; asserted maxTurns absent and the tools list equals the three expected server patterns exactly. Exit 0.
- 'diff' of the two bodies (everything after the closing ---) returned no output => byte-identical.
- git status --porcelain compose/ shows only the pre-existing ' D compose/claude/*' deletions and '?? compose/.claude/', identical to the session-start snapshot => compose/.claude unmodified.

Note on maxTurns: dropping it is required, not cosmetic. maxTurns caps agentic turns for the agent run, and as the main-thread agent that is the whole session, so 'maxTurns: 6' would have halted conversations mid-flight.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added .claude/agents/qdrant_only.md at the repo root (Claude Code loads project agents from the git root, so the existing compose/.claude copy was never picked up). Derived it from the compose copy via sed so the system prompt is byte-identical; widened tools to the server-level patterns mcp__qdrant, mcp__qdrant_remote, mcp__qdrant_local, and removed maxTurns: 6 because it would cap the whole session once this agent drives the main thread. Verified by YAML-parsing the frontmatter with assertions on every field, diffing the body against the compose copy (no differences), and confirming via git status that compose/.claude is untouched.
<!-- SECTION:FINAL_SUMMARY:END -->
