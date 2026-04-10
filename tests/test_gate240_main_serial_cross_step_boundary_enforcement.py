"""Gate 240 cross-step boundary enforcement checks."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from nvda_desk.config import Settings
from nvda_desk.schemas.execution_records import CapitalStateSnapshotPayload
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAVES_LEDGER = REPO_ROOT / "docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_LEAVES_v1.json"
RUNTIME = REPO_ROOT / "src/nvda_desk/services/cognition_runtime.py"
REVIEW = REPO_ROOT / "src/nvda_desk/services/review_explanation.py"
EXECUTION_REVIEW_RUNTIME = REPO_ROOT / "tests/test_execution_review_runtime.py"


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


def test_gate240_sources_and_ledgers_freeze_cross_step_boundary_terms() -> None:
    payload = json.loads(LEAVES_LEDGER.read_text(encoding="utf-8"))

    assert "Gate 240" in payload["completed_gate_ids"]
    runtime_source = RUNTIME.read_text(encoding="utf-8")
    review_source = REVIEW.read_text(encoding="utf-8")
    runtime_test = EXECUTION_REVIEW_RUNTIME.read_text(encoding="utf-8")

    assert "BindingStageName.EXECUTION: execution_post_modifier_pre_final_risk" in runtime_source
    assert 'review_packet["execution_recommendation"]' in review_source
    assert "execution_post_modifier_pre_final_risk" in runtime_test


def test_gate240_execution_stage_packet_carries_recommendation_not_post_join_hybrid() -> None:
    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input.model_copy(update={"vix_level": 34.0, "vvix_level": 120.0}),
        options_flow_input=fixture.options_flow_input.model_copy(update={"vix_level": 34.0, "vvix_level": 120.0}),
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        capital_state_snapshot=_capital_snapshot(),
    )

    assert result.stage_local_handoff is not None
    recommendation = result.stage_local_handoff.execution_post_modifier_pre_final_risk
    assert recommendation is not None
    assert recommendation.lead_playbook_id == "continuation_ladder"
    assert recommendation.target_fresh_deployable_pct == 35.0

    assert result.execution.lead_playbook_id is None
    assert result.execution.target_fresh_deployable_pct == 0.0
    assert result.execution.final_risk_join is not None
    assert result.execution.final_risk_join.action.value == "block"

    execution_packet_payload = result.stage_packets[5].payload.model_dump(mode="json")
    assert execution_packet_payload == recommendation.model_dump(mode="json")
    assert execution_packet_payload["lead_playbook_id"] == "continuation_ladder"
    assert execution_packet_payload["target_fresh_deployable_pct"] == 35.0
    assert execution_packet_payload["final_risk_join"] is None


def test_gate240_review_packet_keeps_recommendation_and_downstream_risk_separate() -> None:
    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        capital_state_snapshot=_capital_snapshot(),
    )

    review_packet = cast(dict[str, Any], result.review.review_packet)
    recommendation = cast(dict[str, Any], review_packet["execution_recommendation"])
    stage_local_handoff = cast(dict[str, Any], review_packet["stage_local_handoff"])
    final_risk_join = cast(dict[str, Any], review_packet["final_risk_join"])
    cda = cast(dict[str, Any], review_packet["capital_deployment_authority"])

    assert recommendation["lead_playbook_id"] == "continuation_ladder"
    assert recommendation["target_fresh_deployable_pct"] == 35.0
    assert recommendation["final_risk_join"] is None
    assert cast(dict[str, Any], stage_local_handoff["execution_post_modifier_pre_final_risk"])[
        "lead_playbook_id"
    ] == "continuation_ladder"
    assert final_risk_join["action"] == "allow"
    assert cda["deployment_action"] == "deploy"
    assert cda["opportunity_target_pct"] == 35.0
