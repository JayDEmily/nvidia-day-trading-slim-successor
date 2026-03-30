"""Gate 111 governance guard tests."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROCESS_LAW = REPO_ROOT / "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md"
AGENTS = REPO_ROOT / "AGENTS.md"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_EXECUTION_LOG_v1.md"


ALLOWED_CURRENT_GATE_MARKERS = {
    "Current active gate: **Gate 111 in the repo-process governance pack**.",
    "Current active gate: **Gate 112 in the repo-process governance pack**.",
    "Current active gate: **none — repo-process governance pack closed through Gate 112 on `main`**.",
    "Current active gate: **none — execution-authority microtranche closed through Gate 113 on `main`**.",
    "Current active gate: **none — research-mode clarity microtranche closed through Gate 114 on `main`**.",
    "Current active gate: **Gate 115 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 116 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 117 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 118 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 119 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 120 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 121 in the historical-evaluation readiness pack**.",
    "Current active gate: **none — historical-evaluation readiness pack closed through Gate 121 on `main`**.",
    "Current active gate: **Gate 122 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 123 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 124 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 125 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 126 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 127 in the signal-coefficient authority pack**.",
    "Current active gate: **none — signal-coefficient authority pack closed through Gate 127 on `main`**.",
}


def test_router_process_law_and_agents_are_coherent() -> None:
    process_law = PROCESS_LAW.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")
    plans = PLANS.read_text(encoding="utf-8")

    assert "## Control-surface routing law" in process_law
    assert "PLANS.md` is a router only" in process_law
    assert "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md" in agents
    assert "## Active pack" in plans
    assert "The persisted `main` baseline is now closed through Gate 105" not in plans


def test_governance_trio_agrees_on_gate111_or_later() -> None:
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "Gate 111: Governance guard tests" in gates
    assert leaves["execution_status"] in {
        "gate_110_governance_pack_active_from_gate_111",
        "gate_111_governance_pack_active_from_gate_112",
        "repo_process_governance_pack_closed_through_gate_112_on_main",
    }
    assert leaves["active_gate"] in {"Gate 111", "Gate 112", "none — repo-process governance pack closed through Gate 112 on main"}
    assert any(marker in gate_map for marker in ALLOWED_CURRENT_GATE_MARKERS)
    assert (
        "Status: active execution log for the repo-process governance pack; Gates 107-110 complete on `main`, Gate 111 next" in execution_log
        or "Status: active execution log for the repo-process governance pack; Gates 107-111 complete on `main`, Gate 112 next" in execution_log
        or "Status: closed execution log for the repo-process governance pack; Gates 107-112 complete on `main`, no active gate" in execution_log
    )
