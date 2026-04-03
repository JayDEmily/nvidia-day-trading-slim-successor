from __future__ import annotations

from datetime import datetime, timezone

from nvda_desk.schemas.dataset import OptionQuote
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.schemas.cognition import OptionsFlowContextInput
from nvda_desk.services.real_data_loader import RealDataLoaderService


def _quote(*, strike: float, side: str, bid: float, ask: float) -> OptionQuote:
    ts = datetime(2026, 3, 23, 14, 0, tzinfo=timezone.utc)
    return OptionQuote(
        ts=ts,
        expiry=ts,
        strike=strike,
        side=side,
        bid=bid,
        ask=ask,
        last=(bid + ask) / 2.0,
        iv=0.6,
        oi=10.0,
        volume=5.0,
    )


def test_gate185_surface_anchor_metric_derives_from_near_spot_call_put_mids() -> None:
    service = RealDataLoaderService()
    quotes = [
        _quote(strike=118.0, side="call", bid=1.4, ask=1.6),
        _quote(strike=118.0, side="put", bid=1.3, ask=1.5),
        _quote(strike=120.0, side="call", bid=3.6, ask=3.8),
        _quote(strike=120.0, side="put", bid=3.4, ask=3.6),
    ]

    metric = service._surface_anchor_to_spot_pct(quotes, spot_price=118.0)

    assert metric is not None
    assert metric > 0.75


def test_gate185_options_flow_output_distinguishes_anchor_away_state() -> None:
    service = OptionsFlowContextService()
    result = service.evaluate(
        OptionsFlowContextInput(
            spot_price=118.0,
            front_dte=4,
            next_dte=11,
            front_atm_iv=0.58,
            next_atm_iv=0.584,
            put_call_skew=0.02,
            gamma_pressure_score=0.22,
            call_put_imbalance=-0.03,
            oi_concentration=0.20,
            atm_straddle_value=5.4,
            front_realised_vol=0.57,
            next_realised_vol=0.56,
            surface_anchor_to_spot_pct=1.05,
        )
    )

    assert result.surface_anchor_state == "anchored_away"
    assert result.options_behavior_cluster == "anchored_translation_tension"
