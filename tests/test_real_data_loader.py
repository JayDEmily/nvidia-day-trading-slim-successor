"""Gate E tests for deterministic real-data runtime preparation."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.dataset import PreparedRuntimeFixturePack
from nvda_desk.services.chain_to_cognition import ChainToCognitionService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.real_data_loader import RealDataLoaderService
from nvda_desk.services.temporal_context import TemporalContextService

FIXTURE_PACK_PATH = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "real_data"
    / "gate_e_prepared_runtime_fixture_pack.json"
)


def _load_fixture_pack() -> PreparedRuntimeFixturePack:
    service = RealDataLoaderService()
    return service.load_fixture_pack(FIXTURE_PACK_PATH)


def test_gate_e_fixture_pack_round_trips_from_disk() -> None:
    """The prepared-runtime fixture pack should validate from disk without mutation."""

    raw = json.loads(FIXTURE_PACK_PATH.read_text(encoding="utf-8"))
    pack = _load_fixture_pack()
    assert pack.pack_id == "gate-e-prepared-runtime"
    assert pack.bundle.provenance.symbol == "NVDA"
    assert pack.prepared_dataset.dataset_id == "gate-e-prepared-runtime-dataset"
    assert pack.model_dump(mode="json") == raw


def test_prepare_runtime_dataset_aligns_repeated_chain_sequence_with_bars_and_events() -> None:
    """Prepared runtime datasets should align chains to bars and preserve sequence lineage."""

    service = RealDataLoaderService()
    pack = _load_fixture_pack()
    rebuilt = service.prepare_runtime_dataset(
        pack.bundle, dataset_id=pack.prepared_dataset.dataset_id
    )

    assert rebuilt == pack.prepared_dataset
    assert len(rebuilt.snapshots) == 3
    assert [snapshot.ts.isoformat() for snapshot in rebuilt.snapshots] == [
        "2026-03-23T14:02:00+00:00",
        "2026-03-23T14:07:00+00:00",
        "2026-03-23T14:12:00+00:00",
    ]
    first_snapshot = rebuilt.snapshots[0]
    assert first_snapshot.aligned_bar_ts.isoformat() == "2026-03-23T14:00:00+00:00"
    assert first_snapshot.bar_age_seconds == 120
    assert first_snapshot.snapshot_sequence_id == "seq-opening-balance"
    assert first_snapshot.snapshot_count == 3
    assert first_snapshot.lineage.event_ids == ["evt-1", "evt-2"]
    assert first_snapshot.lineage.event_lineage_keys == [
        "src:ir:evt-1",
        "src:macro:evt-2",
    ]
    assert first_snapshot.live_event_snapshot is not None
    assert first_snapshot.live_event_snapshot.next_event is not None
    assert first_snapshot.live_event_snapshot.next_event.event_id == "evt-1"
    assert [event.event_id for event in first_snapshot.live_event_snapshot.nearby_events] == [
        "evt-1",
        "evt-2",
    ]
    assert (
        first_snapshot.repeated_snapshot_sequence[-1].ts.isoformat() == "2026-03-23T14:12:00+00:00"
    )
    assert first_snapshot.pin_progression_bias == "pinning_in"


def test_chain_to_cognition_service_converts_prepared_snapshot_to_typed_inputs() -> None:
    """Prepared runtime snapshots should convert directly into cognition-ready inputs."""

    pack = _load_fixture_pack()
    snapshot = pack.prepared_dataset.snapshots[0]
    converted = ChainToCognitionService().convert_snapshot(snapshot)

    assert converted.snapshot_ts == snapshot.ts
    assert converted.lineage.sequence_id == "seq-opening-balance"
    assert converted.temporal_input.ts == snapshot.ts
    assert converted.temporal_input.next_expiry == snapshot.front_expiry
    assert converted.temporal_input.live_event_snapshot == snapshot.live_event_snapshot
    assert converted.options_flow_input.spot_price == snapshot.spot_price
    assert converted.options_flow_input.front_dte == snapshot.front_dte
    assert converted.options_flow_input.call_oi_near_spot == snapshot.call_oi_near_spot
    assert len(converted.options_flow_input.repeated_snapshot_sequence) == 3
    assert len(converted.options_flow_input.tenor_iv_curve) == 3
    assert (
        converted.options_flow_input.pin_progression_sequence[-1].distance_to_pin_pct
        < converted.options_flow_input.pin_progression_sequence[0].distance_to_pin_pct
    )


def test_runtime_snapshot_sanity_report_is_deterministic() -> None:
    """The runtime sanity report should expose coverage and sequencing deterministically."""

    service = RealDataLoaderService()
    pack = _load_fixture_pack()
    rebuilt_report = service.build_runtime_snapshot_sanity_report(
        pack.bundle, pack.prepared_dataset
    )

    assert rebuilt_report == pack.sanity_report
    assert rebuilt_report.prepared_snapshot_count == 3
    assert rebuilt_report.total_bars == 4
    assert rebuilt_report.total_chain_snapshots == 3
    assert rebuilt_report.repeated_sequence_count == 1
    assert rebuilt_report.max_sequence_length == 3
    assert rebuilt_report.orphan_bar_count == 1
    assert rebuilt_report.orphan_chain_count == 0
    assert rebuilt_report.aligned_bar_coverage_pct == 75.0
    assert rebuilt_report.aligned_chain_coverage_pct == 100.0
    assert rebuilt_report.monotonic_snapshot_timestamps is True
    assert "orphan_bar_count:1" in rebuilt_report.reasons


def test_gate_e_runtime_path_validation() -> None:
    """Gate E prepared snapshots should evaluate cleanly through temporal and options layers."""

    pack = _load_fixture_pack()
    converted_inputs = ChainToCognitionService().convert_dataset(pack.prepared_dataset)
    temporal_service = TemporalContextService(Settings())
    options_service = OptionsFlowContextService()

    temporal_outputs = [
        temporal_service.evaluate(packet.temporal_input) for packet in converted_inputs
    ]
    options_outputs = [
        options_service.evaluate(packet.options_flow_input) for packet in converted_inputs
    ]

    assert len(temporal_outputs) == 3
    assert len(options_outputs) == 3
    assert [output.event_window_state for output in temporal_outputs] == [
        "event_imminent_window",
        "event_imminent_window",
        "event_imminent_window",
    ]
    assert all(
        output.repeated_snapshot_state in {"escalating_pressure", "pinning_build", "stable_recheck"}
        for output in options_outputs
    )
    assert options_outputs[0].pin_progression_state == "pinning_in"
    assert options_outputs[0].dominant_strike == 118.0
    assert options_outputs[0].options_behavior_cluster in {
        "compression_breakout_ready",
        "pin_reversion_ready",
        "balanced_options_state",
    }
