"""Gate 157 parallel risk lane foundation bootstrap checks."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import cast

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_LEAVES_v1.json"
EXECUTION_LOG = (
    REPO_ROOT / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_EXECUTION_LOG_v1.md"
)
CHECKLIST = (
    REPO_ROOT
    / "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md"
)
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE157_PARALLEL_RISK_LANE_FOUNDATION_BOOTSTRAP.md"
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
VOCAB = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"
WORKBOOK = (
    REPO_ROOT
    / "data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx"
)
OLD_WORKBOOK = REPO_ROOT / "docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx"


def test_gate157_pack_is_active_and_progressed_lawfully() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_GATES_v1.md" in plans
    assert "2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_LEAVES_v1.json" in plans
    assert "2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_EXECUTION_LOG_v1.md" in plans
    assert "2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md" in plans
    assert (
        any(
            f"active gate: Gate {gate} on `work/gate-157-parallel-risk-lane-planning-pack-20260402`"
            in plans
            for gate in (158, 159, 160, 161, 162, 163, 164)
        )
        or "closed through Gate 164 on `work/gate-157-parallel-risk-lane-planning-pack-20260402`"
        in plans
    )
    assert (
        any(
            f"Current active gate: **Gate {gate} in the parallel risk lane foundation pack**."
            in gate_map
            for gate in (158, 159, 160, 161, 162, 163, 164)
        )
        or "Current active gate: **none — parallel risk lane foundation pack closed through Gate 164"
        in gate_map
    )
    assert leaves["execution_status"] in {
        "gate_157_complete_gate_158_active_on_work_branch",
        "gate_158_complete_gate_159_active_on_work_branch",
        "gate_159_complete_gate_160_active_on_work_branch",
        "gate_160_complete_gate_161_active_on_work_branch",
        "gate_161_complete_gate_162_active_on_work_branch",
        "gate_162_complete_gate_163_active_on_work_branch",
        "gate_163_complete_gate_164_active_on_work_branch",
        "parallel_risk_lane_foundation_pack_closed_through_gate_164_on_work_branch",
    }
    assert leaves["active_gate"] in {
        "Gate 158",
        "Gate 159",
        "Gate 160",
        "Gate 161",
        "Gate 162",
        "Gate 163",
        "Gate 164",
        "none",
    }
    assert execution_log.startswith("# 2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_EXECUTION_LOG_v1")
    assert (
        any(f"Gate {gate} active" in checklist for gate in (158, 159, 160, 161, 162, 163, 164))
        or "closed through Gate 164" in checklist
    )
    assert "Status: closed parallel risk lane foundation pack through Gate 164" in gates or any(
        f"Gates 157-{end} complete" in gates for end in (158, 159, 160, 161, 162, 163, 164)
    )


def test_gate157_admits_minimum_lane_workbook_discoverability() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert WORKBOOK.exists()
    assert OLD_WORKBOOK.exists()
    assert "governed live reference ledger" in normative
    assert str(WORKBOOK.relative_to(REPO_ROOT)) in normative

    index = {entry["canonical_slug"]: entry for entry in vocab["entries"]}
    lane = index["independent_parallel_risk_lane"]
    workbook = index["signal_coefficient_reference_workbook"]
    assert lane["category"] == "workflow"
    assert "parallel risk pipeline" in lane["allowed_aliases"]
    assert "step_1_1" in lane["disallowed_phrases"]
    assert workbook["category"] == "data_classification"
    assert workbook["maps_to_contract"] == str(WORKBOOK.relative_to(REPO_ROOT))
    assert "not direct runtime authority" in receipt


def test_gate157_future_gate_topology_includes_consolidation_and_final_audit() -> None:
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert leaves["pending_gate_ids"] in (
        [
            "Gate 158",
            "Gate 159",
            "Gate 160",
            "Gate 161",
            "Gate 162",
            "Gate 163",
            "Gate 164",
        ],
        [
            "Gate 159",
            "Gate 160",
            "Gate 161",
            "Gate 162",
            "Gate 163",
            "Gate 164",
        ],
        [
            "Gate 160",
            "Gate 161",
            "Gate 162",
            "Gate 163",
            "Gate 164",
        ],
        [
            "Gate 161",
            "Gate 162",
            "Gate 163",
            "Gate 164",
        ],
        ["Gate 164"],
        [],
    )
    assert "Gate 159 — Workbook lineage and consolidation audit" in gates
    assert "Gate 164 — Parallel risk lane foundation anti-drift closeout" in gates
    assert "workbook lineage and consolidation audit" in gate_map
    assert "workbook-lineage closure" in gate_map and "semantic coverage" in gate_map


def test_gate157_future_leaves_are_materially_granular_not_templated() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))["leaves"]

    expected_counts = {
        "Gate 158": 4,
        "Gate 159": 4,
        "Gate 160": 4,
        "Gate 161": 4,
        "Gate 162": 5,
        "Gate 163": 5,
        "Gate 164": 4,
    }
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for leaf in leaves.values():
        grouped[leaf["gate"]].append(leaf)

    assert Counter({gate: len(items) for gate, items in grouped.items()}) >= Counter(
        expected_counts
    )

    for gate, expected in expected_counts.items():
        gate_leaves = grouped[gate]
        assert len(gate_leaves) == expected
        action_sets: set[tuple[object, ...]] = {
            tuple(cast(list[object], leaf["ordered_actions"])) for leaf in gate_leaves
        }
        assert len(action_sets) == expected
        title_set = {leaf["title"] for leaf in gate_leaves}
        assert len(title_set) == expected
        for leaf in gate_leaves:
            assert len(cast(list[object], leaf["ordered_actions"])) >= 4
            assert len(cast(list[object], leaf["forbidden_actions"])) >= 3
            assert leaf["validation_commands"]
            assert leaf["expected_evidence"]
            assert len(cast(list[object], leaf["definition_of_done"])) >= 2
            assert leaf["packaging_requirement"]


def test_gate157_pack_preserves_semantic_gold_explicitly() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves_text = LEAVES.read_text(encoding="utf-8")
    combined = gates_text + "\n" + leaves_text

    required_phrases = [
        "multi-clock",
        "dislocation",
        "impairment",
        "candidate-specific risk audit",
        "environmental risk weather",
        "expression-posture",
        "carry truth",
        "active enough to matter now",
        "distributed caution fog",
        "workbook_ref",
    ]
    for phrase in required_phrases:
        assert phrase in combined


def test_gate157_pack_forces_workbook_lineage_work_before_later_authority_mapping() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    leaf_order = leaves["leaf_order"]

    pos = {leaf_id: i for i, leaf_id in enumerate(leaf_order)}
    assert pos["LEAF-G159-004"] < pos["LEAF-G160-001"] < pos["LEAF-G161-001"]

    gate159_text = json.dumps(
        {k: v for k, v in leaves["leaves"].items() if v["gate"] == "Gate 159"},
        indent=2,
    )
    assert str(OLD_WORKBOOK.relative_to(REPO_ROOT)) in gate159_text
    assert str(WORKBOOK.relative_to(REPO_ROOT)) in gate159_text
    assert "canonical survivor" in gate159_text
    assert "stale reference" in gate159_text or "stale refs" in gate159_text


def test_gate157_gate_specific_validation_targets_are_predeclared() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))["leaves"]
    expected = {
        "Gate 158": "tests/test_gate158_co_resident_parallel_risk_lane_law.py",
        "Gate 159": "tests/test_gate159_workbook_lineage_and_consolidation_audit.py",
        "Gate 160": "tests/test_gate160_governed_signal_coefficient_reference_workbook_law.py",
        "Gate 161": "tests/test_gate161_temporal_calendar_event_and_multi_clock_authority_mapping.py",
        "Gate 162": "tests/test_gate162_market_options_dependency_and_dislocation_mapping.py",
        "Gate 163": "tests/test_gate163_ownership_output_coefficient_and_anti_duplication_law.py",
        "Gate 164": "tests/test_gate164_parallel_risk_lane_foundation_anti_drift_closeout.py",
    }
    for gate, test_path in expected.items():
        gate_leaves = [leaf for leaf in leaves.values() if leaf["gate"] == gate]
        assert gate_leaves
        for leaf in gate_leaves:
            assert any(test_path in cmd for cmd in leaf["validation_commands"])
