# 2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_DOCUMENT_TOUCH_CHECKLIST_v1

Status: capital-deployment authority foundation pack closed through Gate 191 on `main`

## Frozen/process surfaces that must move if this pack changes them

- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`

## Live routing and planning surfaces that must move before closeout

- `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_GATES_v1.md`
- `docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_LEAVES_v1.json`
- `docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_EXECUTION_LOG_v1.md`
- `docs/planning/2026-04-03_GATE187_CAPITAL_DEPLOYMENT_AUTHORITY_PACK_BOOTSTRAP.md`

## Authority surfaces likely to move in later gates

- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`

## Runtime/schema/test surfaces likely to move in later gates

- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/execution_records.py`
- `src/nvda_desk/services/capital_deployment_authority.py` or equivalent service path
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/schemas/dmp_v2.py` only if the admitted contract requires packet carriage
- `tests/test_gate187_capital_deployment_authority_pack_planning.py`
- `tests/test_gate188_capital_deployment_authority_contract.py`
- `tests/test_gate189_capital_deployment_authority_service.py`
- `tests/test_gate190_capital_deployment_authority_integration.py`

## Explicit exclusions preserved by this checklist

- close-position and lifecycle logic remain out of scope for this pack
- recommendation-history persistence remains out of scope for this pack
- a brand-new capital JSON ledger architecture is not required for v1 if the repo-native capital snapshot path suffices


## Current planned sequence

capital-deployment authority foundation pack closed through Gate 191 on `main`.
