# 2026-03-18 Module Registry and Promotion Pass 4

## Scope
Add persisted module specs, promotion decisions, and evaluation-run listing to the local executable repo.

## What changed
- Added `module_spec` and `promotion_decision` tables to the local SQLAlchemy model set.
- Added typed contracts for module spec creation/listing and promotion decision creation/listing.
- Added `ModuleRegistryService` and `PromotionService`.
- Added API routes:
  - `POST /modules/specs`
  - `GET /modules/specs`
  - `POST /modules/promotions`
  - `GET /modules/promotions`
  - `GET /evals/runs`
- Updated `README.md` so the current API surface matches the actual repo state.

## Verified
- `ruff check src tests` -> pass
- `mypy src tests` -> pass
- `pytest -q` -> `21 passed`
- manual smoke with `.venv/bin/python` + `TestClient`:
  - `spec_id = 1`
  - `promotion_to = coded`
  - `eval_id = 1`
  - `eval_count = 1`

## Result
The repo now has an auditable local path for:
`module spec -> evaluation run -> promotion decision`
