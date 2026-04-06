"""Gate 201 evidence-governance planning checks."""

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
INVENTORY = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_EVIDENCE_INVENTORY_BASELINE_v1.md"
PROVENANCE = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_EVIDENCE_PROVENANCE_AND_IMMUTABILITY_RULES_v1.md"
CHANGE_MEMORY = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_EVIDENCE_CHANGE_MEMORY_RULES_v1.md"
PROOF_SLICE = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_EVIDENCE_GOVERNANCE_PROOF_SLICE_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-05_GATE201_TARGET_REPO_EVIDENCE_INVENTORY_AND_PROVENANCE_PLANNING.md"


def test_gate201_control_surfaces_and_docs_are_coherent() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    inventory = INVENTORY.read_text(encoding="utf-8")
    provenance = PROVENANCE.read_text(encoding="utf-8")
    change_memory = CHANGE_MEMORY.read_text(encoding="utf-8")
    proof_slice = PROOF_SLICE.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert any(marker in plans for marker in ["- next active gate: `Gate 202`", "- next active gate: `Gate 203`", "- next active gate: `Gate 204`", "- next active gate: `Gate 205`"])
    assert any(marker in gate_map for marker in [
        "Current active gate: **Gate 202 in the target-repo admitted-evidence successor planning pack on `main`**.",
        "Current active gate: **Gate 203 in the target-repo admitted-evidence successor planning pack on `main`**.",
        "Current active gate: **Gate 204 in the target-repo admitted-evidence successor planning pack on `main`**.",
        "Current active gate: **Gate 205 in the target-repo admitted-evidence successor planning pack on `main`**.",
    ])
    assert any(status in gates for status in [
        "Status: active target-repo admitted-evidence successor planning pack; Gates 200-201 complete on `main`, Gate 202 active, Gates 203-205 planned.",
        "Status: active target-repo admitted-evidence successor planning pack; Gates 200-202 complete on `main`, Gate 203 active, Gates 204-205 planned.",
        "Status: active target-repo admitted-evidence successor planning pack; Gates 200-204 complete on `main`, Gate 205 active.",
    ])
    assert payload["execution_status"] in {"gates_200_201_complete_gate_202_active_on_main", "gates_200_202_complete_gate_203_active_on_main", "gates_200_204_complete_gate_205_active_on_main"}
    assert payload["active_gate"] in {"Gate 202", "Gate 203", "Gate 205"}
    assert payload["completed_gate_ids"] in [["Gate 200", "Gate 201"], ["Gate 200", "Gate 201", "Gate 202"], ["Gate 200", "Gate 201", "Gate 202", "Gate 203", "Gate 204"]]
    assert payload["pending_gate_ids"] in [["Gate 202", "Gate 203", "Gate 204", "Gate 205"], ["Gate 203", "Gate 204", "Gate 205"], ["Gate 205"]]

    assert "Canonical evidence class matrix" in inventory
    assert "fixtures/real_data/gate_101_canonical_raw_runtime_bundle.json" in inventory
    assert "fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json" in inventory
    assert "fixtures/trace_review/gate_132_bounded_trace_fixture_pack.json" in inventory
    assert "fixtures/trace_review/gate_134_bounded_trace_report.json" in inventory
    assert "fixtures/replay/gate_f_replay_regression_fixture_pack.json" in inventory
    assert "fixtures/replay/gate_f_expected_report.json" in inventory
    assert "instrument`, `bar_1m`, and `option_snapshot`" in inventory

    assert "Mandatory provenance fields" in provenance
    assert "Immutable admitted anchors" in provenance
    assert "Persisted reference state" in provenance
    assert "option_snapshot" in provenance

    assert "Mandatory change-memory fields" in change_memory
    assert "retired_from_authority" in change_memory
    assert "Evidence-only standalone docs may not regain authority silently" in change_memory

    assert "Ordered proof commands" in proof_slice
    assert "tests/test_gate201_target_repo_evidence_governance_planning.py" in proof_slice
    assert "Stop conditions that force replanning" in proof_slice

    assert "the successor pack now has an explicit evidence inventory baseline" in receipt
    assert "pending_update_after_validation" not in execution_log
    assert "pending_update_after_validation" not in receipt
    assert any(marker in execution_log for marker in ["Gate 202 is now the active gate in this pack.", "Gate 203 is now the active gate in this pack.", "Gate 205 is now the active gate in this pack."])
    assert any(marker in checklist for marker in ["Gates 200-201 complete on `main`, Gate 202 active.", "Gates 200-202 complete on `main`, Gate 203 active.", "Gates 200-204 complete on `main`, Gate 205 active."])
