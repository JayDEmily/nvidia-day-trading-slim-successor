"""Gate 108 router-only control-surface checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-30_REPO_PROCESS_GOVERNANCE_EXECUTION_LOG_v1.md"


def test_plans_md_is_router_only_and_points_at_gate109() -> None:
    plans = PLANS.read_text(encoding="utf-8")

    assert "## Active pack" in plans
    assert "Gate 108 — complete on `main` in the repo-process governance pack" in plans
    assert "Gate 109 — next active gate on `main` in the repo-process governance pack" in plans
    assert "The persisted `main` baseline is now closed through Gate 105" not in plans
    assert "Gate 102 is the next active gate" not in plans


def test_gate_map_and_governance_trio_agree_on_gate109() -> None:
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "Current active gate: **Gate 109 in the repo-process governance pack**." in gate_map
    assert "| Gate 108 | complete on `main` |" in gate_map
    assert "| Gate 109 | planned; next active gate |" in gate_map
    assert leaves["execution_status"] == "gate_108_governance_pack_active_from_gate_109"
    assert leaves["active_gate"] == "Gate 109"
    assert "Status: active execution log for the repo-process governance pack; Gates 107-108 complete on `main`, Gate 109 next" in execution_log
