# 2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_GATES_v1

Status: active master/child parallel-risk integration pack; Gates 171-175 complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402`, Gate 176 active, Gates 177-180 planned

## Purpose

Route the next bounded tranche that first merges the child planning/reference-data/vocabulary line into the master repo and then implements the runtime parallel-risk lane from the merged law without losing prior pack truth.

## Source artefacts that motivate this pack

- Master repo artefact: `repo_gate170_policy_temporal_observability_successor_pack_closed_workbranch_2026-04-02.zip`
- Child repo artefact: `repo_gate164_parallel_risk_lane_foundation_pack_closed_2026-04-02_slim.zip`
- Child handover note: `PARALLEL_RISK_LANE_PLANNING_HANDOVER_NOTE_2026-04-02.md`

## Gate sequence

| Gate | Status | Meaning now |
|---|---|---|
| Gate 171 | complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402` | activate the master/child integration pack, preserve Gate 164-170 as the latest closed predecessor evidence, and route the repo truthfully to Gate 172 |
| Gate 172 | complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402` | freeze the shared base, unique commit ranges, overlap ledger, child-only import surfaces, and the manual merge law before any code changes occur |
| Gate 173 | complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402` | merge the child planning/reference-data/vocabulary surfaces into master lawfully, including normative additions, workbook promotion/demotion, generator/vocabulary rewires, and router-surface reconciliation |
| Gate 174 | complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402` | implement the parallel-risk lane input contract and lawful-read boundary from the merged normative/operating-model law without introducing arbiter behaviour or a new eighth stage |
| Gate 175 | complete on `work/gate-171-master-child-parallel-risk-integration-pack-20260402` | implement temporal/calendar/event/multi-clock runtime surfaces from the merged child planning law and align them with the governed temporal-status ledger already frozen in master |
| Gate 176 | active on `work/gate-171-master-child-parallel-risk-integration-pack-20260402` | implement market/options dependency, dislocation, and translation surfaces from the merged planning law without duplicating the existing deterministic spine |
| Gate 177 | planned on `work/gate-171-master-child-parallel-risk-integration-pack-20260402` | implement anti-duplication, fragility/output semantics, and lean review integration so the lane is descriptive, candidate-aware, and non-foggy rather than a second caution engine |
| Gate 178 | planned on `work/gate-171-master-child-parallel-risk-integration-pack-20260402` | integrate selective proofs, calibration/receipt metadata, and pack continuity so the new lane is evaluable without widening runtime authority casually |
| Gate 179 | planned on `work/gate-171-master-child-parallel-risk-integration-pack-20260402` | run whole-repo vocabulary/workbook-path hygiene, rebuild/check the canonical vocabulary surfaces, and close any terminology drift introduced by the merge |
| Gate 180 | planned on `work/gate-171-master-child-parallel-risk-integration-pack-20260402` | audit master/child merge fidelity, runtime implementation truth, proof coverage, vocabulary hygiene, and package the exact green repo state honestly |

## Merge and implementation law

1. Master remains the canonical repo surface; child is integrated into master rather than replacing it.
2. Gate numbering from child is evidence only. Commit ancestry and file-level semantics govern the merge order.
3. The child branch may win on parallel-risk planning law, workbook-governance law, and reference-data path rewiring where master does not already own that domain.
4. Master may win on coefficient/policy/temporal/observability planning law already closed through Gate 170.
5. Router surfaces (`PLANS.md`, canonical gate map, `CHANGELOG.jsonl`) must be rewritten manually, not cherry-picked blindly.
6. No gate in this pack may assume that passing tests alone proves semantic correctness; changed docs and code must be read end to end.
7. Gate 173 must finish before any `src/` changes in Gates 174-178.
8. Gate 179 is mandatory even if runtime implementation looks green, because vocabulary/workbook-path drift is a declared repo hygiene concern.

## Out of scope for this pack

- blind patch application from child into master
- an arbiter/final judge layer
- DMP v2 schema-core redesign
- adding new live coefficient surfaces beyond what merged law explicitly admits
- treating the independent lane as `step_1_1`, `step_8`, or an `eighth_stage`

## Gate 180 closeout requirements

Gate 180 must explicitly prove all of the following before the pack can close:

- child planning law was merged faithfully into master
- workbook promotion/demotion is consistent and active references point to the canonical governed workbook
- runtime lane implementation exists only where this pack said it would exist
- review/observability and calibration surfaces reflect the implemented lane truthfully
- vocabulary/build checks pass after the full merge
- remaining drifts or deferred items are listed explicitly
