---
id: TASK-69
title: Document GitHub Pages enablement and the published board in the README
status: To Do
assignee: []
created_date: '2026-08-04 07:26'
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
- [ ] #1 README documents the one-time manual step: repo Settings -> Pages -> Source = "GitHub Actions"
- [ ] #2 README states the published URL (https://carlessanagustin.github.io/ingest-memory-rag/) and that it is a read-only snapshot of the Kanban board, not the interactive `backlog browser`
- [ ] #3 README explains the deploy trigger: push to main affecting backlog/**, plus manual workflow_dispatch
- [ ] #4 README shows how to run the build script locally to preview _site/index.html
- [ ] #5 README notes `backlog browser` remains the local interactive UI at http://127.0.0.1:6420
<!-- AC:END -->
