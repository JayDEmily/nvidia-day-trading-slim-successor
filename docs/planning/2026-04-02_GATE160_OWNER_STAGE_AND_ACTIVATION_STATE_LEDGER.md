# 2026-04-02_GATE160_OWNER_STAGE_AND_ACTIVATION_STATE_LEDGER

Status: complete on `work/gate-157-coefficient-architecture-consolidation-pack-20260402`

## Purpose

Make Workstream 3 executable in repo-native terms.

Gate 160 does not invent a fresh ownership theory. It takes the already-landed seam receipts, the governed authority file, and the live consumer code paths, then freezes one planning ledger for admitted mutable runtime surfaces.

That ledger must answer four questions at once:
1. what owner stage the governed authority declares;
2. which code path directly consumes the surface for live behaviour today;
3. whether the surface is dynamically active or merely admitted at baseline;
4. what closure mode later coding may use to resolve any owner-stage mismatch honestly.

## Scope boundary

Gate 160 is planning-only.

It may:
- classify every admitted mutable runtime surface by declared owner stage, direct live consumer, compatibility carriage, and activation state;
- define mismatch classes and allowed closure modes;
- separate direct-consumer truth from compatibility-only carriage and review exposure.

It may not:
- change runtime packet meaning;
- relabel governed owner stages in config yet;
- widen the admitted surface set;
- or claim that compatibility carriage alone proves live dynamic behaviour.

No new governed vocabulary is admitted in Gate 160.

## Inputs carried forward from earlier receipts

Gate 160 relies on existing repo-native evidence rather than re-deriving the seam from scratch:
- Gate 145 already froze `modifier_runtime_packet` as the authority and `modifier_compatibility_bridge` as bounded compatibility-only carriage, not a second private interpretation.
- Gate 146 already froze Stage 5 admissibility apart from Stage 6 candidate ownership.
- Gate 151 already built the field-level ownership and consumer migration ledger for the stage-local handoff corrective successor pack.
- Gate 152 already froze the non-equivalence law between Stage 5 admissibility and Stage 6 execution candidate ownership.
- Gate 153 already froze the distinction between overlay evaluation, terminal application, and final-join compatibility.

Gate 160 therefore extends the earlier seam law into the coefficient surface world rather than replacing it.

## Activation-state classes frozen by Gate 160

The inventory placeholder from Gate 159 now receives a bounded planning interpretation.

| Activation-state class | Meaning | What does **not** count |
|---|---|---|
| `dynamically_active_direct_consumer` | the surface is admitted, state-policy law can deform it today, and a live consumer uses the resolved value for behaviour | mere presence in the governed file or review packet |
| `governed_baseline_only_direct_consumer` | the surface is admitted and read by a live consumer today, but current state-policy code does not deform it yet | carrying the baseline through execution output without a live consumer |
| `dynamically_active_multi_consumer` | the surface is deformed today and more than one live stage or downstream consumer materially uses the consequence | compatibility-bridge echoes or review snapshots |
| `compatibility_or_review_carriage_only` | the surface or field is carried only so downstream review, migration, or compatibility remains explicit | packet carriage by itself |

## Owner-stage and activation-state ledger for admitted mutable surfaces

| Surface | Declared owner stage in governed authority | Direct live consumer(s) today | Compatibility-only carriage / preserved trace | Gate 160 activation-state verdict | Gate 160 mismatch class | Allowed closure mode now frozen |
|---|---|---|---|---|---|---|
| `entry_gate_score_floor` | `eligibility` | Stage 6 `ExecutionExpressionService.evaluate(...)` consumes the resolved operative surface and downstream SLV admission uses the resulting payload thresholds | execution `modifier_compatibility_bridge`, review packet, stage-local handoff snapshots | `dynamically_active_direct_consumer` | declared Stage 5 owner, direct live use downstream of Stage 5 | either promote true Stage 5 packet consumption, or relabel the owner stage to the real downstream authority; until then treat the Stage 5 label as unresolved, not as proof |
| `zone_score_threshold` | `eligibility` | downstream SLV zone/keep decisions consume the execution payload threshold; execution output carries the field into that path | execution `modifier_compatibility_bridge`, review packet, stage-local handoff snapshots | `governed_baseline_only_direct_consumer` | declared Stage 5 owner, direct live use downstream of Stage 5, but no current modifier deformation | same closure modes as `entry_gate_score_floor`; no one may call this a live Stage 5 dynamic surface until Stage 5 actually consumes it |
| `distance_to_vwap_soft_limit_pct` | `execution` | downstream SLV market scoring consumes the payload threshold against live VWAP distance | execution output field, review packet, stage-local handoff snapshots | `governed_baseline_only_direct_consumer` | owner-aligned execution surface with baseline-only live use today | preserve as execution-owned unless later code either deforms it lawfully or retires it; no relabel needed merely because the current value is baseline-only |
| `risk_vix_caution_threshold` | `posture` | `RiskGatewayService` uses the threshold inside overlay/terminal risk policy evaluation after execution carriage | execution output field, review packet, stage-local handoff snapshots | `governed_baseline_only_direct_consumer` | declared posture owner, direct live use in later risk evaluation | either promote true posture-owned use upstream, or relabel the threshold to the later risk lane / overlay seam when that architecture exists; until then the posture label stays provisional |
| `risk_vix_hot_threshold` | `posture` | `RiskGatewayService` uses the threshold inside overlay/terminal risk policy evaluation after execution carriage | execution output field, review packet, stage-local handoff snapshots | `governed_baseline_only_direct_consumer` | same as `risk_vix_caution_threshold` | same allowed closure modes as the caution threshold above |
| `max_risk_per_trade` | `execution` | Stage 6 sizing logic consumes the resolved cap and later risk may scale the already-selected cap | execution `modifier_compatibility_bridge`, review packet, stage-local handoff snapshots | `dynamically_active_direct_consumer` | primary owner aligned; later risk consequence exists but does not replace Stage 6 ownership truth | preserve Stage 6 execution ownership; later risk may scale or block, but that does not justify relabelling the surface away from execution |
| `target_fresh_deployable_pct` | `execution` | `apply_to_posture(...)` compresses fresh/overnight deployable capital early, Stage 6 carries the resulting target through execution output, and later risk may scale again | posture and execution `modifier_compatibility_bridge`, review packet, stage-local handoff snapshots | `dynamically_active_multi_consumer` | declared execution owner but first material consequence lands in posture-local envelope before Stage 6, then later risk may act again | later coding must either split posture-local capital-envelope consequence from execution target semantics, or relabel/document the dual-consumer reality explicitly; silent ambiguity is not allowed |
| `hedge_required` | `execution` | Stage 6 execution geometry and hedge overlay logic consume the resolved boolean requirement | execution `modifier_compatibility_bridge`, review packet, stage-local handoff snapshots | `dynamically_active_direct_consumer` | owner-aligned primary execution surface with later risk consequence possible | preserve execution ownership unless a later independent risk lane introduces a genuinely separate hedge-forcing authority surface |

## Evidence that differentiates dynamic activity from baseline-only admission

### Surfaces with live modifier deformation today

Current state-policy applications target:
- `target_fresh_deployable_pct`
- `entry_gate_score_floor`
- `max_risk_per_trade`
- `hedge_required`

That is the observed target set in `StateConditionedModifierService` policy applications.

### Surfaces admitted but baseline-only today

Current state-policy applications do **not** target:
- `zone_score_threshold`
- `distance_to_vwap_soft_limit_pct`
- `risk_vix_caution_threshold`
- `risk_vix_hot_threshold`

Those surfaces remain governed and live-consumed, but Gate 160 freezes them as baseline-only until later code proves otherwise.

## Direct-consumer versus compatibility-carriage interpretation law

Gate 160 freezes the following interpretation rules:

1. `modifier_runtime_packet` remains the authority chain for dynamic deformation.
2. `modifier_compatibility_bridge` exists to make packet-authoritative field consequences explicit; it does **not** by itself prove a stage is the true owner.
3. Review packet exposure and `stage_local_handoff` snapshots are explanatory surfaces; they do **not** turn a carried field into a direct live consumer.
4. A field counts as directly consumed only when a live behaviour path reads it for selection, sizing, gating, scoring, blocking, or overlay risk evaluation.
5. A field may be owner-misaligned even when its packet carriage is perfectly explicit.

## Mismatch classes frozen by Gate 160

| Mismatch class | What it means | Present examples |
|---|---|---|
| `declared_owner_downstream_consumer_drift` | the governed owner stage is earlier than the real live consumer | `entry_gate_score_floor`, `zone_score_threshold` |
| `declared_owner_later_risk_drift` | the governed owner stage names posture, but live decision use occurs in later overlay/final risk evaluation | `risk_vix_caution_threshold`, `risk_vix_hot_threshold` |
| `declared_owner_multi_consumer_overlap` | a single admitted surface causes real behaviour at more than one stage or consequence layer today | `target_fresh_deployable_pct` |
| `owner_aligned_baseline_only` | owner label is currently acceptable, but the surface is still baseline-only and must not be overstated as dynamically rich | `distance_to_vwap_soft_limit_pct` |
| `owner_aligned_dynamic` | owner label and direct live consumer are materially aligned today | `max_risk_per_trade`, `hedge_required` |

## Allowed closure modes frozen by Gate 160

Later coding may resolve a mismatch only through one of these explicit modes:

1. **Rewire consumer truth**
   - promote real use into the declared owner stage;
   - retire the downstream substitute path or demote it to compatibility-only carriage.

2. **Relabel owner truth**
   - update the governed owner stage and supporting docs/tests so the declared owner matches the real live consumer.

3. **Split the surface**
   - create two explicitly named surfaces when one admitted surface is currently carrying two genuinely different stage meanings.
   - Gate 160 freezes this as the preferred serious option when one field tries to be both posture-local envelope and execution target semantics.

4. **Defer dynamic use explicitly**
   - keep the surface admitted and live-consumed at baseline, but record that dynamic deformation is not yet active.

5. **Preserve bounded compatibility temporarily**
   - retain compatibility carriage while a later gate or thread closes the seam, but mark the seam as unresolved and non-authoritative.

## Proof burden for later closure claims

No later coding thread may claim a Gate 160 mismatch is resolved unless it shows all of the following for the relevant case:
- the governed authority file, pack docs, and runtime consumer path now agree on owner-stage truth;
- direct-consumer and compatibility-carriage roles are separated explicitly;
- tests cover the new truth rather than only text changes;
- review and handoff surfaces still expose the consequence without smearing ownership back into one blob.

## What Gate 160 hands forward

1. Gate 161 inherits a truthful picture of the current live modifier plane, including which surfaces are actually dynamic and which are baseline-only.
2. Gate 162 inherits explicit closure modes and therefore can route later implementation work without hand-waving.
3. The pack now distinguishes owner truth, direct-consumer truth, compatibility carriage, and activation state instead of treating them as one vague status.

## Definition of done recorded by Gate 160

Gate 160 is complete only because:
- every admitted mutable runtime surface now has one owner-stage and activation-state verdict in repo-native planning law;
- direct-consumer truth is separated from compatibility-only carriage and review exposure;
- and later coding now has explicit closure modes instead of vague instructions to "clean it up".
