"""Gate 143 additive stage-local handoff runtime checks."""

from __future__ import annotations

from typing import Any, cast

from nvda_desk.config import Settings
from nvda_desk.schemas.risk import RiskAction
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime, DeskCognitionRuntimeResult
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def _run_supportive_runtime(*, vix_level: float = 18.4, vvix_level: float = 84.0) -> DeskCognitionRuntimeResult:
    fixture = supportive_runtime_fixture()
    regime_input = fixture.regime_input.model_copy(
        update={"vix_level": vix_level, "vvix_level": vvix_level}
    )
    options_flow_input = fixture.options_flow_input.model_copy(
        update={"vix_level": vix_level, "vvix_level": vvix_level}
    )
    return DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=regime_input,
        options_flow_input=options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )


def test_gate143_preserves_stage_local_handoff_additively() -> None:
    result = _run_supportive_runtime()

    assert result.stage_local_handoff is not None
    assert result.stage_local_handoff.cited_posture_pre_modifier is not None
    assert result.stage_local_handoff.cited_eligibility is not None
    assert result.stage_local_handoff.execution_pre_modifier is not None
    assert result.stage_local_handoff.execution_post_modifier_pre_final_risk is not None
    assert result.stage_local_handoff.terminal_risk_decision is not None
    assert result.stage_local_handoff.terminal_risk_decision.action is RiskAction.ALLOW
    assert result.review.stage_local_handoff is not None
    review_handoff = cast(dict[str, Any], result.review.review_packet["stage_local_handoff"])
    terminal_risk_decision = cast(dict[str, Any], review_handoff["terminal_risk_decision"])
    assert terminal_risk_decision["action"] == "allow"
    assert result.execution.final_risk_join is not None
    assert result.execution.final_risk_join.action is RiskAction.ALLOW


def test_gate143_block_path_keeps_pre_final_execution_visible() -> None:
    result = _run_supportive_runtime(vix_level=34.0, vvix_level=120.0)

    assert result.stage_local_handoff is not None
    assert result.stage_local_handoff.execution_post_modifier_pre_final_risk is not None
    assert result.stage_local_handoff.execution_post_modifier_pre_final_risk.lead_playbook_id == "continuation_ladder"
    assert result.stage_local_handoff.terminal_risk_decision is not None
    assert result.stage_local_handoff.terminal_risk_decision.action is RiskAction.BLOCK
    assert result.execution.final_risk_join is not None
    assert result.execution.final_risk_join.action is RiskAction.BLOCK
    assert result.execution.lead_playbook_id is None
    review_handoff = cast(dict[str, Any], result.review.review_packet["stage_local_handoff"])
    pre_final = cast(dict[str, Any], review_handoff["execution_post_modifier_pre_final_risk"])
    assert pre_final["lead_playbook_id"] == "continuation_ladder"
