---
id: TASK-68
title: Add a GitHub Actions workflow to build and deploy the board to GitHub Pages
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 07:26'
updated_date: '2026-08-04 09:31'
labels:
  - ci
dependencies:
  - TASK-67
ordinal: 70000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add a workflow that builds the static Kanban board (via the TASK-67 script) and deploys it to GitHub Pages using the GitHub Actions Pages mechanism (upload-pages-artifact + deploy-pages), on push to main and on demand. Outcome: the published board at https://carlessanagustin.github.io/ingest-memory-rag/ refreshes automatically when backlog task files change on main.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 New workflow file .github/workflows/pages.yml, separate from and not breaking the existing ci.yml
- [x] #2 Triggers: push to main limited to relevant paths (backlog/**, the build script, and .github/workflows/pages.yml) plus workflow_dispatch
- [x] #3 Uses the GitHub Actions Pages flow: actions/upload-pages-artifact + actions/deploy-pages, with permissions pages: write, id-token: write, contents: read, and the github-pages environment
- [x] #4 Installs the Backlog.md CLI, runs the TASK-67 build script to produce _site/, and uploads _site/ as the Pages artifact
- [x] #5 A concurrency group (e.g. "pages") serializes deploys so runs do not overlap
- [x] #6 Workflow is valid YAML and passes actionlint; action major versions are consistent with the existing ci.yml (checkout@v7 etc.)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
.github/workflows/pages.yml: push to main (paths backlog/**, script, workflow) + workflow_dispatch; permissions contents:read/pages:write/id-token:write; concurrency pages cancel-in-progress:false; github-pages env; job: checkout@v7 (fetch-depth 0), setup-node + npm i -g backlog.md, setup-uv@v9.0.0, run build script, configure-pages@v5, upload-pages-artifact@v3 (_site), deploy-pages@v4.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added .github/workflows/pages.yml (separate from ci.yml): triggers push to main on backlog/**+script+workflow and workflow_dispatch; GitHub-Actions Pages flow (configure/upload-pages-artifact/deploy-pages) with pages:write+id-token:write+contents:read and the github-pages environment; concurrency group pages (no cancel); installs backlog.md + uv and runs the build script to produce/upload _site. Action majors match ci.yml (checkout@v7, setup-uv@v9.0.0). Verified: YAML parses, actionlint exits 0, ci.yml untouched.
<!-- SECTION:FINAL_SUMMARY:END -->
