"""Gate 107 governance-pack activation checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROCESS_LAW = REPO_ROOT / "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md"
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_EXECUTION_LOG_v1.md"

ALLOWED_CURRENT_GATE_MARKERS = {
    "Current active gate: **Gate 108 in the repo-process governance pack**.",
    "Current active gate: **Gate 109 in the repo-process governance pack**.",
    "Current active gate: **Gate 110 in the repo-process governance pack**.",
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


def test_process_law_exists_and_has_precedence() -> None:
    process_law = PROCESS_LAW.read_text(encoding="utf-8")
    normative = NORMATIVE.read_text(encoding="utf-8")

    assert "# 06_REPO_PROCESS_AND_TRANCHE_LAW" in process_law
    assert "## Planning mode" in process_law
    assert "## Execution mode" in process_law
    assert "## Control-surface routing law" in process_law
    assert "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md" in normative


def test_governance_pack_is_present_and_either_active_or_honestly_closed() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "2026-03-30_REPO_PROCESS_GOVERNANCE_GATES_v1.md" in plans
    assert "2026-03-30_REPO_PROCESS_GOVERNANCE_LEAVES_v1.json" in plans
    assert "2026-03-30_REPO_PROCESS_GOVERNANCE_EXECUTION_LOG_v1.md" in plans
    assert ("closed through Gate 112" in plans) or ("2026-03-30_HISTORICAL_EVALUATION_READINESS_GATES_v1.md" in plans)
    assert any(marker in gate_map for marker in ALLOWED_CURRENT_GATE_MARKERS)
    assert "Gate 107: Permanent process-law installation and governance-pack activation" in gates
    assert execution_log.startswith("# 2026-03-30_REPO_PROCESS_GOVERNANCE_EXECUTION_LOG_v1")
    assert leaves["governing_plan"] == "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_GATES_v1.md"
    assert leaves["completed_gate_ids"][0] == "Gate 107"
