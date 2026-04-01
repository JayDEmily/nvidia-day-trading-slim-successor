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


def test_gate141_pack_remains_active_after_later_gate_progression() -> None:
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
    assert (
        "Status: active stage-local handoff and terminal-risk seams pack; Gate 141 complete on `main`, Gate 142 active, Gates 143-149 planned" in gates
        or "Status: active stage-local handoff and terminal-risk seams pack; Gates 141-142 complete on `main`, Gate 143 active, Gates 144-149 planned" in gates
        or "Status: active stage-local handoff and terminal-risk seams pack; Gates 141-143 complete on `main`, Gate 144 active, Gates 145-149 planned" in gates
        or "Status: active stage-local handoff and terminal-risk seams pack; Gates 141-144 complete on `main`, Gate 145 active, Gates 146-149 planned" in gates
        or "Status: active stage-local handoff and terminal-risk seams pack; Gates 141-145 complete on `main`, Gate 146 active, Gates 147-149 planned" in gates
    )
    assert leaves["execution_status"] in {
        "gate_141_complete_gate_142_active_on_main",
        "gate_142_complete_gate_143_active_on_main",
        "gate_143_complete_gate_144_active_on_main",
        "gate_144_complete_gate_145_active_on_main",
        "gate_145_complete_gate_146_active_on_main",
    }
    assert leaves["active_gate"] in {"Gate 142", "Gate 143", "Gate 144", "Gate 145", "Gate 146"}
    assert leaves["completed_gate_ids"][:1] == ["Gate 141"]
    assert len(leaves["completed_leaf_ids"]) >= 4
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
