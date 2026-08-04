---
id: TASK-82
title: Design the responsive Tailwind card board inline in the build script
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 11:45'
updated_date: '2026-08-04 12:20'
labels:
  - ci
dependencies: []
ordinal: 84000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Produce the responsive Tailwind card Kanban design for the GitHub Pages board, authored ENTIRELY inside scripts/build_board_site.sh — the HTML template and the Tailwind input CSS live inline in the script (e.g. heredocs), with NO separate files (no board_mockup.html, no tailwind.input.css). To make the design reviewable before the data wiring (TASK-83), the script may render a sample board with hardcoded tasks. Columns are the configured statuses (To Do / In Progress / Done); each task is a card.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The card-board HTML template and the Tailwind input CSS are authored inline in scripts/build_board_site.sh (e.g. heredocs); no separate template or CSS files are added to the repo
- [x] #2 Layout is a 3-column status board via a responsive grid: single column on small screens, 3 columns from the md breakpoint up
- [x] #3 Each task is a card showing id, title, label badges, and assignee; each column has a header with the status name and a task count
- [x] #4 Light and dark are both supported (Tailwind dark variant via prefers-color-scheme)
- [x] #5 Readable at 320px width with no horizontal page overflow; semantic structure and sufficient contrast (basic a11y)
- [x] #6 The design is reviewable by running the script to emit a sample _site/index.html (hardcoded sample tasks acceptable at this stage); no external resources referenced
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Author, inline in scripts/build_board_site.sh, the responsive Tailwind card-board HTML template (heredoc) + the Tailwind input CSS (heredoc): grid-cols-1 md:grid-cols-3 columns, column headers with counts, task cards (id/title/label badges/assignee), light/dark via dark: variants. No separate files. Reviewable via a sample render.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Responsive Tailwind card-board design authored entirely inline in scripts/build_board_site.sh (HTML template + Tailwind input CSS as heredocs; no board_mockup.html / tailwind.input.css). Grid is grid-cols-1 md:grid-cols-3 (compiled: repeat(1) default, repeat(3) at @media min-width:48rem); each column has a header + count; each task is a card with id badge, title, label badges, assignee; light/dark via dark: variants (prefers-color-scheme:dark present). Verified by building and inspecting the output.
<!-- SECTION:FINAL_SUMMARY:END -->
