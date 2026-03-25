"""Typed bridge from intraday runtime outputs into carry-horizon evaluation."""

from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import (
    ExecutionExpressionOutput,
    OptionsFlowContextOutput,
    PostureRiskOutput,
    TemporalContextOutput,
)
from nvda_desk.schemas.overnight import CarryAction, CarryHorizon, CloseStateCarryHandoff


class CarryHandoffBuilder:
    """Build the typed close-state packet consumed by carry-horizon services.

    Purpose:
        Keep weekend and event carry logic in a separate branch while still using
        deterministic outputs from the intraday runtime.
    Inputs:
        Symbol, evaluation timestamp, and the upstream stage outputs needed to
        describe the close-state surface.
    Outputs:
        `CloseStateCarryHandoff` with explicit horizon taxonomy and allowed
        carry-action envelope.
    Determinism:
        Uses timestamp and stage outputs only; no live calls or hidden state.
    """

    def __init__(self, settings: Settings | None = None):
        self._settings = settings or Settings()
        self._tz = ZoneInfo(self._settings.market_timezone)

    def build(
        self,
        *,
        symbol: str,
        evaluation_ts: datetime,
        temporal: TemporalContextOutput,
        options_flow: OptionsFlowContextOutput,
        posture: PostureRiskOutput,
        execution: ExecutionExpressionOutput,
    ) -> CloseStateCarryHandoff:
        aware_ts = evaluation_ts.astimezone(self._tz) if evaluation_ts.tzinfo else evaluation_ts.replace(tzinfo=self._tz)
        next_session_open_ts = self._next_session_open(aware_ts)
        weekend_window = (next_session_open_ts.date() - aware_ts.date()).days >= 3
        event_carry_window = temporal.event_window_state in {"event_imminent_window", "event_live_window"}
        horizon = CarryHorizon.WEEKEND if weekend_window else (CarryHorizon.EVENT_CARRY if event_carry_window else CarryHorizon.OVERNIGHT)
        allowed_actions = self._allowed_actions(
            permission_state=posture.permission_state.value,
            horizon=horizon,
            event_carry_window=event_carry_window,
        )
        recommended_action_ceiling = allowed_actions[-1] if allowed_actions else CarryAction.BLOCK_CARRY
        rationale_codes: list[str] = [f"horizon:{horizon.value}"]
        if weekend_window:
            rationale_codes.append("weekend_window")
        if event_carry_window:
            rationale_codes.append("event_carry_window")
        if posture.permission_state.value != "allow":
            rationale_codes.append(f"permission:{posture.permission_state.value}")
        if execution.active_playbook_ids:
            rationale_codes.append("active_intraday_playbook_present")
        return CloseStateCarryHandoff(
            symbol=symbol,
            evaluation_ts=aware_ts,
            horizon=horizon,
            next_session_open_ts=next_session_open_ts,
            weekend_window=weekend_window,
            event_carry_window=event_carry_window,
            close_phase=temporal.session_phase,
            desk_window=temporal.desk_window,
            event_window_state=temporal.event_window_state,
            expiry_cycle_state=temporal.expiry_cycle_state,
            permission_state=posture.permission_state.value,
            fresh_deployable_capital_pct=posture.fresh_deployable_capital_pct,
            overnight_deployable_capital_pct=posture.overnight_deployable_capital_pct,
            dealer_pressure_state=options_flow.dealer_pressure_state,
            pin_risk_state=options_flow.pin_risk_state,
            options_behavior_cluster=options_flow.options_behavior_cluster,
            active_playbook_ids=list(execution.active_playbook_ids),
            recommended_action_ceiling=recommended_action_ceiling,
            allowed_actions=allowed_actions,
            rationale_codes=rationale_codes,
        )

    def _allowed_actions(
        self,
        *,
        permission_state: str,
        horizon: CarryHorizon,
        event_carry_window: bool,
    ) -> list[CarryAction]:
        if permission_state == "block":
            return [CarryAction.BLOCK_CARRY]
        if permission_state == "derisk":
            allowed = [CarryAction.FLATTEN, CarryAction.HOLD_SMALL]
        else:
            allowed = [CarryAction.FLATTEN, CarryAction.HOLD_SMALL, CarryAction.HOLD_BASELINE, CarryAction.ADD_CARRY]
        if horizon is CarryHorizon.WEEKEND and CarryAction.ADD_CARRY in allowed:
            allowed.remove(CarryAction.ADD_CARRY)
            allowed.append(CarryAction.HOLD_BASELINE)
        if event_carry_window and CarryAction.ADD_CARRY in allowed:
            allowed.remove(CarryAction.ADD_CARRY)
        return allowed

    def _next_session_open(self, aware_ts: datetime) -> datetime:
        candidate = aware_ts.replace(hour=self._settings.regular_open_hour, minute=self._settings.regular_open_minute, second=0, microsecond=0)
        if aware_ts < candidate:
            return candidate
        next_day = aware_ts + timedelta(days=1)
        while next_day.weekday() >= 5:
            next_day += timedelta(days=1)
        return next_day.replace(
            hour=self._settings.regular_open_hour,
            minute=self._settings.regular_open_minute,
            second=0,
            microsecond=0,
        )
