"""Gate 10 tests for DMP lineage on review and replay surfaces."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.replay_compare import ReplayComparisonService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

FIXTURE_PACK = Path("fixtures/replay/gate_f_replay_regression_fixture_pack.json")


def test_review_output_carries_dmp_lineage_for_the_decision_chain() -> None:
    """Gate 10 should attach ordered packet lineage to the typed review output."""

    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        stack_id="core_full_stack",
        coefficient_set_id="full_stack_base",
    )

    assert result.review.packet_lineage is not None
    lineage = result.review.packet_lineage
    assert lineage.protocol_version == "dmp.v2"
    assert lineage.review_packet_id == result.stage_packet_ids["review"]
    assert lineage.decision_packet_id == result.stage_packet_ids["execution"]
    assert lineage.packet_lineage == list(result.packet_lineage)
    assert lineage.stage_packet_ids == result.stage_packet_ids
    assert result.review.review_packet["dmp_lineage"] == lineage.model_dump(mode="json")
    assert (
        result.stage_packets[-1].lineage.review_trace_id
        == f"review-trace::{lineage.review_packet_id}"
    )
    assert result.stage_packets[-1].packet_id == lineage.review_packet_id


def test_replay_run_result_carries_replay_packet_lineage_without_touching_report_metrics() -> (
    None
):
    """Gate 10 should enrich replay runs with lineage while leaving comparison metrics stable."""

    service = ReplayComparisonService(Settings())
    runs, report = service.compare_from_fixture_pack(FIXTURE_PACK)

    run = next(
        run
        for run in runs
        if run.coefficient_set_id == "full_stack_base" and run.scenario_id == "trend"
    )
    assert run.packet_lineage is not None
    assert run.review.packet_lineage is not None
    replay_lineage = run.packet_lineage
    review_lineage = run.review.packet_lineage
    assert replay_lineage.protocol_version == "dmp.v2"
    assert replay_lineage.review_packet_id == review_lineage.review_packet_id
    assert replay_lineage.decision_packet_id == review_lineage.decision_packet_id
    assert replay_lineage.stage_packet_ids["review"] == replay_lineage.review_packet_id
    assert replay_lineage.packet_lineage[-1] == replay_lineage.review_packet_id
    assert report.reports["full_stack_base"].run_count == 4
    assert report.reports["defensive_stack_tight"].run_count == 4
