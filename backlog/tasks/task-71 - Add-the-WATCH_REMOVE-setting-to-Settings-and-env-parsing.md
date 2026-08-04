---
id: TASK-71
title: Add the WATCH_REMOVE setting to Settings and env parsing
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 07:31'
updated_date: '2026-08-04 07:40'
labels:
  - feature
dependencies: []
ordinal: 73000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Introduce a new opt-in boolean config WATCH_REMOVE that will later drive deleting a source file after it is successfully ingested. This task only adds the setting plumbing (no delete behavior yet). Default is false so existing deployments are unaffected and the destructive behavior is strictly opt-in.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Settings gains a boolean field watch_remove
- [x] #2 Settings.from_env reads WATCH_REMOVE via the existing _env_bool helper with default False
- [x] #3 Truthy values (1/true/yes/on, case-insensitive) enable it; empty/unset/other values keep it False
- [x] #4 A unit test covers the default (False) and at least one truthy parse
- [x] #5 ruff, mypy and pytest pass with coverage staying >=80%
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add `watch_remove: bool` field to the frozen Settings dataclass (grouped with the other watch settings).
2. In Settings.from_env, add `watch_remove=_env_bool("WATCH_REMOVE", default=False)`.
3. tests/test_config.py: assert default is False (unset) and that WATCH_REMOVE=true (and a case-variant) parses True; unknown/empty stays False.
4. Run ruff, mypy, pytest; keep coverage >=80%.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added `watch_remove: bool` to Settings and `watch_remove=_env_bool("WATCH_REMOVE", default=False)` in from_env. Verified: 3 new config tests (default False, empty False, truthy variants true/YES/On/1 → True) pass; full suite 43 passed, config.py 100% coverage; ruff + mypy clean.
<!-- SECTION:FINAL_SUMMARY:END -->
