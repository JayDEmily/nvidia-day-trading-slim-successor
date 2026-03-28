"""Expression and execution service for the Desk Cognition Grammar.

This service converts posture and native playbook hierarchy outputs into
execution shape, sizing, hedge requirements, and exit-plan scaffolding.
"""

from __future__ import annotations

from nvda_desk.schemas.cognition import (
    ExecutionExpressionInput,
    ExecutionExpressionOutput,
    PlaybookDecision,
)
from nvda_desk.schemas.playbook_registry import ExecutionTemplateSpec
from nvda_desk.services.playbook_registry import PlaybookRegistryService


class ExecutionExpressionService:
    """Derive deterministic expression and execution outputs.

    Purpose:
        Turn posture and hierarchy-native playbook eligibility into concrete
        execution shape and sizing.
    Inputs:
        `ExecutionExpressionInput` with posture, playbook eligibility, and options context.
    Outputs:
        `ExecutionExpressionOutput` describing entry style, family/setup lineage,
        laddering, invalidation reasons, exits, and hedge need.
    Determinism:
        Uses checked-in registry order and execution templates with no hidden fallbacks.
    """

    def __init__(self, registry_service: PlaybookRegistryService | None = None):
        self._registry = registry_service or PlaybookRegistryService()

    def evaluate(self, payload: ExecutionExpressionInput) -> ExecutionExpressionOutput:
        """Create deterministic expression and execution state for one snapshot."""

        candidates = {
            candidate.playbook_id: candidate for candidate in payload.eligibility.candidates
        }
        ordered_playbook_ids = self._registry.active_playbook_ids()
        active_playbook_ids = [
            playbook_id
            for playbook_id in ordered_playbook_ids
            if playbook_id in candidates
            and candidates[playbook_id].decision is PlaybookDecision.ELIGIBLE
        ]
        watch_playbook_ids = [
            playbook_id
            for playbook_id in ordered_playbook_ids
            if playbook_id in candidates
            and candidates[playbook_id].decision is PlaybookDecision.WATCH_ONLY
        ]
        active_setup_variant_ids = list(payload.eligibility.active_setup_variant_ids)
        active_family_ids = list(payload.eligibility.active_family_ids)
        lead_playbook_id = active_playbook_ids[0] if active_playbook_ids else None
        lead_setup_variant_id = active_setup_variant_ids[0] if active_setup_variant_ids else None
        lead_family_id = active_family_ids[0] if active_family_ids else None
        reasons: list[str] = []
        invalidation_reasons: list[str] = []
        exit_reasons: list[str] = []
        playbook_execution_styles: dict[str, str] = {}
        setup_variant_execution_styles: dict[str, str] = {}

        if payload.posture.permission_state.value == "block":
            reasons.append("execution_blocked_by_permission")
            return ExecutionExpressionOutput(
                active_playbook_ids=[],
                active_setup_variant_ids=[],
                active_family_ids=[],
                lead_playbook_id=None,
                lead_setup_variant_id=None,
                lead_family_id=None,
                entry_style="no_trade",
                playbook_execution_styles={},
                setup_variant_execution_styles={},
                hedge_required=False,
                inventory_action="reduce",
                fresh_capital_action="reduce",
                thesis_invalidation_state="defer_to_risk_gate",
                target_fresh_deployable_pct=0.0,
                scaling_plan=[],
                invalidation_reasons=["risk_gate_blocked_execution"],
                exit_reasons=["stand_aside_until_permission_clears"],
                exit_plan=["stand_aside_until_permission_clears"],
                reasons=reasons,
            )

        hedge_required = (
            bool(payload.eligibility.hedge_candidates)
            or payload.options_flow.gamma_state.value == "destabilising"
        )

        if active_setup_variant_ids:
            assert lead_setup_variant_id is not None  # runtime guarantee from list truthiness
            template = self._registry.template(
                self._registry.setup_variant(lead_setup_variant_id).execution_expression_id
            )
            entry_style = template.entry_style
            playbook_execution_styles = {
                playbook_id: self._registry.template_for_playbook(playbook_id).entry_style
                for playbook_id in active_playbook_ids
            }
            setup_variant_execution_styles = {
                setup_variant_id: self._registry.template(
                    self._registry.setup_variant(setup_variant_id).execution_expression_id
                ).entry_style
                for setup_variant_id in active_setup_variant_ids
            }
            target = payload.posture.fresh_deployable_capital_pct
            scaling_plan = [round(target * factor, 4) for factor in template.scaling_step_factors]
            thesis_invalidation_state = template.thesis_invalidation_state
            invalidation_reasons = self._invalidation_reasons(template, payload)
            exit_reasons = self._exit_reasons(template, payload)
            exit_plan = list(exit_reasons)
            inventory_action = self._inventory_action(payload, template)
            fresh_capital_action = template.default_fresh_capital_action
            reasons.extend(f"active_family:{family_id}" for family_id in active_family_ids)
            reasons.extend(
                f"active_setup_variant:{setup_variant_id}"
                for setup_variant_id in active_setup_variant_ids
            )
            if lead_playbook_id is not None:
                reasons.append(f"lead_playbook:{lead_playbook_id}")
        elif watch_playbook_ids:
            lead_watch = watch_playbook_ids[0]
            template = self._registry.template_for_playbook(lead_watch)
            entry_style = "watch_only"
            playbook_execution_styles = {
                playbook_id: self._registry.template_for_playbook(playbook_id).watch_execution_style
                for playbook_id in watch_playbook_ids
            }
            setup_variant_execution_styles = {
                setup_variant_id: self._registry.template(
                    self._registry.setup_variant(setup_variant_id).execution_expression_id
                ).watch_execution_style
                for setup_variant_id in payload.eligibility.watch_setup_variant_ids
            }
            target = 0.0
            scaling_plan = []
            thesis_invalidation_state = "not_confirmed"
            invalidation_reasons = ["setup_needs_confirmation"]
            exit_reasons = ["remain_observational"]
            exit_plan = list(exit_reasons)
            inventory_action = "hold"
            fresh_capital_action = "hold"
            reasons.append(f"watch_only_playbook:{lead_watch}")
        else:
            entry_style = "stand_aside"
            template = None
            target = 0.0
            scaling_plan = []
            thesis_invalidation_state = "no_valid_playbook"
            invalidation_reasons = payload.eligibility.no_trade_reasons or ["no_playbook_qualified"]
            exit_reasons = ["stand_aside"]
            exit_plan = list(exit_reasons)
            inventory_action = payload.posture.inventory_action_bias
            fresh_capital_action = "hold"
            reasons.append("no_active_setup_variant")

        if hedge_required:
            reasons.append("hedge_required")
            hedge_exit_reason = (
                template.hedge_exit_reason
                if template is not None
                else "overlay_hedge_if_gamma_reaccelerates"
            )
            if hedge_exit_reason not in exit_reasons:
                exit_reasons.append(hedge_exit_reason)

        return ExecutionExpressionOutput(
            active_playbook_ids=active_playbook_ids,
            active_setup_variant_ids=active_setup_variant_ids,
            active_family_ids=active_family_ids,
            lead_playbook_id=lead_playbook_id,
            lead_setup_variant_id=lead_setup_variant_id,
            lead_family_id=lead_family_id,
            entry_style=entry_style,
            playbook_execution_styles=playbook_execution_styles,
            setup_variant_execution_styles=setup_variant_execution_styles,
            hedge_required=hedge_required,
            inventory_action=inventory_action,
            fresh_capital_action=fresh_capital_action,
            thesis_invalidation_state=thesis_invalidation_state,
            target_fresh_deployable_pct=round(target, 4),
            scaling_plan=scaling_plan,
            invalidation_reasons=invalidation_reasons,
            exit_reasons=exit_reasons,
            exit_plan=exit_plan,
            reasons=reasons,
        )

    def _invalidation_reasons(
        self, template: ExecutionTemplateSpec, payload: ExecutionExpressionInput
    ) -> list[str]:
        reasons = list(template.invalidation_reasons)
        if payload.posture.time_stop_state == "time_stop_near":
            reasons.append("time_stop_near")
        return reasons

    def _exit_reasons(
        self, template: ExecutionTemplateSpec, payload: ExecutionExpressionInput
    ) -> list[str]:
        reasons = list(template.exit_reasons)
        if payload.posture.inventory_posture_state in set(template.inventory_pressure_states):
            reasons.append(template.inventory_pressure_exit_reason)
        return reasons

    def _inventory_action(
        self, payload: ExecutionExpressionInput, template: ExecutionTemplateSpec
    ) -> str:
        if template.respect_posture_biases and payload.posture.inventory_action_bias in set(
            template.posture_override_actions
        ):
            return payload.posture.inventory_action_bias
        return template.default_inventory_action
