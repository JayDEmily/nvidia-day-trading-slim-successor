"""Gate 142 overwrite and ownership inventory checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RECEIPT = REPO_ROOT / "docs/planning/2026-04-01_GATE142_OVERWRITE_AND_OWNERSHIP_INVENTORY.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_LEAVES_v1.json"


def test_gate142_inventory_receipt_freezes_chain_and_matrix() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "## Observed overwrite chain on clean Gate 141 / Gate 140 baseline" in receipt
    assert "cognition_runtime.py" in receipt
    assert "review_explanation.py" in receipt
    assert "## Retain / retire / amend / add matrix" in receipt
    assert "StageLocalHandoffSurface" in receipt
    assert leaves["active_gate"] in {"Gate 143", "Gate 144", "Gate 145", "Gate 146"}
    assert "Gate 142" in leaves["completed_gate_ids"]
    assert {"LEAF-G142-001", "LEAF-G142-002", "LEAF-G142-003"}.issubset(set(leaves["completed_leaf_ids"]))
