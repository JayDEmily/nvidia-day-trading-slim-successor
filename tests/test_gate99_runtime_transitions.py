"""Gate 99 transition and adjacent-snapshot tests."""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.real_data_loader import RealDataLoaderService
from nvda_desk.testing.canonical_runtime_harness import CanonicalRuntimeHarnessService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

FIXTURE_PACK_PATH = Path("fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json")


def test_adjacent_prepared_runtime_snapshots_transition_without_illegal_sideways_behaviour() -> None:
    pack = RealDataLoaderService().load_fixture_pack(FIXTURE_PACK_PATH)
    supportive = supportive_runtime_fixture()
    runtime = DeskCognitionRuntime(Settings())
    service = CanonicalRuntimeHarnessService()

    results = []
    for snapshot in pack.prepared_dataset.snapshots:
        harness = service.build(
            dataset_id=pack.prepared_dataset.dataset_id,
            snapshot=snapshot,
            regime_input=supportive.regime_input,
            inventory_state=supportive.inventory_state,
            risk_budget_remaining_pct=supportive.risk_budget_remaining_pct,
        )
        results.append(
            runtime.run(
                temporal_input=harness.temporal_input,
                regime_input=harness.regime_input,
                options_flow_input=harness.options_flow_input,
                inventory_state=harness.inventory_state,
                risk_budget_remaining_pct=harness.risk_budget_remaining_pct,
            )
        )

    event_minutes = [result.temporal.event_minutes_remaining for result in results]
    assert all(minutes is not None for minutes in event_minutes)
    flow_tension = [result.options_flow.flow_tension_score for result in results]
    fresh_targets = [result.execution.target_fresh_deployable_pct for result in results]
    active_playbooks = [result.execution.active_playbook_ids for result in results]

    ordered_event_minutes = [minutes for minutes in event_minutes if minutes is not None]
    assert ordered_event_minutes == sorted(ordered_event_minutes, reverse=True)
    assert flow_tension[0] < flow_tension[1] <= flow_tension[2]
    assert [result.temporal.event_window_state for result in results] == [
        "event_imminent_window",
        "event_imminent_window",
        "event_imminent_window",
    ]
    assert all(result.execution.final_risk_join is not None for result in results)
    assert [result.execution.final_risk_join.action.value for result in results if result.execution.final_risk_join is not None] == [
        "derisk",
        "derisk",
        "derisk",
    ]
    assert fresh_targets == [0.0, 0.0, 0.0]
    assert active_playbooks == [[], [], []]


def test_ordered_event_window_transition_freezes_allow_derisk_block_progression() -> None:
    fixture = supportive_runtime_fixture()
    runtime = DeskCognitionRuntime(Settings())

    ordered_minutes = [90, 30, -1]
    results = []
    for minutes in ordered_minutes:
        temporal = fixture.temporal_input.model_copy(
            update={"next_event_at": fixture.temporal_input.ts + timedelta(minutes=minutes)}
        )
        results.append(
            runtime.run(
                temporal_input=temporal,
                regime_input=fixture.regime_input,
                options_flow_input=fixture.options_flow_input,
                inventory_state=fixture.inventory_state,
                risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
            )
        )

    assert [result.temporal.event_window_state for result in results] == [
        "same_session_event_window",
        "event_imminent_window",
        "event_live_window",
    ]
    assert [result.posture.permission_state.value for result in results] == [
        "allow",
        "derisk",
        "block",
    ]
    assert [result.execution.target_fresh_deployable_pct for result in results] == [55.0, 0.0, 0.0]
    assert results[-1].execution.active_playbook_ids == []
