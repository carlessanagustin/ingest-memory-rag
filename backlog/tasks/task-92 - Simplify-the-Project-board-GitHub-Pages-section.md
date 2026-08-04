---
id: TASK-92
title: Simplify the Project board (GitHub Pages) section
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 14:39'
updated_date: '2026-08-04 14:54'
labels:
  - docs
dependencies:
  - TASK-91
ordinal: 94000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Trim the Project board section to essentials: the published URL, that it is an auto-deployed static board from the backlog tasks, and a one-line local preview. Condense or drop the verbose one-time-setup and workflow internals.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The section is noticeably shorter while still giving the published URL and that the board auto-deploys from backlog tasks
- [x] #2 Local preview remains as a one-liner; verbose one-time-setup/workflow internals are condensed or dropped
- [x] #3 Changes limited to README.md
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Simplify Project board (URL + auto-deploy + one-line preview). part of one coherent README.md refactor pass
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Project board section trimmed from ~24 lines to ~10: published URL, one line that it auto-deploys from the backlog tasks on every push to main, a one-line local preview (bash scripts/build_board_site.sh -> _site/index.html), and the backlog browser note. Verbose Settings->Pages/workflow internals dropped.
<!-- SECTION:FINAL_SUMMARY:END -->
