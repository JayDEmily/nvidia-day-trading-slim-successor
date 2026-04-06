"""Gate 159 workbook lineage and consolidation audit checks."""

from __future__ import annotations

import json
from pathlib import Path

from ._planning_later_state_helpers import (
    CLEANUP_GATE_MAP_MARKERS,
    CLEANUP_PLAN_MARKERS,
    contains_any,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_LEAVES_v1.json"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE159_WORKBOOK_LINEAGE_AND_CONSOLIDATION_AUDIT.md"
VOCAB = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"
OLD_WORKBOOK = REPO_ROOT / "docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx"
NEW_WORKBOOK = (
    REPO_ROOT
    / "data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx"
)
BUILD_VOCAB = REPO_ROOT / "scripts/build_canonical_vocabulary.py"
AUTH_GATES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_GATES_v1.md"
AUTH_LEAVES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_LEAVES_v1.json"


def test_gate159_is_complete_and_pack_has_moved_to_gate160_or_161() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        contains_any(plans, CLEANUP_PLAN_MARKERS)
        or
        any(
            f"active gate: Gate {gate} on `work/gate-157-parallel-risk-lane-planning-pack-20260402`"
            in plans
            for gate in (160, 161, 162, 163, 164)
        )
        or "closed through Gate 164 on `work/gate-157-parallel-risk-lane-planning-pack-20260402`"
        in plans
    )
    assert (
        contains_any(gate_map, CLEANUP_GATE_MAP_MARKERS)
        or
        any(
            f"Current active gate: **Gate {gate} in the parallel risk lane foundation pack**."
            in gate_map
            for gate in (160, 161, 162, 163, 164)
        )
        or "Current active gate: **none — parallel risk lane foundation pack closed through Gate 164"
        in gate_map
    )
    assert "Status: closed parallel risk lane foundation pack through Gate 164" in gates or any(
        label in gates
        for label in (
            "Gates 157-159 complete",
            "Gates 157-160 complete",
            "Gates 157-161 complete",
            "Gates 157-162 complete",
            "Gates 157-163 complete",
            "Gates 157-164 complete",
        )
    )
    assert leaves["completed_gate_ids"][:3] == ["Gate 157", "Gate 158", "Gate 159"]


def test_gate159_freezes_canonical_survivor_and_rewritten_active_refs() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))
    build = BUILD_VOCAB.read_text(encoding="utf-8")
    auth_gates = AUTH_GATES.read_text(encoding="utf-8")
    auth_leaves = AUTH_LEAVES.read_text(encoding="utf-8")

    assert OLD_WORKBOOK.exists()
    assert NEW_WORKBOOK.exists()
    assert (
        f"canonical governed workbook authority path: `{NEW_WORKBOOK.relative_to(REPO_ROOT)}`"
        in receipt
    )
    assert (
        f"retained at `{OLD_WORKBOOK.relative_to(REPO_ROOT)}`" in receipt
        and "historical archive evidence only" in receipt
    )
    assert "no old-only sheets" in receipt
    assert "clean successor with expanded scope" in receipt
    assert "Repo_Python_Inventory" in receipt and "Signal_Coeff_Handoff" in receipt

    index = {entry["canonical_slug"]: entry for entry in vocab["entries"]}
    assert index["raw_primitive"]["maps_to_contract"] == str(NEW_WORKBOOK.relative_to(REPO_ROOT))
    assert index["derived_feature"]["maps_to_contract"] == str(NEW_WORKBOOK.relative_to(REPO_ROOT))
    assert f'maps_to_contract="{NEW_WORKBOOK.relative_to(REPO_ROOT)}"' in build
    assert str(NEW_WORKBOOK.relative_to(REPO_ROOT)) in auth_gates
    assert str(NEW_WORKBOOK.relative_to(REPO_ROOT)) in auth_leaves


def test_gate159_leaves_are_complete_and_keep_old_path_only_as_archive() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    gate159 = {k: v for k, v in leaves["leaves"].items() if v["gate"] == "Gate 159"}
    assert len(gate159) == 4
    for leaf in gate159.values():
        assert leaf["status"] == "complete"
        assert any(
            "tests/test_gate159_workbook_lineage_and_consolidation_audit.py" in cmd
            for cmd in leaf["validation_commands"]
        )
    combined = json.dumps(gate159, indent=2)
    assert "canonical survivor" in combined
    assert "stale reference" in combined or "stale refs" in combined
    assert str(OLD_WORKBOOK.relative_to(REPO_ROOT)) in combined
    assert str(NEW_WORKBOOK.relative_to(REPO_ROOT)) in combined
