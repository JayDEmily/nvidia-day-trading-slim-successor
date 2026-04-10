"""Gate 189 capital-deployment authority service checks."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import (
    CapitalDeploymentAuthorityAction,
    CapitalDeploymentAuthorityInput,
)
from nvda_desk.schemas.execution_records import CapitalStateSnapshotPayload
from nvda_desk.schemas.risk import RiskAction
from nvda_desk.services.capital_deployment_authority import CapitalDeploymentAuthorityService
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime, DeskCognitionRuntimeResult
from nvda_desk.testing.cognition_fixtures import (
    stressed_runtime_fixture,
    supportive_runtime_fixture,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

EXECUTION_RECORDS_SERVICE = REPO_ROOT / "src/nvda_desk/services/execution_records.py"

def _capital_snapshot(*, buying_power: float = 1000.0, source: str = "controlled_bootstrap") -> CapitalStateSnapshotPayload:
    return CapitalStateSnapshotPayload(
        capital_state_snapshot_id=1,
        created_at=datetime(2026, 4, 3, 15, 0, tzinfo=UTC),
        snapshot_ts=datetime(2026, 4, 3, 15, 0, tzinfo=UTC),
        cash=buying_power,
        equity=buying_power,
        buying_power=buying_power,
        gross_exposure=0.0,
        net_exposure=0.0,
        source=source,
    )

def _runtime_result(*, stressed: bool = False, vix_level: float | None = None, vvix_level: float | None = None) -> DeskCognitionRuntimeResult:
    fixture = stressed_runtime_fixture() if stressed else supportive_runtime_fixture()
    regime_input = fixture.regime_input
    options_flow_input = fixture.options_flow_input
    if vix_level is not None:
        regime_input = regime_input.model_copy(update={"vix_level": vix_level})
        options_flow_input = options_flow_input.model_copy(update={"vix_level": vix_level})
    if vvix_level is not None:
        regime_input = regime_input.model_copy(update={"vvix_level": vvix_level})
        options_flow_input = options_flow_input.model_copy(update={"vvix_level": vvix_level})
    return DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=regime_input,
        options_flow_input=options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

def test_gate189_repo_native_capital_path_still_exposes_latest_capital_snapshot_payload() -> None:
    source = EXECUTION_RECORDS_SERVICE.read_text(encoding="utf-8")

    assert "def latest_capital_state(self) -> CapitalStateSnapshotPayload:" in source
    assert "return self._to_capital_payload(row)" in source
    assert 'buying_power=Decimal("100000.000000")' in source
    assert "buying_power=float(row.buying_power)" in source

def test_gate189_service_deploys_from_controlled_capital_snapshot() -> None:
    capital = _capital_snapshot(buying_power=1000.0)
    result = _runtime_result()

    decision = CapitalDeploymentAuthorityService().evaluate(
        CapitalDeploymentAuthorityInput(
            posture=result.posture,
            eligibility=result.eligibility,
            execution=result.execution,
            stage_local_handoff=result.stage_local_handoff,
            parallel_risk_lane_packet=result.parallel_risk_lane,
            capital_state=capital,
        )
    )

    assert capital.buying_power == 1000.0
    assert decision.deployment_action is CapitalDeploymentAuthorityAction.DEPLOY
    assert decision.authorised_deployable_pct == 35.0
    assert decision.authorised_notional_usd == 350.0
    assert decision.terminal_risk_action is RiskAction.ALLOW

def test_gate189_service_stands_down_when_runtime_candidate_is_blocked() -> None:
    capital = _capital_snapshot(buying_power=1000.0)
    result = _runtime_result(stressed=True)

    decision = CapitalDeploymentAuthorityService().evaluate(
        CapitalDeploymentAuthorityInput(
            posture=result.posture,
            eligibility=result.eligibility,
            execution=result.execution,
            stage_local_handoff=result.stage_local_handoff,
            parallel_risk_lane_packet=result.parallel_risk_lane,
            capital_state=capital,
        )
    )

    assert decision.deployment_action is CapitalDeploymentAuthorityAction.STAND_DOWN
    assert decision.authorised_deployable_pct == 0.0
    assert decision.authorised_notional_usd == 0.0
    assert "stand_down:no_lead_playbook" in decision.rationale_codes

def test_gate189_service_respects_derisked_execution_target_without_zeroing_it() -> None:
    capital = _capital_snapshot(buying_power=1000.0)
    result = _runtime_result(vix_level=25.0, vvix_level=100.0)

    decision = CapitalDeploymentAuthorityService().evaluate(
        CapitalDeploymentAuthorityInput(
            posture=result.posture,
            eligibility=result.eligibility,
            execution=result.execution,
            stage_local_handoff=result.stage_local_handoff,
            parallel_risk_lane_packet=result.parallel_risk_lane,
            capital_state=capital,
        )
    )

    assert result.execution.final_risk_join is not None
    assert result.execution.final_risk_join.action is RiskAction.DERISK
    assert decision.deployment_action is CapitalDeploymentAuthorityAction.DEPLOY
    assert decision.terminal_risk_action is RiskAction.DERISK
    assert decision.authorised_deployable_pct == result.execution.target_fresh_deployable_pct
    assert decision.authorised_notional_usd == round(1000.0 * result.execution.target_fresh_deployable_pct / 100.0, 4)
