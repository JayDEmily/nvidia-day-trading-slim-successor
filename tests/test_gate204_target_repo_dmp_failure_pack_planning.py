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
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "- next active gate: `Gate 205`" in plans
    assert "Current active gate: **Gate 205 in the target-repo admitted-evidence successor planning pack on `main`**." in gate_map
    assert "Status: active target-repo admitted-evidence successor planning pack; Gates 200-204 complete on `main`, Gate 205 active." in gates
    assert payload["execution_status"] == "gates_200_204_complete_gate_205_active_on_main"
    assert payload["active_gate"] == "Gate 205"
    assert payload["completed_gate_ids"] == ["Gate 200", "Gate 201", "Gate 202", "Gate 203", "Gate 204"]
    assert payload["pending_gate_ids"] == ["Gate 205"]

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
    assert "PENDING_UPDATE_AFTER_VALIDATION" not in execution_log
    assert "PENDING_UPDATE_AFTER_VALIDATION" not in receipt
    assert "Gate 205 is now the active gate in this pack." in execution_log
    assert "Gates 200-204 complete on `main`, Gate 205 active." in checklist
