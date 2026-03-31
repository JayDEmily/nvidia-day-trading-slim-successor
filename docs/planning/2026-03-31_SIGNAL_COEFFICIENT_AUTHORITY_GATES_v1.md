Status: closed signal-coefficient authority pack on `main`; Gates 122-127 complete, no active gate
# 2026-03-31 Signal Coefficient Authority Gates v1

## Purpose

Convert the recovered coefficient handoff material, the checked-in signal workbook, and the live Gate 121 runtime into one bounded post-Gate-121 execution pack that freezes where coefficients may lawfully live, what starter baselines and bounds are sane, and how effective-coefficient lineage must become review-visible before later replay and live-paper work can talk about tuning honestly.

## Scope

In scope:
- tranche-one coefficient authority for the eight approved mutable runtime surfaces already admitted by repo law;
- a bounded temporal-threshold and timing-parameter subset derived from the checked-in workbook rather than open-ended module tuning;
- registry, runtime, review, replay, and proof surfaces required to move coefficient authority from split workbook-plus-hard-code state into one governed chain.

Out of scope:
- broad module-by-module coefficient tuning across every legacy playbook or imported module;
- raw Asia, Japan, Europe, commodity, crypto, or single-stock precursor coefficients that are not yet backed by admitted raw runtime truth in this repo;
- live-paper coefficient search loops, optimiser-driven range expansion, or any web-sourced numeric paste-in masquerading as repo authority.

## Supersession and active authority

- This document becomes the active gate authority for Gates 122-127.
- It supersedes the absence of any active pack after Gate 121 closeout.
- It does not supersede the historical-evaluation readiness pack as evidence; that pack remains the latest closed runtime-refinement receipt surface.

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`
- `PLANS.md`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/03_DOMAIN_MODEL.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/TESTING_AND_PROMOTION.md`
- `docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx`
- `config/README.md`
- `config/coefficients_registry.example.yaml`
- `src/nvda_desk/config_models.py`
- `src/nvda_desk/domain/temporal_state.py`
- `src/nvda_desk/schemas/state_policy.py`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/services/state_conditioned_modifier.py`
- `src/nvda_desk/services/review_explanation.py`
- `src/nvda_desk/services/replay_compare.py`
- `src/nvda_desk/services/cognition_runtime.py`

## Workflow placement

This tranche sits after Gate 121 final-risk unification and before any later replay-led coefficient review. It is upstream information authority and downstream audit infrastructure at the same time: it freezes which coefficients may lawfully vary, where those values come from, and how posture, execution, review, and replay consume the same effective-coefficient chain. Later historical evaluation, replay comparison, and live-paper promotion must consume this governed authority. They must not consume workbook sheet values, stale example registry values, or private hard-coded interpretations directly.

Answer explicitly:
- this tranche is upstream information authority for coefficient surfaces and bounded derivation for temporal thresholds, plus downstream review/replay infrastructure for effective-coefficient visibility;
- later modifier application, temporal classification, review explanation, replay comparison, and horizon outputs must consume it;
- workbook sheets, web research, and legacy salvage config must not consume raw outputs directly into runtime authority.

## Intent and workflow anchor

The binding lens remains the human desk-operator cognition chain in `docs/01_NORMATIVE.md`. The repo already freezes the cognition grammar order. This tranche must not reorder that grammar. It must instead make the coefficient law honest across the existing order:

1. freeze which surfaces are allowed to vary;
2. freeze sane starter envelopes and exclusions;
3. define the governing registry contract;
4. move current hard-coded runtime authority onto that governed surface;
5. make review packets show baseline-to-effective lineage;
6. admit one bounded temporal threshold subset;
7. align replay and horizon outputs before closing the pack.

## Starter-universe and exclusion rules

Tranche-one starter authority is intentionally narrow.

Admit now:
- the eight approved mutable runtime surfaces already named in `docs/01_NORMATIVE.md`;
- the bounded temporal threshold subset already drafted in the checked-in workbook;
- timing parameters that define session windows but do not masquerade as alpha coefficients.

Exclude now:
- raw Asia/Japan market-health coefficients until the repo owns admitted raw Asia-session truth;
- any legacy module-specific coefficient from `config/coefficients_registry.example.yaml` unless a later gate explicitly re-admits it into governed authority;
- any coefficient search range that is semantically absurd for the signal family in question.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- `docs/01_NORMATIVE.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`
- `docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx` as research and starter-bounds evidence only

### Retire from authority (compatibility-only unless later removed)
- `config/coefficients_registry.example.yaml` as a candidate runtime authority surface; it remains example/salvage reference only unless a later gate says otherwise
- hard-coded mutable-surface baselines and caps in `src/nvda_desk/services/state_conditioned_modifier.py` as final authority once Gate 124 closes
- hard-coded temporal threshold literals in `src/nvda_desk/domain/temporal_state.py` as final authority once Gate 126 closes

### Mandatory amendments
- `PLANS.md` because the repo needs a truthful active pack again
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md` because Gate 122 must become the active gate and Gates 123-127 must be mapped in order
- `CHANGELOG.jsonl` because a meaningful planning change is being made
- planning guard tests because the router truth has moved from no active pack to an active coefficient-authority pack

### New additions
- `docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_GATES_v1.md`
- `docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_LEAVES_v1.json`
- `docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_EXECUTION_LOG_v1.md`
- `docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- `tests/test_gate122_signal_coefficient_authority_planning.py`

## Vocabulary discipline

- Existing vocabulary authority was read before naming this tranche and before reusing terms such as `baseline_coefficient`, `state_conditioned_modifier`, `effective_coefficient`, and `modifier_runtime_packet`.
- Terms such as `starter envelope`, `timing parameter`, and `legacy salvage config` are planning-language only until a later gate decides whether they need vocabulary admission.
- No execution leaf may introduce a new runtime or packet term without rereading the vocabulary authority first.

## Packet / contract discipline

- `docs/03_DOMAIN_MODEL.md` is mandatory reading for any leaf that changes modifier packets, review packets, replay outputs, horizon outputs, config loaders, or packet carriage.
- Gates 123-127 are packet-sensitive by default.
- Workbook sheets and external handoff bundles remain planning evidence only. They do not become packet authority by mere attachment.

## Document-touch checklist

Checklist file: `docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_DOCUMENT_TOUCH_CHECKLIST_v1.md`

## Testing and promotion discipline

- Repo-local environment required: `.venv` created via `uv sync --extra dev`
- Minimum validation slice for this planning pack:
  - `PYTHONPATH=src pytest -q tests/test_gate122_signal_coefficient_authority_planning.py tests/test_gate121_historical_evaluation_readiness_closeout.py tests/test_gate115_historical_evaluation_readiness_planning.py tests/test_gate114_research_mode_clarity_microtranche.py tests/test_gate113_execution_authority_microtranche.py tests/test_gate112_governance_closeout.py tests/test_gate111_governance_guardrails.py tests/test_gate110_agents_reading_order.py tests/test_gate109_template_pack_governance.py tests/test_gate108_router_only_control_surface.py tests/test_gate107_repo_process_governance.py tests/test_document_hygiene.py`
- A gate is not complete until:
  - the gate-specific proof slice runs green;
  - `PLANS.md`, gate map, active leaves ledger, and active execution log move together;
  - a new full-history zip is created from the exact green repo state.

## Gates

### Gate 122: Freeze coefficient scope, starter envelopes, and preflight drift truth

**Objective**
- Freeze the tranche-one coefficient universe, sane starter bounds, exclusion rules, and coefficient-proof preflight so later schema work does not invent scope mid-execution.

**In-scope surfaces**
- `docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx`
- `docs/01_NORMATIVE.md`
- `src/nvda_desk/services/state_conditioned_modifier.py`
- `src/nvda_desk/domain/temporal_state.py`
- `tests/test_gate78_modifier_runtime_integration.py`
- `tests/test_gate96_canonical_runtime_harness.py`
- `tests/test_gate97_runtime_invariants.py`
- `tests/test_gate98_threshold_edges.py`
- `tests/test_gate102_raw_runtime_harness.py`

**Definition of done**
- the admitted tranche-one coefficient universe is frozen with baseline, floor/cap class, units, and exclusion rules;
- timing parameters are separated from behavioural thresholds and from mutable runtime surfaces;
- pre-existing drift relevant to coefficient work is recorded explicitly so later gates do not inherit hidden red surfaces.


#### Gate 122 frozen mutable runtime surfaces

| Surface | Owner stage | Units | Bound class | Baseline | Min | Max | Asymmetry | Notes |
| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `entry_gate_score_floor` | `eligibility` | `score_fraction_0_to_1` | `score_threshold` | 0.65 | 0.50 | 0.85 | `narrow_bidirectional` | Permission-quality floor consumed before ladder admission. |
| `zone_score_threshold` | `eligibility` | `score_fraction_0_to_1` | `score_threshold` | 0.50 | 0.35 | 0.80 | `narrow_bidirectional` | Zone-quality threshold remains tighter than any salvage variant override. |
| `distance_to_vwap_soft_limit_pct` | `execution` | `percent` | `one_sided_clamp` | 1.50 | 0.40 | 3.00 | `narrow_bidirectional` | Operational distance cap, not an open-ended alpha multiplier. |
| `risk_vix_caution_threshold` | `posture` | `volatility_index_points` | `score_threshold` | 24.00 | 18.00 | 40.00 | `narrow_bidirectional` | Caution threshold consumed by the final risk path via execution carriage. |
| `risk_vix_hot_threshold` | `posture` | `volatility_index_points` | `score_threshold` | 32.00 | 24.00 | 50.00 | `narrow_bidirectional` | Hot threshold must stay above caution threshold at all times. |
| `max_risk_per_trade` | `execution` | `percent` | `one_sided_clamp` | 0.35 | 0.10 | 0.55 | `downward_friendly` | Risk cap may tighten materially but must not explode upward. |
| `target_fresh_deployable_pct` | `execution` | `percent` | `one_sided_clamp` | 55.00 | 0.00 | 55.00 | `downward_only` | Capital deployment cap is allowed to derisk to zero but not exceed baseline in tranche one. |
| `hedge_required` | `execution` | `boolean_flag` | `boolean_requirement` | false | — | — | `boolean_only` | Boolean requirement surface, not a numeric search axis. |

#### Gate 122 frozen temporal behavioural thresholds

| Threshold | Owner stage | Units | Bound class | Starter | Min | Max | Allowed primitive drivers |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| `open_disorder_relvol_min` | `temporal` | `ratio` | `state_definition_threshold` | 1.40 | 1.10 | 1.90 | `relative_volume_ratio` |
| `open_disorder_rv5_bps_min` | `temporal` | `basis_points` | `state_definition_threshold` | 80 | 50 | 140 | `rv5_bps` |
| `open_disorder_vwap_dist_bps_min` | `temporal` | `basis_points` | `state_definition_threshold` | 60 | 35 | 110 | `distance_to_vwap_bps` |
| `anchor_vwap_dist_bps_max` | `temporal` | `basis_points` | `state_definition_threshold` | 35 | 15 | 60 | `distance_to_vwap_bps` |
| `anchor_rv5_bps_max` | `temporal` | `basis_points` | `state_definition_threshold` | 60 | 35 | 90 | `rv5_bps` |
| `anchor_relvol_min` | `temporal` | `ratio` | `state_definition_threshold` | 0.90 | 0.60 | 1.10 | `relative_volume_ratio` |
| `anchor_relvol_max` | `temporal` | `ratio` | `state_definition_threshold` | 1.40 | 1.20 | 1.70 | `relative_volume_ratio` |
| `anchor_impulse_age_min` | `temporal` | `minutes` | `state_definition_threshold` | 5 | 2 | 10 | `impulse_age_minutes` |
| `compression_rv5_bps_max` | `temporal` | `basis_points` | `state_definition_threshold` | 35 | 15 | 55 | `rv5_bps` |
| `compression_range5_bps_max` | `temporal` | `basis_points` | `state_definition_threshold` | 40 | 20 | 65 | `range5_bps` |
| `compression_vwap_dist_bps_max` | `temporal` | `basis_points` | `state_definition_threshold` | 25 | 10 | 45 | `distance_to_vwap_bps` |
| `compression_relvol_max` | `temporal` | `ratio` | `state_definition_threshold` | 0.90 | 0.60 | 1.10 | `relative_volume_ratio` |
| `trend_vwap_slope_bps_min` | `temporal` | `basis_points` | `state_definition_threshold` | 15 | 8 | 30 | `vwap_slope_5m_bps` |
| `trend_vwap_dist_bps_min` | `temporal` | `basis_points` | `state_definition_threshold` | 30 | 15 | 55 | `distance_to_vwap_bps` |
| `trend_relvol_min` | `temporal` | `ratio` | `state_definition_threshold` | 1.05 | 0.90 | 1.35 | `relative_volume_ratio` |
| `trend_impulse_age_max` | `temporal` | `minutes` | `state_definition_threshold` | 5 | 2 | 10 | `impulse_age_minutes` |

#### Gate 122 frozen timing parameters

| Parameter | Owner stage | Units | Bound class | Starter | Min | Max | Allowed primitive drivers |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| `power_hour_window_min` | `temporal` | `minutes` | `timing_parameter` | 60 | 45 | 75 | `minutes_to_close` |
| `unwind_window_min` | `temporal` | `minutes` | `timing_parameter` | 30 | 20 | 45 | `minutes_to_close` |

#### Gate 122 explicit exclusions

- raw Asia/Japan market-health coefficients remain excluded until the repo owns admitted raw Asia-session truth;
- any legacy module-specific coefficient from `config/coefficients_registry.example.yaml` remains reference-only unless a later gate explicitly re-admits it;
- timing parameters are separated from behavioural thresholds and from alpha-weight style coefficients;
- no tranche-one numeric surface may carry absurd search space such as `0.01x` to `100x` style expansion.

#### Gate 122 inherited preflight drift receipt

Coefficient-adjacent inherited drift was frozen before Gate 123 schema work:

- proof command: `PYTHONPATH=src pytest -q tests/test_gate78_modifier_runtime_integration.py tests/test_gate96_canonical_runtime_harness.py tests/test_gate97_runtime_invariants.py tests/test_gate98_threshold_edges.py tests/test_gate102_raw_runtime_harness.py`
- observed result: `20 passed, 6 failed`
- inherited failing tests:
  - `tests/test_gate78_modifier_runtime_integration.py::test_gate78_runtime_applies_deterministic_modifier_caps_and_lineage`
  - `tests/test_gate78_modifier_runtime_integration.py::test_gate78_vocabulary_terms_are_generated_and_committed`
  - `tests/test_gate96_canonical_runtime_harness.py::test_canonical_runtime_harness_run_is_deterministic_and_freezes_outputs`
  - `tests/test_gate97_runtime_invariants.py::test_lineage_and_stage_order_invariants_hold_across_canonical_scenarios`
  - `tests/test_gate98_threshold_edges.py::test_gamma_pressure_edge_cases_are_monotonic_and_bounded[0.95-destabilising]`
  - `tests/test_gate102_raw_runtime_harness.py::test_canonical_raw_runtime_harness_run_is_deterministic_and_freezes_outputs`
- interpretation: Gate 121 final-risk and event-window evolution already moved these expectations; Gate 123 must not pretend those surfaces are newly broken by coefficient-authority work.

### Gate 123: Install the governed coefficient-authority contract

**Objective**
- Define one typed governed registry contract for coefficient authority without promoting the legacy example registry into runtime truth.

**In-scope surfaces**
- `src/nvda_desk/config_models.py`
- `config/README.md`
- `config/coefficients_registry.example.yaml`
- `docs/03_DOMAIN_MODEL.md`
- `tests/test_playbook_registry.py`
- `tests/test_gate52_native_playbook_hierarchy.py`

**Definition of done**
- the new coefficient-authority file shape is typed, validated, and distinguished clearly from the legacy example registry;
- every admitted coefficient surface declares owner stage, units, baseline, min, max, transform family, and allowed upstream drivers;
- invalid or semantically absurd coefficient declarations fail deterministically.

### Gate 124: Externalise mutable-surface baseline authority without behaviour drift

**Objective**
- Move the eight approved mutable-surface baselines and bounds from hard-coded runtime constants into the governed authority chain while preserving current lawful behaviour.

**In-scope surfaces**
- `src/nvda_desk/services/state_conditioned_modifier.py`
- `src/nvda_desk/schemas/state_policy.py`
- `src/nvda_desk/services/cognition_runtime.py`
- `tests/test_gate78_modifier_runtime_integration.py`
- `tests/test_gate118_mutable_surface_operability.py`
- `tests/test_gate121_final_risk_gateway_join.py`

**Definition of done**
- the runtime reads mutable-surface baselines, floors, and caps from the governed authority surface rather than private constants;
- canonical scenario outputs remain behaviourally equivalent except where the new authority path is intentionally more explicit;
- legacy constants are retired from final authority and left only as compatibility scaffolding if still needed.

### Gate 124 closeout note

- Gate 124 completed on `main` by loading mutable-surface baselines, floors, and caps from `config/coefficient_authority.v1.yaml` inside `StateConditionedModifierService` and carrying governed authority metadata into `ResolvedRuntimeSurfaceValue`.
- The inherited Gate 121 drift in the old Gate 78 expectation is now made explicit: modifier-packet target-fresh remains 20.625 for the stressed late-session scenario, while final-risk derisk then compresses execution output to 13.4062.
- Canonical vocabulary was regenerated so the declared Gate 124 proof slice no longer fails on stale committed JSON.

### Gate 125: Make effective-coefficient lineage review-visible

**Objective**
- Carry one baseline-to-effective coefficient chain through posture, execution, and review so no stage keeps a private modifier interpretation.

**In-scope surfaces**
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/services/review_explanation.py`
- `src/nvda_desk/services/state_conditioned_modifier.py`
- `tests/test_execution_review_runtime.py`
- `tests/test_gate103_raw_prepared_parity.py`
- `tests/test_gate121_final_risk_gateway_join.py`

**Definition of done**
- review packets expose baseline value, effective value, clamp state, precedence band, and source policy ids for every admitted mutable surface;
- posture, execution, and review consume the same typed resolved-surface packet;
- regression tests prove the lineage chain survives both prepared and raw canonical paths.

### Gate 125 closeout note

- Gate 125 completed on `main` by extending `EffectivePolicySnapshot` and `ReviewLineagePacket` with the same resolved-surface carriage used by the modifier runtime packet.
- Review output now renders baseline reference, baseline/effective value, clamp state, precedence band, source policy ids, and authority version through `effective_policy.resolved_surfaces` and `review_lineage.resolved_surfaces`.
- Prepared and raw canonical paths preserve that review-visible lineage without divergence.

### Gate 126: Admit a bounded temporal-threshold authority subset

**Objective**
- Move one bounded temporal threshold and timing-parameter subset from workbook research surface into governed runtime authority without turning the workbook into runtime truth directly.

**In-scope surfaces**
- `src/nvda_desk/domain/temporal_state.py`
- `docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx`
- `src/nvda_desk/schemas/cognition.py`
- `tests/test_gate98_threshold_edges.py`
- `tests/test_gate96_canonical_runtime_harness.py`
- `tests/test_gate102_raw_runtime_harness.py`

**Definition of done**
- the admitted temporal thresholds and timing parameters are named, unit-safe, and bounded in governed authority rather than hidden in classifier literals;
- the temporal classifier reads those admitted values deterministically;
- threshold-edge, prepared-path, and raw-path proofs stay bounded and no excluded Asia/Japan raw coefficient leaks in by stealth.

### Gate 126 closeout note

- Gate 126 completed on `main` by wiring the admitted temporal threshold and timing subset from `config/coefficient_authority.v1.yaml` through `TemporalStateClassifier` using typed threshold ids and timing-parameter ids rather than private classifier literals.
- The live classifier now compares workbook-backed basis-point and ratio thresholds directly against runtime primitives such as `price_realised_vol_5m_pct`, `distance_to_vwap_pct`, `vwap_slope_5m_pct`, `rolling_range_5m_pct`, and `relative_volume_ratio`, while keeping non-admitted hits like break-count floors explicit classifier law.
- The declared Gate 126 proof slice is now aligned to current runtime truth: the gamma-pressure edge at `0.95` derisks to `19.6625`, and the canonical prepared/raw harnesses now prove `event_imminent_window` with `final_risk=derisk` and no active playbooks.

### Gate 127: Align replay visibility and close the pack honestly

**Objective**
- Make replay and horizon outputs consume the same governed coefficient state, then close the signal-coefficient authority pack honestly across the planning quartet.

**In-scope surfaces**
- `src/nvda_desk/services/replay_compare.py`
- `src/nvda_desk/schemas/calibration.py`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `PLANS.md`
- `CHANGELOG.jsonl`
- `tests/test_replay_compare_runtime.py`

**Definition of done**
- replay and horizon outputs expose a stable coefficient snapshot identifier plus the admitted effective-surface evidence they consume;
- coefficient-state comparison is review-visible and parity-safe across canonical replay paths;
- the planning quartet and packaging receipts close the pack honestly from the exact green repo state.

### Gate 127 closeout note

- Gate 127 completed on `main` by adding `GovernedCoefficientSnapshot` carriage to replay runs and comparison reports, hashing the admitted resolved-surface evidence into a stable snapshot id, and surfacing that same evidence through replay outputs rather than private runtime reconstruction.
- The deterministic replay report baseline was refreshed to current runtime truth after Gate 126 changed the governed temporal path, so the checked-in comparison report now includes both refreshed means and governed snapshot evidence.
- The signal-coefficient authority pack is now closed honestly through Gate 127; repo-root `PLANS.md` routes no active pack until a later planning pass creates one explicitly.
