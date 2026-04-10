"""Gate E tests for deterministic real-data runtime preparation."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.db.base import Base
from nvda_desk.db.models import Bar1m, Instrument
from nvda_desk.db.session import create_engine_from_url, create_session_factory
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




def test_real_data_loader_populates_promoted_regime_packet_from_live_capture_db(tmp_path: Path) -> None:
    """Loader should build one non-null promoted regime packet from actual captured bars."""

    database_path = tmp_path / "regime_capture.sqlite"
    database_url = f"sqlite+pysqlite:///{database_path}"
    engine = create_engine_from_url(database_url)
    Base.metadata.create_all(bind=engine)
    session_factory = create_session_factory(database_url)
    with session_factory() as session:
        symbols = {
            "NVDA": "equity",
            "QQQ": "etf",
            "SPY": "etf",
            "SOXX": "etf",
            "VIX": "index",
            "VVIX": "index",
            "US10Y": "macro",
            "US2Y": "macro",
            "USDJPY": "fx",
        }
        for symbol, asset_class in symbols.items():
            session.add(Instrument(symbol=symbol, asset_class=asset_class))
        session.flush()
        instrument_map = {instrument.symbol: instrument for instrument in session.query(Instrument).all()}
        rows = {
            "QQQ": [(Decimal("500.0"), Decimal("501.5"), 200000), (Decimal("501.5"), Decimal("503.0"), 220000)],
            "SPY": [(Decimal("600.0"), Decimal("601.0"), 180000), (Decimal("601.0"), Decimal("602.2"), 185000)],
            "SOXX": [(Decimal("250.0"), Decimal("252.0"), 90000), (Decimal("252.0"), Decimal("254.5"), 95000)],
            "VIX": [(Decimal("18.0"), Decimal("18.4"), 50000), (Decimal("18.4"), Decimal("18.8"), 52000)],
            "VVIX": [(Decimal("84.0"), Decimal("85.0"), 25000), (Decimal("85.0"), Decimal("86.5"), 26000)],
            "US10Y": [(Decimal("4.20"), Decimal("4.22"), 1000), (Decimal("4.22"), Decimal("4.24"), 1000)],
            "US2Y": [(Decimal("4.00"), Decimal("4.03"), 1000), (Decimal("4.03"), Decimal("4.05"), 1000)],
            "USDJPY": [(Decimal("148.0"), Decimal("148.6"), 1000), (Decimal("148.6"), Decimal("149.1"), 1000)],
        }
        for symbol, candles in rows.items():
            instrument = instrument_map[symbol]
            for idx, (open_px, close_px, volume) in enumerate(candles):
                ts = datetime(2026, 3, 23, 14, idx * 2, tzinfo=UTC)
                session.add(
                    Bar1m(
                        instrument_id=instrument.id,
                        ts_utc=ts,
                        open=open_px,
                        high=max(open_px, close_px),
                        low=min(open_px, close_px),
                        close=close_px,
                        volume=volume,
                    )
                )
        session.commit()

    pack = _load_fixture_pack()
    loader = RealDataLoaderService(Settings(database_url=database_url))
    rebuilt = loader.prepare_runtime_dataset(pack.bundle, dataset_id=pack.prepared_dataset.dataset_id)
    packet = rebuilt.snapshots[0].promoted_regime_packet

    assert packet is not None
    assert packet.source_family == "prepared_runtime_live_capture"
    assert packet.nq_level == 503.0
    assert packet.es_level == 602.2
    assert packet.sox_level == 254.5
    assert packet.vix_level == 18.8
    assert packet.vvix_level == 86.5
    assert packet.us10y == 4.24
    assert packet.us2y == 4.05
    assert packet.usdjpy == 149.1
    assert packet.nq_return_pct == 0.6
    assert packet.es_return_pct == 0.3667
    assert packet.sox_return_pct == 1.8
    assert packet.completeness_state == "complete_for_live_ingress"
    assert packet.fallback_notes == []
    assert {obs.checkpoint_name for obs in packet.checkpoint_observations} == {
        "upstream_signal.regime_packet.capture_observed"
    }


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
    assert options_outputs[0].surface_anchor_state == "anchored_away"
    assert options_outputs[0].options_behavior_cluster == "anchored_translation_tension"
