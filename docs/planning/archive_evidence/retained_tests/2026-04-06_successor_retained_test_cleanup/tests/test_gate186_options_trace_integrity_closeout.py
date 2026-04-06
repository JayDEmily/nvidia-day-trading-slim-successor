"""Gate 186 options-trace integrity closeout checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_DOCUMENT_TOUCH_CHECKLIST_v1.md"
SCOPE_NOTE = REPO_ROOT / "docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_SCOPE_NOTE_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-03_GATE186_OPTIONS_TRACE_INTEGRITY_CLOSEOUT.md"


def test_gate186_control_surfaces_close_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert any(marker in plans for marker in ["- none currently routed", "docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_GATES_v1.md", "docs/planning/2026-04-05_TARGET_REPO_ADMITTED_EVIDENCE_SUCCESSOR_GATES_v1.md"])
    assert "docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_GATES_v1.md" in plans
    assert any(marker in gate_map for marker in ["Current active gate: **none — options-trace integrity repair pack closed through Gate 186 on `main`**.", "Current active gate: **Gate 188 in the capital-deployment authority foundation pack**.", "Current active gate: **none — capital-deployment authority foundation pack closed through Gate 191 on `main`**.", "Current active gate: **Gate 200 in the target-repo admitted-evidence successor planning pack on `work/gate-200-target-repo-admitted-evidence-successor-pack-20260405`**."])
    assert "Status: closed options-trace integrity repair pack through Gate 186 on `main`" in gates
    assert leaves["execution_status"] == "options_trace_integrity_repair_pack_closed_through_gate_186_on_main"
    assert leaves["active_gate"] == "none"
    assert leaves["remaining_leaf_ids"] == []
    assert leaves["pending_gate_ids"] == []
    assert leaves["completed_gate_ids"] == [
        "Gate 181",
        "Gate 182",
        "Gate 183",
        "Gate 184",
        "Gate 185",
        "Gate 186",
    ]
    assert all(leaf["status"] == "complete" for leaf in leaves["leaves"].values())
    assert "Observed result: `62 passed in 12.76s`" in execution_log
    assert "Current planned sequence\n\noptions-trace integrity repair pack closed through Gate 186 on `main`." in checklist


def test_gate186_receipt_records_bug_split_and_packaging() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    scope = SCOPE_NOTE.read_text(encoding="utf-8")

    assert "F1, F2, and F4 are repaired on the checked-in code path." in receipt
    assert "F3 is addressed as a bounded feature addition" in receipt
    assert "F5 remained out of scope." in receipt
    assert "repo_options_trace_integrity_repair_pack_closed_gate186_main_fullgit_2026-04-03.zip" in receipt
    assert "surface_anchor_to_spot_pct" in scope
