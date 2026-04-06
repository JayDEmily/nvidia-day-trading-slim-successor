"""Gate 204 DMP failure-pack planning checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_DOCUMENT_TOUCH_CHECKLIST_v1.md"
FAMILIES = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_DMP_FAILURE_PACK_FAMILY_SELECTION_v1.md"
BOUNDARY = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_DMP_MACHINE_READABLE_CONTRACT_BOUNDARY_RULES_v1.md"
PROOF_SLICE = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_DMP_FAILURE_PACK_PLANNING_PROOF_SLICE_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-05_GATE204_TARGET_REPO_DMP_PACKET_FAILURE_PACK_AND_CONTRACT_BOUNDARY_PLANNING.md"
INDEX = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_INDEX_AND_CROSS_REFERENCE_v1.md"
CLOSEOUT_PROOF = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_CLOSEOUT_PROOF_ORDER_AND_RECEIPT_REQUIREMENTS_v1.md"
HANDOFF = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_PLANNING_TO_CODING_HANDOFF_BOUNDARY_v1.md"
GATE205_RECEIPT = REPO_ROOT / "docs/planning/2026-04-05_GATE205_TARGET_REPO_SUCCESSOR_PACK_CLOSEOUT_AND_HANDOFF.md"


def test_gate204_control_surfaces_and_docs_are_coherent() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    families = FAMILIES.read_text(encoding="utf-8")
    boundary = BOUNDARY.read_text(encoding="utf-8")
    proof_slice = PROOF_SLICE.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    closeout_proof = CLOSEOUT_PROOF.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    gate205_receipt = GATE205_RECEIPT.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert any(marker in plans for marker in ["- next active gate: `Gate 205`", "- no active pack currently routed"])
    assert any(marker in gate_map for marker in ["Current active gate: **Gate 205 in the target-repo admitted-evidence successor planning pack on `main`**.", "Current active gate: **none — target-repo admitted-evidence successor planning pack closed through Gate 205 on `work/gate-205-successor-pack-closeout-handoff-20260406`**.", "Current active gate: **none — target-repo admitted-evidence successor planning pack closed through Gate 205 on `main`**."])
    assert any(marker in gates for marker in ["Status: active target-repo admitted-evidence successor planning pack; Gates 200-204 complete on `main`, Gate 205 active.", "Status: closed target-repo admitted-evidence successor planning pack through Gate 205 on `work/gate-205-successor-pack-closeout-handoff-20260406`.", "Status: closed target-repo admitted-evidence successor planning pack through Gate 205 on `main`."])
    assert payload["execution_status"] in {"gates_200_204_complete_gate_205_active_on_main", "target_repo_admitted_evidence_successor_pack_closed_through_gate_205_on_work_branch", "target_repo_admitted_evidence_successor_pack_closed_through_gate_205_on_main"}
    assert payload["active_gate"] in {"Gate 205", "none"}
    assert payload["completed_gate_ids"] in [["Gate 200", "Gate 201", "Gate 202", "Gate 203", "Gate 204"], ["Gate 200", "Gate 201", "Gate 202", "Gate 203", "Gate 204", "Gate 205"]]
    assert payload["pending_gate_ids"] in [["Gate 205"], []]

    assert "binding_stage_packet_lineage" in families
    assert "embedded_workflow_packet_carry" in families
    assert "review_replay_lineage_reconstruction" in families
    assert "imported_module_contract_packet_fences" in families
    assert "Gate 89 financial-calendar reference-bundle DMP lanes" in families

    assert "planning_only" in boundary
    assert "schema_plus_example_plus_validator" in boundary
    assert "Do not redesign the `dmp.v2` envelope or block taxonomy" in boundary
    assert "DV` / `PV`" in boundary or "DV` / `PV` repo-native DMP v2 schema-core terms" in boundary

    assert "Ordered proof commands for this planning gate" in proof_slice
    assert "tests/test_gate204_target_repo_dmp_failure_pack_planning.py" in proof_slice
    assert "tests/test_gate89_financial_calendar_crosswalk_and_dmp_lane.py" in proof_slice
    assert "GitHub branch and commit history preserve the closeout lineage" in proof_slice

    assert "Gate 205 is the next active gate" in receipt
    assert "Deterministic reader path" in index
    assert "Evidence-only origins and retired authority" in index
    assert "Gate 209" in index
    assert "Ordered closeout proof sequence" in closeout_proof
    assert "python -m pytest -q tests/test_gate200_target_repo_admitted_evidence_successor_pack_planning.py tests/test_gate201_target_repo_evidence_governance_planning.py tests/test_gate202_target_repo_review_governance_planning.py tests/test_gate203_target_repo_snapshot_and_collection_planning.py tests/test_gate204_target_repo_dmp_failure_pack_planning.py" in closeout_proof
    assert "zip artefact is required only when the operator explicitly requests one" in closeout_proof
    assert "Authoritative inputs for later execution threads" in handoff
    assert "Do not start coding directly from evidence-only standalone docs." in handoff
    assert "No Gate 206 is created or implied by this handoff." in handoff
    assert "PENDING_UPDATE_AFTER_VALIDATION" not in execution_log
    assert "PENDING_UPDATE_AFTER_VALIDATION" not in receipt
    assert "PENDING_UPDATE_AFTER_VALIDATION" not in gate205_receipt
    assert "no active pack currently routed" in gate205_receipt
    assert any(marker in execution_log for marker in ["Gate 205 is now the active gate in this pack.", "no active pack is currently routed"])
    assert any(marker in checklist for marker in ["Gates 200-204 complete on `main`, Gate 205 active.", "through Gate 205 on `work/gate-205-successor-pack-closeout-handoff-20260406`", "through Gate 205 on `main`"])
