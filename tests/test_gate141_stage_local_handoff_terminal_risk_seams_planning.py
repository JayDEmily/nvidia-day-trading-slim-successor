"""Gate 141 stage-local handoff and terminal-risk seams planning checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_DOCUMENT_TOUCH_CHECKLIST_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-01_GATE141_STAGE_LOCAL_HANDOFF_PACK_BOOTSTRAP.md"

ALLOWED_CURRENT_GATE_MARKERS = {
    "Current active gate: **Gate 142 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **Gate 143 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **Gate 144 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **Gate 145 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **Gate 146 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **Gate 147 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **Gate 148 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **Gate 149 in the stage-local handoff and terminal-risk seams pack**.",
    "Current active gate: **none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`**.",
}


def test_gate141_pack_is_active_and_gate142_is_now_routed() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_GATES_v1.md" in plans
    assert "2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_LEAVES_v1.json" in plans
    assert "2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_EXECUTION_LOG_v1.md" in plans
    assert "2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_DOCUMENT_TOUCH_CHECKLIST_v1.md" in plans
    assert any(marker in gate_map for marker in ALLOWED_CURRENT_GATE_MARKERS)
    assert "Status: active stage-local handoff and terminal-risk seams pack; Gate 141 complete on `main`, Gate 142 active, Gates 143-149 planned" in gates
    assert leaves["execution_status"] == "gate_141_complete_gate_142_active_on_main"
    assert leaves["active_gate"] == "Gate 142"
    assert leaves["completed_gate_ids"] == ["Gate 141"]
    assert len(leaves["completed_leaf_ids"]) == 4
    assert execution_log.startswith("# 2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_EXECUTION_LOG_v1")
    assert "Gate 141 -> Gate 142" in checklist or "Gate 141" in checklist


def test_gate141_freezes_workflow_trace_and_authority_rules() -> None:
    gates = GATES.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "## Active vocabulary authority for execution threads" in gates
    assert "## Active packet / data contract authority for execution threads" in gates
    assert "stage-local handoff artefact" in gates
    assert "terminal-risk application seam" in gates
    assert "Gate 141 is planning-only" in gates
    assert "cognition_runtime.py" in receipt
    assert "modifier-mutated posture" in receipt
    assert "final mutated execution packet" in receipt
    assert leaves["global_rules"]["no_new_governed_runtime_vocabulary_in_gate_141"] is True
    assert leaves["global_rules"]["no_runtime_behavior_change_in_gate_141"] is True
