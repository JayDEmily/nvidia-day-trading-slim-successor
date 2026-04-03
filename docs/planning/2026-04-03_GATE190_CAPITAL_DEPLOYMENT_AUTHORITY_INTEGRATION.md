# 2026-04-03_GATE190_CAPITAL_DEPLOYMENT_AUTHORITY_INTEGRATION

## Purpose

Thread the bounded capital-deployment authority decision into the lawful downstream runtime seam without creating a new binding stage.

## Completed work

- added optional current-capital ingress to `DeskCognitionRuntime.run(...)`
- evaluated capital-deployment authority only after the already-formed opening candidate and final risk join exist
- carried the additive decision on `DeskCognitionRuntimeResult`, `ReviewExplanationInput`, `ReviewExplanationOutput`, and `review_packet`
- kept DMP v2 stage-packet construction at seven binding stages

## Key scope holds

- the new service is additive and downstream
- it does not change the serial seven-stage runtime order
- it does not replace posture, eligibility, execution, or the independent parallel-risk lane

## Evidence

- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/review_explanation.py`
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`
- `tests/test_gate190_capital_deployment_authority_integration.py`
