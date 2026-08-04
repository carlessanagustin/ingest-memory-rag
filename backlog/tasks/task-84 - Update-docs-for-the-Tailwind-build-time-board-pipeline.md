---
id: TASK-84
title: Update docs for the Tailwind build-time board pipeline
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 11:45'
updated_date: '2026-08-04 12:22'
labels:
  - docs
dependencies:
  - TASK-83
ordinal: 86000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Reflect the refactored board pipeline in the docs: a single self-contained builder script (scripts/build_board_site.sh) that holds all HTML template and CSS inline and produces a responsive Tailwind card board.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 README Project board section notes the board is a responsive Tailwind card layout that is still fully self-contained (inlined CSS, no CDN) and generated entirely by scripts/build_board_site.sh
- [x] #2 Local-preview prerequisites updated: the Tailwind build step needs Node (npx) available locally, in addition to uv and the backlog CLI
- [x] #3 Comments in scripts/build_board_site.sh reflect the new task list --json + build-time Tailwind pipeline, with all template and CSS inline
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Update README "Project board (GitHub Pages)" section: board is now a responsive Tailwind card layout generated from `backlog task list --json` (not board export), still fully self-contained (Tailwind compiled at build and inlined, no CDN). 2. Local-preview prerequisites: add Node (for the Tailwind CLI) alongside uv + backlog. 3. Script comments already reflect the new pipeline (verify).
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
README Project board section updated: the board is now a responsive Tailwind card layout generated from `backlog task list --json` by scripts/build_board_site.sh, fully self-contained (Tailwind compiled at build and inlined, no CDN). Local-preview prerequisites now list the backlog CLI, uv, and Node (for the pinned Tailwind CLI). The build scripts inline comments already describe the task list --json + build-time Tailwind pipeline. Verified by review.
<!-- SECTION:FINAL_SUMMARY:END -->
