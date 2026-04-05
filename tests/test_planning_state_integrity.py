"""Generic planning-state integrity checks for live and historical packs."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANNING_DIR = REPO_ROOT / "docs/planning"


def iter_real_leaves_ledgers() -> list[Path]:
    return [
        path
        for path in PLANNING_DIR.rglob("*_LEAVES_*.json")
        if "tranche_briefing_template_pack" not in path.parts
    ]


def normalise_leaves(payload: dict[str, object]) -> tuple[set[str], dict[str, str | None]]:
    leaves = payload.get("leaves", {})
    if isinstance(leaves, dict):
        leaf_statuses: dict[str, str | None] = {}
        for leaf_id, leaf in leaves.items():
            if isinstance(leaf_id, str) and isinstance(leaf, dict):
                status = leaf.get("status")
                leaf_statuses[leaf_id] = status if isinstance(status, str) else None
        return set(leaf_statuses), leaf_statuses
    if isinstance(leaves, list):
        ids: set[str] = set()
        statuses: dict[str, str | None] = {}
        for leaf in leaves:
            if not isinstance(leaf, dict):
                continue
            leaf_id = leaf.get("id")
            if not isinstance(leaf_id, str) or not leaf_id:
                continue
            status = leaf.get("status")
            ids.add(leaf_id)
            statuses[leaf_id] = status if isinstance(status, str) else None
        return ids, statuses
    return set(), {}


def test_leaves_ledgers_enforce_state_integrity_invariants() -> None:
    ledgers = iter_real_leaves_ledgers()
    assert ledgers

    for ledger_path in ledgers:
        payload = json.loads(ledger_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or "completed_leaf_ids" not in payload or "remaining_leaf_ids" not in payload:
            continue

        completed = set(payload.get("completed_leaf_ids", []))
        remaining = set(payload.get("remaining_leaf_ids", []))
        leaf_ids, statuses = normalise_leaves(payload)

        assert completed.isdisjoint(remaining), ledger_path
        assert (completed | remaining) <= leaf_ids, ledger_path

        if payload.get("active_gate") == "none":
            assert payload.get("remaining_leaf_ids") == [], ledger_path
            assert payload.get("pending_gate_ids", []) in ([], None), ledger_path
            assert all(status == "complete" for status in statuses.values()), ledger_path
