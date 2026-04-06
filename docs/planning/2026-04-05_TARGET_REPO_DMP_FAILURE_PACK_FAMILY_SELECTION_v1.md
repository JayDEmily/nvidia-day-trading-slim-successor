# 2026-04-05_TARGET_REPO_DMP_FAILURE_PACK_FAMILY_SELECTION_v1

Status: Gate 204 planning authority; first repo-native DMP packet failure-pack families and selection order.

## Purpose

Name the first bounded DMP packet failure-pack families against the packet and stage seams that the repo already exposes, so later packet-planning work starts from real repo-native links instead of abstract standalone packet folklore.

## Evidence anchors read for this plan

- `docs/planning/2026-03-24_DMP_V2_NORMATIVE_SPEC.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`
- `src/nvda_desk/schemas/dmp_v2.py`
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/imported_modules/tranche_a.py`
- `tests/test_dmp_v2_protocol.py`
- `tests/test_dmp_review_trace.py`
- `tests/test_gate54_dmp_binding_surface.py`
- `tests/test_gate56_58_dmp_promotion.py`
- `tests/test_gate89_financial_calendar_crosswalk_and_dmp_lane.py`

## First bounded failure-pack families

| Family id | Repo-native target links | Why this family is first-class | First-wave priority |
|---|---|---|---|
| `binding_stage_packet_lineage` | `temporal -> regime -> options_flow -> posture -> eligibility -> execution -> review` DMP v2 stage packets built in `DeskCognitionRuntime._STAGE_SPECS` and `_dependencies_for_stage(...)` | the repo already emits one canonical ordered packet chain, packet ids, parent ids, dependency ids, grammar roles, and stage packet ids; order or dependency drift here corrupts every later lineage consumer | `first_wave` |
| `embedded_workflow_packet_carry` | ingress and additive packet seams already carried inside stage payloads: `live_event_snapshot`, `precursor_runtime_packet`, `modifier_runtime_packet`, `parallel_risk_lane_packet`, `final_risk_join`, and `stage_local_handoff` | these are the highest-risk places where packet truth can silently fork between runtime, review, and compatibility carriage without any envelope redesign | `second_wave_after_stage_lineage` |
| `review_replay_lineage_reconstruction` | `execution packet -> review packet -> PacketLineageSurface -> replay comparison/report` | the review packet is the review/reference packet for the runtime result and replay reuses the same ids; if this chain drifts, later failure analysis becomes story time instead of packet evidence | `first_wave` |
| `imported_module_contract_packet_fences` | `TrancheA` contract packet emission -> review citations -> `contract_packet_ids` | these packets are already repo-native DMP v2 module outputs, but many dependencies remain fenced or proxied; they are real, but less central than the binding stage chain | `defer_until_after_first_three` |

## Failure assertions each family must capture later

### `binding_stage_packet_lineage`
Later family dossiers must capture at least:

- missing packet for one binding stage;
- stage order drift versus `_STAGE_SPECS`;
- dependency-set drift versus `_dependencies_for_stage(...)`;
- grammar-role or payload-schema drift inside the existing DMP v2 envelope;
- `stage_packet_ids`, `packet_lineage`, or `review_packet_id` / `decision_packet_id` mismatches.

### `embedded_workflow_packet_carry`
Later family dossiers must capture at least:

- ingress packet present in one path but absent in the downstream review path;
- additive preserved seam present, but a hidden competing flat field or prose reconstruction is used instead;
- compatibility bridge treated as co-equal authority when the governing packet is present;
- stage-local handoff, final-risk join, or parallel-risk carriage disagreeing with the consuming review surface.

### `review_replay_lineage_reconstruction`
Later family dossiers must capture at least:

- review packet lineage not matching runtime packet ids;
- replay lineage diverging from review lineage without an admitted reason;
- review packet `dmp_lineage` dump differing from typed lineage surfaces;
- decision packet identity or packet order drift that leaves the review chain machine-readable but normatively wrong.

### `imported_module_contract_packet_fences`
Later family dossiers must capture at least:

- contract packets whose dependency-fence state is not preserved into review citations;
- proxied-vs-fenced status drift for imported module packets;
- packet ids emitted for imported contracts but missing from `contract_packet_ids` or downstream review evidence.

## Execution order frozen by Gate 204

The first later DMP failure-pack execution tranche must begin in this order:

1. `binding_stage_packet_lineage`
2. `review_replay_lineage_reconstruction`
3. `embedded_workflow_packet_carry`
4. `imported_module_contract_packet_fences`

This order is mandatory because the first two families prove the canonical packet spine before any additive seam or imported-module failure pack is interpreted.

## Explicit deferrals

The following DMP-adjacent lanes are real but are not first-wave failure-pack families:

- Gate 89 financial-calendar reference-bundle DMP lanes;
- rich options-surface artefact-reference packets;
- standalone packet corpora that do not map back to the current binding-stage runtime;
- any envelope redesign brief that would turn Gate 204 into a DMP v3 discussion.

## What later work must not do

- import packet family names wholesale from the retired standalone repo;
- treat review disagreement memory as a DMP packet failure family;
- open with artefact-reference bundle lanes before the binding-stage packet spine is proven;
- redesign the existing DMP v2 envelope just to make a failure pack easier to write.
