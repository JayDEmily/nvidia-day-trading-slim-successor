"""Gate 147 overlay-evaluation versus terminal-risk-application checks."""

from __future__ import annotations

from typing import Any, cast

from nvda_desk.config import Settings
from nvda_desk.schemas.risk import RiskAction
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime, DeskCognitionRuntimeResult
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def _run_supportive_runtime(
    *,
    vix_level: float = 18.4,
    vvix_level: float = 84.0,
    inventory_update: dict[str, float] | None = None,
) -> DeskCognitionRuntimeResult:
    fixture = supportive_runtime_fixture()
    inventory_state = fixture.inventory_state
    if inventory_update:
        inventory_state = inventory_state.model_copy(update=inventory_update)
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
        inventory_state=inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )


def test_gate147_allow_path_preserves_overlay_and_terminal_allow_without_overlap_override() -> None:
    result = _run_supportive_runtime()

    assert result.stage_local_handoff is not None
    assert result.stage_local_handoff.overlay_risk_decision is not None
    assert result.stage_local_handoff.overlay_risk_decision.action is RiskAction.ALLOW
    assert result.stage_local_handoff.terminal_risk_application is not None
    assert result.stage_local_handoff.terminal_risk_application.final_decision.action is RiskAction.ALLOW
    assert [item.value for item in result.stage_local_handoff.terminal_risk_application.overlap_classes] == [
        "overlay_allow_no_terminal_override"
    ]
    assert result.execution.final_risk_join is not None
    assert result.execution.final_risk_join.action is RiskAction.ALLOW
    review_handoff = cast(dict[str, Any], result.review.review_packet["stage_local_handoff"])
    terminal_application = cast(dict[str, Any], review_handoff["terminal_risk_application"])
    final_decision = cast(dict[str, Any], terminal_application["final_decision"])
    assert final_decision["action"] == "allow"



def test_gate147_overlay_derisk_path_records_overlay_only_overlap_class() -> None:
    result = _run_supportive_runtime(vix_level=24.0, vvix_level=100.0)

    assert result.stage_local_handoff is not None
    assert result.stage_local_handoff.overlay_risk_decision is not None
    assert result.stage_local_handoff.overlay_risk_decision.action is RiskAction.DERISK
    assert result.stage_local_handoff.terminal_risk_application is not None
    assert result.stage_local_handoff.terminal_risk_application.final_decision.action is RiskAction.DERISK
    assert [item.value for item in result.stage_local_handoff.terminal_risk_application.overlap_classes] == [
        "overlay_derisk_no_terminal_override"
    ]
    assert result.execution.final_risk_join is not None
    assert result.execution.final_risk_join.action is RiskAction.DERISK



def test_gate147_posture_block_escalation_records_overlap_class_against_overlay_allow() -> None:
    result = _run_supportive_runtime(
        inventory_update={
            "existing_inventory_pct": 80.0,
            "fresh_cash_pct": 5.0,
            "capital_lockup_pct": 80.0,
        }
    )

    assert result.posture.permission_state.value == "block"
    assert result.stage_local_handoff is not None
    assert result.stage_local_handoff.overlay_risk_decision is not None
    assert result.stage_local_handoff.overlay_risk_decision.action is RiskAction.ALLOW
    assert result.stage_local_handoff.terminal_risk_application is not None
    assert result.stage_local_handoff.terminal_risk_application.final_decision.action is RiskAction.BLOCK
    assert [item.value for item in result.stage_local_handoff.terminal_risk_application.overlap_classes] == [
        "posture_block_supersedes_overlay_allow"
    ]
    assert result.execution.final_risk_join is not None
    assert result.execution.final_risk_join.action is RiskAction.BLOCK
