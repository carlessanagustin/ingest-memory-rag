---
id: TASK-83
title: >-
  Rewire the build script to generate the card board from task list --json with
  build-time inlined Tailwind
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 11:45'
updated_date: '2026-08-04 12:20'
labels:
  - ci
dependencies:
  - TASK-82
ordinal: 85000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Complete the build pipeline in scripts/build_board_site.sh. Source tasks from `backlog task list --json` (NOT `backlog board export`, which mutates backlog files), group by the configured statuses, fill the TASK-82 inline template with real cards, and compile Tailwind at build (pinned CLI) scanning the generated HTML, inlining the minified CSS. All HTML template and Tailwind input CSS stay INLINE in the script; any files the Tailwind CLI needs are written to TEMP paths during the build and cleaned up — no auxiliary files are committed.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 scripts/build_board_site.sh builds _site/index.html from `backlog task list --json` (no `backlog board export`); columns are the configured statuses in order, tasks grouped by status, cards show id/title/labels/assignee
- [x] #2 The responsive Tailwind card layout from TASK-82 is used (1 column on mobile, 3 columns from md up), driven by real task data
- [x] #3 All CSS lives in the build script: the Tailwind input CSS is defined inline (heredoc) and any files the Tailwind CLI needs are written to temp paths at build time only; no tailwind.input.css / board_mockup.html or other CSS/template files are committed
- [x] #4 Tailwind is compiled at build with a PINNED CLI version, scanning the generated HTML, and the minified CSS is inlined into index.html — no CDN, no external <link>/<script>
- [x] #5 The final _site/index.html has zero external http(s):// references and renders offline; light/dark preserved
- [x] #6 Script is idempotent (rm -rf _site each run), uses set -euo pipefail, needs no secrets, cleans up temp files, and running it does NOT modify anything under backlog/
- [x] #7 Script exits 0 and produces _site/index.html containing all current tasks as cards across the three columns
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Replace `backlog board export` with `backlog task list --json`; parse in Python (uv run), group by configured statuses [To Do, In Progress, Done]; fill the inline template with real cards; write the inline Tailwind input CSS to a temp file and run a pinned @tailwindcss/cli (v4, @source _site/index.html) to compile; inline the minified CSS into _site/index.html; clean temp files; idempotent; set -euo pipefail; no backlog mutation; zero external refs.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Design decision: Tailwind CLI pinned to @tailwindcss/cli@4.1.13, installed into an isolated temp prefix (npm install --no-save --prefix "$tmp") with the input CSS (@import "tailwindcss"; @source _site/index.html) written into that same temp dir so v4 module resolution finds tailwindcss; compiled --minify, inlined, temp removed via trap. Tailwinds inert leading license banner (contains a bare https://) is stripped so the page keeps zero external-http strings.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
scripts/build_board_site.sh now builds _site/index.html from `backlog task list --json` (no board export, so no backlog mutation), groups by To Do/In Progress/Done, and renders the TASK-82 card layout with real data. Tailwind v4.1.13 compiled at build (temp files only, cleaned up) and inlined — no CDN/external link/script. Verified (my own run): exit 0, 86KB output, 0 external http refs, md breakpoint -> 3 columns, dark-mode media query, 85 task cards across 3 columns, idempotent on re-run; git shows only scripts/build_board_site.sh changed with no committed aux files; backlog/ untouched.
<!-- SECTION:FINAL_SUMMARY:END -->
