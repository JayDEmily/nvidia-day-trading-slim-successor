"""Gate 176 market/options dependency and dislocation runtime checks."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import BreadthState, VolatilityRegime
from nvda_desk.schemas.parallel_risk import (
    ParallelRiskDependencyActivationState,
    ParallelRiskDislocationState,
    ParallelRiskEnvironmentalWeatherState,
    ParallelRiskReadableStage,
    ParallelRiskStageReadStatus,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime, DeskCognitionRuntimeResult
from nvda_desk.services.parallel_risk_lane import ParallelRiskLaneService
from nvda_desk.services.real_data_loader import RealDataLoaderService
from nvda_desk.testing.canonical_runtime_harness import (
    CanonicalRuntimeHarnessInput,
    CanonicalRuntimeHarnessService,
)
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]

FIXTURE_PACK_PATH = Path("fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json")

def _runtime_result() -> tuple[CanonicalRuntimeHarnessInput, DeskCognitionRuntimeResult]:
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

def test_gate176_runtime_emits_market_translation_surface_and_marks_stage_reads_used() -> None:
    _, result = _runtime_result()
    packet = result.parallel_risk_lane
    assert packet is not None
    surface = packet.market_translation_surface
    assert surface is not None
    assert surface.active_enough_to_matter_now is True
    assert surface.dependency_activation_state is ParallelRiskDependencyActivationState.ACTIVE_ENOUGH_TO_MATTER_NOW
    assert "options_table_used_as_translation_surface" in surface.notes
    statuses = {record.stage: record.status for record in packet.stage_output_reads}
    assert statuses[ParallelRiskReadableStage.REGIME] is ParallelRiskStageReadStatus.USED
    assert statuses[ParallelRiskReadableStage.OPTIONS_FLOW] is ParallelRiskStageReadStatus.USED

def test_gate176_supportive_fixture_is_classified_as_translation_dislocation_risk() -> None:
    _, result = _runtime_result()
    packet = result.parallel_risk_lane
    assert packet is not None
    surface = packet.market_translation_surface
    assert surface is not None
    assert surface.gamma_state == "destabilising"
    assert surface.dislocation_state is ParallelRiskDislocationState.DISLOCATION_RISK
    assert surface.environmental_weather_state is ParallelRiskEnvironmentalWeatherState.ELEVATED_TRANSLATION_PRESSURE

def test_gate176_impairment_and_justified_repricing_paths_stay_distinct() -> None:
    harness, result = _runtime_result()
    service = ParallelRiskLaneService()
    base_packet = service.evaluate(temporal_input=harness.temporal_input, temporal=result.temporal)

    justified_regime = result.regime.model_copy(update={"signal_conflict_state": "cross_asset_stress", "cross_asset_pressure_score": 0.8})
    justified_packet = service.enrich_market_translation(
        packet=base_packet,
        regime=justified_regime,
        options_flow=result.options_flow,
    )
    assert justified_packet.market_translation_surface is not None
    assert justified_packet.market_translation_surface.dislocation_state is ParallelRiskDislocationState.JUSTIFIED_REPRICING

    impaired_regime = result.regime.model_copy(update={"volatility_regime": VolatilityRegime.STRESSED, "breadth_state": BreadthState.WEAK})
    impaired_packet = service.enrich_market_translation(
        packet=base_packet,
        regime=impaired_regime,
        options_flow=result.options_flow,
    )
    assert impaired_packet.market_translation_surface is not None
    assert impaired_packet.market_translation_surface.dislocation_state is ParallelRiskDislocationState.IMPAIRMENT_RISK
    assert impaired_packet.market_translation_surface.environmental_weather_state is ParallelRiskEnvironmentalWeatherState.IMPAIRED_BACKGROUND
