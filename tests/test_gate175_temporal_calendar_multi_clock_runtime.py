"""Gate 175 temporal/calendar/multi-clock runtime checks."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from nvda_desk.config import Settings
from nvda_desk.schemas.parallel_risk import ParallelRiskGovernanceStatus
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
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


def test_gate175_temporal_surface_aligns_with_runtime_temporal_output() -> None:
    harness, result = _runtime_result()
    packet = result.parallel_risk_lane
    assert packet is not None
    surface = packet.temporal_surface
    assert surface.session_phase == result.temporal.session_phase
    assert surface.behavioural_phase == result.temporal.behavioural_phase
    assert surface.desk_window == result.temporal.desk_window
    assert surface.clock_envelope == result.temporal.clock_envelope
    assert surface.event_window_state == result.temporal.event_window_state
    assert surface.event_overlap_class == result.temporal.event_overlap_class
    assert surface.event_risk_timing_class == result.temporal.event_risk_timing_class
    assert surface.event_carry_sensitivity == result.temporal.event_carry_sensitivity
    assert surface.expiry_cycle_state == result.temporal.expiry_cycle_state
    assert surface.event_minutes_remaining == result.temporal.event_minutes_remaining
    assert surface.expiry_days_remaining == result.temporal.expiry_days_remaining
    assert harness.temporal_input.live_event_snapshot is not None
    assert surface.lineage_keys


def test_gate175_temporal_surface_carries_governance_statuses_honestly() -> None:
    _, result = _runtime_result()
    packet = result.parallel_risk_lane
    assert packet is not None
    surface = packet.temporal_surface
    assert surface.session_clock_governance is ParallelRiskGovernanceStatus.FIXED_STRUCTURAL_HEURISTIC
    assert surface.behavioural_phase_governance is ParallelRiskGovernanceStatus.GOVERNED_LIVE_THRESHOLD
    assert surface.event_source_governance is ParallelRiskGovernanceStatus.INVARIANT_DIRECT_READ
    assert surface.expiry_source_governance is ParallelRiskGovernanceStatus.COMPATIBILITY_TIMESTAMP
    assert surface.calendar_source_governance in {ParallelRiskGovernanceStatus.INVARIANT_DIRECT_READ, ParallelRiskGovernanceStatus.DEFERRED_NOT_ADMITTED}
    assert "co_resident_lane_created_after_temporal_stage_only" in surface.notes
