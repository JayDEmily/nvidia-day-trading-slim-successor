# 2026-04-02_GATE167_SERIAL_CONSERVATISM_BINDING_POINT_LAW

Status: complete on `work/gate-164-policy-temporal-observability-pack-20260402`

## Purpose

Reduce future serial-conservatism confusion inside the current deterministic spine without stealing authority from the parallel independent risk-lane thread.

Gate 167 is descriptive and diagnostic. It freezes where caution currently binds, which stage is the primary binding point for each current outcome family, and what a lightweight conservatism-budget review surface should show. It does **not** reallocate final veto ownership across threads.

## Scope boundary

Gate 167 is planning-only.

It may:
- inventory current caution outcome families across posture, modifier, execution, and risk-gateway seams;
- freeze one primary binding point for each current deterministic-spine outcome family;
- define a lightweight diagnostic conservatism-budget review surface.

It may not:
- allocate or implement independent-risk-lane cap/veto ownership;
- create a new caution engine;
- or claim that serial conservatism is solved by prose alone.

No new governed vocabulary is admitted in Gate 167.

## Current caution outcome families frozen by Gate 167

| Outcome family | Where it is first produced today | What the outcome currently does |
|---|---|---|
| `posture_hard_block` | `PostureRiskService.evaluate(...)` hard-block conditions | sets `PermissionState.BLOCK`, zeroes deployable capital, sets `inventory_action_bias = reduce` |
| `posture_derisk_local_envelope` | `PostureRiskService.evaluate(...)` derisk conditions | reduces posture permission to `DERISK`, compresses fresh/overnight deployable limits, may switch inventory bias to `trim` or `hedge` |
| `modifier_capital_compression` | `StateConditionedModifierService` policy applications on `target_fresh_deployable_pct` plus `apply_to_posture(...)` / `apply_to_execution(...)` | compresses effective deployable capital inside existing posture/execution pathways |
| `modifier_threshold_tightening` | `StateConditionedModifierService` resolved surfaces for `entry_gate_score_floor` and baseline-only carriage for other execution thresholds | tightens admission/execution thresholds through the modifier runtime packet and execution output |
| `modifier_max_risk_clamp` | `StateConditionedModifierService` negative-gamma stress path and execution consumption | reduces `max_risk_per_trade` before downstream execution sizing |
| `modifier_required_hedge` | `StateConditionedModifierService` boolean surface plus `ExecutionExpressionService` / execution output | forces or preserves `hedge_required` in execution geometry |
| `modifier_stand_down_or_kill_switch` | `ModifierRuntimePacket` degradation / stand-down / kill-switch path plus `apply_to_posture(...)` | can convert posture output to block / zero deployable before later overlay risk reads |
| `overlay_risk_derisk_or_block` | `RiskGatewayService.evaluate(...)` and terminal join logic | derisks or blocks after execution payload construction, then terminal join reconciles posture versus overlay decisions |

## Primary binding-point law frozen by Gate 167

| Outcome family | Primary binding point frozen now | Allowed descriptive secondary reads / carriage | Not allowed in this pack |
|---|---|---|---|
| `posture_hard_block` | posture hard invariants / posture output | terminal join may describe supersession or alignment; review may reconstruct it | reallocating final-veto ownership to this pack |
| `posture_derisk_local_envelope` | posture local envelope | execution and review may carry the consequence; overlay risk may later derisk or block independently | pretending later overlay action means posture was never the first binder |
| `modifier_capital_compression` | modifier runtime packet resolved surface, first materially applied through `apply_to_posture(...)` | execution, review, and terminal risk may read the already-compressed result | adding a second independent compression engine here |
| `modifier_threshold_tightening` | modifier runtime packet resolved surface, materially consumed in execution output / downstream execution checks | review and compatibility bridges may expose it; later overlay risk may read execution consequences only | declaring Stage 5 or independent risk ownership without later runtime change |
| `modifier_max_risk_clamp` | modifier runtime packet / execution consumption | later overlay risk may scale the already-selected cap but does not become the primary binder in this pack | reassigning primary ownership to the parallel risk lane here |
| `modifier_required_hedge` | modifier runtime packet / execution consumption | review and later overlay risk may read the requirement | using this pack to define a cross-thread final hedge arbiter |
| `modifier_stand_down_or_kill_switch` | modifier runtime packet, materially applied in posture compatibility update | review and terminal risk may describe the result | claiming this fully replaces future independent risk hard-veto design |
| `overlay_risk_derisk_or_block` | overlay risk evaluation and terminal risk application surface | review may show overlap classes and supersession | moving this family upstream into modifier/posture just because the separate risk lane exists elsewhere |

## Anti-duplication law frozen by Gate 167

1. A caution outcome family may have **one primary binder** in the current deterministic spine.
2. Later stages may describe, carry, or further constrain the already-bound consequence only where repo code already does so.
3. This pack may define a diagnostic stack for duplicated caution pressure; it may not introduce a second authority path merely to make the stack look cleaner.
4. Independent-risk-lane cap/veto reallocation remains reserved to the separate thread.

## Conservatism-budget review surface frozen by Gate 167

Gate 167 freezes one lightweight diagnostic surface, not a new engine.

### Proposed review fields

| Field | Meaning |
|---|---|
| `caution_mechanisms_fired` | ordered list of posture / modifier / overlay caution mechanisms that activated for the decision |
| `primary_binding_mechanism` | the one mechanism that first materially bound the outcome family under the law above |
| `compressed_dimensions` | simple list such as `fresh_deployable`, `entry_gate`, `max_risk`, `hedge_required`, `terminal_allowance` |
| `secondary_reads_or_overrides` | later stages that only carried, described, or further constrained the already-bound result |
| `stacked_caution_flags` | textual flags when more than one layer compressed the same dimension |

### Design rule

This surface is intentionally simple. It is a binding stack, not a score, optimiser, or mathematical theatre object.

## Coordination rule with the parallel risk-lane thread

Gate 167 freezes the following coordination rule:
- this pack may describe where current overlay/terminal risk already binds;
- this pack may reserve merge notes for later risk-lane reconciliation;
- this pack may **not** decide future independent-risk final cap/veto ownership on behalf of the separate thread.

## Successor implementation route frozen by Gate 167

Later coding work for this gate may:
1. expose the diagnostic conservatism-budget view in review output for the existing deterministic spine;
2. label current caution mechanisms and primary binding points explicitly;
3. surface overlap classes and stacked-compression flags without changing terminal-risk ownership.

Later coding work for this gate may not:
- add a new runtime caution surface;
- duplicate overlay-risk behaviour in modifier/posture;
- or merge the separate risk-lane thread into this pack by stealth.

### Proof burden later

A later coding pass may only claim Gate 167 materialised if it proves:
- the diagnostic surface is descriptive of current runtime behaviour, not a new decision engine;
- each caution outcome family has one explicit primary binder in the deterministic spine;
- stacked caution is visible in review without reassigning independent-risk authority;
- and cross-thread boundary notes remain explicit.

## Definition of done recorded by Gate 167

Gate 167 is complete only because:
- the current caution outcome families are inventoried;
- primary binding points and allowed secondary reads are frozen;
- the conservatism-budget review surface is specified in a lean diagnostic form;
- and the boundary against the parallel risk-lane thread remains explicit.
