# 2026-03-29 Financial Calendar Runtime Integration Execution Log v2

Status: active execution log for the reviewed financial-calendar runtime-integration tranche; Gates 91-92 complete on `main`, Gate 93 next

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


### LEAF-G92-001 — Extend cognition-input carriage for rich canonical calendar/event truth

- Branch: `work/gate-92-financial-calendar-temporal-transition-20260329`
- Start commit: `0edecab`
- End commit: pending Gate 92 branch commit
- Files touched: `src/nvda_desk/schemas/cognition.py`, `src/nvda_desk/schemas/dataset.py`, `src/nvda_desk/services/chain_to_cognition.py`, `tests/test_gate92_financial_calendar_temporal_transition.py`
- Validations run: targeted Gate 92 temporal-transition slice in repo `.venv`
- Full suite required: no
- Full suite command/result: not required for Gate 92 closeout
- Exact evidence: `ChainToCognitionService` now carries `desk_calendar_authority` into `TemporalContextInput`, and prepared-runtime fixture packs round-trip without mutation after adding `exclude_if` on the optional carrier field.
- Stop conditions hit: none
- Merge status: pending until Gate 92 branch commit
- Notes: carriage widened without exposing raw import records downstream.

### LEAF-G92-002 — Re-derive event-window semantics from rich live-event packets

- Branch: `work/gate-92-financial-calendar-temporal-transition-20260329`
- Start commit: `0edecab`
- End commit: pending Gate 92 branch commit
- Files touched: `src/nvda_desk/services/temporal_context.py`, `src/nvda_desk/services/event_store.py`, `tests/test_gate92_financial_calendar_temporal_transition.py`, `tests/test_gate81_live_event_temporal_semantics.py`
- Validations run: targeted Gate 92 temporal-transition slice in repo `.venv`
- Full suite required: no
- Full suite command/result: not required for Gate 92 closeout
- Exact evidence: live-event selection now prefers active/cooling-off rich windows over a merely future `next_event`, and event-store query membership now respects retained window bounds instead of `event_at` alone.
- Stop conditions hit: none
- Merge status: pending until Gate 92 branch commit
- Notes: this is the core fix that stops rich company-event windows evaporating before temporal reasoning sees them.

### LEAF-G92-003 — Re-derive venue/session semantics from desk-calendar authority

- Branch: `work/gate-92-financial-calendar-temporal-transition-20260329`
- Start commit: `0edecab`
- End commit: pending Gate 92 branch commit
- Files touched: `src/nvda_desk/services/temporal_context.py`, `tests/test_gate92_financial_calendar_temporal_transition.py`
- Validations run: targeted Gate 92 temporal-transition slice in repo `.venv`
- Full suite required: no
- Full suite command/result: not required for Gate 92 closeout
- Exact evidence: 2026-11-27 half-day desk-calendar authority now drives `session_phase=closed`, `desk_window=closed`, retained closure classes, and a bounded `next_session_open_hint` of 2026-11-30.
- Stop conditions hit: none
- Merge status: pending until Gate 92 branch commit
- Notes: weekday-only session inference no longer dominates half-day truth.

### LEAF-G92-004 — Amend carry routing to use desk-calendar-aware next-session truth

- Branch: `work/gate-92-financial-calendar-temporal-transition-20260329`
- Start commit: `0edecab`
- End commit: pending Gate 92 branch commit
- Files touched: `src/nvda_desk/services/carry_handoff.py`, `tests/test_gate92_financial_calendar_temporal_transition.py`, `tests/test_gate53_carry_handoff.py`
- Validations run: targeted Gate 92 temporal-transition slice in repo `.venv`
- Full suite required: no
- Full suite command/result: not required for Gate 92 closeout
- Exact evidence: `CarryHandoffBuilder` now prefers `temporal.next_session_open_hint`, respects holiday/half-day closure classes, and treats carry-sensitive and cooling-off event states as explicit carry-routing inputs.
- Stop conditions hit: none
- Merge status: pending until Gate 92 branch commit
- Notes: carry routing now reads bounded temporal truth rather than weekday heuristics.

### LEAF-G92-005 — Preserve compatibility hints while keeping them explicitly non-canonical

- Branch: `work/gate-92-financial-calendar-temporal-transition-20260329`
- Start commit: `0edecab`
- End commit: pending Gate 92 branch commit
- Files touched: `src/nvda_desk/services/temporal_context.py`, `tests/test_gate92_financial_calendar_temporal_transition.py`, `tests/test_financial_calendar_planning_v3.py`
- Validations run: targeted Gate 92 temporal-transition slice in repo `.venv`
- Full suite required: no
- Full suite command/result: not required for Gate 92 closeout
- Exact evidence: compatibility `next_event_at` remains subordinate when `live_event_snapshot` is present, and the runtime reasons include `compatibility_next_event_at_subordinate_to_live_event_snapshot`.
- Stop conditions hit: none
- Merge status: pending until Gate 92 branch commit
- Notes: backward compatibility preserved without letting legacy hints reclaim authority.

### LEAF-G92-006 — Prove bounded temporal outputs preserve the rich meaning required by later consumers

- Branch: `work/gate-92-financial-calendar-temporal-transition-20260329`
- Start commit: `0edecab`
- End commit: pending Gate 92 branch commit
- Files touched: `src/nvda_desk/services/temporal_context.py`, `src/nvda_desk/services/carry_handoff.py`, `src/nvda_desk/services/event_store.py`, `tests/test_gate92_financial_calendar_temporal_transition.py`, `tests/test_temporal_context_runtime.py`, `tests/test_temporal_context_signal_state.py`, `tests/test_real_data_loader.py`
- Validations run: targeted Gate 92 temporal-transition slice in repo `.venv`
- Full suite required: no
- Full suite command/result: not required for Gate 92 closeout
- Exact evidence: Gate 92 bounded slice passed with rich event-window, carry-routing, and prepared-runtime fixture coverage, proving later consumers can now see preserved meaning without direct raw-record coupling.
- Stop conditions hit: none
- Merge status: pending until Gate 92 branch commit
- Notes: Gate 92 closes only when rich meaning survives into bounded temporal outputs.
