# 2026-03-20 Config + Boundary Completion Pass 10

## Scope
Complete the four remaining sandbox leaves without superseding the existing planning stack:
- LEAF-CONFIG-003
- LEAF-CONFIG-004
- LEAF-BOUNDARY-001
- LEAF-BOUNDARY-002

## What changed

### Config wiring
- Promoted the example config files into typed runtime/evaluator/coefficient/variant surfaces.
- Added config routes:
  - `GET /config/runtime-settings`
  - `GET /config/evaluation-settings`
  - `GET /config/coefficients`
  - `GET /config/coefficients/{group_key}`
  - `GET /config/strategy-variants`
  - `GET /config/strategy-variants/{variant_name}`
- Added a config-surface service that resolves supported sandbox overrides.

### Coefficients registry wiring
- `S06` can now drive supported VIX caution/hot thresholds in replay/allocation.
- `S08` can now drive supported VWAP-distance soft limits in replay.
- Allocation can consume registry weights via `config_key` and apply strategy-variant weight overrides.

### Strategy variants wiring
- Batch ranking can now accept named variants via `variant_names`.
- Walk-forward and fragility inputs can now consume `strategy_variant_name` and `coefficient_group_name`.
- Unknown strategy variants and coefficient groups now return clean `404` responses at the API boundary.

### Boundary preservation
- Added typed offline-only boundary protocols for:
  - broker adapter
  - OpenAI orchestrator
- Added offline stub implementations only.
- No live OpenAI Responses API call was attempted.
- No live IBKR connectivity was attempted.

## Verification run
- `uv sync --extra dev`
- `ruff check src tests`
- `mypy src tests`
- `pytest -q`
- `make check`
- `NVDA_DESK_DATABASE_URL=sqlite+pysqlite:////tmp/nvda_boundary.db .venv/bin/alembic upgrade head`
- `NVDA_DESK_DATABASE_URL=sqlite+pysqlite:////tmp/nvda_boundary.db .venv/bin/alembic upgrade head --sql`
- direct TestClient smoke for config routes, named variant batch ranking, allocator weight override, and unknown variant handling

## Direct smoke outputs
- `/config/runtime-settings` -> `200`, symbol `NVDA`, broker primary `ibkr`
- `/config/coefficients/S08` -> `200`, supported overrides `['distance_to_vwap_soft_limit_pct']`
- `/config/strategy-variants/conservative` -> `200`, supported overrides include `entry_gate_score_floor`, `zone_score_threshold`, `risk_budget_remaining_pct`, `allocation_weight_overrides`
- named-variant batch ranking -> `200`, ranked variants `['vwap-plus', 'baseline', 'conservative']`
- allocator with `strategy_variant_name=conservative` and `config_key=S06` -> `200`, reasons include `variant_weight_override_applied`, `cash_reserve_pct=40.0`
- unknown variant batch ranking -> `404`, detail `unknown strategy variant: unknown-variant`

## Explicitly unverified
- live IBKR behaviour
- live OpenAI Responses API integration
- Docker/Postgres runtime boot
- real vendor market-data subscriptions
