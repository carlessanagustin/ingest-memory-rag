---
id: TASK-70
title: Verify the GitHub Pages board deploy end to end
status: To Do
assignee: []
created_date: '2026-08-04 07:26'
labels:
  - chore
dependencies:
  - TASK-68
  - TASK-69
ordinal: 72000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Confirm the board build and Pages deployment work, both locally and once deployed. Outcome: evidence that the static board renders correctly and the workflow publishes it without regressing existing CI.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Local: running the build script produces _site/index.html containing all board columns and current tasks, and it renders correctly when opened offline (no network access)
- [ ] #2 Workflow validation: pages.yml passes actionlint and includes workflow_dispatch
- [ ] #3 Post-merge: the Pages workflow run succeeds and the published URL serves the board (HTTP 200 with board content visible)
- [ ] #4 The existing ci.yml workflow still passes (no regressions introduced by the new workflow)
<!-- AC:END -->
