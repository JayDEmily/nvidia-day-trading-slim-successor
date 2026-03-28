"""Prepared-runtime to cognition-input conversion service.

This service converts prepared runtime snapshots into the typed temporal and
options-flow inputs that feed the desk cognition runtime.
"""

from __future__ import annotations

from nvda_desk.schemas.cognition import (
    OptionsFlowContextInput,
    OptionsFlowMicroSnapshot,
    PinProgressionPoint,
    StrikeClusterObservation,
    TemporalContextInput,
    TenorCurvePoint,
)
from nvda_desk.schemas.dataset import (
    PreparedRuntimeDataset,
    PreparedRuntimeSnapshot,
    RealDataCognitionInputs,
)


class ChainToCognitionService:
    """Convert prepared runtime snapshots into cognition-ready inputs.

    Purpose:
        Bridge Gate E prepared-runtime outputs into Gate C/D cognition inputs.
    Inputs:
        `PreparedRuntimeSnapshot` or `PreparedRuntimeDataset` objects.
    Outputs:
        `RealDataCognitionInputs` packets containing typed temporal and
        options-flow inputs.
    Determinism:
        Performs only structural conversion with stable field mapping; no hidden
        inference or mutable runtime state is introduced.
    """

    def convert_snapshot(self, snapshot: PreparedRuntimeSnapshot) -> RealDataCognitionInputs:
        """Convert one prepared runtime snapshot into cognition-ready inputs."""

        temporal_input = TemporalContextInput(
            ts=snapshot.ts,
            next_expiry=snapshot.front_expiry,
            next_event_at=snapshot.next_event_at,
            live_event_snapshot=snapshot.live_event_snapshot,
            precursor_runtime_packet=snapshot.precursor_runtime_packet,
            prior_session_return_pct=snapshot.prior_session_return_pct,
            intraday_move_pct=snapshot.intraday_move_pct,
            prior_close_price=snapshot.prior_close_price,
            official_open_price=snapshot.session_open_price,
            last_price=snapshot.spot_price,
            interval_volume_shares=snapshot.interval_volume_shares,
            cumulative_session_volume=snapshot.cumulative_session_volume,
            session_vwap=snapshot.session_vwap,
            distance_to_vwap_pct=snapshot.distance_to_vwap_pct,
            vwap_slope_5m_pct=snapshot.vwap_slope_5m_pct,
            opening_range_high_5m=snapshot.opening_range_high_5m,
            opening_range_low_5m=snapshot.opening_range_low_5m,
            opening_range_break_count=snapshot.opening_range_break_count,
            price_realised_vol_5m_pct=snapshot.price_realised_vol_5m_pct,
            price_realised_vol_15m_pct=snapshot.price_realised_vol_15m_pct,
            relative_volume_ratio=snapshot.relative_volume_ratio,
            rolling_range_5m_pct=snapshot.rolling_range_5m_pct,
            impulse_age_bars=snapshot.impulse_age_bars,
        )
        options_flow_input = OptionsFlowContextInput(
            spot_price=snapshot.spot_price,
            front_dte=snapshot.front_dte,
            next_dte=snapshot.next_dte,
            front_atm_iv=snapshot.front_atm_iv,
            next_atm_iv=snapshot.next_atm_iv,
            put_call_skew=snapshot.put_call_skew,
            gamma_pressure_score=snapshot.gamma_pressure_score,
            call_put_imbalance=snapshot.call_put_imbalance,
            oi_concentration=snapshot.oi_concentration,
            atm_straddle_value=snapshot.atm_straddle_value,
            front_realised_vol=snapshot.front_realised_vol,
            next_realised_vol=snapshot.next_realised_vol,
            spot_to_pin_distance_pct=snapshot.spot_to_pin_distance_pct,
            call_oi_near_spot=snapshot.call_oi_near_spot,
            put_oi_near_spot=snapshot.put_oi_near_spot,
            front_volume_near_spot=snapshot.front_volume_near_spot,
            next_volume_near_spot=snapshot.next_volume_near_spot,
            nearby_strike_clusters=[
                StrikeClusterObservation(
                    strike=cluster.strike,
                    side=cluster.side,
                    open_interest=cluster.open_interest,
                    volume=cluster.volume,
                    distance_to_spot_pct=cluster.distance_to_spot_pct,
                )
                for cluster in snapshot.nearby_strike_clusters
            ],
            repeated_snapshot_sequence=[
                OptionsFlowMicroSnapshot(
                    ts=point.ts,
                    front_atm_iv=point.front_atm_iv,
                    next_atm_iv=point.next_atm_iv,
                    put_call_skew=point.put_call_skew,
                    gamma_pressure_score=point.gamma_pressure_score,
                    spot_to_pin_distance_pct=point.spot_to_pin_distance_pct,
                )
                for point in snapshot.repeated_snapshot_sequence
            ],
            tenor_iv_curve=[
                TenorCurvePoint(tenor_dte=point.tenor_dte, atm_iv=point.atm_iv)
                for point in snapshot.tenor_iv_curve
            ],
            pin_progression_sequence=[
                PinProgressionPoint(ts=point.ts, distance_to_pin_pct=point.distance_to_pin_pct)
                for point in snapshot.pin_progression_sequence
            ],
        )
        return RealDataCognitionInputs(
            snapshot_ts=snapshot.ts,
            lineage=snapshot.lineage,
            temporal_input=temporal_input,
            options_flow_input=options_flow_input,
        )

    def convert_dataset(
        self, prepared_dataset: PreparedRuntimeDataset
    ) -> list[RealDataCognitionInputs]:
        """Convert a prepared runtime dataset into cognition-ready input packets."""

        return [self.convert_snapshot(snapshot) for snapshot in prepared_dataset.snapshots]
