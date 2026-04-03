# 2026-04-03_GATE183_RAW_OPTION_SURFACE_PARITY

## Purpose

Align any persisted/API surface that claims to expose raw option rows with the richer runtime contract actually consumed by the real-data loader.

## What changed

- added nullable `iv`, `delta`, and `gamma` to `OptionSnapshot` in `src/nvda_desk/db/models.py`
- added the same fields to `OptionSnapshotPayload` in `src/nvda_desk/schemas/options.py`
- threaded the fields through `src/nvda_desk/services/market_state.py`, `src/nvda_desk/services/slv_market.py`, `src/nvda_desk/fixtures.py`, and `src/nvda_desk/db/seed.py`
- added migration `alembic/versions/20260403_0007_option_snapshot_raw_row_contract.py`

## Definition-of-done evidence

- persisted raw option rows can now lawfully carry the per-row fields the runtime consumes
- API retrieval exposes those fields instead of silently pretending a reduced payload is a raw-row payload

## Proof surfaces

- `tests/test_gate183_option_surface_raw_contract.py`
- `tests/test_api.py`
