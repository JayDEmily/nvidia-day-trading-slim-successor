"""Gate 29 coverage checks for the market-context synthesis tranche."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol, cast

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import PlaybookEligibilityInput, PostureRiskInput
from nvda_desk.schemas.dmp import DmpGrammarRole
from nvda_desk.schemas.imported_modules.context_scanners import (
    ContextScannerContext,
    EngineScoreContractOutput,
    MacroSignalScoreContractOutput,
)
from nvda_desk.schemas.imported_modules.market_context_synthesis import (
    MarketContextSynthesisContext,
    RunSignalScanContractOutput,
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
from nvda_desk.schemas.imported_modules.tranche_a import TrancheAUpstreamContext
from nvda_desk.services.imported_modules.context_scanners import (
    ContextScannerContractService,
)
from nvda_desk.services.imported_modules.market_context_synthesis import (
    MarketContextSynthesisContractService,
)
from nvda_desk.services.imported_modules.market_substrate import (
    MarketSubstrateContractService,
)
from nvda_desk.services.imported_modules.tranche_a import (
    TrancheAUpstreamContractService,
)
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.playbook_eligibility import PlaybookEligibilityService
from nvda_desk.services.posture_risk import PostureRiskService
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.testing.cognition_fixtures import (
    stressed_runtime_fixture,
    supportive_runtime_fixture,
)

EXPECTED_GATE29_ORDER = [
    "macro_signal_score",
    "peer_divergence",
    "volume_spike_filter",
    "macro_adaptive_weighting_filter",
    "asia_precursor_context_filter",
    "engine_score",
    "run_signal_scan",
]


class _CanonicalOutput(Protocol):
    canonical_slug: str
    canonical_id: str


def _slug(output: _CanonicalOutput) -> str:
    return output.canonical_slug


def _canonical_id(output: _CanonicalOutput) -> str:
    return output.canonical_id


@dataclass(frozen=True)
class Gate29Bundle:
    upstream_outputs: Mapping[str, object]
    scanner_outputs: Mapping[str, object]
    synthesis_outputs: Mapping[str, object]


def _bundle(*, stressed: bool = False) -> Gate29Bundle:
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
                spot_data_capture=cast(
                    SpotDataCaptureContractOutput,
                    substrate_outputs["spot_data_capture"],
                ),
                peer_equity_capture=cast(
                    PeerEquityCaptureContractOutput,
                    substrate_outputs["peer_equity_capture"],
                ),
                options_data_capture=cast(
                    OptionsDataCaptureContractOutput,
                    substrate_outputs["options_data_capture"],
                ),
                options_metadata_capture=cast(
                    OptionsMetadataCaptureContractOutput,
                    substrate_outputs["options_metadata_capture"],
                ),
                macro_data_capture=cast(
                    MacroDataCaptureContractOutput,
                    substrate_outputs["macro_data_capture"],
                ),
                vwap_accumulator=cast(
                    VwapAccumulatorContractOutput, substrate_outputs["vwap_accumulator"]
                ),
                vwap_roc=cast(VwapRocContractOutput, substrate_outputs["vwap_roc"]),
                stack_id="core_full_stack",
                coefficient_set_id="full_stack_base",
            )
        )
    }
    synthesis_outputs = {
        emission.output.canonical_slug: emission.output
        for emission in MarketContextSynthesisContractService().evaluate(
            MarketContextSynthesisContext(
                emitted_at=fixture.temporal_input.ts,
                temporal=temporal,
                regime=regime,
                options_flow=options_flow,
                posture=posture,
                eligibility=eligibility,
                macro_signal_score=cast(
                    MacroSignalScoreContractOutput,
                    scanner_outputs["macro_signal_score"],
                ),
                engine_score=cast(
                    EngineScoreContractOutput, scanner_outputs["engine_score"]
                ),
                stack_id="core_full_stack",
                coefficient_set_id="full_stack_base",
            )
        )
    }
    return Gate29Bundle(
        upstream_outputs=upstream_outputs,
        scanner_outputs=scanner_outputs,
        synthesis_outputs=synthesis_outputs,
    )


def test_gate29_coverage_is_closed_in_frozen_order_and_run_signal_scan_stays_advisory() -> (
    None
):
    """Gate 29 should close exactly the seven planned synthesis items without execution leakage."""

    supportive = _bundle()
    stressed = _bundle(stressed=True)
    supportive_outputs = {
        **supportive.upstream_outputs,
        **supportive.scanner_outputs,
        **supportive.synthesis_outputs,
    }
    ordered = [
        cast(_CanonicalOutput, supportive_outputs[slug])
        for slug in EXPECTED_GATE29_ORDER
    ]

    assert [_slug(output) for output in ordered] == EXPECTED_GATE29_ORDER
    assert [_canonical_id(output) for output in ordered] == [
        "archive-module-013",
        "archive-module-014",
        "archive-module-018",
        "legacy-module-006",
        "legacy-module-008",
        "archive-module-022",
        "archive-module-052",
    ]

    run_signal_scan = cast(
        RunSignalScanContractOutput, supportive_outputs["run_signal_scan"]
    )
    assert run_signal_scan.grammar_role == DmpGrammarRole.MARKET_REGIME_CONTEXT.value
    assert run_signal_scan.upstream_contract_slugs == [
        "macro_signal_score",
        "engine_score",
    ]
    assert {
        fence.dependency
        for fence in run_signal_scan.dependency_fences
        if fence.status.value == "satisfied"
    } == {
        "context_scanner:macro_signal_score",
        "context_scanner:engine_score",
    }
    assert run_signal_scan.dependency_fences[0].dependency == "runtime_config"
    assert run_signal_scan.dependency_fences[0].status.value == "proxied_from_runtime"
    assert run_signal_scan.scan_state == "scan_ready"

    stressed_scan = cast(
        RunSignalScanContractOutput, stressed.synthesis_outputs["run_signal_scan"]
    )
    assert stressed_scan.scan_state in {"scan_watch_only", "scan_suppressed"}
    assert "No execution trigger" in stressed_scan.contract_notes[1]
