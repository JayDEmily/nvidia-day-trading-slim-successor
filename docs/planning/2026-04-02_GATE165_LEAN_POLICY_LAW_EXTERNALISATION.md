# 2026-04-02_GATE165_LEAN_POLICY_LAW_EXTERNALISATION

Status: complete on `work/gate-164-policy-temporal-observability-pack-20260402`

## Purpose

Externalise the current modifier policy law in the leanest form that actually earns its keep.

Gate 165 does **not** introduce a second engine, a new doctrine essay, or a broad packet redesign. It freezes the smallest declared matrix that future coding can materialise so future-you no longer has to reverse-engineer policy families, IDs, target surfaces, and precedence semantics from `state_conditioned_modifier.py` alone.

## Scope boundary

Gate 165 is planning-only.

It may:
- inventory the currently live modifier policy families and policy IDs already embedded in service code;
- define one compact declared policy-matrix schema for those policies only;
- freeze the review / DMP v2 boundary so later materialisation work stays inside existing payload semantics.

It may not:
- create a second execution engine in documentation form;
- widen the admitted live coefficient universe;
- redesign DMP v2 schema-core;
- or invent extra policy fields that do not reduce ambiguity in runtime behaviour.

No new governed vocabulary is admitted in Gate 165.

## Why Gate 165 exists

The repo already has governed mutable surfaces, typed precedence bands, typed resolved-surface packets, and review-visible active policy IDs. What it still lacks is one compact declared surface that answers, without code archaeology:
1. which modifier policies currently exist;
2. which precedence band each policy belongs to;
3. which target surface each policy is allowed to affect;
4. which operation family it uses; and
5. what review-visible explanation label should stay stable across future passes.

That is the only documentation value Gate 165 is trying to create.

## Current live modifier policy inventory frozen by Gate 165

### Policy families observed directly in current service code

| Policy family | Current policy IDs observed in code | Current precedence band | Current primary target surface(s) | Notes |
|---|---|---|---|---|
| `phase_carry` | `phase_carry:{day_phase_state}:{carry_horizon_state}` plus `:entry_gate` additive sub-policy | `PHASE_CARRY` | `target_fresh_deployable_pct`, `entry_gate_score_floor` | phase/carry context compresses deployable capital and may tighten the entry gate |
| `event_options` | `event_options:negative_gamma_stress`, `event_options:negative_gamma_stress:hedge`, `event_options:negative_gamma_stress:max_risk`, `event_options:pin_risk`, `event_options:event_imminent`, `event_options:event_imminent:entry_gate`, `event_options:macro_event_window`, `event_options:macro_event_window:entry_gate`, `event_options:company_event_window`, `event_options:company_event_window:entry_gate`, `event_options:expiry_distortion`, `event_options:venue_session_distortion`, `event_options:venue_session_distortion:entry_gate` | `EVENT_OPTIONS_STRESS` | `target_fresh_deployable_pct`, `hedge_required`, `max_risk_per_trade`, `entry_gate_score_floor` | options/event stress is the richest current modifier family and already uses stable-ish policy IDs |
| `precursor` | `precursor:stand_down_pressure`, `precursor:tightened_posture`, `precursor:degraded_confidence` | `PRECURSOR` | `target_fresh_deployable_pct` | precursor conditions currently compress posture and may push degradation / stand-down classes |
| `regime` | `regime:stressed_weak_breadth` | `REGIME` | `target_fresh_deployable_pct` | regime family is currently narrow and caution-oriented |
| `kill_switch / hard block` | `triggered_kill_switch` and hard-block lineage rather than one declared matrix row per surface | `KILL_SWITCH` / `HARD_BLOCK` | zero/blocked effective posture and terminal surface suppression | keep this inside the existing typed control-law packet rather than duplicating it in a second matrix |

### Mutable surfaces actually touched by current live modifier policies

Observed current live policy applications touch only:
- `target_fresh_deployable_pct`
- `entry_gate_score_floor`
- `max_risk_per_trade`
- `hedge_required`

Observed governed-but-baseline-only surfaces remain outside current live policy application:
- `zone_score_threshold`
- `distance_to_vwap_soft_limit_pct`
- `risk_vix_caution_threshold`
- `risk_vix_hot_threshold`

Gate 165 freezes that distinction so later matrix work does not overstate current runtime richness.

## Lean declared policy-matrix schema frozen by Gate 165

Gate 165 freezes the minimum useful declared matrix shape for later materialisation.

| Field | Meaning | Why it earns its keep |
|---|---|---|
| `policy_id` | stable repo-visible identifier already emitted or derivable from current runtime | lets review, calibration, and diffs point to one declared policy row |
| `policy_family` | `phase_carry`, `event_options`, `precursor`, `regime`, or future bounded family | groups like-for-like policies without inventing a new engine |
| `precedence_band` | one `ModifierPriorityBand` value | removes hidden band semantics from code archaeology |
| `trigger_summary` | compact human-readable summary of the state/condition that activates the policy | enough to orient the operator without trying to serialize full Python logic |
| `target_surface` | one admitted mutable runtime surface | keeps policy rows tied to the governed surface universe |
| `operation_type` | `multiplicative_scale`, `additive_offset`, `boolean_veto`, `clamp`, or `hard_block_via_control_law` | mirrors the existing transform vocabulary in a compact form |
| `clamp_source` | `governed_surface_bounds`, `policy_local_clamp`, or `control_law_packet` | tells future-you where the limiting rule really lives |
| `explanation_label` | stable review-facing label or note stem | reduces explanation drift across passes |
| `materialisation_status` | `live_in_code`, `declared_only_future`, or `control_law_only` | keeps the matrix honest about what is already runtime versus future documentation |

### Fields deliberately **not** added now

Gate 165 explicitly defers the following because they create document bulk without enough runtime value at this stage:
- full boolean trigger expressions or serialised Python condition trees;
- sample payload snapshots;
- replay score targets;
- free-form narrative paragraphs per policy;
- duplicate copies of clamp / veto / kill-switch rules already typed in `ModifierControlLawAuthorityPacket`.

## Relationship between code, matrix, and typed packets

Gate 165 freezes the following law:
1. code remains the execution engine;
2. the declared matrix becomes the checked-in statement of current live policy law;
3. `ModifierRuntimePacket.active_policy_ids`, `resolved_surfaces`, and `effective_lineage` remain the runtime authority for what actually happened in one decision;
4. the matrix must point back to those runtime/review surfaces rather than try to replace them.

## DMP v2 and review boundary frozen by Gate 165

Gate 165 preserves the current boundary already observed in repo code and doctrine.

- DMP v2 keeps its fixed envelope and payload-block model.
- The current modifier/runtime/review seam already carries active policy IDs and resolved surfaces through existing cognition and review packets.
- Gate 165 does **not** claim a DMP v2 schema-core redesign.
- `DV` / `PV` as current repo-native DMP v2 terms remains **unknown / not verified** and must stay labelled that way.
- If a later coding pass wants declared-policy visibility inside exported packets, the default assumption is: wire through existing payload/review semantics first, not through envelope redesign.

## Successor implementation burden frozen by Gate 165

Later runtime materialisation for this gate must do four things only:
1. create one compact checked-in matrix artefact, ideally beside existing config/runtime authority rather than as another essay doc;
2. bind each declared row to a current runtime `policy_id` or to a clearly-marked `control_law_only` row;
3. expose stable policy IDs and explanation labels in review without widening the live surface set;
4. connect future calibration metadata to those same stable IDs.

### Proof burden later

A later coding pass may only claim Gate 165 materialised if it proves:
- every declared matrix row maps to a real current runtime policy family or an explicitly bounded control-law-only row;
- review output can show stable policy IDs without packet-envelope redesign;
- no second policy engine was created in docs or config;
- and current runtime semantics remain unchanged unless a later gate explicitly says otherwise.

## Definition of done recorded by Gate 165

Gate 165 is complete only because:
- the current modifier policy families and IDs are inventoried in one place;
- the minimal declared matrix schema is frozen and bounded;
- the DMP v2 boundary is explicit and honest;
- and later materialisation/proof burden is routed without creating policy prose for its own sake.
