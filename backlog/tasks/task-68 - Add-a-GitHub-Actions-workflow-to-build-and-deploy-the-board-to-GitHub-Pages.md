---
id: TASK-68
title: Add a GitHub Actions workflow to build and deploy the board to GitHub Pages
status: To Do
assignee: []
created_date: '2026-08-04 07:26'
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
- [ ] #1 New workflow file .github/workflows/pages.yml, separate from and not breaking the existing ci.yml
- [ ] #2 Triggers: push to main limited to relevant paths (backlog/**, the build script, and .github/workflows/pages.yml) plus workflow_dispatch
- [ ] #3 Uses the GitHub Actions Pages flow: actions/upload-pages-artifact + actions/deploy-pages, with permissions pages: write, id-token: write, contents: read, and the github-pages environment
- [ ] #4 Installs the Backlog.md CLI, runs the TASK-67 build script to produce _site/, and uploads _site/ as the Pages artifact
- [ ] #5 A concurrency group (e.g. "pages") serializes deploys so runs do not overlap
- [ ] #6 Workflow is valid YAML and passes actionlint; action major versions are consistent with the existing ci.yml (checkout@v7 etc.)
<!-- AC:END -->
