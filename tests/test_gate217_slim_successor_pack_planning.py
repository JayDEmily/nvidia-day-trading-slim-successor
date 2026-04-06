"""Gate 217 slim-successor pack bootstrap routing checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
AGENTS = REPO_ROOT / "AGENTS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_EXECUTION_LOG_v1.md"
RUNTIME_LEDGER = REPO_ROOT / "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md"
DIFF_NOTE = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_07_SOURCE_DIFF_AND_AGENTS_READ_TRIGGER_NOTE_v1.md"

ACTIVE_BRANCH = "work/gate-217-slim-successor-pack-bootstrap-and-routing-20260406"
ACTIVE_GATES_DOC = "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_GATES_v1.md"
ACTIVE_LEAVES_DOC = "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_LEAVES_v1.json"
ACTIVE_EXECUTION_LOG_DOC = "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_EXECUTION_LOG_v1.md"


def test_gate217_pack_is_complete_and_gate218_is_not_activated() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    runtime_ledger = RUNTIME_LEDGER.read_text(encoding="utf-8")
    diff_note = DIFF_NOTE.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert ACTIVE_GATES_DOC in plans
    assert ACTIVE_LEAVES_DOC in plans
    assert ACTIVE_EXECUTION_LOG_DOC in plans
    assert "no active pack currently routed" not in plans
    assert "- next active gate: `Gate 218`" in plans
    assert (
        "- active pack: slim active-repo cutover and substantive test-audit bootstrap pack "
        f"with Gate 217 complete on `{ACTIVE_BRANCH}`; Gate 218 not yet activated"
    ) in plans

    assert "specialised runtime authority ledger" in agents
    assert "not a universal front-door doctrine file" in agents
    assert "runtime surface ownership" in agents
    assert "stage packet versus workflow packet authority" in agents
    assert "compatibility surface or compatibility carriage law" in agents
    assert "downstream runtime reader permissions" in agents
    assert "replay or bounded-trace or review seam interpretation" in agents
    assert "API compatibility wrappers that preserve older read shapes over newer canonical runtime truth" in agents

    assert "## 0. Classification and read-trigger" in runtime_ledger
    assert "This document is a **specialised runtime authority ledger**." in runtime_ledger
    assert "It is **not** a universal front-door doctrine file" in runtime_ledger
    assert "## 1.1 Relation to the wider doc stack" in runtime_ledger
    assert "## 1.2 Maintenance law" in runtime_ledger

    assert "Version: v1.30" in gate_map
    assert (
        "Current active gate: **none — Gate 217 in the slim active-repo cutover and substantive "
        f"test-audit bootstrap pack is complete on `{ACTIVE_BRANCH}`, and Gate 218 is planned but not yet activated.**"
    ) in gate_map
    assert "Gate 210 | complete on `work/gate-210-operator-surface-alignment-and-active-repo-cutover-criteria-20260406`" in gate_map
    assert f"Gate 217 | complete on `{ACTIVE_BRANCH}`" in gate_map
    assert "Gate 218 | planned" in gate_map
    assert "Gate 219 | planned" in gate_map
    assert "Gate 220 | planned" in gate_map
    assert "Gate 221 | planned" in gate_map
    assert "Gate 218 is planned but not yet activated" in gate_map

    assert (
        "Status: slim-successor planning pack with Gate 217 complete on "
        f"`{ACTIVE_BRANCH}`; Gates 218-221 planned, Gate 218 not yet activated."
    ) in gates
    assert "This document is the active gate authority for the slim successor repo only." in gates
    assert "It must not claim runtime behaviour changed merely because the doctrine text was rewritten." in diff_note

    assert payload["governing_plan"] == ACTIVE_GATES_DOC
    assert payload["execution_status"] == "gate_217_complete_on_work_branch_gate_218_not_yet_activated"
    assert (
        payload["active_gate"]
        == "none — Gate 217 complete on work/gate-217-slim-successor-pack-bootstrap-and-routing-20260406; Gate 218 not yet activated"
    )
    assert payload["completed_gate_ids"] == ["Gate 217"]
    assert payload["completed_leaf_ids"] == ["LEAF-G217-001", "LEAF-G217-002", "LEAF-G217-003"]
    assert payload["pending_gate_ids"] == ["Gate 218", "Gate 219", "Gate 220", "Gate 221"]
    assert len(payload["remaining_leaf_ids"]) == 8
    assert set(payload["completed_leaf_ids"]).isdisjoint(payload["remaining_leaf_ids"])

    assert (
        "Status: successor execution log for slim active-repo cutover and substantive test-audit "
        f"bootstrap; Gate 217 complete on `{ACTIVE_BRANCH}`, Gates 218-221 planned, Gate 218 not yet activated."
    ) in execution_log
    assert "### LEAF-G217-001" in execution_log
    assert "### LEAF-G217-002" in execution_log
    assert "### LEAF-G217-003" in execution_log
    assert (
        "Gate 217 is complete on "
        f"`{ACTIVE_BRANCH}`."
    ) in execution_log
    assert "Gate 218 remains planned and is not yet activated." in execution_log
    assert "Gate 218 is active" not in execution_log
    assert "Gate 219 is active" not in execution_log
    assert "Gate 220 is active" not in execution_log
    assert "Gate 221 is active" not in execution_log
