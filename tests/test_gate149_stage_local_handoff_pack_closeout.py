"""Gate 149 anti-drift closeout checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = (
    REPO_ROOT / "docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_GATES_v1.md"
)
LEAVES = (
    REPO_ROOT
    / "docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_LEAVES_v1.json"
)
EXECUTION_LOG = (
    REPO_ROOT
    / "docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_EXECUTION_LOG_v1.md"
)
CHECKLIST = (
    REPO_ROOT
    / "docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_DOCUMENT_TOUCH_CHECKLIST_v1.md"
)
RECEIPT = (
    REPO_ROOT / "docs/planning/2026-04-01_GATE149_ABSOLUTE_ANTI_DRIFT_AUDIT_AND_PACK_CLOSEOUT.md"
)


def test_gate149_pack_closeout_control_surfaces_agree() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert (
        "no active pack currently routed; stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`"
        in plans
        or "active gate: Gate 149 reopened on `work/gate-149-reopen-full-suite-closeout-20260402`"
        in plans
        or "active gate: Gate 151 on `work/gate-150-corrective-successor-pack-20260402`" in plans
        or "active gate: Gate 152 on `main`" in plans
        or "active gate: Gate 153 on `main`" in plans
        or "active gate: Gate 154 on `main`" in plans
        or "active gate: Gate 155 on `main`" in plans
        or "active gate: Gate 156 on `main`" in plans
        or "no active pack currently routed; stage-local handoff corrective successor pack closed through Gate 156 on `main`"
        in plans
    )
    assert (
        "Current active gate: **none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`**."
        in gate_map
        or "Current active gate: **Gate 149 in the stage-local handoff and terminal-risk seams pack**."
        in gate_map
        or "Current active gate: **Gate 151 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 152 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 153 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 154 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 155 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 156 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **none — stage-local handoff corrective successor pack closed through Gate 156 on `main`**."
        in gate_map
    )
    assert (
        "Status: closed stage-local handoff and terminal-risk seams pack through Gate 149 on `main`"
        in gates
        or "Status: active stage-local handoff and terminal-risk seams pack; Gates 141-148 complete on `main`, Gate 149 reopened"
        in gates
    )
    assert leaves["execution_status"] in {
        "stage_local_handoff_and_terminal_risk_seams_pack_closed_through_gate_149_on_main",
        "gate_148_complete_gate_149_reopened_for_full_suite_closeout_on_branch",
    }
    assert leaves["active_gate"] in {
        "none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on main",
        "Gate 149",
    }
    assert leaves["remaining_leaf_ids"] == [] or leaves["remaining_leaf_ids"] == [
        "LEAF-G149-001",
        "LEAF-G149-002",
        "LEAF-G149-003",
    ]
    assert (
        "Status: closed execution log for the stage-local handoff and terminal-risk seams pack; Gates 141-149 complete on `main`, no active gate"
        in execution_log
        or "Status: active execution log for the stage-local handoff and terminal-risk seams pack; Gates 141-148 complete on `main`, Gate 149 reopened"
        in execution_log
    )
    assert "Gate 149" in checklist
    assert "Run the absolute anti-drift audit" in receipt
    assert "No new governed vocabulary is admitted in Gate 149." in receipt
