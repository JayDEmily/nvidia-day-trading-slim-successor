"""Gate 203 snapshot and collection planning checks."""

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
SNAPSHOT = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_SNAPSHOT_HANDOFF_BRIEF_AND_INPUT_BUNDLE_CONTRACT_v1.md"
DOSSIER = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_REAL_ANCHOR_COLLECTION_AND_ADMISSION_DOSSIER_RULES_v1.md"
PROOF_MATRIX = REPO_ROOT / "docs/planning/2026-04-05_TARGET_REPO_SNAPSHOT_AND_COLLECTION_PROOF_MATRIX_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-05_GATE203_TARGET_REPO_SNAPSHOT_EXECUTION_AND_REAL_ANCHOR_COLLECTION_PLANNING.md"


def test_gate203_control_surfaces_and_docs_are_coherent() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    snapshot = SNAPSHOT.read_text(encoding="utf-8")
    dossier = DOSSIER.read_text(encoding="utf-8")
    proof_matrix = PROOF_MATRIX.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert any(marker in plans for marker in ["- next active gate: `Gate 204`", "- next active gate: `Gate 205`", "- no active pack currently routed"])
    assert any(marker in gate_map for marker in ["Current active gate: **Gate 204 in the target-repo admitted-evidence successor planning pack on `main`**.", "Current active gate: **Gate 205 in the target-repo admitted-evidence successor planning pack on `main`**.", "Current active gate: **none — target-repo admitted-evidence successor planning pack closed through Gate 205 on `work/gate-205-successor-pack-closeout-handoff-20260406`**.", "Current active gate: **none — target-repo admitted-evidence successor planning pack closed through Gate 205 on `main`**."])
    assert any(status in gates for status in ["Status: active target-repo admitted-evidence successor planning pack; Gates 200-203 complete on `main`, Gate 204 active, Gate 205 planned.", "Status: active target-repo admitted-evidence successor planning pack; Gates 200-204 complete on `main`, Gate 205 active.", "Status: closed target-repo admitted-evidence successor planning pack through Gate 205 on `work/gate-205-successor-pack-closeout-handoff-20260406`.", "Status: closed target-repo admitted-evidence successor planning pack through Gate 205 on `main`."])
    assert payload["execution_status"] in {"gates_200_203_complete_gate_204_active_on_main", "gates_200_204_complete_gate_205_active_on_main", "target_repo_admitted_evidence_successor_pack_closed_through_gate_205_on_work_branch", "target_repo_admitted_evidence_successor_pack_closed_through_gate_205_on_main"}
    assert payload["active_gate"] in {"Gate 204", "Gate 205", "none"}
    assert payload["completed_gate_ids"] in [["Gate 200", "Gate 201", "Gate 202", "Gate 203"], ["Gate 200", "Gate 201", "Gate 202", "Gate 203", "Gate 204"], ["Gate 200", "Gate 201", "Gate 202", "Gate 203", "Gate 204", "Gate 205"]]
    assert payload["pending_gate_ids"] in [["Gate 204", "Gate 205"], ["Gate 205"], []]

    assert "Snapshot identity block" in snapshot
    assert "`RealDataLoaderService.prepare_runtime_dataset(...)`" in snapshot
    assert "option_snapshot" in snapshot

    assert "Mandatory admission dossier fields" in dossier
    assert "OptionSnapshot" in dossier
    assert "StrategicLadderMarketService.get_option_surface(...)" in dossier

    assert "Ordered proof commands" in proof_matrix
    assert "dossier_exists_for_each_candidate" in proof_matrix
    assert "GitHub branch and commit history preserve the closeout lineage" in proof_matrix

    assert any(marker in receipt for marker in ["Gate 204 is the next active gate", "Gate 205 is the next active gate"])
    assert "pending_update_after_validation" not in execution_log
    assert "pending_update_after_validation" not in receipt
    assert any(marker in execution_log for marker in ["Gate 204 is now the active gate in this pack.", "Gate 205 is now the active gate in this pack.", "no active pack is currently routed"])
    assert any(marker in checklist for marker in ["DMP packet failure-pack planning docs and tests", "Gates 200-204 complete on `main`, Gate 205 active.", "through Gate 205 on `work/gate-205-successor-pack-closeout-handoff-20260406`", "through Gate 205 on `main`"])
