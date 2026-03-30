from __future__ import annotations

from nvda_desk.config import Settings
from nvda_desk.schemas.risk import RiskAction
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def _run_supportive_runtime(*, vix_level: float = 18.4, vvix_level: float = 84.0):
    fixture = supportive_runtime_fixture()
    regime_input = fixture.regime_input.model_copy(
        update={
            "vix_level": vix_level,
            "vvix_level": vvix_level,
        }
    )
    options_flow_input = fixture.options_flow_input.model_copy(
        update={
            "vix_level": vix_level,
            "vvix_level": vvix_level,
        }
    )
    return DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=regime_input,
        options_flow_input=options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )


def test_gate121_allow_path_keeps_execution_shape_but_records_final_join() -> None:
    result = _run_supportive_runtime()

    assert result.execution.final_risk_join is not None
    assert result.execution.final_risk_join.action is RiskAction.ALLOW
    assert result.execution.pre_final_risk_active_playbook_ids == result.execution.active_playbook_ids
    assert result.execution.pre_final_risk_lead_playbook_id == result.execution.lead_playbook_id
    assert result.review.review_packet["final_risk_join"]["action"] == "allow"
    assert result.review.stage_reason_packets[-1].stage == "final_risk_join"
    assert result.review.stage_reason_packets[-1].summary == "allow"


def test_gate121_derisk_path_reshapes_execution_without_vetoing_candidate() -> None:
    result = _run_supportive_runtime(vix_level=24.0, vvix_level=100.0)

    assert result.execution.final_risk_join is not None
    assert result.execution.final_risk_join.action is RiskAction.DERISK
    assert result.execution.lead_playbook_id == "continuation_ladder"
    assert result.execution.pre_final_risk_lead_playbook_id == "continuation_ladder"
    assert result.execution.target_fresh_deployable_pct == 35.75
    assert result.execution.scaling_plan == [7.15, 10.725, 17.875]
    assert result.execution.max_risk_per_trade == 0.2275
    assert result.execution.per_slice_risk_pct == 0.0759
    assert result.execution.hedge_required is True
    assert result.execution.hedge_ratio == 0.35
    assert "final_risk_derisk_execution" in result.execution.geometry_notes
    assert result.review.review_packet["final_risk_join"]["execution_effect"] == "derisk_execution"


def test_gate121_block_path_exposes_pre_join_execution_and_vetoes_final_output() -> None:
    result = _run_supportive_runtime(vix_level=34.0, vvix_level=120.0)

    assert result.execution.final_risk_join is not None
    assert result.execution.final_risk_join.action is RiskAction.BLOCK
    assert result.execution.pre_final_risk_active_playbook_ids == ["continuation_ladder"]
    assert result.execution.pre_final_risk_lead_playbook_id == "continuation_ladder"
    assert result.execution.pre_final_risk_entry_style == "trend_ladder_3_step"
    assert result.execution.active_playbook_ids == []
    assert result.execution.lead_playbook_id is None
    assert result.execution.entry_style == "final_risk_blocked"
    assert result.execution.target_fresh_deployable_pct == 0.0
    assert result.execution.scaling_plan == []
    assert result.execution.per_slice_risk_pct == 0.0
    assert "final_risk_block_execution" in result.execution.geometry_notes
    assert result.review.review_packet["execution"]["pre_final_risk_lead_playbook_id"] == "continuation_ladder"
    assert result.review.review_packet["final_risk_join"]["execution_effect"] == "block_execution"
