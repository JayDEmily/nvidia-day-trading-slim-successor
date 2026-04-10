from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.db.models import OptionsFlowHistoryObservation
from nvda_desk.schemas.cognition import OptionsFlowContextOutput, TermStructureState, SkewState, GammaState
from nvda_desk.schemas.options import OptionSnapshotPayload, OptionType
from nvda_desk.schemas.options_flow_history import (
    OptionsFlowHistoryLineage,
    OptionsFlowHistoryObservationRecord,
)


def _derived_state() -> OptionsFlowContextOutput:
    return OptionsFlowContextOutput(
        term_structure_state=TermStructureState.FLAT,
        skew_state=SkewState.BALANCED,
        gamma_state=GammaState.NEUTRAL,
        implied_move_envelope_pct=3.2,
        iv_rv_front_state='premium_to_realised',
        iv_rv_next_state='premium_to_realised',
        iv_rv_curve_state='orderly',
        pin_risk_state='contained',
        dealer_pressure_state='balanced',
        vix_spread_state='stable',
        options_behavior_cluster='balanced_participation',
        flow_tension_score=0.31,
        strike_cluster_state='distributed',
        dominant_strike=120.0,
        surface_anchor_state='near_spot',
        repeated_snapshot_state='stable',
        skew_evolution_state='stable',
        tenor_curve_state='ordered',
        pin_progression_state='stable',
        pin_progression_velocity=0.0,
        reasons=['gate243'],
    )


def test_gate243_observation_record_contract_is_bounded_and_non_allocative() -> None:
    observed_at = datetime(2026, 3, 23, 14, 15, tzinfo=UTC)
    record = OptionsFlowHistoryObservationRecord(
        symbol='NVDA',
        observed_at=observed_at,
        chain_ts=observed_at,
        front_expiry=observed_at.date(),
        next_expiry=observed_at.date(),
        derived_state=_derived_state(),
        front_expiry_rows=[
            OptionSnapshotPayload(
                as_of_date=observed_at.date(),
                expiry=observed_at.date(),
                option_type=OptionType.CALL,
                strike=120,
                bid=1.0,
                ask=1.1,
                last=1.05,
                volume=10,
                open_interest=20,
                provenance='fixture',
                confidence='high',
                source_document='fixture',
                source_pages='1',
            )
        ],
        next_expiry_rows=[],
        partiality_state='next_expiry_missing',
        record_completeness_flag=False,
        lineage=OptionsFlowHistoryLineage(
            raw_source_authority='persisted_option_snapshot',
            observed_at=observed_at,
            chain_ts=observed_at,
            raw_source_as_of_date=observed_at.date(),
            source_identity='NVDA:2026-03-23',
        ),
    )

    dumped = record.model_dump()
    assert dumped['symbol'] == 'NVDA'
    assert dumped['partiality_state'] == 'next_expiry_missing'
    assert 'capital' not in dumped
    assert 'deployment' not in dumped
    assert 'recommendation' not in dumped


def test_gate243_observation_store_model_is_distinct_from_recommendation_history() -> None:
    columns = OptionsFlowHistoryObservation.__table__.columns.keys()
    assert {'symbol', 'observed_at', 'chain_ts', 'front_expiry', 'next_expiry'} <= set(columns)
    assert {'derived_state_json', 'front_expiry_rows_json', 'next_expiry_rows_json', 'lineage_json'} <= set(columns)
    assert 'authorised_notional' not in columns
    assert 'module_id' not in columns
