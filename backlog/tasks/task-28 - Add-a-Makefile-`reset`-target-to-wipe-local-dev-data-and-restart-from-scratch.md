---
id: TASK-28
title: Add a Makefile `reset` target to wipe local dev data and restart from scratch
status: Done
assignee:
  - '@carles'
created_date: '2026-07-29 09:31'
updated_date: '2026-07-29 09:35'
labels:
  - docker
  - ops
dependencies: []
references:
  - Makefile
type: chore
ordinal: 30000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add a Makefile target that resets the local development environment to a clean state so the stack can be rebuilt from scratch. It must stop the running stack first, then delete the gitignored local data bind-mount folders qdrant_storage/ and ollama_storage/ while PRESERVING each directory and its .gitkeep placeholder (both are tracked in git only via .gitkeep). Because this discards the ~17GB pulled qwen3.6:27b Ollama model (re-pulled on the next up) and all ingested Qdrant vectors, it is destructive: guard it with an interactive confirmation and print a clear warning. Do NOT delete ./raw (the users source inputs). Follow the existing Makefile conventions: add the target to .PHONY and give it a `## ...` help annotation so it shows in `make help`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A new phony target (e.g. `reset`) exists with a `## ...` help description and appears in `make help`, consistent with the existing target style
- [x] #2 Running it first stops the stack (docker compose down, e.g. with --remove-orphans) and then clears qdrant_storage/ and ollama_storage/, leaving each directory present with only its .gitkeep (so `git status` stays clean for those paths)
- [x] #3 It requires explicit confirmation (interactive y/N prompt or equivalent guard) and prints a warning that the ~17GB Ollama model and all ingested data will be deleted and rebuilt on the next `make up`
- [x] #4 It does NOT delete ./raw or any source files, and modifies no git-tracked files when run
- [x] #5 After running, qdrant_storage/ and ollama_storage/ contain only .gitkeep and no stack containers are running, so the next `make up` starts from a clean state
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add a phony `reset` target with a `## ...` help annotation, matching Makefile style.
2. Recipe (single shell via line-continuations): print a warning, interactive y/N confirm; on yes -> docker compose down --remove-orphans, then rm -rf qdrant_storage ollama_storage && mkdir -p them && touch each .gitkeep. Never touch ./raw.
3. Verify SAFELY without destroying real data: `make help` lists reset; `make -n reset` shows the correct sequence; abort path (printf "n" | make reset) aborts and leaves the real folders (incl. the 16GB model) intact; sandbox-test the rm/mkdir/touch logic in temp dirs to prove contents are cleared but .gitkeep is preserved. Do NOT run the real destructive proceed-path.
Delegated to sherpa:docky; backlog + git in main.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented by the sherpa:docky agent; verified SAFELY (real 16GB model preserved). Added phony `reset` target: prints a warning, interactive read -p [y/N] confirm; on y -> docker compose down --remove-orphans && rm -rf qdrant_storage ollama_storage && mkdir -p them && touch each .gitkeep && "Reset complete"; on anything else -> "Aborted. Nothing was deleted." Single-shell recipe via line continuations. ./raw untouched. Added to .PHONY with a ## help line. Verification: make help lists reset; make -n reset shows the correct sequence; abort path (printf n | make reset) on the real repo printed the warning + Aborted and deleted nothing (ollama_storage/models still 16G, qdrant_storage present after); sandbox test in scratchpad (seeded dummy files + .gitkeep) ran the exact rm/mkdir/touch sequence and left ONLY .gitkeep in each folder. The destructive proceed-path (y) was intentionally NOT run against the real folders to preserve the pulled model. Independently re-confirmed: .PHONY has reset, target block correct, real model intact (16G), only Makefile changed.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added a `make reset` target that stops the stack and wipes qdrant_storage/ + ollama_storage/ back to just .gitkeep so the env rebuilds from scratch, guarded by an interactive [y/N] confirmation + warning (17GB model + ingested data re-created on next make up) and leaving ./raw untouched. Verified safely without destroying the real 16GB model: make help + make -n, the abort path on the real repo (nothing deleted), and a sandbox run proving the wipe leaves only .gitkeep. Makefile-only change.
<!-- SECTION:FINAL_SUMMARY:END -->
