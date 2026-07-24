---
id: TASK-8
title: Add an MIT license to the project
status: Done
assignee:
  - '@claude'
created_date: '2026-07-23 15:54'
updated_date: '2026-07-24 08:24'
labels: []
dependencies: []
ordinal: 10000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The project has no license, leaving usage terms undefined. Add the MIT license so terms are explicit. Copyright holder: Carles San Agustin; year: 2026. Keep the LICENSE file and project metadata consistent.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A LICENSE file at the repo root contains the standard MIT License text with copyright year 2026 and holder Carles San Agustin
- [x] #2 pyproject.toml declares the MIT license consistently (e.g. the license field and/or the OSI MIT classifier) matching the LICENSE file
- [x] #3 The README has a short License section stating the project is MIT-licensed and pointing to the LICENSE file
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add LICENSE at repo root: standard MIT License text, copyright "2026 Carles San Agustin". 2. pyproject.toml: declare MIT via SPDX license = "MIT" + license-files = ["LICENSE"] (fall back to license table + OSI classifier if hatchling rejects SPDX). 3. README: add a short "## License" section pointing to LICENSE. 4. Verify: uv sync rebuilds the project (pyproject valid) and package metadata shows MIT; LICENSE + README section present.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added LICENSE (MIT, copyright 2026 Carles San Agustin), declared license = MIT (SPDX) + license-files = [LICENSE] in pyproject.toml, and added a License section to the README. Verified: uv sync rebuilds the project cleanly (hatchling accepts the SPDX field) and package metadata reports License-Expression: MIT.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added an MIT LICENSE (2026 Carles San Agustin), declared the license in pyproject.toml via the SPDX license field plus license-files, and added a README License section linking to LICENSE. Verified via uv sync + package metadata (License-Expression: MIT).
<!-- SECTION:FINAL_SUMMARY:END -->
