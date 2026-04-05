from __future__ import annotations

from typing import Any, cast

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import (
    ExecutionExpressionInput,
    PlaybookAction,
    PlaybookCandidate,
    PlaybookDecision,
    PlaybookEligibilityOutput,
    ReviewExplanationInput,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime, DeskCognitionRuntimeResult
from nvda_desk.services.execution_expression import ExecutionExpressionService
from nvda_desk.services.review_explanation import ReviewExplanationService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def _supportive_runtime_result() -> DeskCognitionRuntimeResult:
    fixture = supportive_runtime_fixture()
    return DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )


def _multi_eligible_payload(continuation_size: float, compression_size: float) -> ExecutionExpressionInput:
    result = _supportive_runtime_result()
    eligibility = PlaybookEligibilityOutput(
        candidates=[
            PlaybookCandidate(
                playbook_id="continuation_ladder",
                family_id="trend_continuation",
                setup_variant_id="opening_drive_continuation",
                execution_expression_id="continuation_ladder_exec",
                horizon="intraday",
                decision=PlaybookDecision.ELIGIBLE,
                action_bias=PlaybookAction.ADD,
                sizing_fraction=continuation_size,
                hedge_overlay=False,
                reasons=["continuation_conditions_met"],
            ),
            PlaybookCandidate(
                playbook_id="compression_breakout",
                family_id="compression_release",
                setup_variant_id="midday_compression_release",
                execution_expression_id="compression_breakout_exec",
                horizon="intraday",
                decision=PlaybookDecision.ELIGIBLE,
                action_bias=PlaybookAction.ADD,
                sizing_fraction=compression_size,
                hedge_overlay=False,
                reasons=["compression_conditions_met"],
            ),
        ],
        active_family_ids=["trend_continuation", "compression_release"],
        active_setup_variant_ids=["opening_drive_continuation", "midday_compression_release"],
        add_candidates=["continuation_ladder", "compression_breakout"],
        reasons=["two_candidates_live"],
    )
    return ExecutionExpressionInput(
        temporal=result.temporal,
        regime=result.regime,
        options_flow=result.options_flow,
        posture=result.posture,
        eligibility=eligibility,
        modifier_runtime_packet=result.execution.modifier_runtime_packet,
    )


def test_gate119_score_based_adjudication_can_beat_registry_order() -> None:
    payload = _multi_eligible_payload(continuation_size=0.10, compression_size=0.35)
    result = ExecutionExpressionService().evaluate(payload)

    assert result.lead_playbook_id == "compression_breakout"
    assert result.active_playbook_ids[0] == "compression_breakout"
    assert result.contradiction_resolution == "mixed_context_resolved_by_score"
    assert result.candidate_adjudication[0].playbook_id == "compression_breakout"
    assert result.candidate_adjudication[0].score > result.candidate_adjudication[1].score
    assert any(reason.startswith("sizing_fraction:") for reason in result.lead_selection_reasons)


def test_gate119_registry_priority_breaks_true_score_ties() -> None:
    payload = _multi_eligible_payload(continuation_size=0.35, compression_size=0.35)
    result = ExecutionExpressionService().evaluate(payload)

    assert result.lead_playbook_id == "continuation_ladder"
    assert result.contradiction_resolution == "registry_priority_tiebreak"
    assert result.candidate_adjudication[0].registry_priority < result.candidate_adjudication[1].registry_priority
    assert result.candidate_adjudication[0].score == result.candidate_adjudication[1].score


def test_gate119_review_packet_exposes_adjudication_and_contradiction_resolution() -> None:
    runtime_result = _supportive_runtime_result()
    payload = _multi_eligible_payload(continuation_size=0.10, compression_size=0.35)
    execution = ExecutionExpressionService().evaluate(payload)
    review = ReviewExplanationService().evaluate(
        ReviewExplanationInput(
            temporal=runtime_result.temporal,
            regime=runtime_result.regime,
            options_flow=runtime_result.options_flow,
            posture=runtime_result.posture,
            eligibility=payload.eligibility,
            execution=execution,
            modifier_runtime_packet=runtime_result.execution.modifier_runtime_packet,
            temporal_input=supportive_runtime_fixture().temporal_input,
        )
    )

    packet = cast(dict[str, Any], review.review_packet["execution"])
    assert packet["lead_playbook_id"] == "compression_breakout"
    assert packet["contradiction_resolution"] == "mixed_context_resolved_by_score"
    assert packet["candidate_adjudication"][0]["playbook_id"] == "compression_breakout"
