---
id: TASK-67
title: Add a build script that exports the Kanban board to a static HTML site
status: To Do
assignee: []
created_date: '2026-08-04 07:25'
labels:
  - ci
dependencies: []
ordinal: 69000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Produce a committed script that turns the Backlog.md Kanban board into a static, self-contained HTML page suitable for GitHub Pages. This is required because `backlog browser` is a live server bound to 127.0.0.1 that Pages (static-only) cannot host; `backlog board export` gives us a static Markdown board we can render instead. Outcome: a repeatable local/CI build that generates the site output consumed by the Pages workflow.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 A committed script (e.g. scripts/build_board_site.sh) runs `backlog board export` to capture the current Kanban board as Markdown
- [ ] #2 The script renders that Markdown into _site/index.html that is self-contained (inline CSS, no external CDN or network fetch needed to view)
- [ ] #3 The generated page shows all configured columns (To Do, In Progress, Done) with their tasks
- [ ] #4 Re-running the script is idempotent: it regenerates _site/ cleanly and is safe to run repeatedly
- [ ] #5 _site/ is git-ignored (build output, never committed)
- [ ] #6 The script fails fast on error (set -euo pipefail or equivalent) and requires no secrets
<!-- AC:END -->
