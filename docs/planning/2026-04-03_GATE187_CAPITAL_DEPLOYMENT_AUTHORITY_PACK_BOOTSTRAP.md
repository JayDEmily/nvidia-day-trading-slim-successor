# 2026-04-03_GATE187_CAPITAL_DEPLOYMENT_AUTHORITY_PACK_BOOTSTRAP

Status: drafted on `work/gate-187-capital-deployment-authority-pack-20260403`; planning-pack bootstrap receipt pending validation and commit

## What Gate 187 does

Gate 187 is the planning bootstrap for the capital-deployment authority foundation pack. It installs the active planning quartet and scope note, routes the repo from "no active pack" to Gate 188, and freezes a bounded first slice for a new downstream `CapitalDeploymentAuthorityService`.

## Truth frozen by this bootstrap

- the first slice is **not** a full arbiter
- the first slice is **not** close-position logic
- the first slice is **not** recommendation-memory logic
- the first slice is a bounded new-opening capital authoriser that consumes current available capital plus the already-formed opportunity/risk result
- vocabulary admission for the new naming is required later and has deliberately been left as future leaf work rather than being faked as already canonical

## What Gate 187 did not do

- it did not edit runtime behaviour under `src/`
- it did not change packet or schema code
- it did not admit new vocabulary yet
- it did not implement the service yet

## Planned validation slice

- `python -m pytest -q tests/test_gate187_capital_deployment_authority_pack_planning.py tests/test_tranche_briefing_template_pack.py tests/test_planning_state_integrity.py tests/test_document_hygiene.py`

## Planned next active gate

- Gate 188 — authority boundary, vocabulary admission, and decision contract
