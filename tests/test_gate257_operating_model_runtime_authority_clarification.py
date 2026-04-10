"""Gate 257 operating-model runtime-authority clarification checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OPERATING_MODEL = REPO_ROOT / "docs/02_OPERATING_MODEL.md"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-10_OPERATING_MODEL_RUNTIME_AUTHORITY_CLARIFICATION_LEAVES_v1.json"
EXEC_LOG = REPO_ROOT / "docs/planning/2026-04-10_OPERATING_MODEL_RUNTIME_AUTHORITY_CLARIFICATION_EXECUTION_LOG_v1.md"


def test_gate257_router_quartet_closes_truthfully() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXEC_LOG.read_text(encoding="utf-8")

    assert "## Active pack\n\n- none" in plans
    assert "operating-model runtime-authority clarification pack is closed through Gate 257" in plans
    assert leaves["active_gate"] == "none"
    assert leaves["completed_gate_ids"] == ["Gate 257"]
    assert leaves["remaining_leaf_ids"] == []
    assert "Closed through Gate 257" in execution_log
    assert (
        "Current active gate: **No active pack currently routed. "
        "The operating-model runtime-authority clarification pack is closed through Gate 257"
        in gate_map
    )


def test_gate257_operating_model_contains_the_bounded_authority_clarification() -> None:
    text = OPERATING_MODEL.read_text(encoding="utf-8")

    assert "Independent Parallel Risk Lane is co-resident and descriptive." in text
    assert "It is not an eighth serial stage." in text
    assert "It is not an independent final arbiter over the seven-step grammar." in text
    assert (
        "`final_risk_join` remains a compatibility surface and does not silently "
        "outrank preserved downstream seam surfaces." in text
    )
    assert (
        "After Expression and Execution forms the candidate, Capital Deployment "
        "Authority Service is the only downstream fresh-capital authority." in text
    )
    assert "Stage-Local Handoff" in text
    assert "Overlay Risk Decision" in text
    assert "Terminal Risk Application" in text
    assert "Terminal Risk Decision" in text
    assert "Capital Deployment Authority Decision remains the sole downstream fresh-capital decision output" in text
