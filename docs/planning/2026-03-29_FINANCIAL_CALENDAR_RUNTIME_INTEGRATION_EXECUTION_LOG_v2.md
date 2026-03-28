# 2026-03-29 Financial Calendar Runtime Integration Execution Log v2

Status: active execution log for the reviewed financial-calendar runtime-integration tranche; Gate 91 complete on `main`, Gate 92 next

## Purpose

This log records sequential execution receipts for Gates 91-93.

Until a gate begins real execution, this file is only the active receipt surface.
It is not evidence that a gate has already been completed.

## Execution rule

- Record one leaf at a time.
- Record one gate at a time.
- Record branch, start commit, end commit, files touched, validations run, exact evidence, and merge status.
- Do not begin the next gate until the prior gate is complete in the leaf ledger, recorded here, and merged to `main`.

## Maintenance notes

This v2 log exists because the v1 pack was reviewed and found to need tighter leaf granularity.
No execution entries exist yet.

## Entry template

### <LEAF-ID> - <title>

- Branch:
- Start commit:
- End commit:
- Files touched:
- Validations run:
- Full suite required:
- Full suite command/result:
- Exact evidence:
- Stop conditions hit:
- Merge status:
- Notes:

## Entries


### LEAF-G91-001 — Project venue-state facts into desk-calendar authority surfaces

- Branch: `work/gate-91-financial-calendar-canonical-projection-20260329`
- Start commit: `38e176a`
- End commit: `f8c8af4`
- Files touched: `src/nvda_desk/services/financial_calendar_projection.py`, `src/nvda_desk/schemas/events.py`, `src/nvda_desk/services/event_ingestion.py`, `src/nvda_desk/services/event_store.py`, `tests/test_gate91_financial_calendar_canonical_projection.py`, planning control surfaces
- Validations run: targeted Gate 91 projection slice in repo `.venv`
- Full suite required: no
- Full suite command/result: not required for Gate 91 closeout
- Exact evidence: 2026-11-27 half-day desk-calendar authority projection preserves `CalendarClosureClass.HALF_DAY` and `SessionBridgeRule.US_EARLY_CLOSE` for `TradingVenue.NASDAQ_US`.
- Stop conditions hit: none
- Merge status: merged to `main` via fast-forward at `f8c8af4`
- Notes: Gate 91 closeout records one bounded projection tranche rather than pretending thin CRUD sinks became canonical.

### LEAF-G91-002 — Project macro and policy families into canonical event records

- Branch: `work/gate-91-financial-calendar-canonical-projection-20260329`
- Start commit: `38e176a`
- End commit: `f8c8af4`
- Files touched: `src/nvda_desk/services/financial_calendar_projection.py`, `src/nvda_desk/schemas/events.py`, `tests/test_gate91_financial_calendar_canonical_projection.py`
- Validations run: targeted Gate 91 projection slice in repo `.venv`
- Full suite required: no
- Full suite command/result: not required for Gate 91 closeout
- Exact evidence: canonical macro/policy records preserve layer identity, retained tags, and bounded taxonomy under `DeskEventClass.MACRO` and `DeskEventClass.POLICY`.
- Stop conditions hit: none
- Merge status: merged to `main` via fast-forward at `f8c8af4`
- Notes: no free-text taxonomy side channel added.

### LEAF-G91-003 — Project company, peer, and expiry families into canonical event records

- Branch: `work/gate-91-financial-calendar-canonical-projection-20260329`
- Start commit: `38e176a`
- End commit: `f8c8af4`
- Files touched: `src/nvda_desk/services/financial_calendar_projection.py`, `src/nvda_desk/schemas/events.py`, `tests/test_gate91_financial_calendar_canonical_projection.py`
- Validations run: targeted Gate 91 projection slice in repo `.venv`
- Full suite required: no
- Full suite command/result: not required for Gate 91 closeout
- Exact evidence: NVDA earnings and monthly-expiry examples now project into canonical event truth with preserved retained fields and live-event compatibility.
- Stop conditions hit: none
- Merge status: merged to `main` via fast-forward at `f8c8af4`
- Notes: peer/company/expiry remain distinct bounded families.

### LEAF-G91-004 — Project precursor venue-state facts into precursor runtime surfaces

- Branch: `work/gate-91-financial-calendar-canonical-projection-20260329`
- Start commit: `38e176a`
- End commit: `f8c8af4`
- Files touched: `src/nvda_desk/services/financial_calendar_projection.py`, `tests/test_gate91_financial_calendar_canonical_projection.py`
- Validations run: targeted Gate 91 projection slice in repo `.venv`
- Full suite required: no
- Full suite command/result: not required for Gate 91 closeout
- Exact evidence: 2026-01-01 precursor runtime packet marks JPX, HKEX, and mainland venues degraded/missing under bounded precursor posture states.
- Stop conditions hit: none
- Merge status: merged to `main` via fast-forward at `f8c8af4`
- Notes: precursor projection stays bounded and does not piggyback on generic event-window state.

### LEAF-G91-005 — Extend event-store and live-event surfaces so retained meaning survives projection

- Branch: `work/gate-91-financial-calendar-canonical-projection-20260329`
- Start commit: `38e176a`
- End commit: `f8c8af4`
- Files touched: `src/nvda_desk/schemas/events.py`, `src/nvda_desk/services/event_store.py`, `tests/test_gate91_financial_calendar_canonical_projection.py`
- Validations run: targeted Gate 91 projection slice in repo `.venv`
- Full suite required: no
- Full suite command/result: not required for Gate 91 closeout
- Exact evidence: `LiveEventReference` now preserves layer identity, retained tags, entity list, source document, and import lineage required by later temporal/review gates.
- Stop conditions hit: none
- Merge status: merged to `main` via fast-forward at `f8c8af4`
- Notes: retained meaning added only where later gates need it.

### LEAF-G91-006 — Prove thin CRUD sinks and raw import records remain subordinate and non-canonical

- Branch: `work/gate-91-financial-calendar-canonical-projection-20260329`
- Start commit: `38e176a`
- End commit: `f8c8af4`
- Files touched: `tests/test_gate91_financial_calendar_canonical_projection.py`, planning control surfaces
- Validations run: targeted Gate 91 projection slice in repo `.venv`
- Full suite required: no
- Full suite command/result: not required for Gate 91 closeout
- Exact evidence: tests prove imported records still lack canonical event semantics while projected records preserve them with lineage back to repo artefacts.
- Stop conditions hit: none
- Merge status: merged to `main` via fast-forward at `f8c8af4`
- Notes: Gate 91 closes the canonical projection seam without pretending runtime consumers may read import-stage records directly.

