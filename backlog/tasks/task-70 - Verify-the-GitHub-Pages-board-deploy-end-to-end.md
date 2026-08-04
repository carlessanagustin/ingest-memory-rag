---
id: TASK-70
title: Verify the GitHub Pages board deploy end to end
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 07:26'
updated_date: '2026-08-04 11:26'
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
- [x] #3 Post-merge: the Pages workflow run succeeds and the published URL serves the board (HTTP 200 with board content visible)
- [x] #4 The existing ci.yml workflow still passes (no regressions introduced by the new workflow)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Local: run scripts/build_board_site.sh -> assert _site/index.html has all 3 columns + current tasks, offline (no external refs). 2. Workflow: actionlint pages.yml + confirm workflow_dispatch. 3. ci.yml unaffected. 4. Post-merge (needs user): push + enable Pages, then confirm the workflow run succeeds and the URL serves the board (HTTP 200).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Local + static verification done: build script exits 0 and _site/index.html contains all three columns (To Do/In Progress/Done) + 81 TASK ids with zero external http(s) refs (renders offline); actionlint on pages.yml exits 0 and workflow_dispatch is present; ci.yml is unchanged (no regression introduced). AC3 (live URL serves the board, HTTP 200) is BLOCKED on user action: push main and set Settings->Pages->Source=GitHub Actions, after which the pages workflow deploys and the URL can be checked.

Real CI run after push (run 30897183200): the build half of the workflow succeeded on GitHub — checkout, npm install -g backlog.md, setup-uv, and `bash scripts/build_board_site.sh` all passed, confirming the board builds in CI (not just locally). deploy failed at actions/configure-pages@v5: "Get Pages site failed ... verify the repository has Pages enabled and configured to build using GitHub Actions (Not Found)". This is AC3s blocker: Pages is not yet enabled with Source=GitHub Actions. Fix options: (a) Settings->Pages->Source=GitHub Actions, then re-run; or (b) add `with: enablement: true` to the configure-pages step so the workflow enables Pages itself (pages: write permission is already granted). Non-blocking annotation: Node20 deprecation warning on setup-node/configure-pages.

Pages enabled via `gh api -X POST repos/.../pages -f build_type=workflow` (workflow GITHUB_TOKEN could not create the site: "Resource not accessible by integration" even with pages:write; the owner gh token can). Re-ran the workflow (run 30904528854): all steps green incl. configure-pages/upload-pages-artifact/deploy-pages. Live check: https://carlessanagustin.github.io/ingest-memory-rag/ returns HTTP 200 with all three columns, 81 TASK ids, correct <title>, and zero external refs. AC3 satisfied.
<!-- SECTION:NOTES:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: @claude
created: 2026-08-04 09:31
---
AC3 (published URL serves the board) is pending: it needs the branch pushed and repo Settings->Pages->Source set to "GitHub Actions". Left In Progress until that live deploy is confirmed.
---
<!-- COMMENTS:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified end to end. Local: build script produces a self-contained _site/index.html with all columns + tasks, offline. Workflow: actionlint clean, workflow_dispatch present, ci.yml untouched. Live: after enabling Pages (build_type=workflow), the deploy workflow succeeded and https://carlessanagustin.github.io/ingest-memory-rag/ serves the board (HTTP 200, 3 columns, 81 tasks, no external resources).
<!-- SECTION:FINAL_SUMMARY:END -->
