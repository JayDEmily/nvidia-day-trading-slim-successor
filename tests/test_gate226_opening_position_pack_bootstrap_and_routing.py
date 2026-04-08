"""Gate 226 opening-position pack bootstrap and routing invariants."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_EXECUTION_LOG_v1.md"
SCOPE_NOTE = REPO_ROOT / "docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_SCOPE_NOTE_v1.md"
CONTRADICTION_REPORT = REPO_ROOT / "docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_CONTRADICTION_REPORT_v1.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_DOCUMENT_TOUCH_CHECKLIST_v1.md"

ACTIVE_GATES_DOC = "docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1.md"
ACTIVE_LEAVES_DOC = "docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json"
ACTIVE_EXECUTION_LOG_DOC = "docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_EXECUTION_LOG_v1.md"
ACTIVE_SCOPE_NOTE_DOC = "docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_SCOPE_NOTE_v1.md"
ACTIVE_CONTRADICTION_REPORT_DOC = "docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_CONTRADICTION_REPORT_v1.md"


def test_gate226_routes_new_pack_and_stops_before_gate227_activation() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    scope_note = SCOPE_NOTE.read_text(encoding="utf-8")
    contradiction_report = CONTRADICTION_REPORT.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert ACTIVE_GATES_DOC in plans
    assert ACTIVE_LEAVES_DOC in plans
    assert ACTIVE_EXECUTION_LOG_DOC in plans
    assert ACTIVE_SCOPE_NOTE_DOC in plans
    assert ACTIVE_CONTRADICTION_REPORT_DOC in plans
    assert "## Active pack\n\n- none" not in plans
    assert "Gate 226 is complete on `work/gate-226-pack-bootstrap-and-routing-20260408` and Gate 227 is not yet activated" in plans

    assert "Version: v1.42" in gate_map
    assert "Current active gate: **No active gate under the opening-position domain isolation and interface hardening pack. Gate 226 is complete on `work/gate-226-pack-bootstrap-and-routing-20260408`; Gate 227 is not yet activated.**" in gate_map
    for gate_id in ("Gate 226", "Gate 227", "Gate 228", "Gate 229", "Gate 230", "Gate 231", "Gate 232", "Gate 233", "Gate 234", "Gate 235"):
        assert f"| {gate_id} |" in gate_map

    assert payload["governing_plan"] == ACTIVE_GATES_DOC
    assert payload["routing_status"] == "active_pack_routed_gate_226_complete_gate_227_not_yet_activated"
    assert payload["execution_status"] == "gate_226_complete_on_work_branch_gate_227_not_yet_activated"
    assert payload["active_gate"] == "none — Gate 226 complete on `work/gate-226-pack-bootstrap-and-routing-20260408`; Gate 227 not yet activated"
    assert payload["completed_gate_ids"] == ["Gate 226"]
    assert payload["pending_gate_ids"] == ["Gate 227", "Gate 228", "Gate 229", "Gate 230", "Gate 231", "Gate 232", "Gate 233", "Gate 234", "Gate 235"]
    assert set(payload["completed_leaf_ids"]) == {f"LEAF-G226-00{i}" for i in range(1, 6)}
    assert all(leaf["status"] == "complete" for leaf in payload["leaves"] if leaf["id"].startswith("LEAF-G226-"))

    assert "Status: active planning pack for Gates 226-235. Gate 226 is complete on `work/gate-226-pack-bootstrap-and-routing-20260408`; Gate 227 is not yet activated." in gates
    assert "### Gate 226: Pack bootstrap, contradiction scan, and active-pack routing closeout" in gates
    assert "repo-root routing has occurred and the active pack is truthful without falsely claiming Gate 227 execution has already started" in gates

    assert "sandbox repo initialised with Git from the uploaded successor zip" in execution_log
    assert "Gate 226 closeout proof" in execution_log
    assert "Gate 227 was not activated at Gate 226 closeout." in execution_log

    assert "This scope note is now part of the routed active pack for Gates 226-235." in scope_note
    assert "Gate 226 completed the normal quartet update" in contradiction_report
    assert "This checklist was drafted during planning and then used in Gate 226 to route the active pack truthfully." in checklist
