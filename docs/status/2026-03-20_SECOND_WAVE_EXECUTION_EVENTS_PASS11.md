# 2026-03-20 — Second-wave execution and events pass 11

## Scope
Add the next sandbox-safe architectural tranche without touching live IBKR, live OpenAI, MCP, frontend, or real vendor integrations.

## Implemented
- Added canonical second-wave database records:
  - `session_calendar`
  - `market_event`
  - `module_signal_event`
  - `module_veto_event`
  - `risk_block_event`
  - `order_intent`
  - `order_event`
  - `fill_event`
  - `position_snapshot`
  - `capital_state_snapshot`
  - `daily_pnl_report`
- Added Alembic migration `20260320_0005_second_wave_records.py`.
- Seeded baseline session-calendar and market-event rows in dev seed.
- Added `/events/*` surfaces:
  - `POST /events/calendar`
  - `GET /events/calendar`
  - `POST /events/market`
  - `GET /events/market`
  - `GET /events/proximity`
- Added `/execution/*` surfaces:
  - `POST /execution/signals`
  - `GET /execution/signals`
  - `POST /execution/vetoes`
  - `GET /execution/vetoes`
  - `POST /execution/risk-blocks`
  - `GET /execution/risk-blocks`
  - `POST /execution/daily-pnl`
  - `GET /execution/daily-pnl`
- Added `/broker/*` offline surfaces backed by persisted records:
  - `POST /broker/orders/paper`
  - `GET /broker/order-events`
  - `GET /broker/fill-events`
  - `GET /broker/positions`
  - `GET /broker/account-state`
- Added second-wave integration tests for events, execution records, broker paper fills, and daily P&L persistence.

## Verification
- `uv sync --extra dev`
- `.venv/bin/ruff check src tests`
- `.venv/bin/mypy src tests`
- `.venv/bin/pytest -q`
- `make check`
- `NVDA_DESK_DATABASE_URL=sqlite+pysqlite:////tmp/nvda_secondwave.db .venv/bin/alembic upgrade head`
- `NVDA_DESK_DATABASE_URL=sqlite+pysqlite:////tmp/nvda_secondwave.db .venv/bin/alembic upgrade head --sql`

## Explicitly not claimed
- live IBKR connectivity
- live OpenAI Responses API execution
- realistic live fill/slippage semantics
- Docker/Postgres runtime verification
