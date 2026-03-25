# 2026-03-19 — Sandbox Execution Pass 7

## Scope
Executed the next ordered work packages from `PLANS.md` and `docs/planning/2026-03-19_SANDBOX_EXECUTION_TO_EXHAUSTION_PLAN.md` without pausing after the first step.

## What this pass materially added

### Fixture pack completion
- Added machine-readable VWAP case fixtures at `fixtures/legacy/vwap_cases/admitted_cases.jsonl`.
- Added fixture loaders in `src/nvda_desk/fixtures.py`.
- Updated `fixtures/legacy/fixtures_manifest.jsonl` with the new admitted fixture entry.

### SLV replay and attribution
- Added `StrategicLadderReplayService` in `src/nvda_desk/services/slv_replay.py`.
- Added replay schemas, supervisory overlay schema, and rung outcome attribution in `src/nvda_desk/schemas/slv.py`.
- Added routes:
  - `POST /modules/strategic-ladder-validator/replay-from-market`
  - `POST /evals/strategic-ladder-validator/replay-from-market`
- Replay now produces:
  - rung fill detection,
  - phase-at-fill,
  - favorable/adverse excursion,
  - closing return,
  - outcome labels,
  - supervisory overlay action.

### Macro / volatility supervisory overlays
- Added typed risk-policy inputs and decisions in `src/nvda_desk/schemas/risk.py`.
- Added `RiskGatewayService` in `src/nvda_desk/services/risk_gateway.py`.
- Added persistence for risk decisions via `risk_decision_log`.
- Added API routes:
  - `POST /risk/evaluate`
  - `GET /risk/decisions`
- Added Alembic revision `20260319_0003_risk_decision_log.py`.

### Session-clock hardening
- Session phase now appears explicitly in SLV replay outputs (`entry_phase`, `phase_at_fill`).
- Added tests proving phase-sensitive behaviour for the same SLV ladder.

### Overnight Carry Evaluator promotion
- Added `OvernightCarryMarketService` in `src/nvda_desk/services/carry_market.py`.
- Added market-backed carry schemas in `src/nvda_desk/schemas/overnight.py`.
- Added routes:
  - `POST /modules/overnight-carry-evaluator/evaluate-from-market`
  - `POST /evals/overnight-carry-evaluator/from-market`
- Market-backed carry now derives:
  - close distance to VWAP,
  - realized vol,
  - VIX level,
  - VVIX level,
  - session phase.

### Replay / eval strengthening
- Added persisted replay-backed SLV eval logging through the existing `evaluation_run` surface.
- Added persisted carry market eval logging through the existing `evaluation_run` surface.

### Config wiring discipline
- Added typed config document loaders in `src/nvda_desk/config_models.py`.
- Added tests that type-load all four salvaged config example YAML files.

### Seed / market-state improvements
- `seed_dev_data()` now seeds `VIX` and `VVIX` bar series in addition to `NVDA`.
- Instrument count moved to `5`; total seeded bar count moved to `720`.
- Legacy options seeding now uses the fixture loader rather than inline CSV parsing.

## Verification performed
- `uv sync --extra dev`
- `make check` → `33 passed in 5.02s`
- `make init-db`
- `make seed-dev` → `DevSeedSummary(instrument_count=5, bar_count=720, option_snapshot_count=18)`
- Alembic upgrade on clean SQLite DB:
  - `20260318_0001`
  - `20260319_0002`
  - `20260319_0003`
- Offline Alembic SQL generation succeeded.
- Direct API smoke with `TestClient`:
  - SLV replay route returned `supervisory_overlay.action = allow` and `evaluated_bar_count = 21`
  - Carry market route returned `carry_recommendation = hold_small` with `derived_context.vix_level = 20.6`
  - Risk route returned `action = block` with reason `volatility_shock_block`

## Honest limits
Still not verified in this sandbox:
- live Postgres boot via Docker,
- live OpenAI orchestration,
- IBKR,
- MCP/front-end,
- real market data subscriptions.

## Practical state after this pass
The repo is now substantially beyond the earlier skeleton:
- fixture-backed,
- replay-capable for SLV,
- risk-gated,
- market-backed for carry,
- and green locally.

The next environment-facing work is now much more about external integration than about repo shape.
