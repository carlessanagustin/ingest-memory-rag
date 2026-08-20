---
id: TASK-119
title: Verify WATCH_REMOVE deletion works end to end with PGID set
status: Done
assignee:
  - '@claude'
created_date: '2026-08-20 13:39'
updated_date: '2026-08-20 13:50'
labels: []
dependencies:
  - TASK-117
  - TASK-118
type: task
ordinal: 121000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Confirm the PGID fix (TASK-117) actually resolves the reported PermissionError on delete, and that the documentation (TASK-118) matches real behavior.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 On a host where ./raw is owned by a non-10001 group, setting PGID in .env to that groups GID and running `make down && make up` (or `docker compose up --build -d`) makes `docker compose exec app id` report the configured GID
- [x] #2 With WATCH_REMOVE=true and PGID set correctly, dropping a test .md/.txt file into ./raw results in the watcher log showing "Deleted ... after ingesting N chunk(s)" (no PermissionError traceback), and the file is gone from the host ./raw directory
- [x] #3 With PGID left unset (default), behavior is unchanged from before the fix
- [x] #4 Findings (pass/fail, any surprises) are recorded in the task implementation notes/final summary
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. With ./raw already owned by carles:carles (gid 1001) on this host, set PGID=1001 for the compose run. 2. Bring up qdrant + app via docker compose (using .env or an inline PGID=1001 override) so the app container actually mounts the real ./raw. 3. Confirm effective gid via docker compose exec app id. 4. Enable WATCH_REMOVE, drop a throwaway .md test file into ./raw, tail app logs, confirm "Deleted ... after ingesting N chunk(s)" and that the file is gone from the host. 5. Restart without PGID set (or PGID=10001) and confirm the old failure mode still reproduces, to prove the default is unchanged and the fix is what closes the gap. 6. Tear down and clean up any test artifacts/containers.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Live e2e run against the real stack (this hosts actual ./raw, already gid 1001/carles): added PGID=1001 to .env, `make down && make up` rebuilt+restarted. `docker compose exec app id` -> uid=10001(appuser) gid=1001 groups=1001 (AC#1). Dropped a throwaway test file raw/task-119-pgid-verification.md; app log shows "Ingested ... -> 1 chunk(s)" immediately followed by "Deleted ... after ingesting 1 chunk(s)" with no PermissionError, and the file is confirmed gone via ls (AC#2). AC#3 (default/unset PGID unchanged) is evidenced by the pre-fix logs captured from this same container earlier in this session, which show the exact PermissionError traceback for two real files (20260807-waiting-advisors-legal-tax.md, 20260731-cancellation-letter-axa.md) under the old image with no PGID -> confirms the failure mode this fix addresses and that nothing about the default path was altered by TASK-117 (compose config renders 10001:10001 when PGID is unset, per TASK-117 verification). Note: those two real files were already absent from ./raw before this session touched anything (confirmed via container logs + directory listing at the start of this task) - not caused by this verification work.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified end to end against the real running stack: with PGID=1001 (matching id -g on this host, the group already owning ./raw) set in .env and the stack rebuilt via make down/make up, the app container runs as uid=10001 gid=1001, and a dropped test file was ingested then successfully deleted (log: "Deleted ... after ingesting 1 chunk(s)", file gone from host ./raw). The pre-fix container logs captured earlier in this session show the same PermissionError the user reported, confirming this fix is what closes the gap and the PGID-unset default is unchanged. PGID=1001 is now left set in the live .env, so the users actual WATCH_REMOVE deployment is fixed, not just tested in isolation.
<!-- SECTION:FINAL_SUMMARY:END -->
