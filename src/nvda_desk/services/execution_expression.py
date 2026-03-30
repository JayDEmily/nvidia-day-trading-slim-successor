"""Expression and execution service for the Desk Cognition Grammar.

This service converts posture and native playbook hierarchy outputs into
execution shape, sizing, hedge requirements, and exit-plan scaffolding.
"""

from __future__ import annotations

from nvda_desk.schemas.cognition import (
    CandidateAdjudicationRecord,
    ExecutionExpressionInput,
    ExecutionExpressionOutput,
    PlaybookCandidate,
    PlaybookDecision,
)
from nvda_desk.schemas.state_policy import MutableRuntimeSurface
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


    _SURFACE_DEFAULTS: dict[MutableRuntimeSurface, float | bool] = {
        MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR: 0.65,
        MutableRuntimeSurface.ZONE_SCORE_THRESHOLD: 0.50,
        MutableRuntimeSurface.DISTANCE_TO_VWAP_SOFT_LIMIT_PCT: 1.50,
        MutableRuntimeSurface.RISK_VIX_CAUTION_THRESHOLD: 24.0,
        MutableRuntimeSurface.RISK_VIX_HOT_THRESHOLD: 32.0,
        MutableRuntimeSurface.MAX_RISK_PER_TRADE: 0.35,
        MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT: 55.0,
        MutableRuntimeSurface.HEDGE_REQUIRED: False,
    }

    def evaluate(self, payload: ExecutionExpressionInput) -> ExecutionExpressionOutput:
        """Create deterministic expression and execution state for one snapshot."""

        candidate_index = {
            candidate.playbook_id: candidate for candidate in payload.eligibility.candidates
        }
        operative_surfaces = self._operative_surfaces(payload.modifier_runtime_packet)
        ordered_playbook_ids = self._registry.active_playbook_ids()
        registry_priority = {playbook_id: index + 1 for index, playbook_id in enumerate(ordered_playbook_ids)}
        eligible_candidates = [
            candidate_index[playbook_id]
            for playbook_id in ordered_playbook_ids
            if playbook_id in candidate_index
            and candidate_index[playbook_id].decision is PlaybookDecision.ELIGIBLE
        ]
        watch_playbook_ids = [
            playbook_id
            for playbook_id in ordered_playbook_ids
            if playbook_id in candidate_index
            and candidate_index[playbook_id].decision is PlaybookDecision.WATCH_ONLY
        ]
        adjudication = self._adjudicate_candidates(
            eligible_candidates=eligible_candidates,
            registry_priority=registry_priority,
            payload=payload,
        )
        active_playbook_ids = [entry.playbook_id for entry in adjudication]
        active_setup_variant_ids = self._ordered_unique(
            [entry.setup_variant_id for entry in adjudication if entry.setup_variant_id]
            + list(payload.eligibility.active_setup_variant_ids)
        )
        active_family_ids = self._ordered_unique(
            [entry.family_id for entry in adjudication if entry.family_id]
            + list(payload.eligibility.active_family_ids)
        )
        lead_playbook_id = active_playbook_ids[0] if active_playbook_ids else None
        lead_candidate = next(
            (candidate for candidate in eligible_candidates if candidate.playbook_id == lead_playbook_id),
            None,
        )
        lead_setup_variant_id = (
            lead_candidate.setup_variant_id if lead_candidate and lead_candidate.setup_variant_id else None
        ) or (active_setup_variant_ids[0] if active_setup_variant_ids else None)
        lead_family_id = (
            lead_candidate.family_id if lead_candidate and lead_candidate.family_id else None
        ) or (active_family_ids[0] if active_family_ids else None)
        contradiction_resolution = self._contradiction_resolution(adjudication)
        lead_selection_score = adjudication[0].score if adjudication else None
        lead_selection_reasons = list(adjudication[0].reasons) if adjudication else []
        reasons: list[str] = []
        invalidation_reasons: list[str] = []
        exit_reasons: list[str] = []
        playbook_execution_styles: dict[str, str] = {}
        setup_variant_execution_styles: dict[str, str] = {}
        passive_aggressive_bias = "balanced"
        ladder_spacing_bps = 0.0
        max_chase_distance_bps = 0.0
        stop_distance_bps = 0.0
        take_profit_distance_bps = 0.0
        hedge_ratio = 0.0
        per_slice_risk_pct = 0.0
        geometry_notes: list[str] = []

        if payload.posture.permission_state.value == "block":
            reasons.append("execution_blocked_by_permission")
            return ExecutionExpressionOutput(
                active_playbook_ids=[],
                active_setup_variant_ids=[],
                active_family_ids=[],
                lead_playbook_id=None,
                lead_setup_variant_id=None,
                lead_family_id=None,
                adjudication_method="candidate_score_v1",
                contradiction_resolution=None,
                lead_selection_score=None,
                lead_selection_reasons=[],
                candidate_adjudication=[],
                entry_style="no_trade",
                playbook_execution_styles={},
                setup_variant_execution_styles={},
                entry_gate_score_floor=operative_surfaces["entry_gate_score_floor"],
                zone_score_threshold=operative_surfaces["zone_score_threshold"],
                distance_to_vwap_soft_limit_pct=operative_surfaces["distance_to_vwap_soft_limit_pct"],
                risk_vix_caution_threshold=operative_surfaces["risk_vix_caution_threshold"],
                risk_vix_hot_threshold=operative_surfaces["risk_vix_hot_threshold"],
                max_risk_per_trade=operative_surfaces["max_risk_per_trade"],
                passive_aggressive_bias="passive",
                ladder_spacing_bps=0.0,
                max_chase_distance_bps=0.0,
                stop_distance_bps=0.0,
                take_profit_distance_bps=0.0,
                hedge_ratio=0.0,
                per_slice_risk_pct=0.0,
                geometry_notes=["blocked_before_execution_geometry"],
                hedge_required=bool(operative_surfaces["hedge_required"]),
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

        hedge_required = bool(operative_surfaces["hedge_required"]) or (
            bool(payload.eligibility.hedge_candidates)
            or payload.options_flow.gamma_state.value == "destabilising"
        )

        if active_setup_variant_ids:
            assert lead_setup_variant_id is not None
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
            (
                passive_aggressive_bias,
                ladder_spacing_bps,
                max_chase_distance_bps,
                stop_distance_bps,
                take_profit_distance_bps,
                hedge_ratio,
                per_slice_risk_pct,
                geometry_notes,
            ) = self._execution_geometry(
                template=template,
                payload=payload,
                target=target,
                scaling_plan=scaling_plan,
                operative_surfaces=operative_surfaces,
                hedge_required=hedge_required,
            )
            reasons.extend(f"active_family:{family_id}" for family_id in active_family_ids)
            reasons.extend(
                f"active_setup_variant:{setup_variant_id}"
                for setup_variant_id in active_setup_variant_ids
            )
            if lead_playbook_id is not None:
                reasons.append(f"lead_playbook:{lead_playbook_id}")
            if contradiction_resolution is not None:
                reasons.append(f"adjudication:{contradiction_resolution}")
            if lead_selection_score is not None:
                reasons.append(f"lead_score:{lead_selection_score}")
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
            passive_aggressive_bias = "passive"
            geometry_notes = ["watch_only_no_execution_geometry"]
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
            passive_aggressive_bias = "passive"
            geometry_notes = ["no_active_setup_variant"]
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
            adjudication_method="candidate_score_v1",
            contradiction_resolution=contradiction_resolution,
            lead_selection_score=lead_selection_score,
            lead_selection_reasons=lead_selection_reasons,
            candidate_adjudication=adjudication,
            entry_style=entry_style,
            playbook_execution_styles=playbook_execution_styles,
            setup_variant_execution_styles=setup_variant_execution_styles,
            entry_gate_score_floor=operative_surfaces["entry_gate_score_floor"],
            zone_score_threshold=operative_surfaces["zone_score_threshold"],
            distance_to_vwap_soft_limit_pct=operative_surfaces["distance_to_vwap_soft_limit_pct"],
            risk_vix_caution_threshold=operative_surfaces["risk_vix_caution_threshold"],
            risk_vix_hot_threshold=operative_surfaces["risk_vix_hot_threshold"],
            max_risk_per_trade=operative_surfaces["max_risk_per_trade"],
            passive_aggressive_bias=passive_aggressive_bias,
            ladder_spacing_bps=ladder_spacing_bps,
            max_chase_distance_bps=max_chase_distance_bps,
            stop_distance_bps=stop_distance_bps,
            take_profit_distance_bps=take_profit_distance_bps,
            hedge_ratio=hedge_ratio,
            per_slice_risk_pct=per_slice_risk_pct,
            geometry_notes=geometry_notes,
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


    def _ordered_unique(self, values: list[str]) -> list[str]:
        ordered: list[str] = []
        for value in values:
            if value and value not in ordered:
                ordered.append(value)
        return ordered

    def _contradiction_tags(
        self,
        candidate: PlaybookCandidate,
        payload: ExecutionExpressionInput,
    ) -> list[str]:
        tags: list[str] = []
        if candidate.hedge_overlay and candidate.action_bias.value == "add":
            tags.append("add_requires_hedge_overlay")
        if payload.options_flow.gamma_state.value == "destabilising" and candidate.action_bias.value == "add":
            tags.append("destabilising_gamma_add_candidate")
        if payload.temporal.event_window_state != "clear" and candidate.action_bias.value == "add":
            tags.append("event_window_add_candidate")
        if payload.posture.inventory_action_bias in {"reduce", "trim", "hedge"} and candidate.action_bias.value == "add":
            tags.append("posture_bias_opposes_add")
        return tags

    def _candidate_score(
        self,
        candidate: PlaybookCandidate,
        payload: ExecutionExpressionInput,
    ) -> tuple[float, list[str]]:
        score = round(candidate.sizing_fraction * 100.0, 4)
        reasons = [f"sizing_fraction:{candidate.sizing_fraction}"]
        action_bonus = {
            "add": 20.0,
            "hold": 10.0,
            "trim": 6.0,
            "reduce": 2.0,
            "hedge": 8.0,
        }[candidate.action_bias.value]
        score += action_bonus
        reasons.append(f"action_bias_bonus:{action_bonus}")
        if candidate.hedge_overlay:
            score -= 5.0
            reasons.append("hedge_overlay_penalty:-5.0")
        if payload.regime.breadth_state.value == "supportive" and candidate.action_bias.value == "add":
            score += 4.0
            reasons.append("supportive_breadth_bonus:4.0")
        if payload.regime.sector_leadership_state == "semis_leading" and candidate.action_bias.value == "add":
            score += 3.0
            reasons.append("sector_leadership_bonus:3.0")
        if payload.options_flow.gamma_state.value == "destabilising" and candidate.action_bias.value == "add":
            score -= 8.0
            reasons.append("gamma_penalty:-8.0")
        if payload.temporal.event_window_state != "clear" and candidate.action_bias.value == "add":
            score -= 6.0
            reasons.append("event_window_penalty:-6.0")
        if payload.options_flow.gamma_state.value == "destabilising" and candidate.action_bias.value == "hedge":
            score += 8.0
            reasons.append("gamma_hedge_bonus:8.0")
        if candidate.setup_variant_id in payload.eligibility.active_setup_variant_ids:
            score += 2.0
            reasons.append("active_variant_bonus:2.0")
        return round(score, 4), reasons

    def _adjudicate_candidates(
        self,
        eligible_candidates: list[PlaybookCandidate],
        registry_priority: dict[str, int],
        payload: ExecutionExpressionInput,
    ) -> list[CandidateAdjudicationRecord]:
        adjudication: list[CandidateAdjudicationRecord] = []
        for candidate in eligible_candidates:
            score, reasons = self._candidate_score(candidate, payload)
            contradiction_tags = self._contradiction_tags(candidate, payload)
            adjudication.append(
                CandidateAdjudicationRecord(
                    playbook_id=candidate.playbook_id,
                    family_id=candidate.family_id,
                    setup_variant_id=candidate.setup_variant_id,
                    action_bias=candidate.action_bias,
                    sizing_fraction=candidate.sizing_fraction,
                    score=score,
                    registry_priority=registry_priority.get(candidate.playbook_id, 999),
                    contradiction_tags=contradiction_tags,
                    reasons=reasons,
                )
            )
        adjudication.sort(key=lambda item: (-item.score, item.registry_priority, item.playbook_id))
        return adjudication

    def _contradiction_resolution(
        self,
        adjudication: list[CandidateAdjudicationRecord],
    ) -> str | None:
        if not adjudication:
            return None
        if len(adjudication) == 1:
            return "single_candidate_clear"
        if len(adjudication) >= 2 and adjudication[0].score == adjudication[1].score:
            return "registry_priority_tiebreak"
        family_count = len({item.family_id for item in adjudication if item.family_id is not None})
        action_count = len({item.action_bias.value for item in adjudication})
        if family_count > 1 or action_count > 1 or any(item.contradiction_tags for item in adjudication):
            return "mixed_context_resolved_by_score"
        return "score_ranked_candidate_pool"

    def _execution_geometry(
        self,
        template: ExecutionTemplateSpec,
        payload: ExecutionExpressionInput,
        target: float,
        scaling_plan: list[float],
        operative_surfaces: dict[str, float | bool],
        hedge_required: bool,
    ) -> tuple[str, float, float, float, float, float, float, list[str]]:
        passive_aggressive_bias = template.passive_aggressive_bias
        ladder_spacing_bps = template.ladder_spacing_bps
        max_chase_distance_bps = template.max_chase_distance_bps
        stop_distance_bps = template.stop_distance_bps
        take_profit_distance_bps = template.take_profit_distance_bps
        hedge_ratio = template.hedge_ratio if hedge_required else 0.0
        notes: list[str] = []

        if payload.options_flow.gamma_state.value == "destabilising":
            ladder_spacing_bps = round(ladder_spacing_bps * 1.25, 4)
            max_chase_distance_bps = round(max_chase_distance_bps * 0.7, 4)
            stop_distance_bps = round(stop_distance_bps * 1.1, 4)
            hedge_ratio = max(hedge_ratio, 0.35 if hedge_required else 0.0)
            notes.append("gamma_stress_geometry_tightened")
            if passive_aggressive_bias == "aggressive":
                passive_aggressive_bias = "balanced"

        if payload.temporal.event_window_state != "clear":
            max_chase_distance_bps = round(max_chase_distance_bps * 0.6, 4)
            if passive_aggressive_bias == "balanced":
                passive_aggressive_bias = "passive"
            elif passive_aggressive_bias == "aggressive":
                passive_aggressive_bias = "balanced"
            notes.append("event_window_geometry_cautious")

        total_slices = len(scaling_plan) if scaling_plan else 1
        per_slice_risk_pct = round(
            min(
                template.base_risk_per_slice_pct,
                float(operative_surfaces["max_risk_per_trade"]) / total_slices,
            ),
            4,
        )
        if per_slice_risk_pct < template.base_risk_per_slice_pct:
            notes.append("max_risk_per_trade_cap_applied")

        if target == 0.0:
            notes.append("zero_target_geometry")

        return (
            passive_aggressive_bias,
            ladder_spacing_bps,
            max_chase_distance_bps,
            stop_distance_bps,
            take_profit_distance_bps,
            hedge_ratio,
            per_slice_risk_pct,
            notes,
        )

    def _operative_surfaces(self, packet) -> dict[str, float | bool]:
        if packet is None:
            return {
                "entry_gate_score_floor": float(self._SURFACE_DEFAULTS[MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR]),
                "zone_score_threshold": float(self._SURFACE_DEFAULTS[MutableRuntimeSurface.ZONE_SCORE_THRESHOLD]),
                "distance_to_vwap_soft_limit_pct": float(self._SURFACE_DEFAULTS[MutableRuntimeSurface.DISTANCE_TO_VWAP_SOFT_LIMIT_PCT]),
                "risk_vix_caution_threshold": float(self._SURFACE_DEFAULTS[MutableRuntimeSurface.RISK_VIX_CAUTION_THRESHOLD]),
                "risk_vix_hot_threshold": float(self._SURFACE_DEFAULTS[MutableRuntimeSurface.RISK_VIX_HOT_THRESHOLD]),
                "max_risk_per_trade": float(self._SURFACE_DEFAULTS[MutableRuntimeSurface.MAX_RISK_PER_TRADE]),
                "hedge_required": bool(self._SURFACE_DEFAULTS[MutableRuntimeSurface.HEDGE_REQUIRED]),
            }

        def numeric(surface: MutableRuntimeSurface) -> float:
            for item in packet.resolved_surfaces:
                if item.target_surface is surface and item.effective_numeric_value is not None:
                    return float(item.effective_numeric_value)
            return float(self._SURFACE_DEFAULTS[surface])

        def boolean(surface: MutableRuntimeSurface) -> bool:
            for item in packet.resolved_surfaces:
                if item.target_surface is surface and item.effective_boolean_value is not None:
                    return bool(item.effective_boolean_value)
            return bool(self._SURFACE_DEFAULTS[surface])

        return {
            "entry_gate_score_floor": numeric(MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR),
            "zone_score_threshold": numeric(MutableRuntimeSurface.ZONE_SCORE_THRESHOLD),
            "distance_to_vwap_soft_limit_pct": numeric(MutableRuntimeSurface.DISTANCE_TO_VWAP_SOFT_LIMIT_PCT),
            "risk_vix_caution_threshold": numeric(MutableRuntimeSurface.RISK_VIX_CAUTION_THRESHOLD),
            "risk_vix_hot_threshold": numeric(MutableRuntimeSurface.RISK_VIX_HOT_THRESHOLD),
            "max_risk_per_trade": numeric(MutableRuntimeSurface.MAX_RISK_PER_TRADE),
            "hedge_required": boolean(MutableRuntimeSurface.HEDGE_REQUIRED),
        }
