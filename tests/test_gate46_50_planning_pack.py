"""Planning/execution integrity checks for the post-Gate-50 merged state."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAF_LEDGER = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_LEAVES_v3.json"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
PLANS = REPO_ROOT / "PLANS.md"


def test_gate_46_to_50_are_complete_and_gate_45_stays_retired() -> None:
    """The merged repo should keep Gate 45 retired and mark Gates 46-50 complete on main."""

    gate_map = GATE_MAP.read_text()
    plans = PLANS.read_text()

    assert ("post-flight repo consistency pack active at Gate 128" in plans or "post-flight repo consistency pack active at Gate 129" in plans or "post-flight repo consistency pack active at Gate 130" in plans or "post-flight repo consistency pack active at Gate 131" in plans or "no active pack currently routed; post-flight repo consistency pack closed through Gate 131 on `main`" in plans)
    assert "signal-coefficient authority pack closed through Gate 127" in plans
    assert "Gate 45 is retired as a placeholder" in gate_map
    assert "| Gates 46–50 | `LEAF-G46-*` through `LEAF-G50-*` complete on `main` |" in gate_map


def test_gate_46_to_50_leaves_are_present_and_marked_complete() -> None:
    """The leaf ledger should contain the bounded Gate 46-50 leaves as completed."""

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
        assert all(leaf["status"] == "complete" for leaf in matching)

    remaining = set(leaf_ledger["remaining_leaf_ids"])
    assert not {
        leaf_id
        for leaf_id in remaining
        if leaf_id.startswith(("LEAF-G46-", "LEAF-G47-", "LEAF-G48-", "LEAF-G49-", "LEAF-G50-"))
    }
    assert (
        leaf_ledger["execution_status"]
        == "gates_46_to_50_complete_on_main_gate_51_complete_on_main"
    )
