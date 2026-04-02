# 2026-04-02_GATE169_CALIBRATION_METADATA_AND_RECEIPTS

Status: complete on `work/gate-164-policy-temporal-observability-pack-20260402`

## Purpose

Prepare the repo for later evaluation without pretending calibration has already started.

Calibration has not started.

Gate 169 freezes the metadata and receipt architecture that later paper-testing or walk-forward work should rely on. Its job is to make later evaluation architecture-aware so future testing can answer what changed, what helped, what over-tightened, and what stayed dead weight.

## Scope boundary

Gate 169 is planning-only.

It may:
- define metadata fields for each live admitted surface;
- define metadata fields for each declared policy family / policy ID frozen by Gate 165;
- define architecture-aware evaluation-receipt questions for later testing packs.

It may not:
- claim calibration is underway;
- widen the live coefficient surface set;
- create scoring doctrine that outruns available runtime evidence;
- or backdoor the independent risk lane into this pack.

No new governed vocabulary is admitted in Gate 169.

## Live-surface calibration metadata frozen by Gate 169

Gate 169 freezes one lean metadata row per admitted live surface.

### Surfaces in scope

- `entry_gate_score_floor`
- `zone_score_threshold`
- `distance_to_vwap_soft_limit_pct`
- `risk_vix_caution_threshold`
- `risk_vix_hot_threshold`
- `max_risk_per_trade`
- `target_fresh_deployable_pct`
- `hedge_required`

### Minimum metadata fields per surface

| Field | Meaning |
|---|---|
| `surface_id` | governed surface identifier |
| `behavioural_purpose` | what the surface is trying to control in trading behaviour |
| `expected_directionality` | what movement in the surface is expected to do |
| `anti_goal` | what bad behaviour the surface must not encourage |
| `owner_stage` | declared owner stage from governed authority / later owner-stage law |
| `surface_family` | `execution_expression`, `caution_envelope`, `opportunity_gate`, or `risk_read_only` where applicable |
| `review_cadence` | default human review rhythm once later testing begins |
| `activation_state` | `active_runtime`, `baseline_only`, or later bounded status consistent with Gate 160 and Gate 165 |
| `evidence_sources` | which packets/receipts later evaluation should read to understand this surface |

### Design rule

The metadata must describe behavioural intent, not just numeric bounds. A later test should be able to say why a surface exists before it asks whether the surface “worked”.

## Declared-policy evaluation metadata frozen by Gate 169

Gate 169 freezes one metadata row per declared policy family or stable policy ID.

### Minimum metadata fields per policy

| Field | Meaning |
|---|---|
| `policy_id` | stable runtime/declaration identifier |
| `policy_family` | bounded family such as `phase_carry`, `event_options`, `precursor`, `regime`, or `control_law_only` |
| `primary_target_surface` | which admitted surface the policy most directly acts on |
| `behavioural_purpose` | what the policy is trying to achieve |
| `expected_effect` | expected qualitative effect on trading behaviour |
| `anti_goal` | what bad behaviour this policy must not create |
| `over_tightening_signs` | observable signs that the policy is too suppressive |
| `redundancy_signs` | signs the policy adds little beyond other policies |
| `danger_signs` | signs the policy is creating unstable or misleading runtime behaviour |
| `review_cadence` | default review rhythm once later testing exists |
| `evidence_sources` | which runtime/review surfaces later evaluation should read |

### Design rule

Policies must be evaluable as policies, not just as code branches. A later test should be able to ask whether one policy is helping, redundant, or dangerous without inventing a second decision engine.

## Architecture-aware evaluation receipts frozen by Gate 169

Gate 169 freezes one later receipt family for evaluation-ready work.

### Required receipt sections

1. `surface_changes_observed`
2. `policy_firing_summary`
3. `help_vs_harm_assessment`
4. `over_tightening_and_stack_pressure`
5. `redundancy_or_dead_weight_findings`
6. `danger_or_unstable_behaviour_findings`
7. `opportunity_shaping_absence_or_presence`
8. `recommended_next_action`

### Minimum questions later receipts must answer

For surfaces:
- Which surfaces actually changed in the decision/run/session slice?
- Were those changes directionally consistent with the surface’s behavioural purpose?
- Did the surface suppress too much, too little, or about the intended amount?

For policies:
- Which policy IDs actually fired?
- Which policy first materially bound the decision?
- Did the policy help, over-tighten, duplicate another policy, or create danger signs?

For architecture:
- Where did caution stack across layers?
- Where was opportunity shaping absent despite favourable upstream conditions?
- Which behaviour came from richer primitives/features versus from coefficient deformation?

## Evidence chain frozen by Gate 169

Later evaluation receipts must read from the repo’s real chain, not from invented side channels.

Primary evidence sources remain:
- governed surface authority;
- declared policy matrix from Gate 165;
- temporal-status ledger from Gate 166;
- conservatism-budget / binding stack from Gate 167;
- decision-chain review surface from Gate 168 once materialised;
- existing review/runtime packets already emitted by the deterministic spine.

## Successor implementation route frozen by Gate 169

Later coding work for Gate 169 must proceed in this order:
1. attach the metadata fields to the governed surface universe and the declared policy matrix;
2. expose the minimum metadata in review/debug or evaluation-prep surfaces;
3. create receipt templates or typed packets for later evaluation work;
4. keep the whole structure preparatory until real paper-testing or walk-forward work begins.

### Proof burden later

A later coding pass may only claim Gate 169 materialised if it proves:
- every admitted live surface has bounded metadata fields frozen here;
- every declared policy family / stable policy ID has evaluation metadata frozen here;
- later evaluation receipts can ask architecture-aware questions rather than only crude P&L questions;
- and no code path falsely claims that calibration has already begun.

## Definition of done recorded by Gate 169

Gate 169 is complete only because:
- live-surface metadata is frozen in a bounded useful shape;
- declared-policy evaluation metadata is frozen in a bounded useful shape;
- architecture-aware evaluation receipts are defined for later packs;
- and the repo stays preparatory rather than performative.
