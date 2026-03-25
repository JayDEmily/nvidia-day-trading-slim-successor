"""Planning partition checks for the remaining ready-for-contract-import backlog."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKLOG = REPO_ROOT / "docs/planning/2026-03-23_EXECUTABLE_IMPORT_BACKLOG.json"
LEAF_LEDGER = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_LEAVES_v3.json"


def test_gate_28_to_39_leaves_cover_every_ready_item_exactly_once() -> None:
    """The Gate 28-39 leaves should still cover the full ready backlog exactly once."""

    backlog = json.loads(BACKLOG.read_text())
    ready_ids = {
        item["canonical_id"]
        for item in backlog["items"]
        if item["implementation_readiness"] == "ready_for_contract_import"
    }

    leaf_ledger = json.loads(LEAF_LEDGER.read_text())
    tranche_leaves = [
        leaf
        for leaf in leaf_ledger["leaves"]
        if leaf["gate"] in {f"Gate {gate}" for gate in range(28, 40)}
    ]

    assert len(tranche_leaves) == 12

    tranche_ids: list[str] = []
    for leaf in tranche_leaves:
        planned_items = leaf["planned_items"]
        assert planned_items
        tranche_ids.extend(planned_items)

    assert len(tranche_ids) == len(set(tranche_ids))
    assert set(tranche_ids) == ready_ids


def test_remaining_ready_remainder_stays_contiguous_and_gap_free() -> None:
    """The still-planned remainder should stay contiguous, unique, and equal the unclosed ready backlog."""

    backlog = json.loads(BACKLOG.read_text())
    ready_ids = {
        item["canonical_id"]
        for item in backlog["items"]
        if item["implementation_readiness"] == "ready_for_contract_import"
    }

    leaf_ledger = json.loads(LEAF_LEDGER.read_text())
    tranche_leaves = [
        leaf
        for leaf in leaf_ledger["leaves"]
        if leaf["gate"] in {f"Gate {gate}" for gate in range(28, 40)}
    ]
    planned_leaves = [leaf for leaf in tranche_leaves if leaf["status"] == "planned"]
    complete_leaves = [leaf for leaf in tranche_leaves if leaf["status"] == "complete"]

    planned_ids = [canonical_id for leaf in planned_leaves for canonical_id in leaf["planned_items"]]
    complete_ids = [canonical_id for leaf in complete_leaves for canonical_id in leaf["planned_items"]]

    assert len(planned_ids) == len(set(planned_ids))
    assert len(complete_ids) == len(set(complete_ids))
    assert set(planned_ids).isdisjoint(set(complete_ids))
    assert set(planned_ids) | set(complete_ids) == ready_ids

    planned_gate_numbers = sorted(int(leaf["gate"].split()[1]) for leaf in planned_leaves)
    complete_gate_numbers = sorted(int(leaf["gate"].split()[1]) for leaf in complete_leaves)

    if planned_gate_numbers:
        assert planned_gate_numbers == list(range(min(planned_gate_numbers), 40))
    if complete_gate_numbers and planned_gate_numbers:
        assert max(complete_gate_numbers) + 1 == min(planned_gate_numbers)
