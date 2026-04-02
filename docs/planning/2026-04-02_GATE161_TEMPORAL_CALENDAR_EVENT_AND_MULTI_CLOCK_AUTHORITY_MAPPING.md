Status: complete on `work/gate-157-parallel-risk-lane-planning-pack-20260402`; Gate 162 is now the active gate
# Gate 161 — Temporal, Calendar, Event, and Multi-Clock Authority Mapping

## What closed

Gate 161 is complete on `work/gate-157-parallel-risk-lane-planning-pack-20260402`.

The pack now freezes the approved timing and horizon surfaces the future lane may consume for **environmental risk weather** and records the **multi-clock model** as a writing obligation rather than chat memory.

## Repo-native timing and horizon surfaces

The future lane may consume the following repo-native timing and horizon surfaces, subject to the co-resident-lane law frozen in Gate 158:

### Intraday timing and desk-window surfaces

- `temporal_context`
- `temporal_state`
- `desk_window`
- `clock_envelope`
- `session_phase`
- `behavioural_phase`
- `minutes_since_open`
- `minutes_to_close`
- `phase_confidence`
- `signal_coverage_ratio`

These are the lawful surfaces for answering questions such as:
- what kind of session is in progress;
- whether disorder, anchoring, compression, or trend persistence conditions are more likely;
- whether the lane is still in session-start uncertainty, ordinary regular-hours traversal, power-hour, unwind, or a closed/bridge condition.

### Calendar-horizon and event-timing surfaces

- `calendar_horizon_gate`
- `desk_calendar_contract`
- `financial_calendar_reference_bundle`
- `financial_calendar_crosswalk`
- `event_proximity_state`
- `event_window_state`
- `event_overlap_class`
- `event_risk_timing_class`
- `event_carry_sensitivity`
- approved event-family identity carried through the calendar bundle/crosswalk lane

This preserves the distinction between:
- raw scheduled fact;
- approved derived runtime timing semantics;
- and later market translation of those facts.

The future lane therefore sees event timing lawfully without pretending event identity is already the trading answer.

### Precursor / overnight surfaces

- `precursor_universe`
- `precursor_runtime_packet`
- approved precursor venues only:
  - JPX cash
  - HKEX cash
  - Mainland China cash
  - CFFEX index futures

This keeps Asia / precursor truth bounded. The lane may use precursor context to enrich overnight and pre-open risk weather, but it may not become a general global-macro engine or a free-form “everything overseas matters” consumer.

## Raw fact versus approved derived runtime consumption

The pack now freezes the following rule for later implementation:

- raw calendar fact remains owned by the reference bundle and desk-calendar-contract surfaces;
- the lane may consume approved derived runtime timing semantics projected from those facts;
- the lane may not rewrite calendar truth, event identity, market-hours truth, or expiry truth;
- the lane may not smuggle in downstream translation or posture conclusions at the calendar stage.

In plain terms: the lane is allowed to know **what is scheduled, when it matters, and what kind of event window exists**, but it is not allowed to treat event identity by itself as the trading verdict.

## Multi-clock crosswalk

The strongest exploratory finding is now frozen as a pack obligation:

### 1. Slower structural truth
Planning concept for slower structural truth across franchise / ecosystem / demand-side reality. This does not yet have one single repo-native packet and remains a bounded planning concept for later implementation.

### 2. Medium read-through truth
A mixed layer. It partly maps to the financial-calendar read-through lane and partly remains a planning concept for bounded dependency activation.

### 3. Event / calendar truth
The multi-clock record now preserves the exact phrases `event / calendar truth`, `tape / translation truth`, and `expression / carry truth` as future writing obligations.

Repo-native today through:
- `calendar_horizon_gate`
- `desk_calendar_contract`
- financial-calendar bundle/crosswalk
- event-window semantics

### 4. Tape / translation truth
Not fully closed in this gate. This clock is preserved here as a downstream obligation that will be mapped in Gate 162 through market-regime and options/flow translation surfaces.

### 5. Expression / carry truth
Partly present through existing posture/risk and carry-sensitive event semantics, but preserved here as a future writing obligation rather than flattened into one timing score.

## Why this gate matters

Without this gate, later implementation could collapse all timing truth into one generic “risk now” notion and lose the difference between:
- time of day;
- calendar horizon;
- event proximity;
- event overlap;
- event carry sensitivity;
- precursor context;
- and later translation/carry truth.

That flattening would destroy one of the best ideas found in the exploration.

## Out-of-scope honesty

This gate does **not**:
- implement a runtime packet for the future lane;
- decide the final output schema for risk weather;
- solve dependency activation;
- solve dislocation-versus-impairment;
- solve the arbiter.

It only freezes the lawful timing/horizon inputs and the multi-clock writing obligation.

## Receipt

- branch: `work/gate-157-parallel-risk-lane-planning-pack-20260402`
- start commit: current pack baseline after Gate 160
- closing proof command: `.venv/bin/python -m pytest -q tests/test_gate161_temporal_calendar_event_and_multi_clock_authority_mapping.py tests/test_gate160_governed_signal_coefficient_reference_workbook_law.py tests/test_gate157_parallel_risk_lane_foundation_bootstrap.py`
- observed result: `passed`
