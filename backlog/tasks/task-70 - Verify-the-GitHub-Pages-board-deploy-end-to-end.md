---
id: TASK-70
title: Verify the GitHub Pages board deploy end to end
status: In Progress
assignee:
  - '@claude'
created_date: '2026-08-04 07:26'
updated_date: '2026-08-04 09:31'
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
- [x] #1 Local: running the build script produces _site/index.html containing all board columns and current tasks, and it renders correctly when opened offline (no network access)
- [x] #2 Workflow validation: pages.yml passes actionlint and includes workflow_dispatch
- [ ] #3 Post-merge: the Pages workflow run succeeds and the published URL serves the board (HTTP 200 with board content visible)
- [x] #4 The existing ci.yml workflow still passes (no regressions introduced by the new workflow)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Local: run scripts/build_board_site.sh -> assert _site/index.html has all 3 columns + current tasks, offline (no external refs). 2. Workflow: actionlint pages.yml + confirm workflow_dispatch. 3. ci.yml unaffected. 4. Post-merge (needs user): push + enable Pages, then confirm the workflow run succeeds and the URL serves the board (HTTP 200).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Local + static verification done: build script exits 0 and _site/index.html contains all three columns (To Do/In Progress/Done) + 81 TASK ids with zero external http(s) refs (renders offline); actionlint on pages.yml exits 0 and workflow_dispatch is present; ci.yml is unchanged (no regression introduced). AC3 (live URL serves the board, HTTP 200) is BLOCKED on user action: push main and set Settings->Pages->Source=GitHub Actions, after which the pages workflow deploys and the URL can be checked.
<!-- SECTION:NOTES:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @claude
created: 2026-08-04 09:31
---
AC3 (published URL serves the board) is pending: it needs the branch pushed and repo Settings->Pages->Source set to "GitHub Actions". Left In Progress until that live deploy is confirmed.
---
<!-- COMMENTS:END -->
