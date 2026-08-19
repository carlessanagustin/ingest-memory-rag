---
id: TASK-112
title: Move CI workflows to Python 3.14
status: Done
assignee:
  - '@claude'
created_date: '2026-08-19 10:41'
updated_date: '2026-08-19 10:46'
labels:
  - ci
  - python
dependencies:
  - TASK-111
ordinal: 114000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Align the GitHub Actions workflows with the 3.14-only move. In .github/workflows/ci.yml set the lint job python-version to 3.14, replace the unit test matrix ["3.11","3.12"] with ["3.14"], and set the integration job python-version to 3.14. In .github/workflows/pages.yml bump the Python used for the board build (currently 3.12) to 3.14 so `uv run` in scripts/build_board_site.sh satisfies requires-python>=3.14. Recommended subagent: sherpa:devooops (CI/GitHub Actions).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 ci.yml: the unit test matrix python-version is exactly ["3.14"]; the lint and integration jobs use python-version 3.14; no "3.11" or "3.12" python-version remains
- [x] #2 pages.yml uses Python 3.14 for the board build
- [x] #3 Both workflow files remain valid YAML and otherwise unchanged in structure
- [x] #4 Note recorded: the unit matrix still runs ubuntu/macos/windows — flag if any 3.14 wheel (e.g. onnxruntime) is unavailable on a non-linux runner
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. ci.yml: lint job python-version 3.12->3.14; test matrix ["3.11","3.12"]->["3.14"]; integration job 3.12->3.14.
2. pages.yml: board-build python 3.12->3.14 (so uv run satisfies requires-python>=3.14).
3. Verify: no 3.11/3.12 python-version remains in ci.yml; matrix is exactly ["3.14"]; pages.yml is 3.14; both files still valid YAML.
4. Record the macOS/Windows 3.14-wheel note (matrix keeps all three OSes).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
ci.yml: lint job python-version 3.12->3.14, unit test matrix ["3.11","3.12"]->["3.14"], integration job 3.12->3.14. pages.yml: board-build setup-uv python-version 3.12->3.14 (so `uv run` in scripts/build_board_site.sh satisfies requires-python>=3.14). grep confirms no 3.11/3.12 python-version remains; both files parse as valid YAML; job structure otherwise unchanged. RISK NOTE: the unit matrix keeps os=[ubuntu, macos, windows] with python 3.14. 3.14 wheels are confirmed for x86_64 linux and (locally) macOS-arm64 for onnxruntime/pydantic-core/tokenizers/numpy; the GitHub windows and macos runners should also have them, but onnxruntime is the most likely to lag for a new Python. If a non-linux 3.14 wheel is missing, that matrix job would fail on push (Docker/linux build is unaffected); mitigation would be to drop the non-linux OSes or wait for the wheel.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Moved the GitHub Actions workflows to Python 3.14: ci.yml lint/matrix/integration all 3.14 (unit matrix = ["3.14"]) and pages.yml board build 3.14. Verified via grep (no 3.11/3.12) and a YAML parse. Flagged the non-linux 3.14-wheel risk (onnxruntime) since the matrix keeps ubuntu/macos/windows.
<!-- SECTION:FINAL_SUMMARY:END -->
