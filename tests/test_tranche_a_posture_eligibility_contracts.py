"""Gate 16 tests for tranche-A posture and eligibility selector contracts."""

from __future__ import annotations

from datetime import datetime
from typing import cast

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import (
    InventoryState,
    MarketRegimeContextInput,
    OptionsFlowContextInput,
    OptionsFlowMicroSnapshot,
    PostureRiskInput,
    TemporalContextInput,
)
from nvda_desk.schemas.dmp import DmpBehaviourClass, DmpGrammarRole
from nvda_desk.schemas.imported_modules.tranche_a import (
    ArchetypeMatcherContractOutput,
    EntryGateContractOutput,
    TrancheASelectorContext,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime, DeskCognitionRuntimeResult
from nvda_desk.services.imported_modules.tranche_a import TrancheASelectorContractService
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.posture_risk import PostureRiskService
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def _supportive_runtime_result() -> DeskCognitionRuntimeResult:
    runtime = DeskCognitionRuntime(Settings())
    return runtime.run(
        temporal_input=TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-23T14:15:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-03-27T16:00:00-04:00"),
            next_event_at=datetime.fromisoformat("2026-03-23T17:00:00-04:00"),
            prior_session_return_pct=1.4,
            intraday_move_pct=0.8,
        ),
        regime_input=MarketRegimeContextInput(
            nvda_return_pct=0.8,
            nq_return_pct=0.5,
            es_return_pct=0.3,
            sox_return_pct=0.9,
            breadth_score=0.67,
            concentration_score=0.41,
            vix_level=18.4,
            vvix_level=84.0,
            us10y=4.22,
            us2y=4.04,
            usdjpy=148.9,
        ),
        options_flow_input=OptionsFlowContextInput(
            spot_price=118.0,
            front_dte=4,
            next_dte=11,
            front_atm_iv=59.0,
            next_atm_iv=60.0,
            front_realised_vol=60.0,
            next_realised_vol=61.0,
            put_call_skew=0.18,
            gamma_pressure_score=0.33,
            call_put_imbalance=-0.05,
            oi_concentration=0.44,
            atm_straddle_value=5.9,
            vix_level=18.4,
            vvix_level=84.0,
            spot_to_pin_distance_pct=1.9,
            vanna_proxy=0.02,
            charm_proxy=0.01,
            repeated_snapshot_sequence=[
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T18:10:00+00:00"),
                    front_atm_iv=59.8,
                    next_atm_iv=60.4,
                    put_call_skew=0.16,
                    gamma_pressure_score=0.36,
                    spot_to_pin_distance_pct=1.9,
                ),
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T18:15:00+00:00"),
                    front_atm_iv=59.0,
                    next_atm_iv=60.0,
                    put_call_skew=0.18,
                    gamma_pressure_score=0.33,
                    spot_to_pin_distance_pct=1.9,
                ),
            ],
        ),
        inventory_state=InventoryState(
            existing_inventory_pct=10.0,
            fresh_cash_pct=70.0,
            overnight_inventory_pct=0.0,
            open_orders_count=0,
            capital_lockup_pct=12.0,
            cost_basis_gap_pct=0.5,
            thesis_state_input="valid",
            adverse_excursion_pct=-1.0,
            time_stop_minutes_remaining=180,
        ),
        risk_budget_remaining_pct=68.0,
        stack_id="core_full_stack",
        coefficient_set_id="full_stack_base",
    )


def test_selector_contract_service_emits_the_six_tranche_a_selectors_in_order() -> None:
    """Gate 16 should emit the frozen six selector contracts in grammar order."""

    fixture = supportive_runtime_fixture()
    temporal = TemporalContextService(Settings()).evaluate(fixture.temporal_input)
    regime = MarketRegimeContextService().evaluate(fixture.regime_input)
    options_flow = OptionsFlowContextService().evaluate(fixture.options_flow_input)
    posture = PostureRiskService().evaluate(
        PostureRiskInput(
            temporal=temporal,
            regime=regime,
            options_flow=options_flow,
            inventory=fixture.inventory_state,
            risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        )
    )
    emissions = TrancheASelectorContractService().evaluate(
        TrancheASelectorContext(
            emitted_at=fixture.temporal_input.ts,
            temporal=temporal,
            regime=regime,
            options_flow=options_flow,
            posture=posture,
        )
    )

    assert [emission.output.canonical_id for emission in emissions] == [
        "archive-evaluator-eval02",
        "archive-module-051",
        "archive-module-043",
        "archive-module-023",
        "archive-module-024",
        "archive-module-020",
    ]
    assert [emission.packet.grammar_role for emission in emissions[:3]] == [
        DmpGrammarRole.POSTURE_RISK_PERMISSION,
        DmpGrammarRole.POSTURE_RISK_PERMISSION,
        DmpGrammarRole.POSTURE_RISK_PERMISSION,
    ]
    assert [emission.packet.grammar_role for emission in emissions[3:]] == [
        DmpGrammarRole.PLAYBOOK_ELIGIBILITY,
        DmpGrammarRole.PLAYBOOK_ELIGIBILITY,
        DmpGrammarRole.PLAYBOOK_ELIGIBILITY,
    ]
    assert all(emission.packet.behaviour_class is DmpBehaviourClass.MODULE_OUTPUT for emission in emissions)


def test_runtime_cites_tranche_a_selector_contracts_without_playbook_drift() -> None:
    """Gate 16 should cite selector contracts while leaving current playbook outcomes unchanged."""

    result = _supportive_runtime_result()
    archetype_packet_id = result.contract_packet_ids["archetype_matcher"]
    archetype_packet = next(
        packet for packet in result.contract_packets if packet.packet_identity.packet_id == archetype_packet_id
    )
    archetype_output = cast(ArchetypeMatcherContractOutput, archetype_packet.payload)

    assert result.execution.active_playbook_ids == ["continuation_ladder", "compression_breakout"]
    assert result.execution.entry_style == "trend_ladder_3_step"
    assert result.execution.scaling_plan == [11.0, 16.5, 27.5]
    assert len(result.contract_packets) == 13
    assert set(result.contract_packet_ids) >= {
        "signal_conflict_detector",
        "model_confidence_scorer",
        "conviction_tier_allocator",
        "entry_gate",
        "ladder_constructor",
        "archetype_matcher",
    }
    assert any(reason.startswith("contract:signal_conflict_detector:") for reason in result.posture.reasons)
    assert any(reason.startswith("contract:entry_gate:") for reason in result.eligibility.reasons)
    assert any(reason.startswith("contract:archetype_matcher:") for reason in result.eligibility.reasons)
    if archetype_output.matched_playbook is not None:
        matched_candidate = next(
            candidate
            for candidate in result.eligibility.candidates
            if candidate.playbook_id == archetype_output.matched_playbook
        )
        assert any(reason.startswith("contract:archetype_matcher:") for reason in matched_candidate.reasons)


def test_event_veto_selector_citation_propagates_without_inventing_new_playbooks() -> None:
    """Gate 16 should propagate entry-gate veto citations into candidate reasons without adding playbooks."""

    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-23T14:10:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-03-27T16:00:00-04:00"),
            next_event_at=datetime.fromisoformat("2026-03-23T14:35:00-04:00"),
            prior_session_return_pct=1.4,
            intraday_move_pct=0.8,
        ),
        regime_input=MarketRegimeContextInput(
            nvda_return_pct=0.8,
            nq_return_pct=0.5,
            es_return_pct=0.3,
            sox_return_pct=0.9,
            breadth_score=0.67,
            concentration_score=0.41,
            vix_level=18.4,
            vvix_level=84.0,
            us10y=4.22,
            us2y=4.04,
            usdjpy=148.9,
        ),
        options_flow_input=OptionsFlowContextInput(
            spot_price=118.0,
            front_dte=4,
            next_dte=11,
            front_atm_iv=59.0,
            next_atm_iv=60.0,
            front_realised_vol=60.0,
            next_realised_vol=61.0,
            put_call_skew=0.18,
            gamma_pressure_score=0.33,
            call_put_imbalance=-0.05,
            oi_concentration=0.44,
            atm_straddle_value=5.9,
            vix_level=18.4,
            vvix_level=84.0,
            spot_to_pin_distance_pct=1.9,
        ),
        inventory_state=InventoryState(
            existing_inventory_pct=10.0,
            fresh_cash_pct=70.0,
            overnight_inventory_pct=0.0,
            open_orders_count=0,
            capital_lockup_pct=12.0,
            cost_basis_gap_pct=0.5,
            thesis_state_input="valid",
            adverse_excursion_pct=-1.0,
            time_stop_minutes_remaining=180,
        ),
        risk_budget_remaining_pct=68.0,
    )
    entry_packet_id = result.contract_packet_ids["entry_gate"]
    entry_packet = next(
        packet for packet in result.contract_packets if packet.packet_identity.packet_id == entry_packet_id
    )
    entry_output = cast(EntryGateContractOutput, entry_packet.payload)
    archetype_packet_id = result.contract_packet_ids["archetype_matcher"]
    archetype_packet = next(
        packet for packet in result.contract_packets if packet.packet_identity.packet_id == archetype_packet_id
    )
    archetype_output = cast(ArchetypeMatcherContractOutput, archetype_packet.payload)

    assert result.execution.active_playbook_ids == []
    assert entry_output.suppression_tag == "event_window_veto"
    assert archetype_output.matched_playbook in {None, "continuation_ladder", "compression_breakout", "pin_reversion", "negative_gamma_flush"}
    assert all(
        any(reason == "contract:entry_gate:event_window_veto" for reason in candidate.reasons)
        for candidate in result.eligibility.candidates
    )
