# 2026-04-02_GATE168_REVIEW_OBSERVABILITY_CHAIN_STRENGTHENING

Status: complete on `work/gate-164-policy-temporal-observability-pack-20260402`

## Purpose

Strengthen trader-trust review surfaces without turning the repo into a packet-redesign project or a decorative UI exercise.

Gate 168 freezes the smallest decision-chain view that future coding work should materialise so one decision can be reconstructed from environment and baseline through active policy, effective surface, clamp, consuming stage, and downstream compatibility/risk read. It does not claim that the chain is already fully materialised in runtime code.

## Scope boundary

Gate 168 is planning-only.

It may:
- inventory the current review/observability surfaces already emitted by `review_explanation.py`, `cognition_runtime.py`, and the typed cognition schemas;
- define the minimum decision-chain fields still needed in one operator-facing chain view;
- freeze where that chain should live inside existing review/payload semantics;
- preserve the DMP v2 boundary already frozen by Gate 165.

It may not:
- redesign DMP v2 schema-core;
- invent a new packet envelope or a second review engine;
- create a broad UI specification;
- or widen the live surface universe.

No new governed vocabulary is admitted in Gate 168.

## Current review/observability surfaces observed directly

The repo already emits substantial review structure through existing typed packets and `review_packet` content.

### Already present

- `summary` and `desk_readout` already compress the environmental headline.
- `stage_reason_packets` already provide ordered stage summaries.
- `effective_policy` already carries `active_lineage` and `resolved_surfaces`.
- `review_lineage` already carries `modifier_policy_ids`, effective coefficient targets, resolved surfaces, and posture-change reasons.
- `review_governance`, `phase_carry_policy`, `event_options_stress_policy`, and `modifier_control_law` already expose modifier-related governance slices.
- `stage_local_handoff`, `admissibility_surface`, `candidate_ownership`, `overlay_risk_decision`, and `terminal_risk_application` are already inserted into `review_packet` where present.
- `final_risk_join` already records terminal application results on the execution surface.

### Still missing in one place

The repo still lacks one compact operator-facing chain that can answer, without spelunking multiple packets:
1. what the environment said;
2. what the governed baseline for each touched surface was;
3. which policy IDs acted on that surface;
4. what effective value emerged;
5. what clamp source bounded it;
6. which stage first materially consumed it; and
7. whether later compatibility/risk layers only read it, further constrained it, or superseded it.

Gate 168 exists to freeze that missing chain view only.

## Minimum decision-chain review fields frozen by Gate 168

Gate 168 freezes one lean operator-facing decision-chain view with three sections only.

### 1) `environment_readout`

Minimum fields:
- `desk_window`
- `volatility_regime`
- `breadth_concentration_state`
- `options_behavior_cluster`
- `permission_state`
- `lead_family_id`
- `lead_setup_variant_id`
- `inventory_action`

This is not new runtime logic. It is the current desk-readout surface stabilised as the head of the chain.

### 2) `surface_traces`

One row per currently touched or review-worthy admitted runtime surface.

Minimum fields per row:
- `surface_id`
- `baseline_value`
- `active_policy_ids`
- `effective_value`
- `clamp_source`
- `clamp_applied`
- `primary_consuming_stage`
- `downstream_read_path`
- `notes`

### Allowed first materialisation scope

Gate 168 freezes the initial chain rows to the currently relevant deterministic-spine surfaces only:
- `target_fresh_deployable_pct`
- `entry_gate_score_floor`
- `max_risk_per_trade`
- `hedge_required`
- plus baseline-only carried surfaces when later coding can expose them honestly as unchanged:
  - `zone_score_threshold`
  - `distance_to_vwap_soft_limit_pct`
  - `risk_vix_caution_threshold`
  - `risk_vix_hot_threshold`

### Field meaning law

- `baseline_value` means the governed authority starting point or the current stage-local baseline where the governed value has not yet been dynamically touched.
- `active_policy_ids` must come from the current runtime packet or a later declared matrix bound to those same stable IDs.
- `effective_value` means the value after current modifier/control-law consequences.
- `clamp_source` must use the bounded sources already frozen in Gate 165, such as `governed_surface_bounds`, `policy_local_clamp`, or `control_law_packet`.
- `primary_consuming_stage` means the first stage that materially uses the value, not every later reader.
- `downstream_read_path` is descriptive only. It may say `compatibility_bridge`, `review_only`, `overlay_read_only`, `terminal_join_read`, or `not_applicable`.

### 3) `decision_chain_footer`

Minimum fields:
- `primary_binding_mechanism`
- `stacked_caution_flags`
- `terminal_risk_read`
- `final_decision_path`

This section is where Gate 168 connects to Gate 167’s conservatism-budget law without creating another caution engine.

## One operator-facing decision-chain view frozen by Gate 168

Gate 168 freezes the following logical shape for later materialisation:

```text
DecisionChainView
├── environment_readout
├── surface_traces[]
└── decision_chain_footer
```

The chain is intentionally compact. It is trader-trust work, not decorative UI work.

The design rule is:
- one operator should be able to read the chain top to bottom and understand why the system tightened, capped, hedged, carried, or blocked;
- future-you should not need to cross-reference five packets and one source file just to answer which policy touched which surface first.

## Materialisation location frozen by Gate 168

Gate 168 freezes the preferred materialisation path as:
1. stay inside existing `ReviewExplanationOutput` / `review_packet` semantics first;
2. add one typed chain view or one bounded `review_packet["decision_chain_view"]` payload before attempting any export-layer redesign;
3. keep the review chain as the primary operator/debug surface;
4. let exported DMP packets inherit it through existing payload semantics only if later work proves that is helpful.

Gate 168 explicitly rejects a separate observability packet family at this stage.

## DMP v2 boundary preserved by Gate 168

Gate 168 keeps the same DMP v2 boundary frozen in Gate 165.

- DMP v2 envelope and block taxonomy remain unchanged.
- `object_block` payload semantics remain the default place for any later chain-view serialisation.
- `extensions` may continue to carry compatibility metadata where already supported.
- `DV` / `PV` as repo-native DMP v2 terms remains unknown / not verified.
- No schema-core redesign is claimed or implied here.

## Successor implementation route frozen by Gate 168

Later coding work for Gate 168 must proceed in this order:
1. expose one bounded decision-chain view in review output using existing review/payload semantics;
2. bind each chain row to governed baseline, active policy IDs, effective value, and clamp source honestly;
3. expose primary consuming stage and downstream read path without duplicating terminal-risk logic;
4. connect Gate 167’s diagnostic binding fields into the chain footer;
5. stop before any DMP envelope redesign.

### Proof burden later

A later coding pass may only claim Gate 168 materialised if it proves:
- one operator-facing decision-chain view exists and is readable without code archaeology;
- chain rows are limited to current admitted surfaces and current runtime semantics;
- baseline, policy, effective value, clamp, consuming stage, and downstream read path are all explicit;
- later compatibility/risk reads are described without stealing ownership from the parallel risk lane;
- and DMP v2 schema-core remained unchanged.

## Definition of done recorded by Gate 168

Gate 168 is complete only because:
- the current review/observability seam was inventoried honestly;
- the minimum decision-chain field set is frozen in one place;
- one compact operator-facing chain view is defined without UI bloat;
- and the DMP v2 boundary remains explicitly unchanged.
