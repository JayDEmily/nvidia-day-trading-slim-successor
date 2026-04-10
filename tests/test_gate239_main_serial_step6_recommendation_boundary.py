"""Gate 239 Step 6 recommendation-boundary checks."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import CapitalDeploymentAuthorityAction, CapitalDeploymentAuthorityInput, ExecutionExpressionInput, PlaybookEligibilityInput, PostureRiskInput
from nvda_desk.schemas.execution_records import CapitalStateSnapshotPayload
from nvda_desk.services.capital_deployment_authority import CapitalDeploymentAuthorityService
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.execution_expression import ExecutionExpressionService
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.playbook_eligibility import PlaybookEligibilityService
from nvda_desk.services.posture_risk import PostureRiskService
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAVES_LEDGER = REPO_ROOT / "docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_LEAVES_v1.json"
DOC03 = REPO_ROOT / "docs/03_DOMAIN_MODEL.md"
DOC07 = REPO_ROOT / "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md"
VOCAB = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"
RUNTIME = REPO_ROOT / "src/nvda_desk/services/cognition_runtime.py"


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


def _supportive_stage_outputs():
    fixture = supportive_runtime_fixture()
    temporal = TemporalContextService(Settings()).evaluate(fixture.temporal_input)
    regime = MarketRegimeContextService().evaluate(fixture.regime_input)
    options_flow = OptionsFlowContextService().evaluate(fixture.options_flow_input)
    posture = PostureRiskService().evaluate(
        PostureRiskInput(
            temporal=temporal,
            regime=regime,
            options_flow=options_flow,
            inventory=fixture.inventory_state,
            risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        )
    )
    eligibility = PlaybookEligibilityService().evaluate(
        PlaybookEligibilityInput(
            temporal=temporal,
            regime=regime,
            options_flow=options_flow,
            posture=posture,
        )
    )
    return fixture, temporal, regime, options_flow, posture, eligibility


def test_gate239_docs_and_runtime_promote_recommendation_boundary() -> None:
    payload = json.loads(LEAVES_LEDGER.read_text(encoding="utf-8"))
    assert "Gate 239" in payload["completed_gate_ids"]
    assert "recommendation-intensity echo only" in DOC03.read_text(encoding="utf-8")
    assert "Step 6 read rule" in DOC07.read_text(encoding="utf-8")

    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))
    notes = {entry["canonical_slug"]: entry.get("notes", []) for entry in vocab["entries"]}
    assert any("stateless recommendation" in note for note in notes["expression_execution"])

    runtime_source = RUNTIME.read_text(encoding="utf-8")
    assert "execution=execution_post_modifier_pre_final_risk" in runtime_source


def test_gate239_execution_recommendation_ignores_step4_capital_echoes() -> None:
    _, temporal, regime, options_flow, posture, eligibility = _supportive_stage_outputs()
    posture = posture.model_copy(update={
        "fresh_deployable_capital_pct": 12.0,
        "inventory_action_bias": "hedge",
    })
    execution = ExecutionExpressionService().evaluate(
        ExecutionExpressionInput(
            temporal=temporal,
            regime=regime,
            options_flow=options_flow,
            posture=posture,
            eligibility=eligibility,
        )
    )

    assert execution.lead_playbook_id == "continuation_ladder"
    assert execution.target_fresh_deployable_pct == 35.0
    assert execution.inventory_action == "add"


def test_gate239_cda_caps_from_permission_state_downstream() -> None:
    fixture = supportive_runtime_fixture()
    runtime_result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    assert runtime_result.stage_local_handoff.execution_post_modifier_pre_final_risk is not None
    decision = CapitalDeploymentAuthorityService().evaluate(
        CapitalDeploymentAuthorityInput(
            posture=runtime_result.posture.model_copy(update={"fresh_deployable_capital_pct": 5.0}),
            eligibility=runtime_result.eligibility,
            execution=runtime_result.stage_local_handoff.execution_post_modifier_pre_final_risk,
            stage_local_handoff=runtime_result.stage_local_handoff,
            parallel_risk_lane_packet=runtime_result.parallel_risk_lane,
            capital_state=_capital_snapshot(),
        )
    )

    assert decision.deployment_action is CapitalDeploymentAuthorityAction.DEPLOY
    assert decision.opportunity_target_pct == 35.0
    assert decision.posture_cap_pct == 55.0
    assert decision.authorised_deployable_pct == 35.0
    assert decision.authorised_notional_usd == 350.0
