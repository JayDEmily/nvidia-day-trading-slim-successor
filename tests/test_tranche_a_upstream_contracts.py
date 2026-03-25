"""Gate 15 tests for tranche-A upstream detector contracts."""

from __future__ import annotations

from typing import cast

from nvda_desk.config import Settings
from nvda_desk.schemas.dmp import DmpBehaviourClass, DmpGrammarRole
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    GammaPressureContractOutput,
    IvVsRvAnalysisContractOutput,
    PeerDivergenceContractOutput,
    TrancheAUpstreamContext,
    VolumeSpikeFilterContractOutput,
)
from nvda_desk.services.imported_modules.tranche_a import TrancheAUpstreamContractService
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def _supportive_context() -> TrancheAUpstreamContext:
    fixture = supportive_runtime_fixture()
    temporal = TemporalContextService(Settings()).evaluate(fixture.temporal_input)
    regime = MarketRegimeContextService().evaluate(fixture.regime_input)
    options_flow = OptionsFlowContextService().evaluate(
        fixture.options_flow_input.model_copy(
            update={
                "front_realised_vol": 60.0,
                "next_realised_vol": 61.0,
                "repeated_snapshot_sequence": fixture.options_flow_input.repeated_snapshot_sequence,
            }
        )
    )
    return TrancheAUpstreamContext(
        emitted_at=fixture.temporal_input.ts,
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input.model_copy(
            update={
                "front_realised_vol": 60.0,
                "next_realised_vol": 61.0,
                "repeated_snapshot_sequence": fixture.options_flow_input.repeated_snapshot_sequence,
            }
        ),
        temporal=temporal,
        regime=regime,
        options_flow=options_flow,
        stack_id="core_full_stack",
        coefficient_set_id="full_stack_base",
    )


def test_tranche_a_upstream_contracts_emit_the_frozen_seven_modules_in_order() -> None:
    """Gate 15 should emit the seven upstream tranche-A contracts in manifest order."""

    emissions = TrancheAUpstreamContractService().evaluate(_supportive_context())
    assert [emission.output.canonical_id for emission in emissions] == [
        "archive-module-006",
        "archive-module-009",
        "archive-module-018",
        "archive-module-014",
        "archive-module-011",
        "archive-module-010",
        "archive-module-016",
    ]
    assert [emission.packet.grammar_role for emission in emissions] == [
        DmpGrammarRole.TEMPORAL_CONTEXT,
        DmpGrammarRole.MARKET_REGIME_CONTEXT,
        DmpGrammarRole.MARKET_REGIME_CONTEXT,
        DmpGrammarRole.MARKET_REGIME_CONTEXT,
        DmpGrammarRole.OPTIONS_FLOW_CONTEXT,
        DmpGrammarRole.OPTIONS_FLOW_CONTEXT,
        DmpGrammarRole.OPTIONS_FLOW_CONTEXT,
    ]
    assert all(emission.packet.behaviour_class is DmpBehaviourClass.MODULE_OUTPUT for emission in emissions)


def test_tranche_a_upstream_contracts_keep_fenced_dependencies_explicit() -> None:
    """Gate 15 should not hide missing live dependencies behind fake runtime readiness."""

    emissions = {emission.output.canonical_slug: emission.output for emission in TrancheAUpstreamContractService().evaluate(_supportive_context())}
    volume = cast(VolumeSpikeFilterContractOutput, emissions["volume_spike_filter"])
    peer = cast(PeerDivergenceContractOutput, emissions["peer_divergence"])
    gamma = cast(GammaPressureContractOutput, emissions["gamma_pressure"])

    assert volume.computation_mode is ContractComputationMode.FENCED_CONTRACT_ONLY
    assert {fence.dependency for fence in volume.dependency_fences if fence.status.value == "fenced_missing_source"} == {
        "spot_prices",
        "spot_volume_series",
    }
    assert any(fence.dependency == "peer_equities" and fence.status.value == "proxied_from_runtime" for fence in peer.dependency_fences)
    assert gamma.zone_gamma in {"supportive", "neutral", "destabilising"}
    assert gamma.signal_score >= 0.0


def test_tranche_a_upstream_packets_upgrade_to_v2_and_remain_lineage_ready() -> None:
    """Gate 15 should keep upstream contract packets DMP-serialisable and review-lineage ready."""

    emissions = TrancheAUpstreamContractService().evaluate(_supportive_context())
    skew = next(emission for emission in emissions if emission.output.canonical_slug == "skew_inflection")
    ivrv = next(emission for emission in emissions if emission.output.canonical_slug == "iv_vs_rv_analysis")
    ivrv_output = cast(IvVsRvAnalysisContractOutput, ivrv.output)

    assert skew.packet.protocol_version == "dmp.v1"
    assert skew.packet_v2.protocol_version == "dmp.v2"
    assert skew.packet_v2.producer.grammar_role == DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value
    assert skew.packet_v2.summary.trader_summary.startswith("skew_inflection")
    assert ivrv_output.ivrv_ratio is None or ivrv_output.ivrv_ratio > 0.0
    assert ivrv.packet.schema_identifiers.output_model_name == "IvVsRvAnalysisContractOutput"
