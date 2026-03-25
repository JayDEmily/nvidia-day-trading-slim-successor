# Session Clock Feature Family — Promotion Plan

Status: planned
Primary sources: `legacy-feature-001` plus related session-phase passages

## Purpose

Represent the intraday day as behaviourally distinct phases so that research, replay, and runtime logic can condition on market phase rather than treating all minutes as interchangeable.

## Why it survives

This is a durable state-description layer, not a fragile trade call. It improves almost every downstream component.

## Proposed feature family

### Core feature
- `session_clock_phase_id: enum[...]`

### Supporting features
- `minutes_since_open`
- `minutes_to_close`
- `is_pre_market`
- `is_regular_hours`
- `is_power_hour`
- `phase_confidence`

## Proposed initial phase taxonomy

1. `pre_market`
2. `open_disorder`
3. `early_anchor`
4. `institutional_repricing`
5. `midday_compression`
6. `post_lunch_drift`
7. `power_hour`
8. `dealer_unwind_close`
9. `after_hours`

This taxonomy is intentionally simple for v1 and can be refined later.

## Repo mapping

- persistence target: `derived_features`
- consumers: research API, replay engine, runtime module weighting, eval attribution

## Minimum required inputs

- exchange calendar / session schedule
- timestamp in market timezone
- optional realised-vol / volume state inputs for confidence overlays

## What should **not** happen yet

Do not make phase assignment depend on twenty complex indicators on day one. Start with clock-based phases plus optional confidence overlays.

## Eval impact

The session clock should unlock:
- phase-conditioned module performance;
- phase-conditioned veto analysis;
- research summaries that say what part of the day we are in;
- replay reports sliced by phase.

## Minimum implementation slice

1. deterministic phase assignment from timestamp and calendar;
2. one derived feature payload per minute;
3. phase included in market snapshot responses;
4. replay attribution grouped by phase.

## Pass/fail criteria for implementation readiness

Implementation-ready when:
- the taxonomy is frozen for v1;
- timestamp-to-phase mapping is deterministic;
- replay can attribute results by phase;
- no runtime logic depends on ambiguous discretionary phase labels.

## Risks

- making the phase taxonomy too fancy too early;
- pretending the phase labels explain causality on their own;
- using phase labels as a substitute for volatility / liquidity state.

## Recommendation

Promote first. This is the safest and most broadly useful candidate.
