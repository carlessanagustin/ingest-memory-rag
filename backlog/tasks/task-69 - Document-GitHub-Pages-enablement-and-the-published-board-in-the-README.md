---
id: TASK-69
title: Document GitHub Pages enablement and the published board in the README
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 07:26'
updated_date: '2026-08-04 09:31'
labels:
  - docs
dependencies:
  - TASK-68
ordinal: 71000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Document how the published Kanban board works so a maintainer can enable it and understand what it is. Outcome: README covers the one-time Pages setup, the URL, the redeploy trigger, and local preview, and clarifies it is a read-only snapshot distinct from the interactive backlog browser.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 README documents the one-time manual step: repo Settings -> Pages -> Source = "GitHub Actions"
- [x] #2 README states the published URL (https://carlessanagustin.github.io/ingest-memory-rag/) and that it is a read-only snapshot of the Kanban board, not the interactive `backlog browser`
- [x] #3 README explains the deploy trigger: push to main affecting backlog/**, plus manual workflow_dispatch
- [x] #4 README shows how to run the build script locally to preview _site/index.html
- [x] #5 README notes `backlog browser` remains the local interactive UI at http://127.0.0.1:6420
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Add a "Project board (GitHub Pages)" subsection under Development in README covering: the published URL + that it is a read-only snapshot (not the interactive browser); the one-time Settings->Pages->Source=GitHub Actions step; the deploy trigger; local preview via the build script; and that `backlog browser` stays local at 127.0.0.1:6420.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added a README "Project board (GitHub Pages)" subsection: publishes URL https://carlessanagustin.github.io/ingest-memory-rag/ as a read-only board snapshot; documents the one-time Settings->Pages->Source=GitHub Actions step; the deploy trigger (push to main touching backlog/** + manual workflow_dispatch); local preview via `bash scripts/build_board_site.sh` -> _site/index.html; and that `backlog browser` remains the local interactive UI at http://127.0.0.1:6420. Verified by review of the rendered section.
<!-- SECTION:FINAL_SUMMARY:END -->
