"""Gate 174 parallel-risk lane input contract checks."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.parallel_risk import ParallelRiskReadableStage, ParallelRiskStageReadStatus
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime, DeskCognitionRuntimeResult
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

def test_gate174_runtime_emits_co_resident_parallel_lane_packet() -> None:
    _, result = _runtime_result()
    packet = result.parallel_risk_lane
    assert packet is not None
    assert packet.protocol_version == "parallel_risk_lane.v1"
    assert packet.lane_id == "independent_parallel_risk_lane"
    assert packet.serial_spine_preserved is True
    assert packet.co_resident_from_session_start is True
    assert packet.arbiter_active is False
    assert "not_step_1_1" in packet.notes
    assert "not_step_8" in packet.notes
    assert "not_eighth_stage" in packet.notes

def test_gate174_marks_temporal_as_the_first_lawful_stage_output_and_preserves_review_as_downstream() -> None:
    _, result = _runtime_result()
    packet = result.parallel_risk_lane
    assert packet is not None
    statuses = {record.stage: record.status for record in packet.stage_output_reads}
    assert statuses[ParallelRiskReadableStage.TEMPORAL] is ParallelRiskStageReadStatus.USED
    # Gate 174 created the temporal-only bootstrap packet. Later gates may lawfully
    # upgrade additional stage reads, but temporal must remain the first lawful read
    # and review must remain downstream of lane construction.
    for stage in (
        ParallelRiskReadableStage.REGIME,
        ParallelRiskReadableStage.OPTIONS_FLOW,
        ParallelRiskReadableStage.POSTURE,
        ParallelRiskReadableStage.ELIGIBILITY,
        ParallelRiskReadableStage.EXECUTION,
    ):
        assert statuses[stage] in {
            ParallelRiskStageReadStatus.NOT_YET_AVAILABLE,
            ParallelRiskStageReadStatus.USED,
        }
    assert statuses[ParallelRiskReadableStage.REVIEW] is ParallelRiskStageReadStatus.NOT_YET_AVAILABLE
