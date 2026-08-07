---
id: TASK-101
title: Document per-VPS resource sizing in the README
status: Done
assignee:
  - '@claude'
created_date: '2026-08-07 12:42'
updated_date: '2026-08-07 12:51'
labels:
  - docs
  - docker
  - compose
dependencies:
  - TASK-99
ordinal: 103000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add a short README subsection explaining how to size services per VPS deployment: set DEPLOY_ENV in .env to small|medium|large; each tier lives in compose/env/<tier>.yaml and patches only deploy.resources; medium is the default and equals the previous fixed values; how to tune a tier or add a new one; and that it works transparently through `make up` (no -f juggling) because Compose interpolates DEPLOY_ENV into the include path. Recommended subagent: general-purpose (documentation), or sherpa:docky.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 README has a subsection describing DEPLOY_ENV and the compose/env/*.yaml tier files
- [x] #2 It states the default (medium == previous behaviour), how to switch tiers, and how to edit a tier or add a new one
- [x] #3 The section matches the implemented mechanism and introduces no stale or contradictory claims
- [x] #4 It notes the selection works with `make up` / plain `docker compose up` without extra flags
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Update the stale sentence at README (Compose services) so resource limits point to the compose/env/*.yaml tiers instead of docker-compose.yml, and stop implying lobe-chat is covered by the tiers.
2. Add a "### Per-environment resource sizing" subsection under Setup: what compose/env/{small,medium,large}.yaml are, DEPLOY_ENV selection in .env (default medium), works with make up (no -f), how to tune/add a tier, how to check effective values, and that base files carry no deploy.resources (single source of truth).
3. Verify: headings/anchor render, mechanism matches implementation, no stale/contradictory claims.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added the "### Per-environment resource sizing" subsection under Setup (README) and updated the stale Compose-services sentence so limits point to compose/env/*.yaml (no longer docker-compose.yml, and no longer implying lobe-chat is in the tiers). Verified: the intra-doc link (#per-environment-resource-sizing) matches the heading slug; allowed values small|medium|large + default medium match .env.example; the section documents DEPLOY_ENV selection, make up / plain docker compose up (no -f), tuning/adding a tier, checking effective values with `docker compose config`, and the single-source-of-truth note; grep confirms no remaining stale "resource limits … docker-compose.yml" claim.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Documented per-VPS sizing in the README: a dedicated subsection explaining DEPLOY_ENV (default medium), the compose/env/{small,medium,large}.yaml tiers, transparent make up / docker compose up selection, and how to tune/add a tier; plus fixed the stale limits sentence. Verified anchor, allowed-values consistency with .env.example, and absence of contradictory claims via grep.
<!-- SECTION:FINAL_SUMMARY:END -->
