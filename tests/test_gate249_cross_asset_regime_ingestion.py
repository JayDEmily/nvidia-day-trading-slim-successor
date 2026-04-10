"""Gate 249 checkpoint tests for cross-asset regime ingestion."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from nvda_desk.schemas.dataset import PreparedRuntimeRegimePacket, PreparedRuntimeSnapshot
from nvda_desk.services.chain_to_cognition import ChainToCognitionService
from nvda_desk.services.real_data_loader import RealDataLoaderService
from nvda_desk.services.upstream_signal_checkpointing import (
    CHECKPOINT_CHAIN_TO_COGNITION_REGIME_MAPPING,
    CHECKPOINT_REGIME_COMPLETE_REQUIRES_BREADTH_CONCENTRATION,
    UpstreamSignalCheckpointError,
)


def _first_snapshot() -> PreparedRuntimeSnapshot:
    """Load the canonical prepared-runtime fixture pack."""

    pack = RealDataLoaderService().load_fixture_pack(
        Path("fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json")
    )
    return pack.prepared_dataset.snapshots[0]


def test_gate249_chain_to_cognition_builds_live_regime_input_from_promoted_packet() -> None:
    """Positive proof for lawful live regime ingress plus observable checkpoints."""

    snapshot = _first_snapshot().model_copy(
        update={
            "promoted_regime_packet": PreparedRuntimeRegimePacket(
                source_family="fixture_regime_capture",
                source_symbols=["NVDA", "NQ", "ES", "SOX", "VIX", "VVIX", "US10Y", "US2Y", "USDJPY"],
                observed_at=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
                aligned_to_runtime_ts=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
                alignment_age_seconds=0,
                alignment_state="aligned_same_bucket",
                nvda_return_pct=0.8,
                nq_return_pct=0.5,
                es_return_pct=0.3,
                sox_return_pct=0.9,
                breadth_score=0.67,
                concentration_score=0.41,
                vix_level=18.4,
                vvix_level=84.0,
                us10y=4.22,
                us2y=4.04,
                usdjpy=148.9,
                completeness_state="complete_for_live_ingress",
            )
        }
    )
    converted = ChainToCognitionService().convert_snapshot(snapshot)
    checkpoint_names = {obs.checkpoint_name for obs in converted.checkpoint_observations}

    assert converted.regime_input is not None
    assert converted.regime_input.nq_return_pct == 0.5
    assert CHECKPOINT_REGIME_COMPLETE_REQUIRES_BREADTH_CONCENTRATION in checkpoint_names
    assert CHECKPOINT_CHAIN_TO_COGNITION_REGIME_MAPPING in checkpoint_names


def test_gate249_negative_proof_raises_when_complete_packet_lacks_breadth_or_concentration() -> None:
    """Negative proof for the no-fake-completeness checkpoint."""

    snapshot = _first_snapshot().model_copy(
        update={
            "promoted_regime_packet": PreparedRuntimeRegimePacket(
                source_family="fixture_regime_capture",
                source_symbols=["NVDA", "NQ", "ES"],
                observed_at=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
                aligned_to_runtime_ts=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
                alignment_age_seconds=0,
                nvda_return_pct=0.8,
                nq_return_pct=0.5,
                es_return_pct=0.3,
                sox_return_pct=0.9,
                concentration_score=0.41,
                vix_level=18.4,
                vvix_level=84.0,
                us10y=4.22,
                us2y=4.04,
                usdjpy=148.9,
                completeness_state="complete_for_live_ingress",
            )
        }
    )

    with pytest.raises(
        UpstreamSignalCheckpointError,
        match="upstream_signal.regime_packet.complete_requires_breadth_concentration",
    ):
        ChainToCognitionService().convert_snapshot(snapshot)
