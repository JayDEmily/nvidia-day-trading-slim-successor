"""Gate F tests for deterministic replay, calibration, and stack comparison."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.services.replay_compare import ReplayComparisonService

FIXTURE_PACK = Path("fixtures/replay/gate_f_replay_regression_fixture_pack.json")
EXPECTED_REPORT = Path("fixtures/replay/gate_f_expected_report.json")
REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_LEDGER = (
    REPO_ROOT / "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md"
)


def test_stack_definition_loader_and_fixture_pack_are_explicit_runtime_artefacts() -> None:
    """Gate F should load stack definitions and the checked-in fixture pack deterministically."""

    service = ReplayComparisonService(Settings())
    fixture_pack = service.load_fixture_pack(FIXTURE_PACK)
    stack_index = service.load_stack_definitions(FIXTURE_PACK)
    assert fixture_pack.fixture_pack_id == "gate-f-replay-regression-v1"
    assert sorted(stack_index) == ["core_full_stack", "defensive_focus_stack"]
    assert stack_index["core_full_stack"].enabled_playbooks == [
        "continuation_ladder",
        "negative_gamma_flush",
        "pin_reversion",
        "compression_breakout",
    ]
    assert fixture_pack.walk_forward_slices[0].scenario_ids == ["trend", "flush"]


def test_compare_from_fixture_pack_applies_stack_filters_weights_and_coefficients() -> None:
    """Gate F replay should honour stack filtering, module weights, and sub-coefficients."""

    service = ReplayComparisonService(Settings())
    runs, report = service.compare_from_fixture_pack(FIXTURE_PACK)
    assert len(runs) == 8
    run_index = {(run.coefficient_set_id, run.scenario_id): run for run in runs}

    full_flush = run_index[("full_stack_base", "flush")]
    defensive_flush = run_index[("defensive_stack_tight", "flush")]
    defensive_trend = run_index[("defensive_stack_tight", "trend")]

    assert full_flush.active_playbook_ids == ["negative_gamma_flush"]
    assert defensive_flush.active_playbook_ids == []
    assert defensive_flush.veto_observed is True
    assert defensive_flush.veto_correct == 0.0
    assert defensive_trend.coefficient_audit.applied_module_weights["execution_expression"] == 0.7
    assert defensive_trend.coefficient_audit.applied_sub_coefficients["vix_level"] == 1.1
    assert defensive_trend.coefficient_audit.governed_coefficient_snapshot_id is not None
    assert defensive_trend.governed_coefficient_snapshot is not None
    assert defensive_trend.governed_coefficient_snapshot.snapshot_id == defensive_trend.coefficient_audit.governed_coefficient_snapshot_id
    assert defensive_trend.governed_coefficient_snapshot.resolved_surfaces
    assert defensive_trend.replay_score < run_index[("full_stack_base", "trend")].replay_score

    assert set(report.reports) == {"defensive_stack_tight", "full_stack_base"}
    assert report.reports["full_stack_base"].veto_correctness_rate == 1.0
    assert report.reports["defensive_stack_tight"].veto_correctness_rate == 0.75
    assert report.reports["defensive_stack_tight"].mean_playbook_precision == 0.75
    assert (
        report.reports["defensive_stack_tight"].mean_replay_score
        < report.reports["full_stack_base"].mean_replay_score
    )


def test_walk_forward_slice_reports_and_stack_delta_summary_are_deterministic() -> None:
    """Gate F should expose walk-forward slice reports and stable stack deltas."""

    service = ReplayComparisonService(Settings())
    _, report = service.compare_from_fixture_pack(FIXTURE_PACK)
    assert set(report.slice_reports) == {"holdout_window", "train_window"}
    assert report.slice_reports["train_window"]["full_stack_base"].run_count == 2
    assert report.slice_reports["holdout_window"]["defensive_stack_tight"].run_count == 2
    assert set(report.coefficient_snapshots_by_set) == {"defensive_stack_tight", "full_stack_base"}
    assert report.coefficient_snapshots_by_set["full_stack_base"]
    assert len(report.stack_vs_stack_summary) == 1
    summary = report.stack_vs_stack_summary[0]
    assert summary.left_set_id == "defensive_stack_tight"
    assert summary.right_set_id == "full_stack_base"
    assert summary.left_stack_id == "defensive_focus_stack"
    assert summary.right_stack_id == "core_full_stack"
    assert summary.delta_mean_replay_score < 0.0
    assert summary.delta_veto_correctness_rate < 0.0


def test_serialized_report_matches_checked_in_regression_baseline(
    tmp_path: Path,
) -> None:
    """Gate F report serialisation should be stable against the checked-in baseline."""

    service = ReplayComparisonService(Settings())
    _, report = service.compare_from_fixture_pack(FIXTURE_PACK)
    output_path = tmp_path / "gate_f_report.json"
    serialised = service.serialize_report(report, output_path)
    expected = EXPECTED_REPORT.read_text()
    assert serialised == expected
    assert output_path.read_text() == expected
    assert json.loads(serialised)["scenario_ids"] == ["trend", "flush", "event", "pin"]


def test_replay_runs_surface_packet_lineage_deterministically() -> None:
    """Replay lineage stays subordinate to successor-native preserved seam authority."""

    service = ReplayComparisonService(Settings())
    runtime_ledger = RUNTIME_LEDGER.read_text(encoding="utf-8")
    runs, _ = service.compare_from_fixture_pack(FIXTURE_PACK)
    run = next(
        run
        for run in runs
        if run.coefficient_set_id == "full_stack_base" and run.scenario_id == "trend"
    )

    assert "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md" in str(RUNTIME_LEDGER)
    assert "### 3.10 Stage-Local Handoff" in runtime_ledger
    assert "### 3.11 Review and Explanation" in runtime_ledger
    assert "`overlay_risk_decision`, `terminal_risk_application`, and `terminal_risk_decision` outrank `final_risk_join` for seam interpretation." in runtime_ledger
    assert run.packet_lineage is not None
    assert run.governed_coefficient_snapshot is not None
    assert run.coefficient_audit.governed_coefficient_snapshot_id == run.governed_coefficient_snapshot.snapshot_id
    assert run.packet_lineage.packet_lineage[0] == run.packet_lineage.stage_packet_ids["temporal"]
    assert run.packet_lineage.packet_lineage[-1] == run.packet_lineage.stage_packet_ids["review"]
    assert (
        run.packet_lineage.replay_trace_id
        == "replay-trace::core_full_stack::full_stack_base::trend"
    )
