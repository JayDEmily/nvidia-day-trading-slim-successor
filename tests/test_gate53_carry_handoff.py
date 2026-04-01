from __future__ import annotations

from datetime import datetime
from typing import Any, cast

from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.schemas.cognition import LifecycleAction
from nvda_desk.schemas.overnight import (
    CarryAction,
    CarryHorizon,
    CarryRecommendation,
    CloseStateCarryHandoff,
    OvernightCarryMarketInput,
)
from nvda_desk.services.carry_handoff import CarryHandoffBuilder
from nvda_desk.services.carry_market import OvernightCarryMarketService
from tests.test_gate48_carry_handoff import (
    _execution_output,
    _inventory_state,
    _options_output,
    _posture_output,
    _temporal_output,
)


class _FakeClassifier:
    def classify(
        self, _ts: datetime
    ) -> object:  # pragma: no cover - fallback path not exercised here
        raise AssertionError("classifier fallback should not be used when handoff is supplied")


class _FakeSnapshot:
    latest_bar = None


class _FakeMarketStateService:
    def get_intraday_bars(self, *, symbol: str, ts: datetime, limit: int) -> object:  # noqa: ARG002
        class _Bars:
            bars: list[object] = []

        return _Bars()

    def get_market_snapshot(self, *, symbol: str, ts: datetime) -> _FakeSnapshot:  # noqa: ARG002
        return _FakeSnapshot()


class _FakeSessionFactory:
    pass


def _market_service() -> OvernightCarryMarketService:
    return OvernightCarryMarketService(
        cast(sessionmaker[Session], _FakeSessionFactory()),
        cast(Any, _FakeClassifier()),
        cast(Any, _FakeMarketStateService()),
    )


def test_carry_handoff_blocks_baseline_when_no_inventory_and_no_active_thesis() -> None:
    handoff = CarryHandoffBuilder().build(
        symbol="NVDA",
        evaluation_ts=datetime.fromisoformat("2026-03-24T15:45:00-04:00"),
        temporal=_temporal_output(ts="2026-03-24T15:45:00-04:00"),
        options_flow=_options_output(),
        posture=_posture_output(),
        inventory=_inventory_state(existing=0.0, overnight=0.0),
        execution=_execution_output([]),
    )

    assert handoff.allowed_actions == [CarryAction.FLATTEN]
    assert handoff.existing_inventory_pct == 0.0
    assert handoff.active_playbook_ids == []


def test_carry_handoff_caps_to_hold_small_when_thesis_invalid() -> None:
    posture = _posture_output().model_copy(update={"thesis_state": "invalid"})
    handoff = CarryHandoffBuilder().build(
        symbol="NVDA",
        evaluation_ts=datetime.fromisoformat("2026-03-24T15:45:00-04:00"),
        temporal=_temporal_output(ts="2026-03-24T15:45:00-04:00"),
        options_flow=_options_output(),
        posture=posture,
        inventory=_inventory_state(existing=15.0, overnight=10.0),
        execution=_execution_output(["pin_reversion"]),
    )

    assert handoff.allowed_actions == [CarryAction.FLATTEN, CarryAction.HOLD_SMALL]
    assert handoff.recommended_action_ceiling is CarryAction.HOLD_SMALL
    assert "thesis_state:invalid" in handoff.rationale_codes


def test_market_service_downgrades_add_carry_when_handoff_blocks_it() -> None:
    service = _market_service()
    handoff = CloseStateCarryHandoff(
        symbol="NVDA",
        evaluation_ts=datetime.fromisoformat("2026-03-24T15:45:00-04:00"),
        horizon=CarryHorizon.OVERNIGHT,
        next_session_open_ts=datetime.fromisoformat("2026-03-25T09:30:00-04:00"),
        weekend_window=False,
        event_carry_window=False,
        close_phase=SessionClockPhase.DEALER_UNWIND_CLOSE,
        desk_window="close",
        event_window_state="clear_window",
        expiry_cycle_state="monthly_expiry_week",
        permission_state="allow",
        fresh_deployable_capital_pct=40.0,
        overnight_deployable_capital_pct=10.0,
        existing_inventory_pct=15.0,
        overnight_inventory_pct=5.0,
        open_orders_count=0,
        inventory_action_bias="hold",
        thesis_state="valid",
        dealer_pressure_state="dealer_balancing",
        pin_risk_state="pin_risk_present",
        options_behavior_cluster="pin_reversion_ready",
        active_family_ids=["pin_behaviour"],
        active_setup_variant_ids=["late_session_pin_reversion"],
        active_playbook_ids=["pin_reversion"],
        lifecycle_setup_variant_id="opening_drive_continuation",
        lifecycle_execution_expression_id="continuation_ladder_exec",
        lifecycle_state="carry_nomination_ready",
        lifecycle_next_action=LifecycleAction.HOLD_SMALL_OVERNIGHT,
        lifecycle_carry_candidate=True,
        lifecycle_action_ceiling=CarryAction.HOLD_SMALL,
        lifecycle_fired_rules=["late_session_carry_nomination"],
        lifecycle_blocked_rules=[],
        lifecycle_rationale_codes=["gate_138_test"],
        recommended_action_ceiling=CarryAction.HOLD_SMALL,
        allowed_actions=[CarryAction.FLATTEN, CarryAction.HOLD_SMALL],
        rationale_codes=["test"],
    )
    result = service.evaluate_from_market(
        OvernightCarryMarketInput(
            symbol="NVDA",
            evaluation_ts=datetime.fromisoformat("2026-03-24T15:45:00-04:00"),
            asia_precursor_composite=0.35,
            risk_budget_remaining_pct=30.0,
            gross_exposure_pct=10.0,
            open_orders_count=0,
            close_state_handoff=handoff,
        )
    )

    assert result.carry_recommendation is CarryRecommendation.HOLD_SMALL
    assert result.carry_action is CarryAction.HOLD_SMALL
    assert "handoff:downgraded_from:add_carry" in result.rationale_codes
    assert "handoff:lifecycle_ceiling:hold_small" in result.rationale_codes
