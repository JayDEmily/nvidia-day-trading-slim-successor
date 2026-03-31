"""Gate 97 lawful-output and lineage invariants."""

from __future__ import annotations

from pathlib import Path

import pytest

from nvda_desk.config import Settings
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.real_data_loader import RealDataLoaderService
from nvda_desk.testing.canonical_raw_runtime_harness import CanonicalRawRuntimeHarnessService
from nvda_desk.testing.canonical_runtime_harness import CanonicalRuntimeHarnessService
from nvda_desk.testing.cognition_fixtures import (
    stressed_runtime_fixture,
    supportive_runtime_fixture,
)

FIXTURE_PACK_PATH = Path("fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json")
EXPECTED_REVIEW_STAGE_ORDER = ["temporal", "regime", "options_flow", "posture", "eligibility", "execution", "final_risk_join"]
EXPECTED_PACKET_STAGE_ORDER = ["temporal", "regime", "options_flow", "posture", "eligibility", "execution"]


def _canonical_prepared_result():
    pack = RealDataLoaderService().load_fixture_pack(FIXTURE_PACK_PATH)
    supportive = supportive_runtime_fixture()
    harness = CanonicalRuntimeHarnessService().build(
        dataset_id=pack.prepared_dataset.dataset_id,
        snapshot=pack.prepared_dataset.snapshots[0],
        regime_input=supportive.regime_input,
        inventory_state=supportive.inventory_state,
        risk_budget_remaining_pct=supportive.risk_budget_remaining_pct,
    )
    return DeskCognitionRuntime(Settings()).run(
        temporal_input=harness.temporal_input,
        regime_input=harness.regime_input,
        options_flow_input=harness.options_flow_input,
        inventory_state=harness.inventory_state,
        risk_budget_remaining_pct=harness.risk_budget_remaining_pct,
    )


def _canonical_raw_result():
    supportive = supportive_runtime_fixture()
    harness = CanonicalRawRuntimeHarnessService().build_from_path(
        raw_bundle_path=Path("fixtures/real_data/gate_101_canonical_raw_runtime_bundle.json"),
        dataset_id="gate-e-prepared-runtime-dataset",
        regime_input=supportive.regime_input,
        inventory_state=supportive.inventory_state,
        risk_budget_remaining_pct=supportive.risk_budget_remaining_pct,
    )
    return DeskCognitionRuntime(Settings()).run(
        temporal_input=harness.temporal_input,
        regime_input=harness.regime_input,
        options_flow_input=harness.options_flow_input,
        inventory_state=harness.inventory_state,
        risk_budget_remaining_pct=harness.risk_budget_remaining_pct,
    )


def _supportive_result():
    fixture = supportive_runtime_fixture()
    return DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )


def _stressed_result():
    fixture = stressed_runtime_fixture()
    return DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )


@pytest.mark.parametrize(
    ("scenario_name", "result"),
    [
        ("supportive", _supportive_result()),
        ("stressed", _stressed_result()),
        ("canonical_prepared", _canonical_prepared_result()),
        ("canonical_raw", _canonical_raw_result()),
    ],
    ids=["supportive", "stressed", "canonical_prepared", "canonical_raw"],
)
def test_lawful_output_invariants_hold_across_canonical_scenarios(scenario_name: str, result) -> None:
    assert result.packet_lineage[0] == result.stage_packet_ids["temporal"]
    assert result.packet_lineage[-1] == result.stage_packet_ids["review"]

    if result.posture.permission_state.value == "block":
        assert result.posture.fresh_deployable_capital_pct == 0.0, scenario_name
        assert result.execution.target_fresh_deployable_pct == 0.0, scenario_name
        assert result.execution.active_playbook_ids == [], scenario_name
        assert "permission_blocked" in result.eligibility.no_trade_reasons, scenario_name
    else:
        assert result.execution.target_fresh_deployable_pct >= 0.0, scenario_name

    if result.execution.active_playbook_ids:
        assert result.posture.permission_state.value != "block", scenario_name
        assert result.eligibility.add_candidates or result.eligibility.hold_candidates, scenario_name


def test_lineage_and_stage_order_invariants_hold_across_canonical_scenarios() -> None:
    for result in (_supportive_result(), _stressed_result(), _canonical_prepared_result(), _canonical_raw_result()):
        assert [packet.stage for packet in result.review.stage_reason_packets] == EXPECTED_REVIEW_STAGE_ORDER
        assert list(result.stage_packet_ids) == EXPECTED_PACKET_STAGE_ORDER + ["review"]
        assert result.packet_lineage == tuple(result.stage_packet_ids[stage] for stage in result.stage_packet_ids)
