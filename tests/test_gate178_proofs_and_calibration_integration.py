"""Gate 178 selective proof and calibration/evaluation-prep checks."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from nvda_desk.config import Settings
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.real_data_loader import RealDataLoaderService
from nvda_desk.testing.canonical_runtime_harness import CanonicalRuntimeHarnessService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

FIXTURE_PACK_PATH = Path("fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json")
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE178_PROOFS_AND_CALIBRATION_INTEGRATION.md"


def _runtime_result():
    pack = RealDataLoaderService().load_fixture_pack(FIXTURE_PACK_PATH)
    supportive = supportive_runtime_fixture()
    harness = CanonicalRuntimeHarnessService().build(
        dataset_id=pack.prepared_dataset.dataset_id,
        snapshot=pack.prepared_dataset.snapshots[0],
        regime_input=supportive.regime_input,
        inventory_state=supportive.inventory_state,
        risk_budget_remaining_pct=supportive.risk_budget_remaining_pct,
    )
    return DeskCognitionRuntime(Settings()).run(
        temporal_input=harness.temporal_input,
        regime_input=harness.regime_input,
        options_flow_input=harness.options_flow_input,
        inventory_state=harness.inventory_state,
        risk_budget_remaining_pct=harness.risk_budget_remaining_pct,
    )


def test_gate178_runtime_exposes_parallel_lane_evaluation_prep_packet() -> None:
    result = _runtime_result()
    packet = result.parallel_risk_calibration
    assert packet is not None
    assert packet.lane_id == "independent_parallel_risk_lane"
    assert packet.implemented_surfaces == [
        "temporal_surface",
        "market_translation_surface",
        "candidate_audit_surface",
    ]
    assert packet.required_receipt_sections == [
        "surface_changes_observed",
        "policy_firing_summary",
        "help_vs_harm_assessment",
        "over_tightening_and_stack_pressure",
        "redundancy_or_dead_weight_findings",
        "danger_or_unstable_behaviour_findings",
        "opportunity_shaping_absence_or_presence",
        "recommended_next_action",
    ]
    assert packet.selective_proof_order == [
        "parallel_risk_runtime_targeted",
        "parallel_risk_review_targeted",
        "imported_child_pack_continuity",
        "vocabulary_build_then_hygiene",
    ]
    surface_ids = [row.surface_id for row in packet.surface_metadata]
    assert surface_ids == packet.implemented_surfaces
    policy_ids = [row.policy_id for row in packet.policy_metadata]
    assert policy_ids == [
        "parallel_risk:temporal_calendar_multi_clock",
        "parallel_risk:market_options_dependency_translation",
        "parallel_risk:candidate_fragility_anti_duplication",
    ]
    assert "calibration_has_not_started" in packet.notes


def test_gate178_receipt_stays_preparatory_and_reuses_gate169_architecture() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    assert "Calibration has not started." in receipt
    assert "Gate 169" in receipt
    assert "independent_parallel_risk_lane" in receipt
    assert "surface_changes_observed" in receipt
    assert "vocabulary build" in receipt.lower()
