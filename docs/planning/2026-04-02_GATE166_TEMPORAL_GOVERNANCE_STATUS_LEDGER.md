# 2026-04-02_GATE166_TEMPORAL_GOVERNANCE_STATUS_LEDGER

Status: complete on `work/gate-164-policy-temporal-observability-pack-20260402`

## Purpose

Finish the temporal-governance planning pass by making the current classifier's number/status truth explicit.

Gate 166 does **not** try to externalise every number in `temporal_state.py`. It freezes the only thing that matters at this stage: which values are already governed, which values remain intentionally fixed heuristics, which values are deferred candidates for later admission, and whether anything is already evidenced as removable.

## Scope boundary

Gate 166 is planning-only.

It may:
- inventory authority-backed temporal thresholds and timing parameters already consumed by the classifier;
- classify each remaining hard-coded temporal threshold or heuristic by explicit status;
- freeze operator/review wording for those status classes.

It may not:
- claim all hard-coded values are bad by definition;
- perform blanket externalisation for the sake of symmetry;
- or widen the temporal authority file without a later coding gate.

No new governed vocabulary is admitted in Gate 166.

## Governed temporal subset already live

### Authority-backed temporal thresholds currently loaded from `coefficient_authority.v1.yaml`

Gate 166 freezes the current authority-backed threshold set as:
- `open_disorder_relvol_min`
- `open_disorder_rv5_bps_min`
- `open_disorder_vwap_dist_bps_min`
- `anchor_vwap_dist_bps_max`
- `anchor_rv5_bps_max`
- `anchor_relvol_min`
- `anchor_relvol_max`
- `anchor_impulse_age_min`
- `compression_rv5_bps_max`
- `compression_range5_bps_max`
- `compression_vwap_dist_bps_max`
- `compression_relvol_max`
- `trend_vwap_slope_bps_min`
- `trend_vwap_dist_bps_min`
- `trend_relvol_min`
- `trend_impulse_age_max`

### Authority-backed timing parameters currently loaded from `coefficient_authority.v1.yaml`

Gate 166 freezes the current authority-backed timing set as:
- `power_hour_window_min`
- `unwind_window_min`

### Workbook provenance that remains relevant

The current governed subset is already traceable back to workbook temporal sources, especially:
- `Temporal_Step1_Framework`
- `Temporal_Bounds_Draft`
- `Bounds_Method`
- `Signal_Coeff_Handoff`

Gate 166 preserves that provenance without treating the workbook as live runtime truth.

## Temporal-status classes frozen by Gate 166

| Status class | Meaning | What it is **not** |
|---|---|---|
| `governed_live_threshold` | value currently loads from the governed authority file and is used live by the classifier | workbook-only provenance or a hand-waved future candidate |
| `fixed_structural_heuristic` | intentionally fixed classifier scaffolding that defines cadence, fallback shape, or confidence semantics right now | a secret candidate knob waiting to be widened casually |
| `deferred_candidate` | currently hard-coded market-state threshold/guard that may deserve later authority admission after replay evidence | already governed truth |
| `removal_candidate` | value or guard with plausible redundancy that later work should test for deletion rather than admission | immediate removal claim without evidence |

## Remaining hard-coded temporal heuristics and their frozen status

### Fixed structural heuristics

Gate 166 freezes the following as `fixed_structural_heuristic` for now because they describe classifier scaffolding rather than the first priority for authority admission:
- `coverage_ratio < 0.375` fallback threshold
- legacy phase windows in `_legacy_phase(...)`: `<30`, `<90`, `<150`, `<240`
- phase-confidence scaffolding: base `0.72`, `0.82`, `0.88`, bonus `+0.04`, and `min(0.08, coverage_ratio * 0.1)`
- `power_hour:active_volume` evidence-only check at `relative_volume_ratio >= 1.1`

Reason frozen now:
- these values shape fallback cadence, confidence labelling, or explanatory tags more than the primary behavioural-state corridors already admitted through Gate 126.

### Deferred candidates for later admission or structured review

Gate 166 freezes the following as `deferred_candidate` because they are market-state decision guards that could later justify authority admission, but are not yet strong enough to externalise automatically:
- open-disorder window `minutes_since_open <= 75`
- open-disorder range guard `range5_bps >= 80.0`
- open-disorder break-count guard `break_count >= 2`
- open-disorder impulse-age guard `impulse_age_minutes <= 2`
- open-disorder hit threshold `disorder_hits >= 3`
- early-anchor window `10 <= minutes_since_open <= 120`
- early-anchor break-count guard `break_count <= 1`
- early-anchor hit threshold `anchor_hits >= 4`
- midday-compression start guard `minutes_since_open >= 90`
- compression impulse-age guard `impulse_age_minutes >= 6`
- compression hit threshold `compression_hits >= 4`
- trend start guard `minutes_since_open >= 45`
- trend range guard `range5_bps >= 45.0`
- trend hit threshold `trend_hits >= 4`
- institutional-repricing vs post-lunch split at `minutes_since_open < 180`

Reason frozen now:
- these are real behavioural-state guards, but the current repo has stronger evidence for the authority-backed threshold subset than for immediate admission of the surrounding windows / hit-count logic.

### Removal candidates

Gate 166 records **no live `removal_candidate` values yet**.

Reason frozen now:
- the current evidence supports classification and later replay review, not confident deletion.

## Operator / review wording frozen by Gate 166

Later runtime/review surfaces should use the following wording and no looser synonyms:
- `authority:{id}` for `governed_live_threshold`
- `fixed_heuristic:{id}` for `fixed_structural_heuristic`
- `deferred_candidate:{id}` for `deferred_candidate`
- `removal_candidate:{id}` for `removal_candidate`

The operator-facing rule is simple:
- if a value comes from governed authority, say so literally;
- if it is intentionally fixed, say so literally;
- if it is deferred, say so literally.

That is enough. Gate 166 explicitly rejects essay-like review prose here.

## Successor implementation route frozen by Gate 166

Later coding work for temporal status should proceed in this order:
1. annotate or ledger the current classifier values by the four status classes above;
2. expose the status wording in review/debug surfaces without changing classifier semantics;
3. only then consider whether any specific `deferred_candidate` deserves admission to authority;
4. stop immediately if a proposed authority addition cannot show why it is better than staying fixed.

### Proof burden later

A later coding pass may only claim Gate 166 materialised if it proves:
- every current classifier value falls into exactly one frozen status class;
- review/debug surfaces can tell whether a value is governed, fixed, or deferred;
- no blanket externalisation happened merely for symmetry;
- any newly admitted temporal value carries explicit authority provenance and did not silently widen the classifier.

## Definition of done recorded by Gate 166

Gate 166 is complete only because:
- the governed temporal subset is enumerated explicitly;
- every remaining hard-coded temporal heuristic has a frozen status;
- review wording is fixed in a lean machine-adjacent form;
- and later temporal-governance work is routed without inventing new status theory.
