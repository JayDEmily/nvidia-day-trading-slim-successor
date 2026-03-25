"""Gate 30 coverage checks for the options-ingress tranche."""

from __future__ import annotations

from typing import cast

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import PlaybookEligibilityInput, PostureRiskInput
from nvda_desk.schemas.dmp import DmpGrammarRole
from nvda_desk.schemas.imported_modules.context_scanners import ContextScannerContext
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
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    GammaPressureContractOutput,
    IvVsRvAnalysisContractOutput,
    TrancheAUpstreamContext,
)
from nvda_desk.services.imported_modules.context_scanners import ContextScannerContractService
from nvda_desk.services.imported_modules.market_substrate import MarketSubstrateContractService
from nvda_desk.services.imported_modules.tranche_a import TrancheAUpstreamContractService
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.playbook_eligibility import PlaybookEligibilityService
from nvda_desk.services.posture_risk import PostureRiskService
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

EXPECTED_GATE30_ORDER = [
    "options_data_capture",
    "options_metadata_capture",
    "gamma_pressure",
    "iv_vs_rv_analysis",
    "skew_inflection",
    "vol_corridor",
    "vix_spread_detector",
]


def test_gate30_coverage_is_closed_in_frozen_order_with_honest_options_fences() -> None:
    """Gate 30 should close exactly the seven planned options-ingress and primary-flow items."""

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
    eligibility = PlaybookEligibilityService().evaluate(
        PlaybookEligibilityInput(
            temporal=temporal,
            regime=regime,
            options_flow=options_flow,
            posture=posture,
        )
    )
    upstream_outputs = {
        emission.output.canonical_slug: emission.output
        for emission in TrancheAUpstreamContractService().evaluate(
            TrancheAUpstreamContext(
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
        )
    }
    substrate_outputs = {
        emission.output.canonical_slug: emission.output
        for emission in MarketSubstrateContractService().evaluate(
            MarketSubstrateContext(
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
        )
    }
    scanner_outputs = {
        emission.output.canonical_slug: emission.output
        for emission in ContextScannerContractService().evaluate(
            ContextScannerContext(
                emitted_at=fixture.temporal_input.ts,
                temporal_input=fixture.temporal_input,
                regime_input=fixture.regime_input,
                options_flow_input=fixture.options_flow_input,
                temporal=temporal,
                regime=regime,
                options_flow=options_flow,
                posture=posture,
                eligibility=eligibility,
                spot_data_capture=cast(SpotDataCaptureContractOutput, substrate_outputs["spot_data_capture"]),
                peer_equity_capture=cast(PeerEquityCaptureContractOutput, substrate_outputs["peer_equity_capture"]),
                options_data_capture=cast(OptionsDataCaptureContractOutput, substrate_outputs["options_data_capture"]),
                options_metadata_capture=cast(OptionsMetadataCaptureContractOutput, substrate_outputs["options_metadata_capture"]),
                macro_data_capture=cast(MacroDataCaptureContractOutput, substrate_outputs["macro_data_capture"]),
                vwap_accumulator=cast(VwapAccumulatorContractOutput, substrate_outputs["vwap_accumulator"]),
                vwap_roc=cast(VwapRocContractOutput, substrate_outputs["vwap_roc"]),
                stack_id="core_full_stack",
                coefficient_set_id="full_stack_base",
            )
        )
    }

    outputs = {
        **upstream_outputs,
        **substrate_outputs,
        **scanner_outputs,
    }
    ordered = [outputs[slug] for slug in EXPECTED_GATE30_ORDER]

    assert [output.canonical_slug for output in ordered] == EXPECTED_GATE30_ORDER
    assert [output.canonical_id for output in ordered] == [
        "archive-module-003",
        "archive-module-004",
        "archive-module-011",
        "archive-module-010",
        "archive-module-016",
        "archive-module-012",
        "archive-module-019",
    ]

    options_data_capture = cast(OptionsDataCaptureContractOutput, outputs["options_data_capture"])
    options_metadata_capture = cast(OptionsMetadataCaptureContractOutput, outputs["options_metadata_capture"])
    gamma_pressure = cast(GammaPressureContractOutput, outputs["gamma_pressure"])
    iv_vs_rv = cast(IvVsRvAnalysisContractOutput, outputs["iv_vs_rv_analysis"])

    assert options_data_capture.computation_mode is ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY
    assert options_metadata_capture.computation_mode is ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY
    assert gamma_pressure.dependency_fences[0].dependency == "options_chain"
    assert gamma_pressure.dependency_fences[0].status.value == "proxied_from_runtime"
    assert {fence.dependency for fence in iv_vs_rv.dependency_fences if fence.status.value == "satisfied"} == {
        "rv_metrics",
    }
    assert outputs["vol_corridor"].grammar_role == DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value
