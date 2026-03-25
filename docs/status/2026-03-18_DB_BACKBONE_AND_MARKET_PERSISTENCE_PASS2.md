# 2026-03-18 DB backbone and market persistence pass 2

## Scope
This pass moved the executable repo beyond pure in-memory services.

## What changed
- Added a lightweight SQLAlchemy persistence path under `src/nvda_desk/db/`.
- Added `Instrument` and `Bar1m` models.
- Added `create_schema()` and `seed_dev_data()` for local development.
- Added a Typer CLI with:
  - `python -m nvda_desk.cli init-db`
  - `python -m nvda_desk.cli seed-dev`
- Updated `MarketStateService` to read the latest bar and bounded intraday bars from persisted storage.
- Added `/market/intraday` API route.
- Updated `README.md`, `.env.example`, `Makefile`, and `.gitignore`.
- Added tests covering seeded persistence and API reads backed by SQLite.

## Verified in sandbox
```bash
make check
make init-db
make seed-dev
```

Observed results:
- `make check` -> `15 passed`
- `make init-db` -> `initialized_database=sqlite+pysqlite:///./var/nvda_desk_dev.db`
- `make seed-dev` -> `DevSeedSummary(instrument_count=4, bar_count=24)`

## What is still not done
- PostgreSQL engine and Alembic migrations are still not wired.
- No research/eval persistence yet.
- No live market ingestion.
- No IBKR adapter.
- No replay attribution persisted by session phase.

## Next gate
Promote the lightweight DB path into the intended architecture:
1. Postgres/Alembic migration base.
2. Persist research/eval artefacts.
3. Add replay outputs grouped by session clock phase.
