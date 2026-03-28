"""Gate 66 desk-calendar and venue-contract integrity checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.config import DeskCalendarAuthorityResponse
from nvda_desk.schemas.events import (
    CalendarAwareEventContract,
    ExpiryCalendarInteraction,
    VenueSessionEventSubclass,
)
from nvda_desk.schemas.session_clock import (
    CalendarClosureClass,
    DeskCalendarAuthorityPacket,
    SessionBridgeRule,
    SessionTemplate,
    TradingVenue,
    VenueSessionContract,
    VenueTimezone,
)
from scripts.build_canonical_vocabulary import build_document
from tests._successor_pack_helpers import successor_pack_position

REPO_ROOT = Path(__file__).resolve().parents[1]
GATES = REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_GATES_v6.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v6.json"
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
OPERATING_MODEL = REPO_ROOT / "docs/02_OPERATING_MODEL.md"
DOMAIN_MODEL = REPO_ROOT / "docs/03_DOMAIN_MODEL.md"
GUARDRAILS = REPO_ROOT / "docs/05_GUARDRAILS.md"
VOCAB_PATH = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"


def test_gate66_status_closeout_and_leaf_progress_are_recorded() -> None:
    gates_text = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert (
        "## Gate 66 — Session, holiday, and venue-calendar contracts\n\nStatus: complete on `main`"
        in gates_text
    )
    assert "### Gate 66 closeout note" in gates_text
    assert leaves["completed_gate_ids"][:8] == [
        "Gate 59",
        "Gate 60",
        "Gate 61",
        "Gate 62",
        "Gate 63",
        "Gate 64",
        "Gate 65",
        "Gate 66",
    ]
    assert successor_pack_position(leaves["active_gate"]) >= 67

    gate66 = [leaf for leaf in leaves["leaves"] if leaf["gate"] == "Gate 66"]
    assert len(gate66) == 5
    assert all(leaf["status"] == "complete" for leaf in gate66)


def test_gate66_docs_freeze_venue_timezone_and_bridge_law() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    guardrails = GUARDRAILS.read_text(encoding="utf-8")

    assert "## Desk-calendar and venue law" in normative
    assert (
        "the canonical venue set for this tranche is US Nasdaq cash, JPX cash, HKEX cash, SSE/SZSE cash, and CFFEX index futures"
        in normative
    )
    assert (
        "US early-close and half-day semantics, HK holiday-eve half-day semantics, Japan split-session semantics, and Mainland China bridge/make-up-day semantics"
        in normative
    )

    assert "## Gate 66 desk-calendar authority" in operating_model
    assert (
        "venue contracts carry timezone authority, session template, closure classes, and bridge rules"
        in operating_model
    )

    assert "### 4g. Desk-calendar and venue objects" in domain_model
    assert (
        "**Venue calendar truth must come from explicit venue contracts, not one generic market-open flag.**"
        in guardrails
    )


def test_gate66_schema_surface_matches_frozen_calendar_authority() -> None:
    assert [item.value for item in TradingVenue] == [
        "nasdaq_us",
        "jpx_cash",
        "hkex_cash",
        "sse_cash",
        "szse_cash",
        "cffex_index_futures",
    ]
    assert [item.value for item in VenueTimezone] == [
        "America/New_York",
        "Asia/Tokyo",
        "Asia/Hong_Kong",
        "Asia/Shanghai",
    ]
    assert [item.value for item in SessionTemplate] == [
        "us_equity_continuous",
        "jpx_split_session",
        "hkex_split_session_with_cas",
        "mainland_china_split_session",
        "index_futures_split_session",
    ]
    assert [item.value for item in CalendarClosureClass] == [
        "weekend",
        "full_holiday",
        "half_day",
        "holiday_eve_half_day",
        "bridge_holiday",
        "makeup_working_day",
        "observed_holiday",
    ]

    nasdaq = VenueSessionContract(
        venue=TradingVenue.NASDAQ_US,
        timezone=VenueTimezone.AMERICA_NEW_YORK,
        template=SessionTemplate.US_EQUITY_CONTINUOUS,
        trading_days=["monday", "tuesday", "wednesday", "thursday", "friday"],
        session_segments=["pre_market", "regular_session", "after_hours"],
        closure_classes=[
            CalendarClosureClass.WEEKEND,
            CalendarClosureClass.FULL_HOLIDAY,
            CalendarClosureClass.OBSERVED_HOLIDAY,
            CalendarClosureClass.HALF_DAY,
        ],
        bridge_rules=[SessionBridgeRule.US_EARLY_CLOSE],
        notes=[
            "Nasdaq cash follows US full holidays and 1:00pm ET early closes on designated dates."
        ],
    )
    jpx = VenueSessionContract(
        venue=TradingVenue.JPX_CASH,
        timezone=VenueTimezone.ASIA_TOKYO,
        template=SessionTemplate.JPX_SPLIT_SESSION,
        trading_days=["monday", "tuesday", "wednesday", "thursday", "friday"],
        session_segments=["morning_session", "lunch_break", "afternoon_session"],
        closure_classes=[
            CalendarClosureClass.WEEKEND,
            CalendarClosureClass.FULL_HOLIDAY,
        ],
        bridge_rules=[SessionBridgeRule.PRECURSOR_NEXT_US_SESSION_ONLY],
        notes=[
            "JPX cash is split 09:00-11:30 and 12:30-15:30 JST with exchange holidays including Jan 1-3 and Dec 31."
        ],
    )
    hkex = VenueSessionContract(
        venue=TradingVenue.HKEX_CASH,
        timezone=VenueTimezone.ASIA_HONG_KONG,
        template=SessionTemplate.HKEX_SPLIT_SESSION_WITH_CAS,
        trading_days=["monday", "tuesday", "wednesday", "thursday", "friday"],
        session_segments=[
            "pre_open",
            "morning_session",
            "extended_morning_session",
            "afternoon_session",
            "closing_auction",
        ],
        closure_classes=[
            CalendarClosureClass.WEEKEND,
            CalendarClosureClass.FULL_HOLIDAY,
            CalendarClosureClass.HOLIDAY_EVE_HALF_DAY,
        ],
        bridge_rules=[
            SessionBridgeRule.HK_HOLIDAY_EVE_HALF_DAY,
            SessionBridgeRule.PRECURSOR_NEXT_US_SESSION_ONLY,
        ],
        notes=["HKEX runs half days on the eves of Christmas, New Year, and Lunar New Year."],
    )
    china = VenueSessionContract(
        venue=TradingVenue.SSE_CASH,
        timezone=VenueTimezone.ASIA_SHANGHAI,
        template=SessionTemplate.MAINLAND_CHINA_SPLIT_SESSION,
        trading_days=["monday", "tuesday", "wednesday", "thursday", "friday"],
        session_segments=[
            "opening_call_auction",
            "morning_session",
            "lunch_break",
            "afternoon_session",
            "closing_call_auction",
        ],
        closure_classes=[
            CalendarClosureClass.WEEKEND,
            CalendarClosureClass.FULL_HOLIDAY,
            CalendarClosureClass.BRIDGE_HOLIDAY,
            CalendarClosureClass.MAKEUP_WORKING_DAY,
        ],
        bridge_rules=[
            SessionBridgeRule.CHINA_WEEKEND_MAKEUP_WORKDAY,
            SessionBridgeRule.PRECURSOR_NEXT_US_SESSION_ONLY,
        ],
        notes=[
            "Mainland exchanges use explicit holiday calendars with occasional weekend make-up working days and no ordinary cash-market half days."
        ],
    )
    authority = DeskCalendarAuthorityResponse(
        authority=DeskCalendarAuthorityPacket(
            venues=[nasdaq, jpx, hkex, china],
            closure_classes=list(CalendarClosureClass),
            bridge_rules=list(SessionBridgeRule),
            expiry_interaction_notes=[
                "Expiry on a shortened session must stay explicit rather than inferred by downstream policy."
            ],
        )
    )
    interaction = CalendarAwareEventContract(
        venue_event_subclass=VenueSessionEventSubclass.HALF_DAY,
        expiry_calendar_interaction=ExpiryCalendarInteraction.EARLY_CLOSE_EXPIRY,
        notes=[
            "Friday monthly expiry on a US early close is materially different from a normal full session."
        ],
    )

    assert authority.authority.venues[0].bridge_rules == [SessionBridgeRule.US_EARLY_CLOSE]
    assert interaction.expiry_calendar_interaction is ExpiryCalendarInteraction.EARLY_CLOSE_EXPIRY


def test_gate66_vocabulary_terms_are_present_and_generated() -> None:
    generated = build_document().entry_index()
    committed = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    committed_slugs = {entry["canonical_slug"] for entry in committed["entries"]}

    assert "desk_calendar_contract" in generated
    assert (
        generated["desk_calendar_contract"].maps_to_contract
        == "nvda_desk.schemas.session_clock.DeskCalendarAuthorityPacket"
    )
    assert "desk_calendar_contract" in committed_slugs
