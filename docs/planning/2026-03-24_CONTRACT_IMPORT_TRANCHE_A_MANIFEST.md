# 2026-03-24 Contract Import Tranche A Manifest

Status: Frozen active manifest  
Version: v1.0  
Authority: Subordinate to `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md` and paired with `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_LEAVES_v3.json`.

## Purpose

This file freezes the **only** bounded contract-import tranche that may execute before the repo reaches the Gate 17 decision point.

The tranche is capped at thirteen backlog items. It is deliberately limited to modules that deepen the current four-playbook runtime without opening a second programme, inventing a fifth playbook, or pretending vendor-feed gaps are already solved.

## Scope boundary

Current live playbooks:
- `continuation_ladder`
- `compression_breakout`
- `pin_reversion`
- `negative_gamma_flush`

Grammar-order preservation is binding:
1. `temporal_context`
2. `market_regime_context`
3. `options_flow_context`
4. `posture_risk_permission`
5. `playbook_eligibility`

## Outcome bands

- `contract_surface_only` — typed contract plus deterministic DMP packet emission, with dependency fences still visible.
- `runtime_integrated_advisory` — typed contract imported and cited by the current runtime in an advisory/reviewable way, without claiming full live-data readiness.
- `approved_live_runtime` — forbidden inside tranche A.

## Stop rules

1. No vendor-feed implementation work inside tranche A.
2. No new ontology work or stack-family expansion inside tranche A.
3. No fifth playbook or named-playbook expansion inside tranche A.
4. No silent promotion of imported items to approved live-trading runtime.

## Gate 17 review and replay truth rules

Where tranche-A items are surfaced in runtime review or replay artefacts, the repo must expose:
- exact contract packet ids;
- an honest maturity band of `implemented_runtime_proxy` or `concept_contract_only`;
- an explicit approval state of `not_approved` unless a separate promotion path proves otherwise.

This rule exists to stop advisory contract imports from being mistaken for approved live-trading logic.

## Frozen tranche-A items

### Temporal context

1. `archive-module-006` / `event_flag_capture`
   - Outcome band: `contract_surface_only`
   - Why it stays in tranche A: event windows already influence the live runtime, so this contract makes that surface explicit without faking a live event feed.
   - Blockers: `missing_runtime_translation`, `dependency:manual_or_api_events`

### Market-regime context

2. `archive-module-009` / `realized_volatility_engine`
   - Outcome band: `contract_surface_only`
   - Why it stays in tranche A: realised-volatility context deepens regime and options interpretation for the current playbooks.
   - Blockers: `missing_runtime_translation`, `dependency:spot_prices`

3. `archive-module-018` / `volume_spike_filter`
   - Outcome band: `contract_surface_only`
   - Why it stays in tranche A: volume spikes are desk-relevant, but the missing volume series must remain explicit.
   - Blockers: `missing_runtime_translation`, `dependency:spot_prices`, `dependency:spot_volume_series`

4. `archive-module-014` / `peer_divergence`
   - Outcome band: `contract_surface_only`
   - Why it stays in tranche A: peer divergence materially sharpens regime state without requiring a new playbook family.
   - Blockers: `missing_runtime_translation`, `dependency:peer_equities`, `dependency:spot_prices`

### Options-flow context

5. `archive-module-011` / `gamma_pressure`
   - Outcome band: `contract_surface_only`
   - Why it stays in tranche A: gamma-pressure state is already central to flush, pin, and continuation interpretation.
   - Blockers: `missing_runtime_translation`, `dependency:options_chain`, `dependency:options_metadata`, `dependency:spot_prices`

6. `archive-module-010` / `iv_vs_rv_analysis`
   - Outcome band: `contract_surface_only`
   - Why it stays in tranche A: IV-versus-RV state explains compression, expansion, and anomaly context that the current playbooks already care about.
   - Blockers: `missing_runtime_translation`, `dependency:options_chain`, `dependency:rv_metrics`

7. `archive-module-016` / `skew_inflection`
   - Outcome band: `contract_surface_only`
   - Why it stays in tranche A: skew turns help distinguish supportive flow from destabilising flow.
   - Blockers: `missing_runtime_translation`, `dependency:options_chain`

### Posture and risk permission

8. `archive-evaluator-eval02` / `signal_conflict_detector`
   - Outcome band: `runtime_integrated_advisory`
   - Why it stays in tranche A: conflict detection lets posture and review cite disagreement explicitly.
   - Blockers: `missing_runtime_translation`, `dependency:execution_decisions`, `dependency:signal_outputs`

9. `archive-module-051` / `model_confidence_scorer`
   - Outcome band: `runtime_integrated_advisory`
   - Why it stays in tranche A: confidence reporting is additive and keeps model quality reviewable.
   - Blockers: `missing_runtime_translation`, `dependency:engine_score`, `dependency:signal_conflicts`

10. `archive-module-043` / `conviction_tier_allocator`
    - Outcome band: `runtime_integrated_advisory`
    - Why it stays in tranche A: conviction tier sits directly above permissioning and can remain fenced where macro-score inputs are absent.
    - Blockers: `missing_runtime_translation`, `dependency:engine_score`, `dependency:macro_signal_score`

### Playbook eligibility

11. `archive-module-023` / `entry_gate`
    - Outcome band: `runtime_integrated_advisory`
    - Why it stays in tranche A: entry gating can be cited by the live playbooks without changing their current outcomes.
    - Blockers: `missing_runtime_translation`, `dependency:engine_score`, `dependency:macro_signal_score`

12. `archive-module-024` / `ladder_constructor`
    - Outcome band: `runtime_integrated_advisory`
    - Why it stays in tranche A: ladder construction is directly relevant to the continuation family already present in the live registry.
    - Blockers: `missing_runtime_translation`, `dependency:options_metadata`, `dependency:spot_prices`

13. `archive-module-020` / `archetype_matcher`
    - Outcome band: `runtime_integrated_advisory`
    - Why it stays in tranche A: archetype tagging gives the current playbooks explicit setup labels without inventing new playbooks.
    - Blockers: `missing_runtime_translation`, `dependency:optional_context_signals`, `dependency:spot_prices`

## Explicit non-goals

This manifest must not be used to justify:
- vendor integration;
- broker integration;
- full execution-chain imports;
- named-playbook expansion;
- approval theatre for partially imported modules.

## Pairing

Use this manifest together with:
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_LEAVES_v3.json`
- `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_LOG_v3.md`
