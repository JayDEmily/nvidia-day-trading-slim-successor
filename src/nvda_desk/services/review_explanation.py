"""Review and explanation service for the Desk Cognition Grammar.

This service builds machine-readable review packets that reconstruct how the
runtime reached a posture, playbook, and execution decision.
"""

from __future__ import annotations

from nvda_desk.schemas.cognition import (
    ContradictionSurface,
    PlaybookDecision,
    RejectedPlaybookReason,
    ReviewExplanationInput,
    ReviewExplanationOutput,
    StageReasonPacket,
)


class ReviewExplanationService:
    """Build deterministic review and explanation packets.

    Purpose:
        Reconstruct the runtime decision as a structured stage-by-stage review.
    Inputs:
        `ReviewExplanationInput` containing the outputs from all prior runtime
        layers, including explicit playbook action buckets.
    Outputs:
        `ReviewExplanationOutput` with stage packets, rejected playbooks,
        contradiction surfaces, conflict density, and module attribution hooks.
    Determinism:
        Produces ordered packets from live model payloads with fixed rules.
    """

    def evaluate(self, payload: ReviewExplanationInput) -> ReviewExplanationOutput:
        """Create a structured review packet for one runtime snapshot."""

        conflict_tags = self._conflict_tags(payload)
        signal_conflict_density = round(min(1.0, len(conflict_tags) / 5.0), 4)
        summary = (
            f"window={payload.temporal.desk_window}; "
            f"permission={payload.posture.permission_state.value}; "
            f"families={payload.execution.active_family_ids or ['none']}; "
            f"setups={payload.execution.active_setup_variant_ids or ['none']}; "
            f"playbooks={payload.execution.active_playbook_ids or ['none']}"
        )
        stage_reason_packets = [
            StageReasonPacket(
                stage="temporal",
                summary=payload.temporal.desk_window,
                reasons=payload.temporal.reasons,
            ),
            StageReasonPacket(
                stage="regime",
                summary=payload.regime.signal_conflict_state,
                reasons=payload.regime.reasons,
            ),
            StageReasonPacket(
                stage="options_flow",
                summary=payload.options_flow.options_behavior_cluster,
                reasons=payload.options_flow.reasons,
            ),
            StageReasonPacket(
                stage="posture",
                summary=payload.posture.permission_state.value,
                reasons=payload.posture.reasons,
            ),
            StageReasonPacket(
                stage="eligibility",
                summary=(
                    f"families={payload.eligibility.active_family_ids or ['none']} / "
                    f"setups={payload.eligibility.active_setup_variant_ids or ['none']} / "
                    f"eligible={payload.eligibility.add_candidates or payload.eligibility.trim_candidates or ['none']}"
                ),
                reasons=payload.eligibility.reasons,
            ),
            StageReasonPacket(
                stage="execution",
                summary=(
                    f"{payload.execution.entry_style} / "
                    f"family={payload.execution.lead_family_id or 'none'} / "
                    f"setup={payload.execution.lead_setup_variant_id or 'none'}"
                ),
                reasons=payload.execution.reasons,
            ),
        ]
        rejected_playbooks = [
            RejectedPlaybookReason(
                playbook_id=candidate.playbook_id,
                decision=candidate.decision,
                action_bias=candidate.action_bias,
                reasons=candidate.reasons,
            )
            for candidate in payload.eligibility.candidates
            if candidate.decision is not PlaybookDecision.ELIGIBLE
        ]
        contradictions = [
            ContradictionSurface(
                contradiction_id=tag,
                description=self._contradiction_description(tag),
                implicated_stages=self._contradiction_stages(tag),
            )
            for tag in conflict_tags
        ]
        module_attribution = self._module_attribution(stage_reason_packets)
        stage_summaries = {packet.stage: "; ".join(packet.reasons) for packet in stage_reason_packets}
        desk_readout = self._desk_readout(payload)
        review_packet: dict[str, object] = {
            "temporal": payload.temporal.model_dump(mode="json"),
            "regime": payload.regime.model_dump(mode="json"),
            "options_flow": payload.options_flow.model_dump(mode="json"),
            "posture": payload.posture.model_dump(mode="json"),
            "eligibility": payload.eligibility.model_dump(mode="json"),
            "execution": payload.execution.model_dump(mode="json"),
            "hierarchy_summary": {
                "active_family_ids": list(payload.execution.active_family_ids),
                "active_setup_variant_ids": list(payload.execution.active_setup_variant_ids),
                "lead_family_id": payload.execution.lead_family_id,
                "lead_setup_variant_id": payload.execution.lead_setup_variant_id,
                "lead_playbook_id": payload.execution.lead_playbook_id,
            },
            "stage_summaries": stage_summaries,
            "stage_reason_packets": [packet.model_dump(mode="json") for packet in stage_reason_packets],
            "rejected_playbooks": [packet.model_dump(mode="json") for packet in rejected_playbooks],
            "contradictions": [surface.model_dump(mode="json") for surface in contradictions],
            "module_attribution": module_attribution,
            "signal_conflict_density": signal_conflict_density,
            "desk_readout": desk_readout,
            "conflicts": conflict_tags,
        }
        return ReviewExplanationOutput(
            summary=summary,
            conflict_tags=conflict_tags,
            signal_conflict_density=signal_conflict_density,
            stage_reason_packets=stage_reason_packets,
            rejected_playbooks=rejected_playbooks,
            contradictions=contradictions,
            module_attribution=module_attribution,
            review_packet=review_packet,
        )

    def _conflict_tags(self, payload: ReviewExplanationInput) -> list[str]:
        conflict_tags: list[str] = []
        if payload.regime.signal_conflict_state != "aligned_regime":
            conflict_tags.append("regime_signal_conflict")
        if payload.posture.signal_conflict_state != "aligned_signals":
            conflict_tags.append("posture_signal_conflict")
        if payload.eligibility.no_trade_reasons and payload.execution.active_playbook_ids:
            conflict_tags.append("event_veto_breached")
        if payload.options_flow.gamma_state.value == "destabilising" and not payload.execution.hedge_required:
            conflict_tags.append("missing_hedge_under_destabilising_gamma")
        if payload.posture.inventory_posture_state in {"trapped", "capital_locked"} and payload.execution.inventory_action == "add":
            conflict_tags.append("adding_into_locked_inventory")
        return conflict_tags

    def _module_attribution(self, stage_reason_packets: list[StageReasonPacket]) -> dict[str, float]:
        raw_scores = {
            packet.stage: max(1.0, float(len(packet.reasons)))
            for packet in stage_reason_packets
        }
        total = sum(raw_scores.values())
        return {stage: round(score / total, 4) for stage, score in raw_scores.items()}

    def _desk_readout(self, payload: ReviewExplanationInput) -> str:
        return (
            f"{payload.temporal.desk_window} | "
            f"{payload.regime.volatility_regime.value} / {payload.regime.breadth_concentration_state} | "
            f"{payload.options_flow.options_behavior_cluster} | "
            f"permission={payload.posture.permission_state.value} | "
            f"family={payload.execution.lead_family_id or 'none'} | "
            f"setup={payload.execution.lead_setup_variant_id or 'none'} | "
            f"inventory={payload.execution.inventory_action}"
        )

    def _contradiction_description(self, tag: str) -> str:
        descriptions = {
            "regime_signal_conflict": "The regime layer still shows unresolved cross-signal conflict.",
            "posture_signal_conflict": "Posture remained conflicted after options and inventory checks.",
            "event_veto_breached": "Execution stayed active despite an explicit no-trade event veto.",
            "missing_hedge_under_destabilising_gamma": "Destabilising gamma was present without a hedge overlay.",
            "adding_into_locked_inventory": "Execution proposed adding into trapped or locked inventory.",
        }
        return descriptions.get(tag, "Runtime contradiction detected.")

    def _contradiction_stages(self, tag: str) -> list[str]:
        stage_map = {
            "regime_signal_conflict": ["regime", "posture", "review_explanation"],
            "posture_signal_conflict": ["options_flow", "posture", "review_explanation"],
            "event_veto_breached": ["temporal", "eligibility", "execution"],
            "missing_hedge_under_destabilising_gamma": ["options_flow", "execution"],
            "adding_into_locked_inventory": ["posture", "execution"],
        }
        return stage_map.get(tag, ["review_explanation"])
