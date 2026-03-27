from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.session_clock import SessionClockFeaturePayload
from nvda_desk.schemas.temporal_surface import TemporalStateFeaturePayload


class PrecursorVenueUniverse(StrEnum):
    """Bounded ex-US precursor venue families allowed by Gate 68."""

    JPX_CASH_INDEX_COMPLEX = "jpx_cash_index_complex"
    HKEX_CASH_INDEX_COMPLEX = "hkex_cash_index_complex"
    MAINLAND_CHINA_CASH_INDEX_COMPLEX = "mainland_china_cash_index_complex"
    CFFEX_INDEX_FUTURES_COMPLEX = "cffex_index_futures_complex"


class PrecursorSourceClass(StrEnum):
    """Permitted precursor source classes."""

    CASH_EQUITY_INDEX = "cash_equity_index"
    INDEX_FUTURES = "index_futures"


class RawPrecursorField(StrEnum):
    """Raw precursor facts allowed to enter later stitching gates."""

    SESSION_RETURN_PCT = "session_return_pct"
    OPENING_GAP_PCT = "opening_gap_pct"
    SESSION_RANGE_PCT = "session_range_pct"
    REALISED_VOL_PCT = "realised_vol_pct"
    CLOSE_LOCATION_IN_RANGE = "close_location_in_range"
    RELATIVE_VOLUME_RATIO = "relative_volume_ratio"
    FUTURES_BASIS_PCT = "futures_basis_pct"
    CLOSE_TIMESTAMP = "close_timestamp"


class DerivedPrecursorField(StrEnum):
    """Derived precursor summaries that later policy gates may consume."""

    DIRECTIONAL_COMPOSITE_SCORE = "directional_composite_score"
    CROSS_VENUE_AGREEMENT_SCORE = "cross_venue_agreement_score"
    FUTURES_CASH_DIVERGENCE_SCORE = "futures_cash_divergence_score"
    IMPULSE_PERSISTENCE_SCORE = "impulse_persistence_score"
    PRECURSOR_PRESSURE_SCORE = "precursor_pressure_score"
    CARRY_RISK_WARNING_SCORE = "carry_risk_warning_score"


class SessionAlignmentExpectation(StrEnum):
    """How precursor sessions align to the next US decision window."""

    USE_LAST_COMPLETE_SESSION = "use_last_complete_session"
    NO_PARTIAL_SESSION_PROJECTION = "no_partial_session_projection"
    MAP_TO_NEXT_US_CASH_OPEN = "map_to_next_us_cash_open"
    WEEKEND_AND_HOLIDAY_GAPS_MUST_STAY_EXPLICIT = "weekend_and_holiday_gaps_must_stay_explicit"


class ExcludedPrecursorSource(StrEnum):
    """Tempting but out-of-scope sources explicitly excluded by Gate 68."""

    EUROPEAN_CASH_INDICES = "european_cash_indices"
    COMMODITIES_COMPLEX = "commodities_complex"
    CRYPTO_24X7 = "crypto_24x7"
    SINGLE_STOCK_CHATTER = "single_stock_chatter"


class PrecursorVenueContract(BaseModel):
    """One bounded precursor venue contract frozen by Gate 68."""

    model_config = ConfigDict(extra="forbid")

    venue: PrecursorVenueUniverse
    source_class: PrecursorSourceClass
    included_in_live_read_set: bool = True
    allowed_raw_fields: list[RawPrecursorField] = Field(default_factory=list)
    allowed_derived_fields: list[DerivedPrecursorField] = Field(default_factory=list)
    session_alignment: list[SessionAlignmentExpectation] = Field(default_factory=list)
    rationale: list[str] = Field(default_factory=list)
    exclusion_notes: list[str] = Field(default_factory=list)


class PrecursorUniverseAuthorityPacket(BaseModel):
    """Frozen Gate 68 authority for precursor markets and allowed fields."""

    model_config = ConfigDict(extra="forbid")

    venues: list[PrecursorVenueContract] = Field(default_factory=list)
    raw_fields: list[RawPrecursorField] = Field(default_factory=list)
    derived_fields: list[DerivedPrecursorField] = Field(default_factory=list)
    session_alignment_expectations: list[SessionAlignmentExpectation] = Field(default_factory=list)
    excluded_sources: list[ExcludedPrecursorSource] = Field(default_factory=list)


class Bar1mPayload(BaseModel):
    ts_utc: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


class MarketSnapshotResponse(BaseModel):
    symbol: str
    requested_at: datetime
    temporal_state: TemporalStateFeaturePayload
    session_clock: SessionClockFeaturePayload
    latest_bar: Bar1mPayload | None = None


class IntradayBarsResponse(BaseModel):
    symbol: str
    requested_at: datetime
    bars: list[Bar1mPayload]
