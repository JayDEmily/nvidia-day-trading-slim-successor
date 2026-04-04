"""Gate 103 raw/prepared parity checks."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime, DeskCognitionRuntimeResult
from nvda_desk.services.real_data_loader import RealDataLoaderService
from nvda_desk.testing.canonical_raw_runtime_harness import CanonicalRawRuntimeHarnessInput, CanonicalRawRuntimeHarnessService
from nvda_desk.testing.canonical_runtime_harness import CanonicalRuntimeHarnessInput, CanonicalRuntimeHarnessService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

FIXTURE_PACK_PATH = Path("fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json")
RAW_BUNDLE_PATH = Path("fixtures/real_data/gate_101_canonical_raw_runtime_bundle.json")
GATE103_DOC = Path("docs/planning/2026-03-30_GATE103_RAW_PREPARED_PARITY.md")


def _prepared_harness() -> CanonicalRuntimeHarnessInput:
    pack = RealDataLoaderService().load_fixture_pack(FIXTURE_PACK_PATH)
    supportive = supportive_runtime_fixture()
    return CanonicalRuntimeHarnessService().build(
        dataset_id=pack.prepared_dataset.dataset_id,
        snapshot=pack.prepared_dataset.snapshots[0],
        regime_input=supportive.regime_input,
        inventory_state=supportive.inventory_state,
        risk_budget_remaining_pct=supportive.risk_budget_remaining_pct,
    )


def _raw_harness() -> CanonicalRawRuntimeHarnessInput:
    pack = RealDataLoaderService().load_fixture_pack(FIXTURE_PACK_PATH)
    supportive = supportive_runtime_fixture()
    return CanonicalRawRuntimeHarnessService().build_from_path(
        raw_bundle_path=RAW_BUNDLE_PATH,
        dataset_id=pack.prepared_dataset.dataset_id,
        regime_input=supportive.regime_input,
        inventory_state=supportive.inventory_state,
        risk_budget_remaining_pct=supportive.risk_budget_remaining_pct,
    )


def _run(harness: CanonicalRuntimeHarnessInput | CanonicalRawRuntimeHarnessInput) -> DeskCognitionRuntimeResult:
    return DeskCognitionRuntime(Settings()).run(
        temporal_input=harness.temporal_input,
        regime_input=harness.regime_input,
        options_flow_input=harness.options_flow_input,
        inventory_state=harness.inventory_state,
        risk_budget_remaining_pct=harness.risk_budget_remaining_pct,
    )


def test_raw_and_prepared_canonical_harnesses_match_on_comparable_surfaces() -> None:
    prepared = _prepared_harness()
    raw = _raw_harness()

    assert raw.sequence_id == prepared.sequence_id == "seq-opening-balance"
    assert raw.temporal_input == prepared.temporal_input
    assert raw.options_flow_input == prepared.options_flow_input
    assert raw.regime_input == prepared.regime_input
    assert raw.inventory_state == prepared.inventory_state
    assert raw.risk_budget_remaining_pct == prepared.risk_budget_remaining_pct


def test_raw_and_prepared_runtime_results_match_on_frozen_lawful_surfaces() -> None:
    prepared_result = _run(_prepared_harness())
    raw_result = _run(_raw_harness())

    assert raw_result.stage_packet_ids == prepared_result.stage_packet_ids
    assert raw_result.packet_lineage == prepared_result.packet_lineage
    assert raw_result.review.review_packet == prepared_result.review.review_packet
    assert raw_result.review.effective_policy == prepared_result.review.effective_policy
    assert raw_result.review.review_lineage == prepared_result.review.review_lineage
    assert raw_result.temporal.event_window_state == prepared_result.temporal.event_window_state
    assert raw_result.options_flow.options_behavior_cluster == prepared_result.options_flow.options_behavior_cluster
    assert raw_result.posture.permission_state == prepared_result.posture.permission_state
    assert raw_result.execution.target_fresh_deployable_pct == prepared_result.execution.target_fresh_deployable_pct
    assert raw_result.execution.active_playbook_ids == prepared_result.execution.active_playbook_ids
    assert raw_result.execution.pre_final_risk_active_playbook_ids == prepared_result.execution.pre_final_risk_active_playbook_ids
    assert raw_result.execution.final_risk_join == prepared_result.execution.final_risk_join
    assert raw_result.review.review_packet["final_risk_join"] == prepared_result.review.review_packet["final_risk_join"]
    assert raw_result.review.summary == prepared_result.review.summary


def test_gate103_doc_freezes_bounded_parity_basis() -> None:
    doc = GATE103_DOC.read_text(encoding="utf-8")

    assert "Status: Gate 103 complete on `main`; Gate 104 is the next active gate in the successor testing pack" in doc
    assert "The canonical raw-path harness and the canonical prepared-runtime harness are semantically equal on the bounded comparable surface frozen here." in doc
    assert "Gate 104 may begin" in doc
