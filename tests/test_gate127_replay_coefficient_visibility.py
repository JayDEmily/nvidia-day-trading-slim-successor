"""Gate 127 replay coefficient visibility checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.services.replay_compare import ReplayComparisonService

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PACK = REPO_ROOT / "fixtures/replay/gate_f_replay_regression_fixture_pack.json"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
ACTIVE_LEAVES = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_LEAVES_v1.json"
ACTIVE_EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_EXECUTION_LOG_v1.md"
RUNTIME_LEDGER = REPO_ROOT / "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md"
GATES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_EXECUTION_LOG_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-03-31_GATE127_REPLAY_COEFFICIENT_VISIBILITY_AND_PACK_CLOSEOUT.md"


def test_gate127_replay_report_surfaces_governed_coefficient_snapshots() -> None:
    runs, report = ReplayComparisonService(Settings()).compare_from_fixture_pack(FIXTURE_PACK)

    trend_run = next(
        run
        for run in runs
        if run.coefficient_set_id == "full_stack_base" and run.scenario_id == "trend"
    )
    assert trend_run.governed_coefficient_snapshot is not None
    assert trend_run.coefficient_audit.governed_coefficient_snapshot_id == trend_run.governed_coefficient_snapshot.snapshot_id
    assert trend_run.governed_coefficient_snapshot.snapshot_id.startswith("coefficient-snapshot::2026-03-31.tranche1::")
    assert report.coefficient_snapshots_by_set["full_stack_base"]
    assert any(
        snapshot.snapshot_id == trend_run.governed_coefficient_snapshot.snapshot_id
        for snapshot in report.coefficient_snapshots_by_set["full_stack_base"]
    )


def test_gate127_closeout_closes_the_pack_honestly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    active_leaves = json.loads(ACTIVE_LEAVES.read_text(encoding="utf-8"))
    active_execution_log = ACTIVE_EXECUTION_LOG.read_text(encoding="utf-8")
    runtime_ledger = RUNTIME_LEDGER.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "successor retained-test cleanup execution pack" in plans
    assert (
        "Gate 223 active on `work/gate-223-successor-boundary-and-light-retarget-20260406`"
        in plans
    ) or (
        "Gate 223 is complete on `work/gate-223-successor-boundary-and-light-retarget-20260406`"
        in plans
    )
    assert (
        "Current active gate: **Gate 223 active on `work/gate-223-successor-boundary-and-light-retarget-20260406` under the successor retained-test cleanup execution pack.**"
        in gate_map
    ) or (
        "Current active gate: **No active gate under the successor retained-test cleanup execution pack. Gate 223 is complete on `work/gate-223-successor-boundary-and-light-retarget-20260406`; Gate 224 is not yet activated.**"
        in gate_map
    )
    assert "Status: closed signal-coefficient authority pack on `main`; Gates 122-127 complete, no active gate" in gates
    assert leaves["execution_status"] == "signal_coefficient_authority_pack_closed_through_gate_127_on_main"
    assert leaves["active_gate"] in {
        "none — signal-coefficient authority pack closed through Gate 127 on main",
        "Gate 128",
        "Gate 129",
        "Gate 130",
        "Gate 131",
        "none — post-flight repo consistency pack closed through Gate 131 on main",
        "Gate 149",
        "none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on main",
    }
    assert leaves["remaining_leaf_ids"] == []
    assert "Status: closed execution log for the signal-coefficient authority pack; Gates 122-127 complete on `main`, no active gate" in execution_log
    assert "Status: complete on `main`; signal-coefficient authority pack is now closed through Gate 127" in receipt
    assert active_leaves["governing_plan"] == "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_GATES_v1.md"
    assert active_leaves["active_gate"] in {
        "Gate 223",
        "none — Gate 223 complete on work/gate-223-successor-boundary-and-light-retarget-20260406; Gate 224 not yet activated",
    }
    assert "duplicate replay-shadow retirement moves to Gate 223" in active_execution_log
    assert "### 3.10 Stage-Local Handoff" in runtime_ledger
    assert "### 3.11 Review and Explanation" in runtime_ledger
