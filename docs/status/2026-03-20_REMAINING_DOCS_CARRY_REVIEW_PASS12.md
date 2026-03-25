# 2026-03-20 — Remaining docs, carry replay, review packets, and admin wrappers (pass 12)

## Scope
Finish the ready/todo V2 leaves without drifting into live integrations:
- remaining legacy-doc extraction artefacts;
- overnight carry replay weekend/event-window extension;
- backend review packets over second-wave execution records;
- docs/code reconciliation;
- admin-only CLI wrappers.

## What this pass materially added

### Remaining-doc extraction artefacts
- Added `backlog/remaining_legacy_source_inventory.jsonl`.
- Added `backlog/legacy_data_fixtures_manifest.jsonl`.
- Added `backlog/legacy_feature_backlog_additions.jsonl`.
- Added `backlog/legacy_module_backlog_additions.jsonl`.
- Added `docs/legacy/LEGACY_FAILURE_PATTERNS_REMAINING_DOCS.md`.
- Added `docs/planning/2026-03-18_REMAINING_DOCS_PROMOTION_RECOMMENDATION.md`.
- Refreshed `docs/legacy/REMAINING_DOCS_PAGE_MAP.md` with frozen source inventory language.

### Carry replay extension
- Added `OvernightCarryReplayService` in `src/nvda_desk/services/carry_replay.py`.
- Added replay contracts in `src/nvda_desk/schemas/overnight.py`.
- Added route:
  - `POST /evals/overnight-carry-evaluator/replay-from-market`
- Replay now compares:
  - `flatten`
  - `hold_baseline`
  - `follow_recommendation`
- Output now carries:
  - `weekend_window`
  - `event_window_open`
  - `next_session_open_ts`
  - `next_session_reference_source`

### Review packet surfaces
- Added `src/nvda_desk/schemas/review.py`.
- Added `src/nvda_desk/services/review_packets.py`.
- Added routes:
  - `GET /review/module-health/{module_id}`
  - `GET /review/daily-packet`
- Review packets now summarize:
  - evaluation count
  - experiment count
  - signal/veto/risk-block/order/fill counts
  - latest daily PnL
  - recent events
  - current positions / account state

### Docs/code reconciliation
- Updated `docs/planning/CONFIG_AND_VARIANTS_CROSSWALK.md` so it reflects the now-real typed config surfaces instead of claiming config remains example-only.

### Admin wrappers
- Extended `src/nvda_desk/cli.py` with:
  - `legacy-source-inventory`
  - `legacy-fixture-summary`
  - `carry-replay`
  - `review-daily-packet`
- Added `src/nvda_desk/services/legacy_extraction.py` for offline artefact summaries.
- Hardened `Makefile` so `make check` and friends use `python -m ...` module entrypoints instead of stale venv shebangs after zip extraction.

## Verification performed
- `uv sync --extra dev`
- `.venv/bin/python -m ruff check src tests`
- `.venv/bin/python -m mypy src tests`
- `.venv/bin/python -m pytest -q` → `46 passed in 8.75s`
- `make check` → `46 passed in 9.55s`
- `NVDA_DESK_DATABASE_URL=sqlite+pysqlite:////tmp/nvda_pass12_alembic.db .venv/bin/python -m alembic upgrade head`
- `NVDA_DESK_DATABASE_URL=sqlite+pysqlite:////tmp/nvda_pass12_alembic.db .venv/bin/python -m alembic upgrade head --sql`
- Direct API smoke via `TestClient`:
  - carry replay returned `best_path_name = flatten`, `event_window_open = true`, `next_session_reference_source = derived_from_last_close`
  - module-health returned signal count `1` and order-event count `2`
  - daily review packet returned trade count `1`, module-health count `1`, recent-events count `1`
- Direct CLI smoke:
  - `legacy-source-inventory` returned document count `4`
  - `carry-replay` returned `next_session_open_ts = 2026-03-19T13:30:00Z`

## Honest limits
Still not verified here:
- live IBKR
- live OpenAI Responses API orchestration
- Docker-backed Postgres runtime
- real overnight market-open truth for next session beyond seeded / derived sandbox references

## Practical state after this pass
The V2 leaf ledger is now fully exhausted:
- legacy extraction artefacts frozen;
- carry replay extended;
- review packet surfaces present;
- docs reconciled;
- admin wrappers added.
