"""Gate 85 horizon economic-behaviour checks."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.calibration import (
    ComparisonMetrics,
    ComparisonReport,
    StabilityComparisonRule,
    WalkForwardHarnessAuthorityPacket,
    WalkForwardStartOffset,
    WalkForwardWindowMode,
    WalkForwardWindowRole,
)
from nvda_desk.services.replay_compare import ReplayComparisonService

FIXTURE_PACK = Path("fixtures/replay/gate_f_replay_regression_fixture_pack.json")


def test_gate85_report_level_fragility_and_ablation_expose_failed_economic_axes() -> (
    None
):
    service = ReplayComparisonService(Settings())
    fixture_pack = service.load_fixture_pack(FIXTURE_PACK)
    authority = WalkForwardHarnessAuthorityPacket(
        harness_id="gate85-economic-failures",
        window_mode=WalkForwardWindowMode.ANCHORED,
        calibration_window=1,
        validation_window=1,
        candidate_forward_blocks=[1],
        step_size=1,
        start_offsets=[WalkForwardStartOffset(offset_id="offset_0", offset_sessions=0)],
        surface_keys=["surface_economic_fail"],
        stability_rule=StabilityComparisonRule(
            max_replay_score_spread=0.3,
            max_veto_correctness_spread=0.3,
            max_playbook_precision_spread=0.3,
            max_fresh_deployable_spread=5.0,
            max_active_playbook_rate_spread=0.35,
            max_conflict_count_spread=1.5,
            min_review_completeness_rate=0.8,
            minimum_forward_windows=2,
        ),
    )
    windows = service.build_walk_forward_windows(fixture_pack.scenarios, authority)
    report = ComparisonReport(
        fixture_pack_id="synthetic-g85",
        scenario_ids=[scenario.scenario_id for scenario in fixture_pack.scenarios],
        reports={},
        slice_reports={},
    )
    for window in windows:
        if window.role is not WalkForwardWindowRole.FORWARD:
            continue
        report.slice_reports[window.window_id] = {
            "alpha": ComparisonMetrics(
                run_count=1,
                veto_rate=0.0,
                veto_correctness_rate=1.0,
                mean_fresh_deployable_pct=80.0,
                mean_replay_score=1.0,
                mean_contradiction_rate=0.0,
                mean_playbook_precision=1.0,
                review_completeness_rate=0.95,
                active_playbook_rate=1.0,
                mean_active_playbook_count=1.0,
                mean_conflict_count=0.0,
            ),
            "beta": ComparisonMetrics(
                run_count=1,
                veto_rate=0.0,
                veto_correctness_rate=1.0,
                mean_fresh_deployable_pct=60.0,
                mean_replay_score=0.95,
                mean_contradiction_rate=0.0,
                mean_playbook_precision=0.95,
                review_completeness_rate=0.70,
                active_playbook_rate=0.40,
                mean_active_playbook_count=1.0,
                mean_conflict_count=2.0,
            ),
        }
    report.reports = next(iter(report.slice_reports.values()))

    harness_report = service.evaluate_horizon_discovery(
        report=report,
        authority=authority,
        generated_windows=windows,
        scenarios=fixture_pack.scenarios,
    )

    assert harness_report.group_results[0].economic_behaviour_consistent is False
    assert any(
        note.startswith("economic_axis_failures:")
        for note in harness_report.group_results[0].notes
    )
    assert harness_report.fragility.economic_axis_failures["surface_economic_fail"] == [
        "active_playbook_rate_spread",
        "conflict_count_spread",
        "fresh_deployable_spread",
        "review_completeness_floor",
    ]
    assert (
        harness_report.ablation.economic_axis_failures
        == harness_report.fragility.economic_axis_failures
    )
