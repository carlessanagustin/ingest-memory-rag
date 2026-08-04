---
id: TASK-67
title: Add a build script that exports the Kanban board to a static HTML site
status: Done
assignee:
  - '@claude'
created_date: '2026-08-04 07:25'
updated_date: '2026-08-04 09:31'
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
- [x] #1 A committed script (e.g. scripts/build_board_site.sh) runs `backlog board export` to capture the current Kanban board as Markdown
- [x] #2 The script renders that Markdown into _site/index.html that is self-contained (inline CSS, no external CDN or network fetch needed to view)
- [x] #3 The generated page shows all configured columns (To Do, In Progress, Done) with their tasks
- [x] #4 Re-running the script is idempotent: it regenerates _site/ cleanly and is safe to run repeatedly
- [x] #5 _site/ is git-ignored (build output, never committed)
- [x] #6 The script fails fast on error (set -euo pipefail or equivalent) and requires no secrets
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. scripts/build_board_site.sh (set -euo pipefail): cd repo root; rm -rf _site && mkdir -p _site; backlog board export _site/board.md --force; render to _site/index.html via `uv run --with markdown python` (tables ext, self-contained inline CSS); rm board.md. 2. Add _site/ to .gitignore.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added scripts/build_board_site.sh: runs `backlog board export` then renders the Markdown board to a self-contained _site/index.html (inline CSS, light/dark, sticky headers, horizontal scroll) via uv+markdown; rm -rf _site each run makes it idempotent; set -euo pipefail; no secrets. _site/ added to .gitignore. Verified: script exits 0, _site/index.html contains all 3 columns + 81 TASK ids and zero external http(s) refs; second run rebuilds cleanly.
<!-- SECTION:FINAL_SUMMARY:END -->
