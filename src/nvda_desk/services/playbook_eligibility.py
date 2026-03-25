"""Playbook-eligibility service for the Desk Cognition Grammar.

This service decides which playbooks are eligible, watch-only, or ineligible
once temporal, regime, options, and posture layers are known.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Literal

from nvda_desk.schemas.cognition import (
    PlaybookCandidate,
    PlaybookDecision,
    PlaybookEligibilityInput,
    PlaybookEligibilityOutput,
)
from nvda_desk.schemas.playbook_registry import PlaybookDecisionProfile, PlaybookSpec
from nvda_desk.services.playbook_registry import PlaybookRegistryService


class PlaybookEligibilityService:
    """Determine deterministic playbook eligibility for one snapshot.

    Purpose:
        Translate desk state into explicit playbook-family decisions and action biases.
    Inputs:
        `PlaybookEligibilityInput` carrying temporal, regime, options, and
        posture outputs from upstream runtime layers.
    Outputs:
        `PlaybookEligibilityOutput` with continuation, negative-gamma flush,
        pin-reversion, and compression-breakout families plus veto surfaces.
    Determinism:
        Uses checked-in registry order plus fixed rule evaluation with no live calls.
    """

    def __init__(self, registry_service: PlaybookRegistryService | None = None):
        self._registry = registry_service or PlaybookRegistryService()
        self._rule_evaluators: dict[str, Callable[[PlaybookEligibilityInput, list[str], PlaybookSpec], PlaybookCandidate]] = {
            "continuation_ladder": self._continuation_ladder,
            "compression_breakout": self._compression_breakout,
            "pin_reversion": self._pin_reversion,
            "negative_gamma_flush": self._negative_gamma_flush,
            "front_expiry_pin_pressure": self._front_expiry_pin_pressure,
            "term_structure_dislocation": self._term_structure_dislocation,
            "skew_pressure_reversal": self._skew_pressure_reversal,
        }

    def evaluate(self, payload: PlaybookEligibilityInput) -> PlaybookEligibilityOutput:
        """Return eligible, watch-only, probe-only, and ineligible playbooks."""

        no_trade_reasons = self._no_trade_reasons(payload)
        candidates = [
            self._evaluate_spec(spec, payload, no_trade_reasons)
            for spec in self._registry.ordered_playbooks()
        ]
        add_candidates = [candidate.playbook_id for candidate in candidates if candidate.action_bias.value == "add"]
        hold_candidates = [candidate.playbook_id for candidate in candidates if candidate.action_bias.value == "hold"]
        trim_candidates = [candidate.playbook_id for candidate in candidates if candidate.action_bias.value == "trim"]
        reduce_candidates = [candidate.playbook_id for candidate in candidates if candidate.action_bias.value == "reduce"]
        hedge_candidates = [candidate.playbook_id for candidate in candidates if candidate.action_bias.value == "hedge"]
        probe_candidates = [
            candidate.playbook_id
            for candidate in candidates
            if candidate.decision is PlaybookDecision.ELIGIBLE and candidate.sizing_fraction <= 0.15
        ]
        watch_only_candidates = [candidate.playbook_id for candidate in candidates if candidate.decision is PlaybookDecision.WATCH_ONLY]
        rejected_playbook_reasons = {
            candidate.playbook_id: candidate.reasons
            for candidate in candidates
            if candidate.decision is not PlaybookDecision.ELIGIBLE
        }
        reasons = [f"permission_state:{payload.posture.permission_state.value}"]
        reasons.extend(f"no_trade:{reason}" for reason in no_trade_reasons)
        return PlaybookEligibilityOutput(
            candidates=candidates,
            add_candidates=add_candidates,
            hold_candidates=hold_candidates,
            trim_candidates=trim_candidates,
            reduce_candidates=reduce_candidates,
            hedge_candidates=hedge_candidates,
            probe_candidates=probe_candidates,
            watch_only_candidates=watch_only_candidates,
            no_trade_reasons=no_trade_reasons,
            rejected_playbook_reasons=rejected_playbook_reasons,
            reasons=reasons,
        )

    def _evaluate_spec(
        self,
        spec: PlaybookSpec,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
    ) -> PlaybookCandidate:
        evaluator = self._rule_evaluators[spec.rule_id]
        return evaluator(payload, no_trade_reasons, spec)

    def _candidate_from_profile(
        self,
        spec: PlaybookSpec,
        profile_name: Literal["eligible", "watch_only", "ineligible"],
        reasons: list[str],
    ) -> PlaybookCandidate:
        profile: PlaybookDecisionProfile = getattr(spec, profile_name)
        return PlaybookCandidate(
            playbook_id=spec.playbook_id,
            family_id=spec.family_id,
            setup_variant_id=spec.setup_variant_id,
            execution_expression_id=spec.execution_expression_id,
            horizon=spec.horizon.value,
            decision=profile.decision,
            action_bias=profile.action_bias,
            sizing_fraction=profile.sizing_fraction,
            hedge_overlay=profile.hedge_overlay,
            reasons=list(reasons),
        )

    def _no_trade_reasons(self, payload: PlaybookEligibilityInput) -> list[str]:
        reasons: list[str] = []
        if payload.posture.permission_state.value == "block":
            reasons.append("permission_blocked")
        if payload.temporal.event_window_state in {"event_live_window", "event_imminent_window"}:
            reasons.append("event_window_veto")
        if payload.options_flow.options_behavior_cluster == "event_suppressed":
            reasons.append("options_surface_event_suppressed")
        return reasons

    def _continuation_ladder(
        self,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
        spec: PlaybookSpec,
    ) -> PlaybookCandidate:
        reasons: list[str] = []
        if no_trade_reasons:
            reasons.extend(no_trade_reasons)
            return self._candidate_from_profile(spec, "ineligible", reasons)
        if (
            payload.regime.sector_leadership_state == "semis_leading"
            and payload.regime.breadth_state.value == "supportive"
            and payload.temporal.desk_window in {"early_anchor", "mid_morning", "trend_window", "late_session"}
            and payload.options_flow.options_behavior_cluster not in {"negative_gamma_flush", "event_suppressed"}
        ):
            return self._candidate_from_profile(spec, "eligible", ["leadership_and_breadth_supportive"])
        if payload.regime.sector_leadership_state in {"nvda_only_leadership", "leadership_mixed"}:
            return self._candidate_from_profile(spec, "watch_only", ["leadership_not_clean_enough"])
        return self._candidate_from_profile(spec, "ineligible", ["continuation_not_supported"])

    def _negative_gamma_flush(
        self,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
        spec: PlaybookSpec,
    ) -> PlaybookCandidate:
        reasons: list[str] = []
        if no_trade_reasons:
            reasons.extend(no_trade_reasons)
            return self._candidate_from_profile(spec, "ineligible", reasons)
        if payload.temporal.recent_path_tag == "intraday_flush" and payload.options_flow.options_behavior_cluster == "negative_gamma_flush":
            if payload.posture.permission_state.value == "derisk":
                return self._candidate_from_profile(spec, "watch_only", ["hostile_flush_context"])
            return self._candidate_from_profile(spec, "eligible", ["buyable_flush_probe"])
        return self._candidate_from_profile(spec, "ineligible", ["no_negative_gamma_flush_context"])

    def _pin_reversion(
        self,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
        spec: PlaybookSpec,
    ) -> PlaybookCandidate:
        reasons: list[str] = []
        if no_trade_reasons:
            reasons.extend(no_trade_reasons)
            return self._candidate_from_profile(spec, "ineligible", reasons)
        if (
            payload.options_flow.pin_risk_state in {"pin_risk_high", "pin_risk_present"}
            and payload.options_flow.strike_cluster_state in {"live_pin_cluster", "inferred_pin_cluster"}
            and payload.options_flow.pin_progression_state in {"pinning_in", "pin_stable"}
            and payload.temporal.desk_window in {"lunch", "trend_window", "late_session", "close"}
        ):
            if payload.options_flow.dealer_pressure_state == "dealer_destabilising":
                return self._candidate_from_profile(spec, "watch_only", ["pin_active_but_flow_destabilising"])
            return self._candidate_from_profile(spec, "eligible", ["pin_reversion_supported"])
        return self._candidate_from_profile(spec, "ineligible", ["no_pin_reversion_context"])

    def _compression_breakout(
        self,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
        spec: PlaybookSpec,
    ) -> PlaybookCandidate:
        reasons: list[str] = []
        if no_trade_reasons:
            reasons.extend(no_trade_reasons)
            return self._candidate_from_profile(spec, "ineligible", reasons)
        if (
            payload.options_flow.options_behavior_cluster == "compression_breakout_ready"
            and payload.temporal.desk_window in {"lunch", "trend_window", "late_session"}
        ):
            if payload.posture.permission_state.value == "derisk":
                return self._candidate_from_profile(spec, "watch_only", ["compression_ready_but_posture_derisk"])
            return self._candidate_from_profile(spec, "eligible", ["compression_breakout_supported"])
        if payload.options_flow.gamma_state.value == "supportive":
            return self._candidate_from_profile(spec, "watch_only", ["supportive_options_need_more_confirmation"])
        return self._candidate_from_profile(spec, "ineligible", ["compression_not_supported"])

    def _front_expiry_pin_pressure(
        self,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
        spec: PlaybookSpec,
    ) -> PlaybookCandidate:
        reasons: list[str] = []
        if no_trade_reasons:
            reasons.extend(no_trade_reasons)
            return self._candidate_from_profile(spec, "ineligible", reasons)
        if payload.temporal.expiry_cycle_state not in {"expiry_day", "front_week"}:
            return self._candidate_from_profile(spec, "ineligible", ["not_front_expiry_window"])
        if payload.temporal.desk_window not in {"early_anchor", "mid_morning"}:
            return self._candidate_from_profile(spec, "ineligible", ["pin_pressure_window_not_open"])
        if (
            payload.options_flow.pin_risk_state in {"pin_risk_high", "pin_risk_present"}
            and payload.options_flow.strike_cluster_state in {"live_pin_cluster", "inferred_pin_cluster"}
            and payload.options_flow.pin_progression_state in {"pinning_in", "pin_stable"}
        ):
            if payload.options_flow.dealer_pressure_state == "dealer_destabilising":
                return self._candidate_from_profile(spec, "watch_only", ["pin_build_visible_but_flow_destabilising"])
            return self._candidate_from_profile(spec, "eligible", ["front_expiry_pin_pressure_supported"])
        return self._candidate_from_profile(spec, "ineligible", ["no_front_expiry_pin_pressure_context"])

    def _term_structure_dislocation(
        self,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
        spec: PlaybookSpec,
    ) -> PlaybookCandidate:
        reasons: list[str] = []
        if no_trade_reasons:
            reasons.extend(no_trade_reasons)
            return self._candidate_from_profile(spec, "ineligible", reasons)
        if payload.temporal.expiry_cycle_state == "far_cycle":
            return self._candidate_from_profile(spec, "ineligible", ["term_dislocation_not_relevant_far_cycle"])
        if payload.options_flow.term_structure_state.value == "flat":
            return self._candidate_from_profile(spec, "ineligible", ["term_structure_flat"])
        if (
            payload.options_flow.tenor_curve_state in {"backwardated_curve", "hump_curve", "front_loaded_curve", "back_loaded_curve"}
            and payload.options_flow.iv_rv_curve_state in {"front_expiry_rich", "next_expiry_rich", "both_expiries_rich"}
            and payload.options_flow.repeated_snapshot_state in {"stable_recheck", "escalating_pressure"}
            and payload.temporal.desk_window in {"early_anchor", "mid_morning", "trend_window"}
        ):
            return self._candidate_from_profile(spec, "eligible", ["term_structure_dislocation_supported"])
        if payload.options_flow.tenor_curve_state in {"backwardated_curve", "hump_curve", "front_loaded_curve", "back_loaded_curve"}:
            return self._candidate_from_profile(spec, "watch_only", ["term_structure_dislocation_needs_iv_confirmation"])
        return self._candidate_from_profile(spec, "ineligible", ["no_term_structure_dislocation_context"])

    def _skew_pressure_reversal(
        self,
        payload: PlaybookEligibilityInput,
        no_trade_reasons: list[str],
        spec: PlaybookSpec,
    ) -> PlaybookCandidate:
        reasons: list[str] = []
        if no_trade_reasons:
            reasons.extend(no_trade_reasons)
            return self._candidate_from_profile(spec, "ineligible", reasons)
        if payload.options_flow.options_behavior_cluster == "negative_gamma_flush":
            return self._candidate_from_profile(spec, "ineligible", ["full_flush_already_has_priority"])
        if (
            payload.options_flow.dealer_pressure_state == "dealer_destabilising"
            and payload.options_flow.skew_evolution_state in {"downside_skew_expanding", "upside_skew_expanding"}
            and payload.options_flow.repeated_snapshot_state in {"stable_recheck", "cooling_pressure"}
            and payload.options_flow.options_behavior_cluster in {"dealer_flow_tension", "balanced_options_state"}
            and payload.temporal.desk_window in {"early_anchor", "mid_morning", "trend_window"}
        ):
            if payload.posture.permission_state.value == "derisk":
                return self._candidate_from_profile(spec, "watch_only", ["skew_reversal_visible_but_posture_derisk"])
            return self._candidate_from_profile(spec, "eligible", ["skew_pressure_reversal_supported"])
        if payload.options_flow.skew_evolution_state in {"downside_skew_expanding", "upside_skew_expanding"}:
            return self._candidate_from_profile(spec, "watch_only", ["skew_pressure_visible_needs_reversal_confirmation"])
        return self._candidate_from_profile(spec, "ineligible", ["no_skew_pressure_reversal_context"])
