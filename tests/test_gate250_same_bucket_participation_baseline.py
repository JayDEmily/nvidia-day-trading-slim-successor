"""Gate 250 checkpoint tests for same-bucket participation baseline promotion."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from nvda_desk.config import Settings
from nvda_desk.services.upstream_signal_checkpointing import (
    CHECKPOINT_PARTICIPATION_AVAILABLE_REQUIRES_BASELINE_VOLUME,
    CHECKPOINT_PARTICIPATION_PROXY_BASELINE_OBSERVED,
    CHECKPOINT_PARTICIPATION_RATIO_POSITIVE_WHEN_PRESENT,
    UpstreamSignalCheckpointError,
)
from nvda_desk.services.upstream_signal_ingress import (
    build_participation_baseline_packet,
    session_bucket_label,
)


def test_gate250_bucket_labels_differentiate_open_lunch_and_close() -> None:
    """Positive proof for bounded session-bucket classification."""

    settings = Settings()
    open_bucket = session_bucket_label(datetime(2026, 3, 23, 13, 35, tzinfo=UTC), settings)
    lunch_bucket = session_bucket_label(datetime(2026, 3, 23, 16, 30, tzinfo=UTC), settings)
    close_bucket = session_bucket_label(datetime(2026, 3, 23, 19, 50, tzinfo=UTC), settings)

    assert open_bucket == "open_drive"
    assert lunch_bucket == "lunch"
    assert close_bucket == "close_auction"


def test_gate250_reconstructs_proxy_volume_baseline_from_relative_volume_ratio_with_checkpoints() -> None:
    """Positive proof for lawful proxy-baseline reconstruction plus observations."""

    packet = build_participation_baseline_packet(
        ts=datetime(2026, 3, 23, 16, 30, tzinfo=UTC),
        interval_volume_shares=1200.0,
        relative_volume_ratio=1.5,
        settings=Settings(),
        calendar_owner_present=True,
    )
    checkpoint_names = {obs.checkpoint_name for obs in packet.checkpoint_observations}

    assert packet.baseline_available is True
    assert packet.baseline_interval_volume_share == 800.0
    assert packet.calendar_owner == "financial_calendar_reference_bundle"
    assert packet.fallback_state == "proxy_reconstructed_from_relative_volume_ratio_not_historical_same_bucket"
    assert CHECKPOINT_PARTICIPATION_RATIO_POSITIVE_WHEN_PRESENT in checkpoint_names
    assert CHECKPOINT_PARTICIPATION_AVAILABLE_REQUIRES_BASELINE_VOLUME in checkpoint_names
    assert CHECKPOINT_PARTICIPATION_PROXY_BASELINE_OBSERVED in checkpoint_names


def test_gate250_negative_proof_raises_when_relative_volume_ratio_is_non_positive() -> None:
    """Negative proof for the positive-ratio checkpoint."""

    with pytest.raises(
        UpstreamSignalCheckpointError,
        match="upstream_signal.participation_baseline.relative_volume_ratio_positive_when_present",
    ):
        build_participation_baseline_packet(
            ts=datetime(2026, 3, 23, 16, 30, tzinfo=UTC),
            interval_volume_shares=1200.0,
            relative_volume_ratio=0.0,
            settings=Settings(),
            calendar_owner_present=False,
        )
