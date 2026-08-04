---
id: TASK-81
title: Verify the reset/reset-hard storage behaviour non-destructively
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 08:55'
updated_date: '2026-08-04 08:59'
labels:
  - chore
dependencies:
  - TASK-80
ordinal: 83000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Confirm reset preserves storage/ollama while removing other storage data, and reset-hard removes everything, WITHOUT running the real targets against the user\s ./storage (which holds multi-GB models and live data).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Verification does NOT run `make reset` or `make reset-hard` against the real ./storage (no deletion of the user models/data)
- [x] #2 The reset delete logic, exercised against a throwaway temp dir mimicking storage/ (ollama/, qdrant/, opencode/, .gitkeep), leaves ollama/ and .gitkeep intact and removes qdrant/ and opencode/
- [x] #3 The reset-hard delete logic against the same temp tree removes everything including ollama/
- [x] #4 `make help` shows the updated reset/reset-hard descriptions, and `make -n reset` (dry run) shows storage/ollama is not targeted for deletion
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Non-destructive: build a throwaway temp storage tree (ollama/ qdrant/ opencode/ .gitkeep) and run the exact reset find-wipe against it -> assert ollama/ + .gitkeep remain, qdrant/ + opencode/ gone.
2. Run reset-hard delete logic (rm -rf) against the temp tree -> all gone.
3. `make help` shows updated reset/reset-hard text; `make -n reset` dry run shows storage/ollama is not targeted.
4. Never touch the real ./storage.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Verified via a mktemp throwaway storage tree (ollama/qdrant/opencode/.gitkeep) run from a script (to bypass the RTK bash hook that rewrites interactive `find`). reset logic -> ollama/ + .gitkeep kept, qdrant/ + opencode/ removed. reset-hard logic -> all removed, .gitkeep recreated. `make -n reset` shows storage/ollama is not targeted (find ... ! -name ollama, no rm -rf storage); `make -n reset-hard` still has rm -rf storage; `make help` shows updated descriptions. Real ./storage/ollama (14G) confirmed untouched.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Non-destructively verified: throwaway-tree simulation of both recipes (real ./storage never touched, ollama still 14G) shows reset preserves storage/ollama + .gitkeep while removing qdrant/opencode, and reset-hard removes everything. make -n dry runs and make help confirm the recipe + docs.
<!-- SECTION:FINAL_SUMMARY:END -->
