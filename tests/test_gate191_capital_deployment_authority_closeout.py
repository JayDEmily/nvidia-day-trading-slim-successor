"""Gate 191 capital-deployment authority closeout checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_EXECUTION_LOG_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md"
SCOPE_NOTE = REPO_ROOT / "docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_SCOPE_NOTE_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-03_GATE191_CAPITAL_DEPLOYMENT_AUTHORITY_CLOSEOUT.md"


def test_gate191_control_surfaces_close_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "- none currently routed" in plans
    assert "docs/planning/2026-04-03_CAPITAL_DEPLOYMENT_AUTHORITY_FOUNDATION_GATES_v1.md" in plans
    assert "Current active gate: **none — capital-deployment authority foundation pack closed through Gate 191 on `main`**." in gate_map
    assert "Status: closed capital-deployment authority foundation pack through Gate 191 on `main`" in gates
    assert leaves["execution_status"] == "capital_deployment_authority_foundation_pack_closed_through_gate_191_on_main"
    assert leaves["active_gate"] == "none"
    assert leaves["remaining_leaf_ids"] == []
    assert leaves["pending_gate_ids"] == []
    assert leaves["completed_gate_ids"] == ["Gate 187", "Gate 188", "Gate 189", "Gate 190", "Gate 191"]
    assert all(leaf["status"] == "complete" for leaf in leaves["leaves"].values())
    assert "Observed result: `25 passed" in execution_log
    assert "Observed result: `17 passed" in execution_log
    assert "capital-deployment authority foundation pack closed through Gate 191 on `main`." in checklist


def test_gate191_receipt_records_closeout_and_packaging() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    scope = SCOPE_NOTE.read_text(encoding="utf-8")

    assert "CapitalDeploymentAuthorityService is closed as a bounded downstream capital authoriser" in receipt
    assert "no active pack currently routed; capital-deployment authority foundation pack closed through Gate 191 on `main`" in receipt
    assert "repo_capital_deployment_authority_pack_closed_gate191_main_fullgit_2026-04-03.zip" in receipt
    assert "recommendation-memory lookback logic" in scope
