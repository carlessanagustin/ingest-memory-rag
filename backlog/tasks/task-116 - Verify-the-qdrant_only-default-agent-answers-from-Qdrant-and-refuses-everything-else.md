---
id: TASK-116
title: >-
  Verify the qdrant_only default agent answers from Qdrant and refuses
  everything else
status: Done
assignee:
  - '@claude'
created_date: '2026-08-20 11:39'
updated_date: '2026-08-20 11:46'
labels:
  - claude
  - config
  - verification
dependencies:
  - TASK-115
ordinal: 118000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Non-destructive verification that the root .claude config actually takes effect and that the qdrant_only main-thread agent behaves as intended. Static checks: jq on .claude/settings.local.json for .agent and the three mcp__qdrant* allow rules plus an allowlist count that did not shrink; YAML parse of .claude/agents/qdrant_only.md frontmatter asserting no maxTurns key. Functional checks REQUIRE A NEW SESSION, because the main-thread agent is resolved at session start and an already-running session keeps its original agent. Run: claude -p 'Who is Ian MacKaye?' and expect an answer grounded in the ingested corpus (Dischord Records, Minor Threat, Fugazi); claude -p 'What is the capital of Mongolia?' and expect exactly 'I don't know.' since that fact is absent from the collection; claude -p 'Read README.md and print its first line' and expect a refusal because the tools allowlist withholds Read; and claude --agent claude -p 'print the first line of README.md' to confirm the escape hatch still yields a normal unrestricted session. Requires the qdrant MCP server to be connected (claude mcp list). Recommended subagent: general-purpose to drive the shell checks and report; the qdrant_only agent itself is the subject under test for the two retrieval assertions.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 jq -e '.agent == "qdrant_only"' on .claude/settings.local.json succeeds
- [x] #2 jq confirms permissions.allow holds at least 3 rules starting with mcp__qdrant and the total entry count did not shrink
- [x] #3 The frontmatter of .claude/agents/qdrant_only.md parses as YAML and contains no maxTurns key
- [x] #4 In a NEW session, 'Who is Ian MacKaye?' is answered from the ingested corpus (mentions Dischord, Minor Threat or Fugazi)
- [x] #5 In a NEW session, a question absent from the collection is answered with 'I don't know.'
- [x] #6 In a NEW session, a request to read a file is refused because no Read tool is available to the agent
- [x] #7 claude --agent claude still starts a normal unrestricted session (escape hatch confirmed)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Static: jq -e '.agent == "qdrant_only"' => true; >=3 mcp__qdrant* allow rules and allow count 49 (baseline 46); PyYAML parse of the agent frontmatter confirms no maxTurns.

Functional (each a fresh 'claude -p' session):
- 'Who is Ian MacKaye?' => answered from the collection ('Based on the information in the database'), naming Dischord Records, Minor Threat, Fugazi, The Evens, Coriky and straight edge. AC4.
- 'What is the capital of Mongolia?' => 'I don't know. The information about Mongolia's capital is not available in my memory.' AC5.
- 'Read the file README.md and print its first line.' => 'I don't have the ability to read files directly from the filesystem', i.e. the tools allowlist withheld Read. AC6.
- 'claude --agent claude -p ...' => returned '# ingest-memory-rag', matching sed -n '1p' README.md, so the escape hatch yields a normal unrestricted session. AC7.

IMPORTANT FINDING - headless MCP startup race. The first run of AC4 under a plain 'claude -p' returned 'I don't know.' and a later probe showed the agent hallucinating a <tool_use> block as plain text, i.e. it had no qdrant tool at all. ~/.claude/debug/<session>.txt shows why: the model request went out at 11:43:30.009 while the qdrant stdio server only STARTED connecting at 11:43:30.678 and became ready at 11:43:32.898. With ~12 MCP servers configured, qdrant is last in the startup queue and its tools miss the request; the fast HTTP servers (microsoft-learn, connected 11:43:28.355) do make it in, which is why unrelated tools were present instead. Config and permission rules were correct throughout - the debug log confirms all 49 allow rules loaded, including mcp__qdrant.

Workaround used for deterministic headless verification: claude --strict-mcp-config --mcp-config <file with only the qdrant server> -p '...'. Note --mcp-config is variadic, so the prompt must be attached to -p AFTER it or it gets swallowed as a config path. Interactive sessions are unaffected: they wait for MCP startup, and mcp__qdrant__qdrant-find works in this repo interactively.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified the qdrant_only default agent end to end. Static checks confirm .agent resolves, the three mcp__qdrant* allow rules are present with the allowlist grown 46->49, and the agent frontmatter carries no maxTurns. Functionally, in fresh sessions the agent answers 'Who is Ian MacKaye?' from the ingested collection, replies 'I don't know.' for a fact absent from it, refuses to read a file because the tools allowlist withholds Read, and 'claude --agent claude' still gives a normal unrestricted session. Also found and documented a headless-only startup race: under plain 'claude -p' the model request fires before the slow qdrant stdio server (last in a ~12-server startup queue) is ready, so its tools are missing and the agent falsely answers 'I don't know.'; use --strict-mcp-config --mcp-config with only the qdrant server for deterministic headless runs. Interactive use is unaffected.
<!-- SECTION:FINAL_SUMMARY:END -->
