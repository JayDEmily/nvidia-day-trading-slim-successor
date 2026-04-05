"""Gate 96 canonical prepared-runtime harness checks."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.dataset import PreparedRuntimeFixturePack
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.real_data_loader import RealDataLoaderService
from nvda_desk.testing.canonical_runtime_harness import (
    CanonicalRuntimeHarnessInput,
    CanonicalRuntimeHarnessService,
)
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

FIXTURE_PACK_PATH = Path("fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json")


def _canonical_harness() -> tuple[PreparedRuntimeFixturePack, CanonicalRuntimeHarnessInput]:
    pack = RealDataLoaderService().load_fixture_pack(FIXTURE_PACK_PATH)
    supportive = supportive_runtime_fixture()
    harness = CanonicalRuntimeHarnessService().build(
        dataset_id=pack.prepared_dataset.dataset_id,
        snapshot=pack.prepared_dataset.snapshots[0],
        regime_input=supportive.regime_input,
        inventory_state=supportive.inventory_state,
        risk_budget_remaining_pct=supportive.risk_budget_remaining_pct,
    )
    return pack, harness


def test_canonical_runtime_harness_helper_preserves_snapshot_identity() -> None:
    pack, harness = _canonical_harness()

    assert harness.fixture_id == "canonical_prepared_runtime_harness"
    assert harness.dataset_id == pack.prepared_dataset.dataset_id
    assert harness.source_snapshot_ts == pack.prepared_dataset.snapshots[0].ts
    assert harness.sequence_id == "seq-opening-balance"
    assert harness.temporal_input.ts == pack.prepared_dataset.snapshots[0].ts
    assert harness.temporal_input.live_event_snapshot == pack.prepared_dataset.snapshots[0].live_event_snapshot
    assert harness.options_flow_input.spot_price == pack.prepared_dataset.snapshots[0].spot_price
    assert harness.options_flow_input.repeated_snapshot_sequence


def test_canonical_runtime_harness_run_is_deterministic_and_freezes_outputs() -> None:
    _, harness = _canonical_harness()
    runtime = DeskCognitionRuntime(Settings())

    first = runtime.run(
        temporal_input=harness.temporal_input,
        regime_input=harness.regime_input,
        options_flow_input=harness.options_flow_input,
        inventory_state=harness.inventory_state,
        risk_budget_remaining_pct=harness.risk_budget_remaining_pct,
    )
    second = runtime.run(
        temporal_input=harness.temporal_input,
        regime_input=harness.regime_input,
        options_flow_input=harness.options_flow_input,
        inventory_state=harness.inventory_state,
        risk_budget_remaining_pct=harness.risk_budget_remaining_pct,
    )

    assert first.stage_packet_ids == second.stage_packet_ids
    assert first.packet_lineage == second.packet_lineage
    assert first.review.review_packet == second.review.review_packet

    assert first.temporal.event_window_state == "event_imminent_window"
    assert first.options_flow.options_behavior_cluster == "anchored_translation_tension"
    assert first.posture.permission_state.value == "allow"
    assert round(first.execution.target_fresh_deployable_pct, 4) == 0.0
    assert first.eligibility.add_candidates == []
    assert first.execution.active_playbook_ids == []
    assert first.review.summary == "window=early_anchor; permission=allow; families=['none']; setups=['none']; playbooks=['none']; final_risk=derisk"
    assert first.packet_lineage[0] == first.stage_packet_ids["temporal"]
    assert first.packet_lineage[-1] == first.stage_packet_ids["review"]
