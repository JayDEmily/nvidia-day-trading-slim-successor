"""Gate 102 canonical raw-path harness checks."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.testing.canonical_raw_runtime_harness import CanonicalRawRuntimeHarnessService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

RAW_BUNDLE_PATH = Path("fixtures/real_data/gate_101_canonical_raw_runtime_bundle.json")
GATE102_DOC = Path("docs/planning/2026-03-30_GATE102_CANONICAL_RAW_PATH_HARNESS.md")


def _canonical_raw_harness():
    supportive = supportive_runtime_fixture()
    return CanonicalRawRuntimeHarnessService().build_from_path(
        raw_bundle_path=RAW_BUNDLE_PATH,
        dataset_id="gate102_canonical_raw_runtime",
        regime_input=supportive.regime_input,
        inventory_state=supportive.inventory_state,
        risk_budget_remaining_pct=supportive.risk_budget_remaining_pct,
    )


def test_canonical_raw_runtime_harness_proves_the_checked_in_raw_path() -> None:
    harness = _canonical_raw_harness()

    assert harness.fixture_id == "canonical_raw_runtime_harness"
    assert harness.dataset_id == "gate102_canonical_raw_runtime"
    assert harness.raw_bundle_path == RAW_BUNDLE_PATH.as_posix()
    assert harness.raw_bundle.provenance.symbol == "NVDA"
    assert len(harness.raw_bundle.bars) == 4
    assert len(harness.raw_bundle.option_chain_snapshots) == 3
    assert len(harness.raw_bundle.events) == 2
    assert harness.prepared_snapshot_count == 3
    assert harness.sanity_report.prepared_snapshot_count == 3
    assert harness.sanity_report.aligned_bar_coverage_pct == 75.0
    assert harness.sanity_report.aligned_chain_coverage_pct == 100.0
    assert "orphan_bar_count:1" in harness.sanity_report.reasons
    assert harness.sequence_id == "seq-opening-balance"
    assert harness.temporal_input.ts == harness.source_snapshot_ts
    assert harness.temporal_input.live_event_snapshot is not None
    assert harness.options_flow_input.spot_price == 116.0
    assert len(harness.options_flow_input.repeated_snapshot_sequence) == 3


def test_canonical_raw_runtime_harness_run_is_deterministic_and_freezes_outputs() -> None:
    harness = _canonical_raw_harness()
    runtime = DeskCognitionRuntime(Settings())

    first = runtime.run(
        temporal_input=harness.temporal_input,
        regime_input=harness.regime_input,
        options_flow_input=harness.options_flow_input,
        inventory_state=harness.inventory_state,
        risk_budget_remaining_pct=harness.risk_budget_remaining_pct,
    )
    second = runtime.run(
        temporal_input=harness.temporal_input,
        regime_input=harness.regime_input,
        options_flow_input=harness.options_flow_input,
        inventory_state=harness.inventory_state,
        risk_budget_remaining_pct=harness.risk_budget_remaining_pct,
    )

    assert first.stage_packet_ids == second.stage_packet_ids
    assert first.packet_lineage == second.packet_lineage
    assert first.review.review_packet == second.review.review_packet

    assert first.temporal.event_window_state == "event_imminent_window"
    assert first.options_flow.options_behavior_cluster == "anchored_translation_tension"
    assert first.posture.permission_state.value == "allow"
    assert round(first.execution.target_fresh_deployable_pct, 4) == 0.0
    assert first.eligibility.add_candidates == []
    assert first.execution.active_playbook_ids == []
    assert first.review.summary == "window=early_anchor; permission=allow; families=['none']; setups=['none']; playbooks=['none']; final_risk=derisk"
    assert first.packet_lineage[0] == first.stage_packet_ids["temporal"]
    assert first.packet_lineage[-1] == first.stage_packet_ids["review"]


def test_gate102_doc_freezes_the_raw_path_basis_and_next_step() -> None:
    doc = GATE102_DOC.read_text(encoding="utf-8")

    assert "Status: Gate 102 complete on `main`; Gate 103 is the next active gate in the successor testing pack" in doc
    assert "raw bundle -> prepared runtime dataset -> cognition inputs -> review outputs" in doc
    assert "No prepared snapshot was injected by hand" in doc
    assert "Gate 103 may begin" in doc
