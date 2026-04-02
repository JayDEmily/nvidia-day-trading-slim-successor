# 2026-04-02_GATE178_PROOFS_AND_CALIBRATION_INTEGRATION

Status: complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`

## Purpose

Integrate selective proof order and lean calibration/evaluation-prep metadata for the implemented **Independent Parallel Risk Lane** without pretending calibration has started and without widening runtime authority.

Calibration has not started.

Gate 178 therefore does three bounded things only:

1. materialise one typed evaluation-prep packet for the implemented lane slices;
2. reuse the architecture-aware receipt shape already frozen by Gate 169;
3. declare the selective proof order for the merged master/child runtime tranche.

## Vocabulary authority used

Gate 178 explicitly follows the canonical vocabulary dictionary already present in the repo:

- canonical lane term: `independent_parallel_risk_lane`
- canonical workbook term: `signal_coefficient_reference_workbook`

Source of truth:

- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `scripts/build_canonical_vocabulary.py`

Allowed aliases remain dictionary-governed only. Gate 178 does not admit new vocabulary.

## Runtime materialised in this gate

### Typed evaluation-prep packet

A lean typed packet is now frozen in `src/nvda_desk/schemas/calibration.py` and emitted from the lane service/runtime result.

Bounded fields:

- `lane_id`
- `implemented_surfaces`
- `surface_metadata`
- `policy_metadata`
- `required_receipt_sections`
- `selective_proof_order`
- `notes`

### Implemented surface rows

The packet currently covers only the implemented runtime slices:

- `temporal_surface`
- `market_translation_surface`
- `candidate_audit_surface`

Each row carries the Gate 169 metadata shape adapted to the lane:

- behavioural purpose
- expected directionality
- anti-goal
- owner stage
- surface family
- review cadence
- activation state
- evidence sources

### Stable policy rows frozen here

Gate 178 freezes three stable evaluation-prep policy IDs for the implemented lane slices only:

- `parallel_risk:temporal_calendar_multi_clock`
- `parallel_risk:market_options_dependency_translation`
- `parallel_risk:candidate_fragility_anti_duplication`

These are evaluation-prep identifiers, not a new arbiter or a new coefficient surface family.

## Reuse of Gate 169 architecture

Gate 178 deliberately reuses the receipt architecture already frozen in Gate 169.

Required receipt sections remain:

1. `surface_changes_observed`
2. `policy_firing_summary`
3. `help_vs_harm_assessment`
4. `over_tightening_and_stack_pressure`
5. `redundancy_or_dead_weight_findings`
6. `danger_or_unstable_behaviour_findings`
7. `opportunity_shaping_absence_or_presence`
8. `recommended_next_action`

This keeps the lane evaluation-prep surface architecture-aware without inventing a second evaluation framework.

## Selective proof order frozen here

Gate 178 freezes the following proof order for the merged master/child lane tranche:

1. `parallel_risk_runtime_targeted`
2. `parallel_risk_review_targeted`
3. `imported_child_pack_continuity`
4. `vocabulary_build_then_hygiene` (run the vocabulary build before the hygiene proof slice).

This is deliberately narrow. No omnibus full-suite claim is made here.

## Out of scope preserved

Gate 178 does not:

- start calibration;
- create an arbiter;
- redesign DMP v2 schema-core;
- add new live coefficient surfaces;
- or widen the lane beyond the implemented Gate 174-177 slices.

## Definition of done recorded by Gate 178

Gate 178 is complete because:

- the merged runtime now emits one lean typed evaluation-prep packet for the implemented lane slices;
- the packet reuses the Gate 169 metadata/receipt architecture rather than inventing a new one;
- the selective proof order is explicit and bounded;
- and the repo still says truthfully: **Calibration has not started.**
