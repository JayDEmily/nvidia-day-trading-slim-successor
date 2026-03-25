from __future__ import annotations

import json
from datetime import UTC
from typing import cast

from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.orm import Session, sessionmaker

from nvda_desk.db.models import RiskDecisionLog
from nvda_desk.schemas.risk import (
    RiskAction,
    RiskDecision,
    RiskDecisionListResponse,
    RiskDecisionPayload,
    RiskPolicyInput,
)


class RiskGatewayService:
    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory

    def evaluate(self, payload: RiskPolicyInput) -> RiskDecision:
        reasons: list[str] = []
        action = RiskAction.ALLOW
        confidence_scalar = 1.0

        if payload.session_phase.value in {"closed", "after_hours"}:
            reasons.append("phase_no_trade_window")
            action = RiskAction.BLOCK
        if payload.data_age_seconds > 300:
            reasons.append("stale_market_state")
            action = RiskAction.BLOCK
        if payload.gross_exposure_pct >= 95 or payload.risk_budget_remaining_pct <= 5:
            reasons.append("exposure_or_budget_breached")
            action = RiskAction.BLOCK
        if payload.conflict_tags:
            reasons.append("module_conflict_present")
            action = RiskAction.BLOCK

        volatility_hot = (
            payload.vix_level >= payload.vix_hot_threshold
            or payload.vvix_level >= 115
            or payload.vix_change_pct_15m >= 18
            or payload.vvix_change_pct_15m >= 22
        )
        volatility_caution = (
            payload.vix_level >= payload.vix_caution_threshold
            or payload.vvix_level >= 95
            or payload.vix_change_pct_15m >= 8
            or payload.vvix_change_pct_15m >= 12
        )

        if volatility_hot:
            reasons.append("volatility_shock_block")
            action = RiskAction.BLOCK
        elif volatility_caution and action is RiskAction.ALLOW:
            reasons.append("volatility_caution_derisk")
            action = RiskAction.DERISK

        if payload.open_orders_count > 12 and action is RiskAction.ALLOW:
            reasons.append("order_pressure_derisk")
            action = RiskAction.DERISK

        if action is RiskAction.BLOCK:
            confidence_scalar = 0.0
        elif action is RiskAction.DERISK:
            confidence_scalar = 0.65
        if not reasons:
            reasons.append("risk_gateway_clear")

        return RiskDecision(
            action=action,
            reasons=reasons,
            confidence_scalar=confidence_scalar,
            vix_level=payload.vix_level,
            vvix_level=payload.vvix_level,
            vix_change_pct_15m=payload.vix_change_pct_15m,
            vvix_change_pct_15m=payload.vvix_change_pct_15m,
        )

    def record(self, payload: RiskPolicyInput) -> RiskDecisionPayload:
        decision = self.evaluate(payload)
        with self._session_factory() as session:
            row = RiskDecisionLog(
                symbol=payload.symbol,
                module_id=payload.module_id,
                action=decision.action.value,
                requested_at=payload.requested_at.astimezone(UTC)
                if payload.requested_at.tzinfo
                else payload.requested_at.replace(tzinfo=UTC),
                input_json=self._dump_model(payload),
                output_json=self._dump_model(decision),
            )
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._to_payload(row)

    def list_decisions(self, module_id: str | None = None, limit: int = 20) -> RiskDecisionListResponse:
        with self._session_factory() as session:
            stmt = select(RiskDecisionLog)
            if module_id:
                stmt = stmt.where(RiskDecisionLog.module_id == module_id)
            stmt = stmt.order_by(desc(RiskDecisionLog.created_at)).limit(limit)
            rows = list(session.scalars(stmt))
        return RiskDecisionListResponse(decisions=[self._to_payload(row) for row in rows])

    def _dump_model(self, model: BaseModel) -> str:
        return json.dumps(model.model_dump(mode="json"))

    def _to_payload(self, row: RiskDecisionLog) -> RiskDecisionPayload:
        output_payload = dict(json.loads(row.output_json))
        return RiskDecisionPayload(
            decision_id=row.id,
            created_at=row.created_at,
            symbol=row.symbol,
            module_id=row.module_id,
            requested_at=row.requested_at,
            action=cast(RiskAction, row.action),
            reasons=list(output_payload.get("reasons", [])),
            confidence_scalar=float(output_payload.get("confidence_scalar", 0.0)),
            input_payload=dict(json.loads(row.input_json)),
            output_payload=output_payload,
        )
