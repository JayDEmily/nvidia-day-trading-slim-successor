# 2026-03-20 — Experiment persistence, allocator, and batch ranking pass

## Scope

This pass implements the next sandbox-safe tranche after replay/risk/logging:

- persist experiment runs rather than returning ad hoc summaries only;
- add SLV walk-forward and fragility experiment services;
- add multi-config batch experiment ranking;
- add module/regime capital allocation driven by persisted experiment outputs;
- deepen failure-mode extraction from walk-forward and fragility results.

## Implemented

### Database

- Added `experiment_run` persistence model in `src/nvda_desk/db/models.py`.
- Added Alembic migration `alembic/versions/20260320_0004_experiment_run.py`.

### Schemas

- Expanded `src/nvda_desk/schemas/eval.py` with:
  - walk-forward contracts;
  - fragility contracts;
  - batch-ranking contracts;
  - experiment-run payloads;
  - failure-mode summaries.
- Added `src/nvda_desk/schemas/allocation.py` for module/regime capital allocation.

### Services

- Added `src/nvda_desk/services/experiment_log.py`.
- Added `src/nvda_desk/services/slv_experiments.py`.
- Added `src/nvda_desk/services/capital_allocator.py`.

### API surface

- `GET /evals/experiments`
- `POST /evals/strategic-ladder-validator/walk-forward-from-market`
- `POST /evals/strategic-ladder-validator/fragility-from-market`
- `POST /evals/strategic-ladder-validator/batch-rank-from-market`
- `POST /allocation/module-regime`

## Verification

Commands actually run:

- `uv sync --extra dev`
- `ruff check src tests`
- `mypy src tests`
- `pytest -q`
- `make check`
- `DATABASE_URL=sqlite+pysqlite:////tmp/nvda_experiments.db alembic upgrade head`
- `DATABASE_URL=sqlite+pysqlite:////tmp/nvda_experiments.db alembic upgrade head --sql`

Observed results:

- `pytest -q` → `36 passed in 7.27s`
- `make check` → `36 passed in 5.46s`
- Alembic upgraded through revision `20260320_0004`

Direct smoke outputs:

- walk-forward route returned HTTP `200` with:
  - `evaluation_count = 3`
  - `average_forward_score = 0.1667`
  - failure mode `no_fills` at share `0.6667`
- fragility route returned HTTP `200` with:
  - `fragility_score = 0.2`
  - `worst_case_drop = 0.5`
  - failure mode `rejection_prone` at share `1.0`
- batch-ranking route returned HTTP `200` with top variant:
  - `name = base`
  - `ranking_score = 0.2517`
- allocator route returned HTTP `200` with:
  - `cash_reserve_pct = 40.0`
  - `allocation_pct = 60.0`
  - allocator reasons including `average_forward_score_below_floor`
- experiment listing returned HTTP `200` with `7` persisted experiment rows for `slv-v3-replay`

## Boundary kept

Not claimed in this pass:

- live IBKR integration;
- external market-data subscriptions;
- Docker/Postgres runtime verification beyond offline Alembic SQL and SQLite upgrade;
- real fill/slippage realism.
