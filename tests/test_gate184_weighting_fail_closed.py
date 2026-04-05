from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.schemas.dataset import OptionQuote
from nvda_desk.services.real_data_loader import RealDataLoaderService


def _quote(*, strike: float, side: str = "call", oi: float | None = 0.0, volume: float | None = 0.0) -> OptionQuote:
    ts = datetime(2026, 3, 23, 14, 0, tzinfo=UTC)
    return OptionQuote(
        ts=ts,
        expiry=ts,
        strike=strike,
        side=side,
        bid=1.0,
        ask=1.1,
        last=1.05,
        iv=0.6,
        oi=oi,
        volume=volume,
    )


def test_gate184_dominant_strike_returns_none_without_lawful_weight() -> None:
    service = RealDataLoaderService()
    quotes = [_quote(strike=117.0), _quote(strike=118.0)]

    assert service._dominant_strike(quotes) is None


def test_gate184_nearby_clusters_ignore_zero_weight_row_order() -> None:
    service = RealDataLoaderService()
    quotes = [_quote(strike=117.0), _quote(strike=118.0), _quote(strike=119.0, oi=10.0)]

    clusters = service._nearby_strike_clusters(quotes, spot_price=118.0)

    assert [cluster.strike for cluster in clusters] == [119.0]
