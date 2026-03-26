"""Gate 19 tests for context and scanner contracts."""

from __future__ import annotations

from typing import cast

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import PlaybookEligibilityInput, PostureRiskInput
from nvda_desk.schemas.dmp import DmpBehaviourClass, DmpGrammarRole
from nvda_desk.schemas.imported_modules.context_scanners import (
    ContextScannerContext,
    EngineScoreContractOutput,
    ExecutionContextScoreContractOutput,
    VixSpreadDetectorContractOutput,
)
from nvda_desk.schemas.imported_modules.market_substrate import (
    MacroDataCaptureContractOutput,
    MarketSubstrateContext,
    OptionsDataCaptureContractOutput,
    OptionsMetadataCaptureContractOutput,
    PeerEquityCaptureContractOutput,
    SpotDataCaptureContractOutput,
    VwapAccumulatorContractOutput,
    VwapRocContractOutput,
)
from nvda_desk.services.imported_modules.context_scanners import ContextScannerContractService
from nvda_desk.services.imported_modules.market_substrate import MarketSubstrateContractService
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.playbook_eligibility import PlaybookEligibilityService
from nvda_desk.services.posture_risk import PostureRiskService
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.testing.cognition_fixtures import (
    stressed_runtime_fixture,
    supportive_runtime_fixture,
)

EXPECTED_GATE19_ORDER = [
    "macro_signal_score",
    "execution_context_score",
    "vix_spread_detector",
    "vol_corridor",
    "options_behaviour_cluster",
    "asia_precursor_context_filter",
    "macro_adaptive_weighting_filter",
    "engine_score",
]


def _context_from_fixture(*, stressed: bool = False) -> ContextScannerContext:
    fixture = stressed_runtime_fixture() if stressed else supportive_runtime_fixture()
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
    eligibility = PlaybookEligibilityService().evaluate(
        PlaybookEligibilityInput(
            temporal=temporal,
            regime=regime,
            options_flow=options_flow,
            posture=posture,
        )
    )
    substrate_context = MarketSubstrateContext(
        emitted_at=fixture.temporal_input.ts,
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        temporal=temporal,
        regime=regime,
        options_flow=options_flow,
        stack_id="core_full_stack",
        coefficient_set_id="full_stack_base",
    )
    substrate_outputs = {
        emission.output.canonical_slug: emission.output
        for emission in MarketSubstrateContractService().evaluate(substrate_context)
    }
    spot_data_capture = cast(SpotDataCaptureContractOutput, substrate_outputs["spot_data_capture"])
    peer_equity_capture = cast(PeerEquityCaptureContractOutput, substrate_outputs["peer_equity_capture"])
    options_data_capture = cast(OptionsDataCaptureContractOutput, substrate_outputs["options_data_capture"])
    options_metadata_capture = cast(OptionsMetadataCaptureContractOutput, substrate_outputs["options_metadata_capture"])
    macro_data_capture = cast(MacroDataCaptureContractOutput, substrate_outputs["macro_data_capture"])
    vwap_accumulator = cast(VwapAccumulatorContractOutput, substrate_outputs["vwap_accumulator"])
    vwap_roc = cast(VwapRocContractOutput, substrate_outputs["vwap_roc"])

    return ContextScannerContext(
        emitted_at=fixture.temporal_input.ts,
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        temporal=temporal,
        regime=regime,
        options_flow=options_flow,
        posture=posture,
        eligibility=eligibility,
        spot_data_capture=spot_data_capture,
        peer_equity_capture=peer_equity_capture,
        options_data_capture=options_data_capture,
        options_metadata_capture=options_metadata_capture,
        macro_data_capture=macro_data_capture,
        vwap_accumulator=vwap_accumulator,
        vwap_roc=vwap_roc,
        stack_id="core_full_stack",
        coefficient_set_id="full_stack_base",
    )


def test_context_scanner_contracts_emit_the_frozen_eight_modules_in_order() -> None:
    """Gate 19 should emit the eight context/scanner contracts in gate-map order."""

    emissions = ContextScannerContractService().evaluate(_context_from_fixture())
    assert [emission.output.canonical_slug for emission in emissions] == EXPECTED_GATE19_ORDER
    assert [emission.packet.grammar_role for emission in emissions] == [
        DmpGrammarRole.MARKET_REGIME_CONTEXT,
        DmpGrammarRole.OPTIONS_FLOW_CONTEXT,
        DmpGrammarRole.OPTIONS_FLOW_CONTEXT,
        DmpGrammarRole.OPTIONS_FLOW_CONTEXT,
        DmpGrammarRole.OPTIONS_FLOW_CONTEXT,
        DmpGrammarRole.MARKET_REGIME_CONTEXT,
        DmpGrammarRole.MARKET_REGIME_CONTEXT,
        DmpGrammarRole.MARKET_REGIME_CONTEXT,
    ]
    assert all(emission.packet.behaviour_class is DmpBehaviourClass.MODULE_OUTPUT for emission in emissions)


def test_context_scanner_contracts_keep_provenance_explicit_for_execution_context_and_engine_score() -> None:
    """Gate 19 should keep provenance explicit for the two aggregate scanner contracts."""

    emissions = {
        emission.output.canonical_slug: emission.output
        for emission in ContextScannerContractService().evaluate(_context_from_fixture())
    }
    execution_context = cast(ExecutionContextScoreContractOutput, emissions["execution_context_score"])
    engine_score = cast(EngineScoreContractOutput, emissions["engine_score"])

    assert execution_context.upstream_contract_slugs == [
        "spot_data_capture",
        "options_data_capture",
        "options_metadata_capture",
        "macro_data_capture",
    ]
    assert execution_context.execution_state == "deployable_context"
    assert execution_context.context_score > 0.7
    assert {fence.dependency for fence in execution_context.dependency_fences if fence.status.value == "satisfied"} == {
        "market_substrate:spot_data_capture",
        "market_substrate:options_data_capture",
        "market_substrate:options_metadata_capture",
        "market_substrate:macro_data_capture",
    }

    assert engine_score.upstream_contract_slugs == [
        "macro_signal_score",
        "execution_context_score",
        "options_behaviour_cluster",
    ]
    assert engine_score.conviction_band == "constructive"
    assert engine_score.engine_score > 0.65
    assert {fence.dependency for fence in engine_score.dependency_fences if fence.status.value == "satisfied"} == {
        "context_scanner:macro_signal_score",
        "context_scanner:execution_context_score",
        "context_scanner:options_behaviour_cluster",
    }


def test_context_scanner_contracts_reflect_stressed_conditions_without_fake_approval_state() -> None:
    """Gate 19 should degrade the stressed fixture honestly while staying packet-safe."""

    emissions = ContextScannerContractService().evaluate(_context_from_fixture(stressed=True))
    outputs = {emission.output.canonical_slug: emission.output for emission in emissions}
    engine_score = cast(EngineScoreContractOutput, outputs["engine_score"])
    execution_context = cast(ExecutionContextScoreContractOutput, outputs["execution_context_score"])
    vix_spread = cast(VixSpreadDetectorContractOutput, outputs["vix_spread_detector"])

    assert execution_context.execution_state == "do_not_press"
    assert engine_score.conviction_band == "suppressed"
    assert engine_score.engine_score < 0.3
    assert vix_spread.risk_tag == "vvix_dislocation"
    assert emissions[-1].packet.summary.trader_summary.startswith("engine_score")
