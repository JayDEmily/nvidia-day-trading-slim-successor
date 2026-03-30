"""Gate 112 governance-pack closeout checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_EXECUTION_LOG_v1.md"
CLOSEOUT = REPO_ROOT / "docs/planning/2026-03-30_GATE112_REPO_PROCESS_GOVERNANCE_CLOSEOUT.md"


def test_governance_pack_is_closed_honestly_across_the_quartet() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "## Active pack\n\n- none" in plans
    assert ("repo-process governance pack closed through Gate 112 on `main`" in plans) or ("2026-03-30_REPO_PROCESS_GOVERNANCE_GATES_v1.md" in plans)
    assert ("Current active gate: **none — repo-process governance pack closed through Gate 112 on `main`**." in gate_map) or ("Current active gate: **none — execution-authority microtranche closed through Gate 113 on `main`**." in gate_map)
    assert "| Gate 112 | complete on `main` |" in gate_map
    assert "Status: closed repo-process governance pack on `main`; Gates 107-112 complete, no active gate" in gates
    assert leaves["execution_status"] == "repo_process_governance_pack_closed_through_gate_112_on_main"
    assert leaves["active_gate"] == "none — repo-process governance pack closed through Gate 112 on main"
    assert leaves["completed_gate_ids"] == ["Gate 107", "Gate 108", "Gate 109", "Gate 110", "Gate 111", "Gate 112"]
    assert leaves["remaining_leaf_ids"] == []
    assert "Status: closed execution log for the repo-process governance pack; Gates 107-112 complete on `main`, no active gate" in execution_log


def test_gate112_closeout_doc_freezes_packaging_intent() -> None:
    closeout = CLOSEOUT.read_text(encoding="utf-8")
    assert "Status: Gate 112 complete on `main`; repo-process governance pack closed honestly" in closeout
    assert "The repo-process governance pack is closed through Gate 112 on `main`." in closeout
    assert "nvda_repo_process_governance_pack_closed_gate112_main_2026-03-30.zip" in closeout
