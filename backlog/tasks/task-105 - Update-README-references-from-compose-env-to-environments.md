---
id: TASK-105
title: Update README references from compose/env to environments
status: Done
assignee:
  - '@claude'
created_date: '2026-08-07 13:33'
updated_date: '2026-08-07 13:36'
labels:
  - docs
  - docker
  - compose
dependencies:
  - TASK-104
ordinal: 107000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update the README so the Per-environment resource sizing section (and any other mention) points at ./environments instead of ./compose/env, keeping the described mechanism accurate (tier .env files selected by DEPLOY_ENV, loaded by make via --env-file, .env last so it can override). Affected spots include the [`compose/env/`](compose/env/) link, the `make` command example, the tune/add-a-tier bullets (e.g. environments/xlarge.env), and the "check the effective values" command. Recommended subagent: general-purpose (documentation).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 No occurrence of `compose/env` remains in README.md; all such references now read `environments`
- [x] #2 The relative link to the folder resolves to environments/ and the example commands use environments/<tier>.env
- [x] #3 The described selection/override mechanism remains accurate and internally consistent (tier first, .env last)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Update the README Per-environment resource sizing section: the [compose/env/](compose/env/) link, the make command example, the tune/add-a-tier bullets (environments/<tier>.env, environments/xlarge.env), and the "check the effective values" command -> all environments/.
2. Verify: grep README.md for compose/env returns nothing; the folder link and example commands resolve to environments/; mechanism (tier first, .env last) stays accurate.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Updated all five README references (folder link, make command example, tune/add-a-tier bullets, and the check-the-effective-values command) from compose/env to environments. Verified: grep for compose/env in README.md returns nothing; the folder link now targets environments/ and example commands use environments/<tier>.env; the tier-first / .env-last ordering and DEPLOY_ENV selection description are unchanged and accurate.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Repointed the README Per-environment resource sizing section from compose/env to environments (5 references). Verified via grep that no compose/env reference remains and the mechanism description stays accurate.
<!-- SECTION:FINAL_SUMMARY:END -->
