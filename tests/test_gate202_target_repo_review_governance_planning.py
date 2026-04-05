"""Gate 202 review-governance planning checks."""

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
SCORECARD = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_EVIDENCE_COVERAGE_SCORECARD_AND_GAP_REGISTER_v1.md"
REDUNDANCY = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_EVIDENCE_REDUNDANCY_AND_COVERAGE_STRENGTHENING_RULES_v1.md"
SEMANTIC = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_EVIDENCE_SEMANTIC_REVIEW_AND_DISAGREEMENT_MEMORY_RULES_v1.md"
PROOF_SLICE = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_EVIDENCE_REVIEW_GOVERNANCE_PROOF_SLICE_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-05_GATE202_TARGET_REPO_COVERAGE_REVIEW_AND_DISAGREEMENT_PLANNING.md"


def test_gate202_control_surfaces_and_docs_are_coherent() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    scorecard = SCORECARD.read_text(encoding="utf-8")
    redundancy = REDUNDANCY.read_text(encoding="utf-8")
    semantic = SEMANTIC.read_text(encoding="utf-8")
    proof_slice = PROOF_SLICE.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "- next active gate: `Gate 203`" in plans
    assert "Current active gate: **Gate 203 in the target-repo admitted-evidence successor planning pack on `main`**." in gate_map
    assert "Status: active target-repo admitted-evidence successor planning pack; Gates 200-202 complete on `main`, Gate 203 active, Gates 204-205 planned." in gates
    assert payload["execution_status"] == "gates_200_202_complete_gate_203_active_on_main"
    assert payload["active_gate"] == "Gate 203"
    assert payload["completed_gate_ids"] == ["Gate 200", "Gate 201", "Gate 202"]
    assert payload["pending_gate_ids"] == ["Gate 203", "Gate 204", "Gate 205"]

    assert "Coverage scorecard axes" in scorecard
    assert "GAP-RAW-002" in scorecard
    assert "market-persisted reference state" in scorecard

    assert "Core decision outcomes" in redundancy
    assert "reject_duplicate" in redundancy
    assert "accept_strengthening_existing_family" in redundancy

    assert "Required worksheet fields" in semantic
    assert "review_outcome" in semantic
    assert "resolved_with_memory" in semantic
    assert "Semantic-review memory may inform later governance" in semantic

    assert "Ordered proof commands" in proof_slice
    assert "tests/test_gate202_target_repo_review_governance_planning.py" in proof_slice
    assert "GitHub branch and commit history preserve the closeout lineage" in proof_slice

    assert "Gate 203 is the next active gate" in receipt
    assert "PENDING_UPDATE_AFTER_VALIDATION" not in execution_log
    assert "PENDING_UPDATE_AFTER_VALIDATION" not in receipt
    assert "Gate 203 is now the active gate in this pack." in execution_log
    assert "Gates 200-202 complete on `main`, Gate 203 active." in checklist
