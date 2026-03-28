"""Gate 17 tests for tranche-A review/replay lineage and honest maturity state."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.review import (
    ImportedModuleApprovalState,
    ImportedModuleMaturityState,
)
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.replay_compare import ReplayComparisonService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

FIXTURE_PACK = Path("fixtures/replay/gate_f_replay_regression_fixture_pack.json")


EXPECTED_TRANCHE_A_ORDER = [
    "event_flag_capture",
    "realized_volatility_engine",
    "volume_spike_filter",
    "peer_divergence",
    "gamma_pressure",
    "iv_vs_rv_analysis",
    "skew_inflection",
    "signal_conflict_detector",
    "model_confidence_scorer",
    "conviction_tier_allocator",
    "entry_gate",
    "ladder_constructor",
    "archetype_matcher",
]


def test_review_packet_cites_tranche_a_modules_with_honest_maturity_and_no_fake_approval() -> (
    None
):
    """Gate 17 should surface tranche-A lineage in review without promotion theatre."""

    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        stack_id="core_full_stack",
        coefficient_set_id="full_stack_base",
    )

    citations = result.review.imported_module_citations
    assert [
        citation.canonical_slug for citation in citations
    ] == EXPECTED_TRANCHE_A_ORDER
    assert len(citations) == 13
    assert (
        result.review.review_packet["imported_module_maturity_counts"]
        == result.review.imported_module_maturity_counts
    )
    assert result.review.imported_module_maturity_counts == {
        "concept_contract_only": 8,
        "implemented_runtime_proxy": 5,
    }
    assert all(
        citation.approval_state is ImportedModuleApprovalState.NOT_APPROVED
        for citation in citations
    )
    assert [citation.packet_id for citation in citations] == [
        result.contract_packet_ids[slug] for slug in EXPECTED_TRANCHE_A_ORDER
    ]
    citation_index = {citation.canonical_slug: citation for citation in citations}
    assert (
        citation_index["volume_spike_filter"].maturity_state
        is ImportedModuleMaturityState.CONCEPT_CONTRACT_ONLY
    )
    assert (
        citation_index["event_flag_capture"].maturity_state
        is ImportedModuleMaturityState.IMPLEMENTED_RUNTIME_PROXY
    )
    assert any(
        fence.status == "fenced_missing_source"
        for fence in citation_index["volume_spike_filter"].dependency_fences
    )


def test_replay_run_result_carries_tranche_a_citations_without_changing_report_shape() -> (
    None
):
    """Gate 17 should carry tranche-A citation state into replay results without drift."""

    service = ReplayComparisonService(Settings())
    runs, report = service.compare_from_fixture_pack(FIXTURE_PACK)

    run = next(
        run
        for run in runs
        if run.coefficient_set_id == "full_stack_base" and run.scenario_id == "trend"
    )
    assert [
        citation.canonical_slug for citation in run.imported_module_citations
    ] == EXPECTED_TRANCHE_A_ORDER
    assert (
        run.imported_module_maturity_counts
        == run.review.imported_module_maturity_counts
    )
    assert run.imported_module_maturity_counts["concept_contract_only"] >= 1
    assert all(
        citation.approval_state is ImportedModuleApprovalState.NOT_APPROVED
        for citation in run.imported_module_citations
    )
    assert report.reports["full_stack_base"].run_count == 4
    assert report.reports["defensive_stack_tight"].run_count == 4
