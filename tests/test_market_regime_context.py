"""Gate D tests for deterministic market-regime classification."""

from __future__ import annotations

from nvda_desk.schemas.cognition import (
    BreadthState,
    MarketRegimeContextInput,
    VolatilityRegime,
)
from nvda_desk.services.market_regime_context import MarketRegimeContextService


def test_market_regime_context_flags_narrow_stress_and_cross_asset_pressure() -> None:
    """Gate D regime logic should make concentration, rates, and FX stress explicit."""

    service = MarketRegimeContextService()
    result = service.evaluate(
        MarketRegimeContextInput(
            nvda_return_pct=-2.5,
            nq_return_pct=-1.0,
            es_return_pct=-0.6,
            sox_return_pct=-1.8,
            breadth_score=0.33,
            concentration_score=0.82,
            vix_level=29.0,
            vvix_level=116.0,
            us10y=4.62,
            us2y=4.89,
            usdjpy=143.8,
        )
    )
    assert result.volatility_regime is VolatilityRegime.STRESSED
    assert result.breadth_state is BreadthState.WEAK
    assert result.breadth_concentration_state == "narrow_stress"
    assert result.rates_regime_state == "rates_shock_headwind"
    assert result.fx_stress_state == "yen_carry_unwind"
    assert result.cross_asset_pressure_score >= 0.8


def test_market_regime_context_exposes_semis_leading_without_breadth_as_conflict() -> (
    None
):
    """Gate D should separate single-name leadership from broad participation."""

    service = MarketRegimeContextService()
    result = service.evaluate(
        MarketRegimeContextInput(
            nvda_return_pct=2.6,
            nq_return_pct=0.8,
            es_return_pct=0.4,
            sox_return_pct=1.9,
            breadth_score=0.39,
            concentration_score=0.73,
            vix_level=21.5,
            vvix_level=91.0,
            us10y=4.28,
            us2y=4.36,
            usdjpy=146.2,
        )
    )
    assert result.sector_leadership_state == "semis_leading"
    assert result.signal_conflict_state == "leadership_without_breadth"
    assert result.breadth_concentration_state == "narrow_stress"


def test_market_regime_context_marks_broad_risk_on_when_leadership_and_breadth_align() -> (
    None
):
    """Gate D should surface broad participation cleanly when beta and breadth agree."""

    service = MarketRegimeContextService()
    result = service.evaluate(
        MarketRegimeContextInput(
            nvda_return_pct=2.4,
            nq_return_pct=1.2,
            es_return_pct=0.8,
            sox_return_pct=2.1,
            breadth_score=0.72,
            concentration_score=0.41,
            vix_level=18.5,
            vvix_level=84.0,
            us10y=4.12,
            us2y=3.95,
            usdjpy=148.6,
        )
    )
    assert result.volatility_regime is VolatilityRegime.CALM
    assert result.breadth_concentration_state == "broad_risk_on"
    assert result.signal_conflict_state == "aligned_regime"
    assert result.beta_leadership_score > 1.0
