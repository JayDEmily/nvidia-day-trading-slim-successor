"""Gate 255 live prepared-handoff reconciliation checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-10_LIVE_PREPARED_HANDOFF_RECONCILIATION_LEAVES_v1.json"
EXEC_LOG = REPO_ROOT / "docs/planning/2026-04-10_LIVE_PREPARED_HANDOFF_RECONCILIATION_EXECUTION_LOG_v1.md"
CONTRADICTION = REPO_ROOT / "docs/planning/2026-04-10_LIVE_PREPARED_HANDOFF_RECONCILIATION_CONTRADICTION_REPORT_v1.md"
MANIFEST = REPO_ROOT / "docs/planning/2026-04-10_LIVE_PREPARED_HANDOFF_RECONCILIATION_IMPORT_MANIFEST_v1.md"
AGENTS = REPO_ROOT / "AGENTS.md"


def test_gate255_router_quartet_closes_truthfully() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXEC_LOG.read_text(encoding="utf-8")

    assert "## Active pack\n\n- none" in plans
    assert "live prepared-handoff reconciliation pack retained through Gate 255" in plans
    assert leaves["active_gate"] == "none"
    assert leaves["completed_gate_ids"] == ["Gate 255"]
    assert leaves["remaining_leaf_ids"] == []
    assert "Closed through Gate 255" in execution_log
    assert (
        "latest closed live prepared-handoff reconciliation gate authority "
        "retained as predecessor evidence for Gate 255" in gate_map
    )


def test_gate255_records_gate254_as_predecessor_evidence() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")

    assert "2026-04-10_LIVE_PREPARED_HANDOFF_RECONCILIATION_GATES_v1.md" in plans
    assert "2026-04-10_DOCTRINE_BASELINE_REFRESH_FOR_AGENTS_AND_01_NORMATIVE_GATES_v1.md" in gate_map
    assert "| Gate 254 | imported prepared handoff evidence retained in the live repo |" in gate_map


def test_gate255_agents_deferral_is_explicit_and_future_safe() -> None:
    agents = AGENTS.read_text(encoding="utf-8")
    contradiction = CONTRADICTION.read_text(encoding="utf-8")
    manifest = MANIFEST.read_text(encoding="utf-8")
    testing_doctrine = REPO_ROOT / "docs/08_TESTING_AND_PROMOTION.md"

    assert testing_doctrine.is_file()
    assert "docs/08_TESTING_AND_PROMOTION.md" in agents
    assert "numbered `08` slot" in contradiction
    assert "AGENTS.md" in manifest
    assert "missing numbered-08 doctrine path" in manifest
