"""Gate 79 harness tests for walk-forward review-horizon discovery."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.calibration import (
    ComparisonMetrics,
    ComparisonReport,
    HorizonDiscoveryOutcome,
    OffsetComparisonOutcome,
    StabilityComparisonRule,
    WalkForwardHarnessAuthorityPacket,
    WalkForwardStartOffset,
    WalkForwardWindowMode,
    WalkForwardWindowRole,
)
from nvda_desk.services.replay_compare import ReplayComparisonService

FIXTURE_PACK = Path("fixtures/replay/gate_f_replay_regression_fixture_pack.json")


def test_walk_forward_window_generation_is_chronological_and_no_leakage() -> None:
    service = ReplayComparisonService(Settings())
    fixture_pack = service.load_fixture_pack(FIXTURE_PACK)
    authority = WalkForwardHarnessAuthorityPacket(
        harness_id="gate79-window-contract",
        window_mode=WalkForwardWindowMode.ANCHORED,
        calibration_window=1,
        validation_window=1,
        candidate_forward_blocks=[1, 2],
        step_size=1,
        start_offsets=[
            WalkForwardStartOffset(offset_id="offset_0", offset_sessions=0),
            WalkForwardStartOffset(offset_id="offset_1", offset_sessions=1),
        ],
        surface_keys=["gamma_pressure", "event_policy"],
    )

    windows = service.build_walk_forward_windows(fixture_pack.scenarios, authority)
    assert windows
    assert {window.surface_key for window in windows} == {"gamma_pressure", "event_policy"}
    for window in windows:
        assert window.start_index < window.end_index
        if window.role is WalkForwardWindowRole.FORWARD:
            assert len(window.scenario_ids) == window.block_sessions
    forward_windows = [window for window in windows if window.role is WalkForwardWindowRole.FORWARD]
    assert any(window.block_sessions == 1 for window in forward_windows)
    assert any(window.block_sessions == 2 for window in forward_windows)


def test_harness_from_fixture_pack_returns_bounded_report_and_bindings() -> None:
    service = ReplayComparisonService(Settings())
    authority = WalkForwardHarnessAuthorityPacket(
        harness_id="gate79-fixture-run",
        window_mode=WalkForwardWindowMode.ANCHORED,
        calibration_window=1,
        validation_window=1,
        candidate_forward_blocks=[1],
        step_size=1,
        start_offsets=[WalkForwardStartOffset(offset_id="offset_0", offset_sessions=0)],
        surface_keys=["default_review_surface"],
    )

    response = service.discover_review_horizons_from_fixture_pack(FIXTURE_PACK, authority)

    assert response.fixture_pack_id == "gate-f-replay-regression-v1"
    assert response.report.group_results[0].surface_key == "default_review_surface"
    assert response.report.downstream_binding.review_consumer_mode.value == "review_context_only"
    assert response.report.fragility.hidden_fragility_detected in {True, False}
    assert response.report.event_slice_reports
    assert response.report.regime_slice_reports
    assert response.report.session_slice_reports


def test_offset_sensitive_and_coverage_insufficient_outcomes_are_explicit() -> None:
    service = ReplayComparisonService(Settings())
    fixture_pack = service.load_fixture_pack(FIXTURE_PACK)
    authority = WalkForwardHarnessAuthorityPacket(
        harness_id="gate79-synthetic-eval",
        window_mode=WalkForwardWindowMode.ANCHORED,
        calibration_window=1,
        validation_window=1,
        candidate_forward_blocks=[1, 2],
        step_size=1,
        start_offsets=[
            WalkForwardStartOffset(offset_id="offset_0", offset_sessions=0),
            WalkForwardStartOffset(offset_id="offset_1", offset_sessions=1),
        ],
        surface_keys=["surface_offset_sensitive", "surface_too_short"],
        stability_rule=StabilityComparisonRule(
            max_replay_score_spread=0.3,
            max_veto_correctness_spread=0.3,
            max_playbook_precision_spread=0.3,
            max_fresh_deployable_spread=5.0,
            min_review_completeness_rate=0.8,
            minimum_forward_windows=2,
        ),
    )
    windows = service.build_walk_forward_windows(fixture_pack.scenarios, authority)
    scenario_ids = [scenario.scenario_id for scenario in fixture_pack.scenarios]
    report = ComparisonReport(
        fixture_pack_id="synthetic-g79",
        scenario_ids=scenario_ids,
        reports={
            "alpha": ComparisonMetrics(
                run_count=4,
                veto_rate=0.0,
                veto_correctness_rate=1.0,
                mean_fresh_deployable_pct=80.0,
                mean_replay_score=1.0,
                mean_contradiction_rate=0.0,
                mean_playbook_precision=1.0,
                review_completeness_rate=1.0,
                active_playbook_rate=1.0,
                mean_active_playbook_count=1.0,
                mean_conflict_count=0.0,
            ),
            "beta": ComparisonMetrics(
                run_count=4,
                veto_rate=0.0,
                veto_correctness_rate=1.0,
                mean_fresh_deployable_pct=81.0,
                mean_replay_score=0.9,
                mean_contradiction_rate=0.0,
                mean_playbook_precision=1.0,
                review_completeness_rate=1.0,
                active_playbook_rate=1.0,
                mean_active_playbook_count=1.0,
                mean_conflict_count=0.0,
            ),
        },
        slice_reports={},
    )
    # Force ranking flip across offsets for the first surface and coverage insufficiency for the second.
    for window in windows:
        if window.role is not WalkForwardWindowRole.FORWARD:
            continue
        if window.surface_key == "surface_offset_sensitive" and window.block_sessions == 1:
            alpha_score = 1.0 if window.offset_id == "offset_0" else 0.6
            beta_score = 0.8 if window.offset_id == "offset_0" else 1.1
            report.slice_reports[window.window_id] = {
                "alpha": ComparisonMetrics(
                    run_count=1,
                    veto_rate=0.0,
                    veto_correctness_rate=1.0,
                    mean_fresh_deployable_pct=80.0,
                    mean_replay_score=alpha_score,
                    mean_contradiction_rate=0.0,
                    mean_playbook_precision=1.0,
                    review_completeness_rate=1.0,
                    active_playbook_rate=1.0,
                    mean_active_playbook_count=1.0,
                    mean_conflict_count=0.0,
                ),
                "beta": ComparisonMetrics(
                    run_count=1,
                    veto_rate=0.0,
                    veto_correctness_rate=1.0,
                    mean_fresh_deployable_pct=82.0,
                    mean_replay_score=beta_score,
                    mean_contradiction_rate=0.0,
                    mean_playbook_precision=1.0,
                    review_completeness_rate=1.0,
                    active_playbook_rate=1.0,
                    mean_active_playbook_count=1.0,
                    mean_conflict_count=0.0,
                ),
            }
        elif window.surface_key == "surface_too_short" and window.block_sessions == 1 and window.offset_id == "offset_0" and "iter_0::forward" in window.window_id:
            report.slice_reports[window.window_id] = {
                "alpha": ComparisonMetrics(
                    run_count=1,
                    veto_rate=0.0,
                    veto_correctness_rate=1.0,
                    mean_fresh_deployable_pct=80.0,
                    mean_replay_score=1.0,
                    mean_contradiction_rate=0.0,
                    mean_playbook_precision=1.0,
                    review_completeness_rate=1.0,
                    active_playbook_rate=1.0,
                    mean_active_playbook_count=1.0,
                    mean_conflict_count=0.0,
                )
            }

    harness_report = service.evaluate_horizon_discovery(
        report=report,
        authority=authority,
        generated_windows=windows,
        scenarios=fixture_pack.scenarios,
    )
    result_map = {result.surface_key: result for result in harness_report.group_results}
    assert result_map["surface_offset_sensitive"].outcome is HorizonDiscoveryOutcome.OFFSET_SENSITIVE
    assert result_map["surface_offset_sensitive"].offset_outcome is OffsetComparisonOutcome.OFFSET_SENSITIVE
    assert result_map["surface_too_short"].outcome is HorizonDiscoveryOutcome.COVERAGE_INSUFFICIENT
    assert harness_report.fragility.hidden_fragility_detected is True
