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
    assert "live prepared-handoff reconciliation pack is closed through Gate 255" in plans
    assert leaves["active_gate"] == "none"
    assert leaves["completed_gate_ids"] == ["Gate 255"]
    assert leaves["remaining_leaf_ids"] == []
    assert "Closed through Gate 255" in execution_log
    assert "Current active gate: **No active pack currently routed. The live prepared-handoff reconciliation pack is closed through Gate 255" in gate_map


def test_gate255_records_gate254_as_predecessor_evidence() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")

    assert "2026-04-10_WORKFLOW_LAW_AND_TEMPLATE_PACK_REFRESH_GATES_v1.md" in plans
    assert "2026-04-10_DOCTRINE_BASELINE_REFRESH_FOR_AGENTS_AND_01_NORMATIVE_GATES_v1.md" in gate_map
    assert "| Gate 254 | imported prepared handoff evidence retained in the live repo |" in gate_map


def test_gate255_agents_deferral_is_explicit_and_future_safe() -> None:
    agents = AGENTS.read_text(encoding="utf-8")
    contradiction = CONTRADICTION.read_text(encoding="utf-8")
    manifest = MANIFEST.read_text(encoding="utf-8")
    docs_08 = REPO_ROOT / "docs/08_GITHUB_OR_CHATGPT_GITHUB_INTERACTIONS.md"

    if "docs/08_GITHUB_OR_CHATGPT_GITHUB_INTERACTIONS.md" in agents:
        assert docs_08.is_file()
    else:
        assert not docs_08.exists()
        assert "keep the live repo `AGENTS.md` unchanged" in contradiction
        assert "AGENTS.md" in manifest
        assert "depends on missing `docs/08_GITHUB_OR_CHATGPT_GITHUB_INTERACTIONS.md`" in manifest
