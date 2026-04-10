"""Gate 190 capital-deployment authority runtime integration checks."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import CapitalDeploymentAuthorityAction
from nvda_desk.schemas.execution_records import CapitalStateSnapshotPayload
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.testing.cognition_fixtures import (
    stressed_runtime_fixture,
    supportive_runtime_fixture,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _capital_snapshot() -> CapitalStateSnapshotPayload:
    return CapitalStateSnapshotPayload(
        capital_state_snapshot_id=1,
        created_at=datetime(2026, 4, 3, 15, 0, tzinfo=UTC),
        snapshot_ts=datetime(2026, 4, 3, 15, 0, tzinfo=UTC),
        cash=1000.0,
        equity=1000.0,
        buying_power=1000.0,
        gross_exposure=0.0,
        net_exposure=0.0,
        source="controlled_bootstrap",
    )

def test_gate190_runtime_carries_capital_deployment_authority_without_creating_an_eighth_stage() -> None:
    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        capital_state_snapshot=_capital_snapshot(),
    )

    assert result.capital_deployment_authority is not None
    assert result.capital_deployment_authority.deployment_action is CapitalDeploymentAuthorityAction.DEPLOY
    assert result.capital_deployment_authority.authorised_notional_usd == 350.0
    assert len(result.stage_packets) == 7
    review_packet = cast(dict[str, Any], result.review.review_packet)
    assert "capital_deployment_authority" in review_packet
    capital_review = cast(dict[str, Any], review_packet["capital_deployment_authority"])
    assert capital_review["service_id"] == "capital_deployment_authority_service"
    assert result.execution.lead_playbook_id == "continuation_ladder"

def test_gate190_runtime_stands_down_additively_when_candidate_is_blocked() -> None:
    fixture = stressed_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        capital_state_snapshot=_capital_snapshot(),
    )

    assert result.capital_deployment_authority is not None
    assert result.capital_deployment_authority.deployment_action is CapitalDeploymentAuthorityAction.STAND_DOWN
    assert result.capital_deployment_authority.authorised_notional_usd == 0.0
    review_packet = cast(dict[str, Any], result.review.review_packet)
    capital_review = cast(dict[str, Any], review_packet["capital_deployment_authority"])
    assert capital_review["deployment_action"] == "stand_down"

def test_gate190_runtime_omits_capital_authority_when_no_capital_snapshot_is_supplied() -> None:
    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    assert result.capital_deployment_authority is None
    assert "capital_deployment_authority" not in result.review.review_packet
