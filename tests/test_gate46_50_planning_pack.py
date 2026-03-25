"""Planning-pack integrity checks for the Gate 46-50 tranche."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAF_LEDGER = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_LEAVES_v3.json"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
PLANS = REPO_ROOT / "PLANS.md"


def test_gate_46_is_active_and_gate_45_is_retired_in_the_planning_pack() -> None:
    """The planning pack should retire Gate 45 and install Gate 46 as the active gate."""

    gate_map = GATE_MAP.read_text()
    plans = PLANS.read_text()

    assert "Gate 45 — retired placeholder on the current planning branch" in plans
    assert "Gate 46 — active planning gate on the current planning branch" in plans
    assert "Gate 45 is retired as a placeholder" in gate_map
    assert "Current active gate on the current planning branch: **Gate 46**." in gate_map


def test_gate_46_to_50_leaves_are_present_and_marked_planned() -> None:
    """The leaf ledger should contain the bounded Gate 46-50 planning leaves."""

    leaf_ledger = json.loads(LEAF_LEDGER.read_text())
    leaves = {leaf["id"]: leaf for leaf in leaf_ledger["leaves"]}

    expected_prefixes = {
        "LEAF-G46-": 3,
        "LEAF-G47-": 5,
        "LEAF-G48-": 5,
        "LEAF-G49-": 4,
        "LEAF-G50-": 5,
    }

    for prefix, count in expected_prefixes.items():
        matching = [leaf for leaf_id, leaf in leaves.items() if leaf_id.startswith(prefix)]
        assert len(matching) == count
        assert all(leaf["status"] == "planned" for leaf in matching)

    remaining = set(leaf_ledger["remaining_leaf_ids"])
    expected_remaining = {
        leaf_id
        for leaf_id in leaves
        if leaf_id.startswith(("LEAF-G46-", "LEAF-G47-", "LEAF-G48-", "LEAF-G49-", "LEAF-G50-"))
    }
    assert remaining == expected_remaining
    assert leaf_ledger["execution_status"] == "gate_46_planning_pack_authored_gate_47_to_50_leafed_on_branch"
