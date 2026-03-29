"""Gate 100 bounded scenario-matrix checks."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.services.replay_compare import ReplayComparisonService

FIXTURE_PACK = Path("fixtures/replay/gate_f_replay_regression_fixture_pack.json")


def test_bounded_scenario_matrix_stays_small_and_materially_distinct() -> None:
    service = ReplayComparisonService(Settings())
    runs, report = service.compare_from_fixture_pack(FIXTURE_PACK)

    assert report.scenario_ids == ["trend", "flush", "event", "pin"]
    assert len(report.scenario_ids) == 4

    full_stack = {
        run.scenario_id: run
        for run in runs
        if run.coefficient_set_id == "full_stack_base"
    }
    assert set(full_stack) == {"trend", "flush", "event", "pin"}

    assert full_stack["trend"].permission_state == "allow"
    assert full_stack["trend"].active_playbook_ids == ["continuation_ladder"]
    assert full_stack["flush"].active_playbook_ids == ["negative_gamma_flush"]
    assert full_stack["event"].permission_state == "derisk"
    assert full_stack["event"].active_playbook_ids == []
    assert full_stack["pin"].active_playbook_ids == ["pin_reversion"]

    signature_set = {
        (run.permission_state, tuple(run.active_playbook_ids), run.veto_observed)
        for run in full_stack.values()
    }
    assert len(signature_set) == 4


def test_bounded_scenario_matrix_retains_replay_lineage_and_slice_coverage() -> None:
    service = ReplayComparisonService(Settings())
    runs, report = service.compare_from_fixture_pack(FIXTURE_PACK)

    assert set(report.slice_reports) == {"holdout_window", "train_window"}
    assert report.slice_reports["train_window"]["full_stack_base"].run_count == 2
    assert report.slice_reports["holdout_window"]["full_stack_base"].run_count == 2

    trend_run = next(
        run
        for run in runs
        if run.coefficient_set_id == "full_stack_base" and run.scenario_id == "trend"
    )
    assert trend_run.packet_lineage is not None
    assert trend_run.packet_lineage.packet_lineage[0] == trend_run.packet_lineage.stage_packet_ids["temporal"]
    assert trend_run.packet_lineage.packet_lineage[-1] == trend_run.packet_lineage.stage_packet_ids["review"]
