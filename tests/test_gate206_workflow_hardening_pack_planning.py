"""Gate 206 workflow-hardening pack bootstrap checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md"
SCOPE_NOTE = REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_SCOPE_NOTE_v1.md"
CONTRADICTION = REPO_ROOT / "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_CONTRADICTION_REPORT_v1.md"


def test_gate206_pack_bootstrap_is_coherent() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")
    contradiction = CONTRADICTION.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_GATES_v1.md" in plans
    assert "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_LEAVES_v1.json" in plans
    assert "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_EXECUTION_LOG_v1.md" in plans
    assert "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md" in plans
    assert "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_SCOPE_NOTE_v1.md" in plans
    assert "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_CONTRADICTION_REPORT_v1.md" in plans
    assert "- next active gate: `Gate 206`" in plans

    assert "Current active gate: **Gate 206 in the workflow hardening and active-repo reset foundation pack on `work/gate-206-workflow-hardening-and-active-repo-reset-foundation-20260406`**." in gate_map
    assert "Gate 205 | complete on `main`" in gate_map
    assert "Gate 206 | active on `work/gate-206-workflow-hardening-and-active-repo-reset-foundation-20260406`" in gate_map
    assert "Gate 207 | planned" in gate_map
    assert "Gate 210 | planned" in gate_map

    assert payload["governing_plan"] == "docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_GATES_v1.md"
    assert payload["execution_status"] == "gate_206_active"
    assert payload["active_gate"] == "Gate 206"
    assert payload["completed_gate_ids"] == []
    assert payload["completed_leaf_ids"] == []
    assert payload["remaining_leaf_ids"][0] == "LEAF-G206-001"
    assert payload["leaves"][0]["id"] == "LEAF-G206-001"
    assert payload["leaves"][0]["status"] == "planned"

    assert "Status: active execution log for workflow hardening and active-repo reset foundation; Gate 206 active, no leaves completed yet" in execution_log
    assert "Receipt-empty at pack bootstrap." in execution_log
    assert "GitHub branch/commit/merge receipts are the default execution ledger" in execution_log

    assert "current active gates master — none currently routed when this pack was written" in checklist
    assert "contradiction report" in checklist
    assert "one active pack exists again" in scope_note
    assert "Proceed with a new planning pack." in contradiction
    assert "template pack still encodes routine zip handoff as the default completion model" in contradiction
