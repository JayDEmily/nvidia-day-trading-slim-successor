# 2026-04-05_TARGET_REPO_SNAPSHOT_AND_COLLECTION_PROOF_MATRIX_v1

Status: Gate 203 planning authority; bounded proof matrix for later snapshot execution and real-anchor collection.

## Purpose

Freeze the ordered proof matrix for later snapshot and collection work so future execution does not improvise identity checks, dossier presence checks, or closeout expectations.

## Surfaces that must move together in later snapshot and collection work

- `PLANS.md`
- `CHANGELOG.jsonl`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_GATES_v1.md`
- `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_LEAVES_v1.json`
- `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_EXECUTION_LOG_v1.md`
- `docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- `docs/planning/2026-04-05_TARGET_REPO_SNAPSHOT_HANDOFF_BRIEF_AND_INPUT_BUNDLE_CONTRACT_v1.md`
- `docs/planning/2026-04-05_TARGET_REPO_REAL_ANCHOR_COLLECTION_AND_ADMISSION_DOSSIER_RULES_v1.md`
- `docs/planning/2026-04-05_TARGET_REPO_SNAPSHOT_AND_COLLECTION_PROOF_MATRIX_v1.md`
- the gate-specific receipt for the active snapshot-and-collection planning gate
- `tests/test_gate200_target_repo_admitted_evidence_successor_pack_planning.py`
- `tests/test_gate201_target_repo_evidence_governance_planning.py`
- `tests/test_gate202_target_repo_review_governance_planning.py`
- `tests/test_gate203_target_repo_snapshot_and_collection_planning.py`

## Ordered proof commands

1. Gate-local successor-pack coherence:
   - `pytest -q tests/test_gate200_target_repo_admitted_evidence_successor_pack_planning.py tests/test_gate201_target_repo_evidence_governance_planning.py tests/test_gate202_target_repo_review_governance_planning.py tests/test_gate203_target_repo_snapshot_and_collection_planning.py`
2. Historical planning-guard compatibility:
   - `pytest -q tests/test_gate192_phase3_main_target_repair_pack_planning.py tests/test_gate191_capital_deployment_authority_closeout.py tests/test_gate186_options_trace_integrity_closeout.py`
3. Generic planning integrity and hygiene:
   - `pytest -q tests/test_planning_state_integrity.py tests/test_tranche_briefing_template_pack.py tests/test_document_hygiene.py`

## Proof assertions that must hold later

- `snapshot_identity_block_complete_for_each_candidate`
- `dossier_exists_for_each_candidate`
- `loader_and_storage_bindings_are_named`
- `no_candidate_claims_admission_before_review`

## Stop conditions that force replanning

- the snapshot identity block cannot name one exact repo commit and evidence baseline;
- a candidate collection would touch persisted market state with no named binding surface;
- a later proof would need to assume a real anchor already exists in order to validate the dossier;
- the leaves ledger cannot keep completed and remaining leaves disjoint after Gate 203 closeout.

## Closeout rule for later snapshot and collection gates

A later snapshot and collection gate is not complete until:

- the ordered proof commands above are green;
- the receipt names the exact moved surfaces;
- the execution log records the observed proof result;
- GitHub branch and commit history preserve the closeout lineage; and
- a zip artefact exists only if the operator explicitly asks for one or backup/transfer is required.
