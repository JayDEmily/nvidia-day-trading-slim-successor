"""Gate 248 checkpoint and docstring-compliance tests."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from nvda_desk.schemas.checkpoints import CheckpointObservation
from nvda_desk.schemas.dataset import (
    PreparedParticipationBaselinePacket,
    PreparedRuntimeRegimePacket,
    PreparedRuntimeSnapshot,
    RealDataCognitionInputs,
)
from nvda_desk.services.chain_to_cognition import ChainToCognitionService
from nvda_desk.services.real_data_loader import RealDataLoaderService
from nvda_desk.services.upstream_signal_ingress import (
    build_market_regime_input,
    build_participation_baseline_packet,
)


def _first_snapshot() -> PreparedRuntimeSnapshot:
    """Load the canonical prepared-runtime fixture pack."""

    pack = RealDataLoaderService().load_fixture_pack(
        Path("fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json")
    )
    return pack.prepared_dataset.snapshots[0]


def _require_docstring_sections(docstring: str, *, label: str) -> None:
    """Validate the mandatory docstring sections using explicit checkpoint logic."""

    required_sections = [
        "Purpose:",
        "Inputs:",
        "Outputs:",
        "Side Effects:",
        "Failure Modes:",
        "Checkpoints:",
    ]
    for section in required_sections:
        if section not in docstring:
            raise RuntimeError(f"CHECKPOINT_FAILURE:gate248.docstring.{label}.{section}")


def test_gate248_snapshot_contract_admits_bounded_packets_and_checkpoint_observations() -> None:
    """Positive proof for the bounded packet contract."""

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
                checkpoint_observations=[
                    CheckpointObservation(
                        checkpoint_name="fixture.regime_packet.observed",
                        timestamp=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
                        input_snapshot={"source": "fixture"},
                        output_snapshot={"complete": True},
                    )
                ],
            ),
            "participation_baseline_packet": PreparedParticipationBaselinePacket(
                observed_at=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
                session_bucket_label="lunch",
                observed_interval_volume_share=1200.0,
                baseline_interval_volume_share=800.0,
                relative_volume_ratio=1.5,
                baseline_available=True,
                fallback_state="baseline_present",
                checkpoint_observations=[
                    CheckpointObservation(
                        checkpoint_name="fixture.participation_packet.observed",
                        timestamp=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
                        input_snapshot={"source": "fixture"},
                        output_snapshot={"baseline_available": True},
                    )
                ],
            ),
        }
    )

    assert snapshot.promoted_regime_packet is not None
    assert snapshot.promoted_regime_packet.checkpoint_observations[0].checkpoint_name == (
        "fixture.regime_packet.observed"
    )
    assert snapshot.participation_baseline_packet is not None
    assert snapshot.participation_baseline_packet.checkpoint_observations[0].output_snapshot == {
        "baseline_available": True
    }


def test_gate248_negative_proof_rejects_malformed_checkpoint_observations() -> None:
    """Negative proof for the checkpoint-observation contract."""

    with pytest.raises(ValidationError):
        PreparedParticipationBaselinePacket.model_validate(
            {
                "observed_at": datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
                "session_bucket_label": "lunch",
                "checkpoint_observations": [
                    {
                        "timestamp": datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
                        "input_snapshot": {},
                        "output_snapshot": {},
                    }
                ],
            }
        )


def test_gate248_docstrings_meet_checkpoint_extension_requirements() -> None:
    """Positive proof for structured docstring compliance on modified boundaries."""

    _require_docstring_sections(
        PreparedRuntimeRegimePacket.__doc__ or "",
        label="PreparedRuntimeRegimePacket",
    )
    _require_docstring_sections(
        PreparedParticipationBaselinePacket.__doc__ or "",
        label="PreparedParticipationBaselinePacket",
    )
    _require_docstring_sections(
        RealDataCognitionInputs.__doc__ or "",
        label="RealDataCognitionInputs",
    )
    _require_docstring_sections(
        ChainToCognitionService.__doc__ or "",
        label="ChainToCognitionService",
    )
    _require_docstring_sections(
        build_market_regime_input.__doc__ or "",
        label="build_market_regime_input",
    )
    _require_docstring_sections(
        build_participation_baseline_packet.__doc__ or "",
        label="build_participation_baseline_packet",
    )


def test_gate248_docstring_negative_proof_turns_red_when_required_section_is_removed() -> None:
    """Negative proof for the docstring compliance checkpoint."""

    with pytest.raises(RuntimeError, match="gate248.docstring.synthetic.Checkpoints"):
        _require_docstring_sections(
            "Purpose:\nInputs:\nOutputs:\nSide Effects:\nFailure Modes:",
            label="synthetic",
        )
