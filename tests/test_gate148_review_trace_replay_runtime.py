"""Gate 148 review, trace, replay, and legacy expectation checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from nvda_desk.config import Settings
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.testing.bounded_trace_review import BoundedTraceReviewService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = REPO_ROOT / "fixtures" / "trace_review" / "gate_132_bounded_trace_fixture_pack.json"


def test_gate148_review_packet_exposes_preserved_seam_surfaces_additively() -> None:
    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    review_packet = cast(dict[str, Any], result.review.review_packet)
    admissibility_surface = cast(dict[str, Any], review_packet["admissibility_surface"])
    candidate_ownership = cast(dict[str, Any], review_packet["candidate_ownership"])
    overlay_risk_decision = cast(dict[str, Any], review_packet["overlay_risk_decision"])
    terminal_risk_application = cast(dict[str, Any], review_packet["terminal_risk_application"])
    final_risk_join = cast(dict[str, Any], review_packet["final_risk_join"])
    stage_local_handoff = cast(dict[str, Any], review_packet["stage_local_handoff"])
    assert admissibility_surface["admissible_playbook_ids"] == [
        "continuation_ladder"
    ]
    assert candidate_ownership["lead_playbook_id"] == "continuation_ladder"
    assert overlay_risk_decision["action"] == "allow"
    assert (
        cast(dict[str, Any], terminal_risk_application["final_decision"])["action"]
        == final_risk_join["action"]
    )
    assert cast(dict[str, Any], cast(dict[str, Any], stage_local_handoff["terminal_risk_application"])["final_decision"])["action"] == "allow"


def test_gate148_bounded_trace_report_carries_preserved_seam_models_and_markdown_snapshot() -> None:
    service = BoundedTraceReviewService(Settings())
    report = service.run_fixture_pack(PACK_PATH)
    runs = {run.scenario_id: run for run in report.runs}
    markdown = service.render_markdown_report(report)

    clear = runs["clear_window_continuation"]
    assert clear.admissibility_surface is not None
    assert clear.admissibility_surface.admissible_playbook_ids == ["continuation_ladder"]
    assert clear.candidate_ownership is not None
    assert clear.candidate_ownership.lead_playbook_id == "continuation_ladder"
    assert clear.overlay_risk_decision is not None
    assert clear.overlay_risk_decision.action.value == "allow"
    assert clear.terminal_risk_application is not None
    assert clear.terminal_risk_application.final_decision.action.value == clear.final_risk_action

    blocked = runs["mild_down_block"]
    assert blocked.overlay_risk_decision is not None
    assert blocked.terminal_risk_application is not None
    assert blocked.terminal_risk_application.final_decision.action.value == blocked.final_risk_action

    assert "## Preserved seam snapshot" in markdown
    assert "clear_window_continuation: admitted=continuation_ladder; lead_owner=continuation_ladder; overlay=allow; terminal=allow" in markdown
