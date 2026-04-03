# 2026-04-03_GATE188_CAPITAL_DEPLOYMENT_AUTHORITY_CONTRACT

## Purpose

Freeze the bounded first-slice contract for capital-deployment authority before service code and runtime integration proceed.

## Completed work

- froze the first-slice boundary as new-opening capital authorisation only
- admitted `Capital Deployment Authority Service` and `Capital Deployment Authority Decision` into the canonical vocabulary dictionary
- added the typed `CapitalDeploymentAuthorityInput` and `CapitalDeploymentAuthorityDecision` contracts
- updated the domain and architecture docs to mirror the bounded contract and runtime placement

## Key scope holds

- new-opening capital authorisation only
- no recommendation-memory lookback logic
- no close-position logic
- no full arbiter or cross-book portfolio brain

## Evidence

- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `src/nvda_desk/schemas/cognition.py`
- `tests/test_gate188_capital_deployment_authority_contract.py`

Vocabulary admission landed before code used the term.
