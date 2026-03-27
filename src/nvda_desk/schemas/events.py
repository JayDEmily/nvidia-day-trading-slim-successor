from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ImpactLevel = Literal["low", "medium", "high"]


class DeskEventClass(StrEnum):
    """Bounded top-level event classes recognised by the desk."""

    COMPANY = "company"
    PEER_COMPANY = "peer_company"
    MACRO = "macro"
    POLICY = "policy"
    EXPIRY = "expiry"
    VENUE_SESSION = "venue_session"


class EventSemanticPhase(StrEnum):
    """Trader-grade distinction between existence, pricing, and realised path."""

    KNOWN_RISK = "known_risk"
    PRICED_RISK = "priced_risk"
    REALISED_REACTION = "realised_reaction"


class EventMaterialityTier(StrEnum):
    """Bounded impact ladder used before later posture matrices exist."""

    BACKGROUND = "background"
    MONITOR = "monitor"
    POSTURE_RELEVANT = "posture_relevant"
    DESK_CRITICAL = "desk_critical"


class CompanyEventSubclass(StrEnum):
    """NVDA-specific company events that are desk-relevant."""

    NVDA_EARNINGS = "nvda_earnings"
    NVDA_GUIDANCE = "nvda_guidance"
    NVDA_PRODUCT_EVENT = "nvda_product_event"
    NVDA_SHAREHOLDER_EVENT = "nvda_shareholder_event"
    NVDA_SUPPLY_CHAIN_UPDATE = "nvda_supply_chain_update"
    NVDA_REGULATORY_FILING = "nvda_regulatory_filing"


class PeerEventSubclass(StrEnum):
    """Bounded peer events used as contextual, not identity-defining, inputs."""

    MEGA_CAP_AI_EARNINGS = "mega_cap_ai_earnings"
    SEMICONDUCTOR_PEER_EARNINGS = "semiconductor_peer_earnings"
    PEER_GUIDANCE_RESET = "peer_guidance_reset"
    PEER_PRODUCT_EVENT = "peer_product_event"
    PEER_SUPPLY_CHAIN_WARNING = "peer_supply_chain_warning"


class MacroEventSubclass(StrEnum):
    """Bounded macro and data-release classes relevant to the NVDA desk."""

    CPI = "cpi"
    PPI = "ppi"
    NONFARM_PAYROLLS = "nonfarm_payrolls"
    RETAIL_SALES = "retail_sales"
    GDP = "gdp"
    ISM = "ism"
    JOBLESS_CLAIMS = "jobless_claims"
    TREASURY_AUCTION = "treasury_auction"


class PolicyEventSubclass(StrEnum):
    """Policy-significant events kept distinct from ordinary macro releases."""

    FOMC_RATE_DECISION = "fomc_rate_decision"
    FOMC_MINUTES = "fomc_minutes"
    FED_CHAIR_SPEECH = "fed_chair_speech"
    FED_SPEAKER_CLUSTER = "fed_speaker_cluster"
    BOJ_RATE_DECISION = "boj_rate_decision"
    PBOC_POLICY_SIGNAL = "pboc_policy_signal"
    US_EXPORT_CONTROL_ACTION = "us_export_control_action"


class ExpiryEventSubclass(StrEnum):
    """Expiry and maturity events that can distort posture lawfully."""

    WEEKLY_OPTIONS_EXPIRY = "weekly_options_expiry"
    MONTHLY_OPTIONS_EXPIRY = "monthly_options_expiry"
    QUARTERLY_EXPIRY = "quarterly_expiry"
    INDEX_OPTION_EXPIRY = "index_option_expiry"
    FUTURES_ROLL = "futures_roll"


class VenueSessionEventSubclass(StrEnum):
    """Venue and session-linked event classes required by later calendar gates."""

    MARKET_HOLIDAY = "market_holiday"
    HALF_DAY = "half_day"
    HOLIDAY_EVE = "holiday_eve"
    SESSION_DISLOCATION = "session_dislocation"
    CLOSING_AUCTION_DISTORTION = "closing_auction_distortion"


class EventTaxonomyRecord(BaseModel):
    """One governed event taxonomy record."""

    model_config = ConfigDict(extra="forbid")

    event_class: DeskEventClass
    subclass: str = Field(min_length=1)
    semantic_phase: EventSemanticPhase
    materiality_tier: EventMaterialityTier
    review_visible: bool = True
    notes: list[str] = Field(default_factory=list)


class EventTaxonomyAuthorityPacket(BaseModel):
    """Frozen Gate 65 authority packet for bounded event identity."""

    model_config = ConfigDict(extra="forbid")

    top_level_classes: list[DeskEventClass] = Field(default_factory=list)
    semantic_phases: list[EventSemanticPhase] = Field(default_factory=list)
    materiality_tiers: list[EventMaterialityTier] = Field(default_factory=list)
    company_subclasses: list[CompanyEventSubclass] = Field(default_factory=list)
    peer_subclasses: list[PeerEventSubclass] = Field(default_factory=list)
    macro_subclasses: list[MacroEventSubclass] = Field(default_factory=list)
    policy_subclasses: list[PolicyEventSubclass] = Field(default_factory=list)
    expiry_subclasses: list[ExpiryEventSubclass] = Field(default_factory=list)
    venue_session_subclasses: list[VenueSessionEventSubclass] = Field(default_factory=list)


class SessionCalendarCreate(BaseModel):
    session_date: date
    venue: str = Field(default="NASDAQ", min_length=1)
    market_open_utc: datetime
    market_close_utc: datetime
    session_label: str = Field(default="regular", min_length=1)
    is_half_day: bool = False


class SessionCalendarPayload(SessionCalendarCreate):
    calendar_id: int


class SessionCalendarListResponse(BaseModel):
    sessions: list[SessionCalendarPayload]


class MarketEventCreate(BaseModel):
    event_ts: datetime
    event_type: str = Field(min_length=1)
    title: str = Field(min_length=1)
    impact_level: ImpactLevel = "medium"
    symbol: str | None = Field(default=None, min_length=1)
    source_document: str = Field(default="manual", min_length=1)
    notes_md: str = ""


class MarketEventPayload(MarketEventCreate):
    event_id: int
    created_at: datetime


class MarketEventListResponse(BaseModel):
    events: list[MarketEventPayload]


class EventProximityResponse(BaseModel):
    requested_at: datetime
    symbol: str | None = None
    event_risk_window_open: bool
    upcoming_events: list[MarketEventPayload]
    recent_events: list[MarketEventPayload]
