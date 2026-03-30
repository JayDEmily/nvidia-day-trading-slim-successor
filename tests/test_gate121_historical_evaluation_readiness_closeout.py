"""Gate 121 historical-evaluation readiness closeout checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-30_HISTORICAL_EVALUATION_READINESS_EXECUTION_LOG_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-03-31_GATE121_FINAL_RISK_GATEWAY_JOIN.md"


ACTIVE_PACK_NONE_MARKER = "## Active pack\n\n- none"


def test_historical_evaluation_readiness_pack_is_closed_honestly_across_the_quartet() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert ACTIVE_PACK_NONE_MARKER in plans
    assert "historical-evaluation readiness pack closed through Gate 121 on `main`" in plans
    assert (
        "Current active gate: **none — historical-evaluation readiness pack closed through Gate 121 on `main`**."
        in gate_map
    )
    assert "| Gate 121 | complete on `main` |" in gate_map
    assert (
        "Status: closed historical-evaluation readiness pack on `main`; Gates 115-121 complete, no active gate"
        in gates
    )
    assert (
        leaves["execution_status"]
        == "historical_evaluation_readiness_pack_closed_through_gate_121_on_main"
    )
    assert (
        leaves["active_gate"]
        == "none — historical-evaluation readiness pack closed through Gate 121 on main"
    )
    assert leaves["completed_gate_ids"] == [
        115,
        116,
        "Gate 117",
        "Gate 118",
        "Gate 119",
        "Gate 120",
        "Gate 121",
    ]
    assert leaves["remaining_leaf_ids"] == []
    assert (
        "Status: closed execution log for the historical-evaluation readiness pack; Gates 115-121 complete on `main`, no active gate"
        in execution_log
    )


def test_gate121_receipt_freezes_packaging_intent() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    assert (
        "Status: complete on `main`; historical-evaluation readiness pack closed through Gate 121"
        in receipt
    )
    assert (
        "final risk is now part of the runtime authority chain instead of a detached downstream service"
        in receipt
    )
    assert (
        "historical-evaluation readiness pack is closed honestly through Gate 121 on `main`"
        in receipt
    )
    assert "nvda_repo_historical_evaluation_readiness_pack_closed_gate121_main_2026-03-31.zip" in receipt
