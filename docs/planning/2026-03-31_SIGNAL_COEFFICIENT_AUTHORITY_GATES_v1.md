Status: active signal-coefficient authority pack; Gate 122 active, Gates 123-127 planned
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
