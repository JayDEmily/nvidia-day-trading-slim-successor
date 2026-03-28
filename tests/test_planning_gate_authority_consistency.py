"""Planning authority consistency checks for the active gate quartet."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAF_LEDGER = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_LEAVES_v3.json"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
PLANS = REPO_ROOT / "PLANS.md"


def test_gate7_baseline_leaf_is_explicit_across_the_planning_quartet() -> None:
    """Gate 7 should be named explicitly as baseline leaf LEAF-G7-BASELINE everywhere it matters."""

    leaf_ledger = json.loads(LEAF_LEDGER.read_text())
    gate_map = GATE_MAP.read_text()
    plans = PLANS.read_text()

    baseline = leaf_ledger["global_rules"]["completed_admin_baseline"]
    assert baseline["gate"] == "Gate 7"
    assert baseline["leaf_id"] == "LEAF-G7-BASELINE"
    assert baseline["status"] == "complete_on_main"

    baseline_leaf_ids = leaf_ledger["completed_baseline_leaf_ids"]
    assert baseline_leaf_ids == ["LEAF-G7-BASELINE"]

    baseline_leaves = leaf_ledger["completed_baseline_leaves"]
    assert len(baseline_leaves) == 1
    assert baseline_leaves[0]["id"] == "LEAF-G7-BASELINE"
    assert baseline_leaves[0]["gate"] == "Gate 7"

    assert "Gate 7 | baseline leaf `LEAF-G7-BASELINE` complete on `main`" in gate_map
    assert "records Gate 7 explicitly as baseline leaf `LEAF-G7-BASELINE`" in plans


def test_completed_leaf_ids_match_leaf_entries() -> None:
    """Every completed leaf id should map to a unique completed leaf entry."""

    leaf_ledger = json.loads(LEAF_LEDGER.read_text())
    leaves = leaf_ledger["leaves"]
    completed_ids = set(leaf_ledger["completed_leaf_ids"])

    leaf_ids = [leaf["id"] for leaf in leaves]
    assert len(leaf_ids) == len(set(leaf_ids))
    assert completed_ids == {leaf["id"] for leaf in leaves if leaf["status"] == "complete"}
