"""Gate 177 anti-duplication semantics and lean review integration checks."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from nvda_desk.config import Settings
from nvda_desk.schemas.parallel_risk import (
    ParallelRiskCandidateAuditState,
    ParallelRiskConsequenceClass,
    ParallelRiskEnvironmentalWeatherState,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.parallel_risk_lane import ParallelRiskLaneService
from nvda_desk.services.real_data_loader import RealDataLoaderService
from nvda_desk.testing.canonical_runtime_harness import CanonicalRuntimeHarnessService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

FIXTURE_PACK_PATH = Path("fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json")


def _runtime_result():
    pack = RealDataLoaderService().load_fixture_pack(FIXTURE_PACK_PATH)
    supportive = supportive_runtime_fixture()
    harness = CanonicalRuntimeHarnessService().build(
        dataset_id=pack.prepared_dataset.dataset_id,
        snapshot=pack.prepared_dataset.snapshots[0],
        regime_input=supportive.regime_input,
        inventory_state=supportive.inventory_state,
        risk_budget_remaining_pct=supportive.risk_budget_remaining_pct,
    )
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=harness.temporal_input,
        regime_input=harness.regime_input,
        options_flow_input=harness.options_flow_input,
        inventory_state=harness.inventory_state,
        risk_budget_remaining_pct=harness.risk_budget_remaining_pct,
    )
    return harness, result


def test_gate177_runtime_preserves_environmental_weather_without_candidate_fog() -> None:
    _, result = _runtime_result()
    packet = result.parallel_risk_lane
    assert packet is not None
    candidate = packet.candidate_audit_surface
    assert candidate is not None
    assert candidate.candidate_state is ParallelRiskCandidateAuditState.INACTIVE_NO_CANDIDATE
    assert candidate.anti_duplication_primary_binding_point == "not_applicable_no_candidate"
    assert candidate.duplicate_caution_suppressed is True
    assert candidate.environmental_weather_state is ParallelRiskEnvironmentalWeatherState.ELEVATED_TRANSLATION_PRESSURE


def test_gate177_can_describe_candidate_specific_shape_without_becoming_arbiter() -> None:
    harness, result = _runtime_result()
    service = ParallelRiskLaneService()
    packet = service.evaluate(temporal_input=harness.temporal_input, temporal=result.temporal)
    packet = service.enrich_market_translation(packet=packet, regime=result.regime, options_flow=result.options_flow)
    execution = result.execution.model_copy(
        update={
            "active_family_ids": ["breakout"],
            "active_setup_variant_ids": ["breakout_orb"],
            "lead_family_id": "breakout",
            "lead_setup_variant_id": "breakout_orb",
            "lead_playbook_id": "orb_long",
            "entry_style": "staggered_entry",
            "hedge_required": True,
            "target_fresh_deployable_pct": 80.0,
            "inventory_action": "hold",
            "fresh_capital_action": "deploy",
        }
    )
    candidate_packet = service.enrich_candidate_semantics(
        packet=packet,
        posture=result.posture,
        eligibility=result.eligibility,
        execution=execution,
    )
    surface = candidate_packet.candidate_audit_surface
    assert surface is not None
    assert surface.candidate_state is ParallelRiskCandidateAuditState.ACTIVE_CANDIDATE
    assert surface.consequence_class is ParallelRiskConsequenceClass.HEDGE_REQUIRED
    assert surface.anti_duplication_primary_binding_point == "execution_expression_output"
    assert "execution_expression_output" in surface.descriptive_secondary_reads


def test_gate177_review_packet_exposes_lane_summary_without_dmp_redesign() -> None:
    _, result = _runtime_result()
    review_packet = result.review.review_packet
    assert "parallel_risk_lane" in review_packet
    assert "parallel_risk_lane_summary" in review_packet
    summary = review_packet["parallel_risk_lane_summary"]
    assert summary["lane_id"] == "independent_parallel_risk_lane"
    assert "weather=" in summary["summary"]
    assert "candidate_state=" in summary["summary"]
