"""Downstream capital-deployment authority service.

Purpose:
    Decide whether an already-formed opening candidate deserves fresh capital
    now, and if so how much notional is authorised.
Inputs:
    `CapitalDeploymentAuthorityInput` carrying posture, eligibility,
    execution, preserved handoff/risk carriage, and the current capital
    snapshot.
Outputs:
    `CapitalDeploymentAuthorityDecision` with a bounded deploy-or-stand-down
    action, authorised percentage, authorised notional, and rationale codes.
Determinism:
    Uses fixed precedence rules over existing runtime surfaces; it does not
    recalculate upstream cognition or introduce recommendation memory.
"""

from __future__ import annotations

from nvda_desk.schemas.cognition import (
    CapitalDeploymentAuthorityAction,
    CapitalDeploymentAuthorityDecision,
    CapitalDeploymentAuthorityInput,
)
from nvda_desk.schemas.parallel_risk import ParallelRiskLanePacket
from nvda_desk.schemas.risk import RiskAction


class CapitalDeploymentAuthorityService:
    """Authorise bounded fresh-capital deployment from existing runtime truth."""

    _NON_DEPLOY_ACTIONS = {"hold", "reduce", "block"}

    def evaluate(
        self,
        payload: CapitalDeploymentAuthorityInput,
    ) -> CapitalDeploymentAuthorityDecision:
        """Return the bounded fresh-capital authority decision for one runtime pass."""

        buying_power = round(max(0.0, payload.capital_state.buying_power), 4)
        opportunity_target_pct = round(max(0.0, min(100.0, payload.execution.target_fresh_deployable_pct)), 4)
        posture_cap_pct = round(max(0.0, min(100.0, payload.posture.fresh_deployable_capital_pct)), 4)
        terminal_risk_action, notes = self._terminal_risk_action(payload)
        weather_state = self._weather_state(payload.parallel_risk_lane_packet)
        consequence_class = self._consequence_class(payload.parallel_risk_lane_packet)

        rationale_codes = [
            f"lead_playbook:{payload.execution.lead_playbook_id or 'none'}",
            f"fresh_capital_action:{payload.execution.fresh_capital_action}",
            f"posture_permission:{payload.posture.permission_state.value}",
            f"terminal_risk:{terminal_risk_action.value if terminal_risk_action is not None else 'unknown'}",
            f"buying_power:{buying_power:.4f}",
            f"opportunity_target_pct:{opportunity_target_pct:.4f}",
            f"posture_cap_pct:{posture_cap_pct:.4f}",
        ]
        if weather_state is not None:
            rationale_codes.append(f"weather_state:{weather_state}")
        if consequence_class is not None:
            rationale_codes.append(f"consequence_class:{consequence_class}")

        if payload.execution.lead_playbook_id is None:
            return self._stand_down(
                payload=payload,
                buying_power=buying_power,
                opportunity_target_pct=opportunity_target_pct,
                posture_cap_pct=posture_cap_pct,
                terminal_risk_action=terminal_risk_action,
                weather_state=weather_state,
                consequence_class=consequence_class,
                rationale_codes=[*rationale_codes, "stand_down:no_lead_playbook"],
                notes=notes,
            )

        if payload.execution.fresh_capital_action in self._NON_DEPLOY_ACTIONS:
            return self._stand_down(
                payload=payload,
                buying_power=buying_power,
                opportunity_target_pct=opportunity_target_pct,
                posture_cap_pct=posture_cap_pct,
                terminal_risk_action=terminal_risk_action,
                weather_state=weather_state,
                consequence_class=consequence_class,
                rationale_codes=[*rationale_codes, "stand_down:non_deploy_capital_action"],
                notes=notes,
            )

        if terminal_risk_action is RiskAction.BLOCK:
            return self._stand_down(
                payload=payload,
                buying_power=buying_power,
                opportunity_target_pct=opportunity_target_pct,
                posture_cap_pct=posture_cap_pct,
                terminal_risk_action=terminal_risk_action,
                weather_state=weather_state,
                consequence_class=consequence_class,
                rationale_codes=[*rationale_codes, "stand_down:terminal_block"],
                notes=notes,
            )

        if buying_power <= 0.0:
            return self._stand_down(
                payload=payload,
                buying_power=buying_power,
                opportunity_target_pct=opportunity_target_pct,
                posture_cap_pct=posture_cap_pct,
                terminal_risk_action=terminal_risk_action,
                weather_state=weather_state,
                consequence_class=consequence_class,
                rationale_codes=[*rationale_codes, "stand_down:no_buying_power"],
                notes=notes,
            )

        authorised_pct = round(min(opportunity_target_pct, posture_cap_pct), 4)
        authorised_notional_usd = round(buying_power * (authorised_pct / 100.0), 4)
        if authorised_pct <= 0.0 or authorised_notional_usd <= 0.0:
            return self._stand_down(
                payload=payload,
                buying_power=buying_power,
                opportunity_target_pct=opportunity_target_pct,
                posture_cap_pct=posture_cap_pct,
                terminal_risk_action=terminal_risk_action,
                weather_state=weather_state,
                consequence_class=consequence_class,
                rationale_codes=[*rationale_codes, "stand_down:no_authorised_capacity"],
                notes=notes,
            )

        return CapitalDeploymentAuthorityDecision(
            deployment_action=CapitalDeploymentAuthorityAction.DEPLOY,
            lead_playbook_id=payload.execution.lead_playbook_id,
            opportunity_target_pct=opportunity_target_pct,
            posture_cap_pct=posture_cap_pct,
            authorised_deployable_pct=authorised_pct,
            authorised_notional_usd=authorised_notional_usd,
            available_buying_power_usd=buying_power,
            capital_source=payload.capital_state.source,
            terminal_risk_action=terminal_risk_action,
            environmental_weather_state=weather_state,
            consequence_class=consequence_class,
            rationale_codes=[*rationale_codes, "deploy:bounded_fresh_capital_authorised"],
            notes=notes,
        )

    def _stand_down(
        self,
        *,
        payload: CapitalDeploymentAuthorityInput,
        buying_power: float,
        opportunity_target_pct: float,
        posture_cap_pct: float,
        terminal_risk_action: RiskAction | None,
        weather_state: str | None,
        consequence_class: str | None,
        rationale_codes: list[str],
        notes: list[str],
    ) -> CapitalDeploymentAuthorityDecision:
        return CapitalDeploymentAuthorityDecision(
            deployment_action=CapitalDeploymentAuthorityAction.STAND_DOWN,
            lead_playbook_id=payload.execution.lead_playbook_id,
            opportunity_target_pct=opportunity_target_pct,
            posture_cap_pct=posture_cap_pct,
            authorised_deployable_pct=0.0,
            authorised_notional_usd=0.0,
            available_buying_power_usd=buying_power,
            capital_source=payload.capital_state.source,
            terminal_risk_action=terminal_risk_action,
            environmental_weather_state=weather_state,
            consequence_class=consequence_class,
            rationale_codes=rationale_codes,
            notes=notes,
        )

    def _terminal_risk_action(
        self,
        payload: CapitalDeploymentAuthorityInput,
    ) -> tuple[RiskAction | None, list[str]]:
        if (
            payload.stage_local_handoff is not None
            and payload.stage_local_handoff.terminal_risk_application is not None
        ):
            return payload.stage_local_handoff.terminal_risk_application.final_decision.action, []
        if payload.execution.final_risk_join is not None:
            return payload.execution.final_risk_join.action, [
                "compatibility_fallback:final_risk_join_used_without_stage_local_handoff"
            ]
        return None, ["terminal_risk_action_unknown"]

    def _weather_state(self, packet: ParallelRiskLanePacket | None) -> str | None:
        if packet is None or packet.market_translation_surface is None:
            return None
        return packet.market_translation_surface.environmental_weather_state.value

    def _consequence_class(self, packet: ParallelRiskLanePacket | None) -> str | None:
        if packet is None or packet.candidate_audit_surface is None:
            return None
        if packet.candidate_audit_surface.consequence_class is None:
            return None
        return packet.candidate_audit_surface.consequence_class.value
