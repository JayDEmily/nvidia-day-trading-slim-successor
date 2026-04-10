"""Gate 251 checkpoint tests for raw-to-cognition wiring."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from nvda_desk.config import Settings
from nvda_desk.schemas.dataset import (
    PreparedParticipationBaselinePacket,
    PreparedRuntimeRegimePacket,
    PreparedRuntimeSnapshot,
)
from nvda_desk.services.chain_to_cognition import ChainToCognitionService
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.real_data_loader import RealDataLoaderService
from nvda_desk.services.upstream_signal_checkpointing import (
    CHECKPOINT_CHAIN_TO_COGNITION_PARTICIPATION_MAPPING,
    CHECKPOINT_CHAIN_TO_COGNITION_REGIME_MAPPING,
    CHECKPOINT_PARTICIPATION_AVAILABLE_REQUIRES_BASELINE_VOLUME,
    UpstreamSignalCheckpointError,
)
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def _first_snapshot() -> PreparedRuntimeSnapshot:
    """Load the canonical prepared-runtime fixture pack."""

    pack = RealDataLoaderService().load_fixture_pack(
        Path("fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json")
    )
    return pack.prepared_dataset.snapshots[0]


def test_gate251_chain_to_cognition_wires_regime_and_participation_truth() -> None:
    """Positive proof for raw-to-cognition wiring plus checkpoint observations."""

    snapshot = _first_snapshot().model_copy(
        update={
            "promoted_regime_packet": PreparedRuntimeRegimePacket(
                source_family="fixture_regime_capture",
                source_symbols=["NVDA", "NQ", "ES", "SOX", "VIX", "VVIX", "US10Y", "US2Y", "USDJPY"],
                observed_at=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
                aligned_to_runtime_ts=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
                alignment_age_seconds=0,
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
            ),
            "participation_baseline_packet": PreparedParticipationBaselinePacket(
                observed_at=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
                session_bucket_label="lunch",
                observed_interval_volume_share=1200.0,
                baseline_interval_volume_share=800.0,
                relative_volume_ratio=1.5,
                observed_spread_bps=12.5,
                baseline_spread_bps=None,
                observed_trade_count=42,
                baseline_trade_count=None,
                baseline_available=True,
                fallback_state="baseline_present",
            ),
        }
    )
    converted = ChainToCognitionService().convert_snapshot(snapshot)
    checkpoint_names = {obs.checkpoint_name for obs in converted.checkpoint_observations}

    assert converted.regime_input is not None
    assert converted.temporal_input.session_bucket_label == "lunch"
    assert converted.temporal_input.same_bucket_interval_volume_share_baseline == 800.0
    assert converted.options_flow_input.same_bucket_spread_bps == 12.5
    assert converted.options_flow_input.same_bucket_trade_count == 42
    assert CHECKPOINT_CHAIN_TO_COGNITION_REGIME_MAPPING in checkpoint_names
    assert CHECKPOINT_CHAIN_TO_COGNITION_PARTICIPATION_MAPPING in checkpoint_names


def test_gate251_negative_proof_raises_when_mutated_participation_packet_claims_missing_baseline() -> None:
    """Negative proof for the final participation wiring checkpoint."""

    snapshot = _first_snapshot().model_copy(
        update={
            "participation_baseline_packet": PreparedParticipationBaselinePacket(
                observed_at=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
                session_bucket_label="lunch",
                observed_interval_volume_share=1200.0,
                baseline_interval_volume_share=None,
                relative_volume_ratio=1.5,
                baseline_available=True,
                fallback_state="mutated_invalid_state",
            )
        }
    )

    with pytest.raises(
        UpstreamSignalCheckpointError,
        match="upstream_signal.participation_baseline.available_requires_baseline_volume",
    ):
        ChainToCognitionService().convert_snapshot(snapshot)


def test_gate251_corrected_runtime_path_stays_callable_without_redesign() -> None:
    """Positive proof that the corrected runtime remains callable."""

    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )
    assert result.execution.target_fresh_deployable_pct == 35.0
    assert result.review is not None
