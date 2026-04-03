# 2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_SCOPE_NOTE_v1

Current routed state: master/child parallel-risk integration pack closed through Gate 180 on `main`.

## Why this pack exists

The repo now has two relevant lines of work:

- **master**: the canonical repo state from `repo_gate170_policy_temporal_observability_successor_pack_closed_workbranch_2026-04-02.zip`
- **child**: the external planning/reference-data/vocabulary line from `repo_gate164_parallel_risk_lane_foundation_pack_closed_2026-04-02_slim.zip`

The operator explicitly wants master to remain canonical while child is folded in carefully rather than treated as a disposable side branch.

## Verified starting truths

1. Master and child share a clean git base and then diverge into separate work-branch lines.
2. The child branch introduces parallel-risk planning law, workbook promotion/demotion, workbook-governance law, and vocabulary/build rewiring.
3. The child branch did **not** introduce `src/` runtime-code deltas relative to the shared base. That means the child is a planning-law/reference-data branch, not a runtime implementation branch.
4. The child handover note was checked line by line and found substantively accurate, with only minor citation corrections.
5. Master already contains closed planning packs for coefficient architecture consolidation and policy/temporal/observability successor work.

## Pack order

This pack is intentionally split into two tranches plus closeout:

- **Tranche A**: merge child planning/reference-data/vocabulary into master
- **Tranche B**: implement the runtime parallel-risk lane from the merged law
- **Tranche C**: proofs, repo-wide vocabulary/workbook-path hygiene, and final audit/closeout

No gate may skip directly to Tranche B.

## Non-negotiable scope rules

- Do not blind-apply patches from child into master.
- Do not use child gate numbering as the primary merge surface; commit ancestry and semantic file reads govern the merge.
- Do not create an arbiter, `step_1_1`, `step_8`, or `eighth_stage` under the guise of the lane.
- Do not let the new lane become an arbiter by slow scope drift or duplicate caution ownership.
- Do not redesign DMP v2 schema-core in this pack.
- Do not add new live coefficient surfaces casually.
- Do not leave whole-repo vocabulary/workbook-path hygiene for “later”.

## Gold that must not be left behind

### From the child line
- co-resident independent parallel-risk lane law
- workbook promotion/demotion and discoverability law
- multi-clock timing/event authority mapping
- market/options dependency and dislocation mapping
- ownership/anti-duplication/fragility law

### From the master line
- no distributed caution fog
- lean policy-law externalisation rather than policy bloat
- temporal-status ledger discipline
- review-chain strengthening with no DMP v2 schema-core redesign
- calibration/evaluation receipt readiness

## Documentation discipline

This pack may write planning and implementation receipts only where they remove ambiguity or route real work. It must not create documentation for its own sake.

## Unknown / not verified boundaries preserved

- `DV` / `PV` as current repo-native DMP v2 schema-core terms remains unknown / not verified.
- The child artefact does not currently prove runtime risk-lane implementation because no `src/` deltas were present.
