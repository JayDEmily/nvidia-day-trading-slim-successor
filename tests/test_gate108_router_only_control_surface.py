"""Gate 108 router-only control-surface checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_EXECUTION_LOG_v1.md"

ALLOWED_CURRENT_GATE_MARKERS = {
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
    "Current active gate: **Gate 128 in the post-flight repo consistency pack**.",
    "Current active gate: **Gate 129 in the post-flight repo consistency pack**.",
    "Current active gate: **Gate 130 in the post-flight repo consistency pack**.",
    "Current active gate: **Gate 131 in the post-flight repo consistency pack**.",
    "Current active gate: **none — post-flight repo consistency pack closed through Gate 131 on `main`**.",
}


def test_plans_md_is_router_only_and_points_at_gate109_or_later() -> None:
    plans = PLANS.read_text(encoding="utf-8")

    assert "## Active pack" in plans
    assert ("- none" in plans) or ("2026-03-30_HISTORICAL_EVALUATION_READINESS_GATES_v1.md" in plans) or ("2026-03-31_POST_FLIGHT_REPO_CONSISTENCY_GATES_v1.md" in plans)
    assert "The persisted `main` baseline is now closed through Gate 105" not in plans
    assert "Gate 102 is the next active gate" not in plans


def test_gate_map_and_governance_trio_agree_on_gate109_or_later() -> None:
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert any(marker in gate_map for marker in ALLOWED_CURRENT_GATE_MARKERS)
    assert "| Gate 108 | complete on `main` |" in gate_map
    assert leaves["execution_status"] in {
        "gate_108_governance_pack_active_from_gate_109",
        "gate_109_governance_pack_active_from_gate_110",
        "gate_110_governance_pack_active_from_gate_111",
        "gate_111_governance_pack_active_from_gate_112",
        "repo_process_governance_pack_closed_through_gate_112_on_main",
    }
    assert leaves["active_gate"] in {"Gate 109", "Gate 110", "Gate 111", "Gate 112", "none — repo-process governance pack closed through Gate 112 on main"}
    assert (
        "Status: active execution log for the repo-process governance pack; Gates 107-108 complete on `main`, Gate 109 next" in execution_log
        or "Status: active execution log for the repo-process governance pack; Gates 107-109 complete on `main`, Gate 110 next" in execution_log
        or "Status: active execution log for the repo-process governance pack; Gates 107-110 complete on `main`, Gate 111 next" in execution_log
        or "Status: active execution log for the repo-process governance pack; Gates 107-111 complete on `main`, Gate 112 next" in execution_log
        or "Status: closed execution log for the repo-process governance pack; Gates 107-112 complete on `main`, no active gate" in execution_log
    )
