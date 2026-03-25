"""Signal-aware Step-1 temporal-context coverage."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import TemporalContextInput
from nvda_desk.schemas.dataset import PreparedRuntimeFixturePack
from nvda_desk.services.chain_to_cognition import ChainToCognitionService
from nvda_desk.services.temporal_context import TemporalContextService

FIXTURE_PACK_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "real_data" / "gate_e_prepared_runtime_fixture_pack.json"


def _load_fixture_pack() -> PreparedRuntimeFixturePack:
    return PreparedRuntimeFixturePack.model_validate_json(FIXTURE_PACK_PATH.read_text(encoding="utf-8"))


def test_temporal_context_keeps_open_disorder_alive_when_signals_stay_chaotic() -> None:
    """Step 1 should not force an early-anchor label purely because the clock crossed 10:00."""

    output = TemporalContextService(Settings()).evaluate(
        TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-23T10:07:00-04:00"),
            prior_session_return_pct=-0.8,
            intraday_move_pct=1.2,
            distance_to_vwap_pct=0.62,
            vwap_slope_5m_pct=0.12,
            opening_range_break_count=3,
            price_realised_vol_5m_pct=1.45,
            price_realised_vol_15m_pct=0.92,
            relative_volume_ratio=1.84,
            rolling_range_5m_pct=1.18,
            impulse_age_bars=1,
        )
    )

    assert output.session_phase.value == "open_disorder"
    assert output.behavioural_phase is not None and output.behavioural_phase.value == "open_disorder"
    assert output.desk_window == "open_disorder"
    assert "behavioural_phase:signal_override" in output.reasons



def test_temporal_context_can_anchor_before_the_legacy_bucket_switch() -> None:
    """Step 1 should allow a stable tape to anchor before the legacy 30-minute bucket."""

    output = TemporalContextService(Settings()).evaluate(
        TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-23T09:47:00-04:00"),
            prior_session_return_pct=0.3,
            intraday_move_pct=0.4,
            distance_to_vwap_pct=0.08,
            vwap_slope_5m_pct=0.03,
            opening_range_break_count=0,
            price_realised_vol_5m_pct=0.42,
            price_realised_vol_15m_pct=0.48,
            relative_volume_ratio=0.94,
            rolling_range_5m_pct=0.24,
            impulse_age_bars=6,
        )
    )

    assert output.session_phase.value == "early_anchor"
    assert output.behavioural_phase is not None and output.behavioural_phase.value == "early_anchor"
    assert output.desk_window == "early_anchor"
    assert "behavioural_phase:signal_override" in output.reasons



def test_chain_to_cognition_carries_the_new_step1_primitives() -> None:
    """Prepared runtime snapshots should expose the Step-1 primitive observables downstream."""

    snapshot = _load_fixture_pack().prepared_dataset.snapshots[0]
    converted = ChainToCognitionService().convert_snapshot(snapshot)

    assert converted.temporal_input.last_price == snapshot.spot_price
    assert converted.temporal_input.interval_volume_shares == snapshot.interval_volume_shares
    assert converted.temporal_input.cumulative_session_volume == snapshot.cumulative_session_volume
    assert converted.temporal_input.session_vwap == snapshot.session_vwap
    assert converted.temporal_input.distance_to_vwap_pct == snapshot.distance_to_vwap_pct
    assert converted.temporal_input.relative_volume_ratio == snapshot.relative_volume_ratio
