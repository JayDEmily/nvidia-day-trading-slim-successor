"""Testing doctrine and Phase 0 workbook-audit guards."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TESTING_DOC = REPO_ROOT / "docs" / "TESTING_AND_PROMOTION.md"
PHASE0_AUDIT_MD = REPO_ROOT / "docs" / "planning" / "2026-03-30_PHASE0_SIGNAL_WORKBOOK_AUDIT.md"
PHASE0_AUDIT_JSON = REPO_ROOT / "docs" / "planning" / "2026-03-30_PHASE0_SIGNAL_WORKBOOK_AUDIT.json"
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "phase0_signal_workbook_audit.py"


def test_testing_doctrine_freezes_phase_sequence_and_anti_patterns() -> None:
    text = TESTING_DOC.read_text(encoding="utf-8")

    assert "Phase 0 — one canonical real-data snapshot viability audit" in text
    assert "Phase 1 — deterministic full-runtime scenario harness from one canonical real-data snapshot" in text
    assert "Phase 2 — invariant and lawful-output testing" in text
    assert "Phase 3 — targeted property and threshold-edge testing" in text
    assert "Phase 4 — transition and adjacent-snapshot testing" in text
    assert "Phase 5 — controlled scenario-matrix expansion" in text
    assert "fabricate missing raw inputs" in text
    assert "coverage percentage as the primary truth metric" in text


def test_phase0_audit_artifacts_record_workbook_failure_honestly() -> None:
    assert PHASE0_AUDIT_MD.exists()
    assert PHASE0_AUDIT_JSON.exists()
    assert AUDIT_SCRIPT.exists()

    audit = json.loads(PHASE0_AUDIT_JSON.read_text(encoding="utf-8"))
    assert audit["artifact"] == "docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx"
    assert audit["sheet_count"] == 20
    assert audit["phase_zero_gate"]["status"] == "fail"
    assert audit["phase_zero_gate"]["single_canonical_real_run_viable"] is False
    assert audit["observed_runtime_surface_presence"]["actual_option_chain_quote_rows_present"] is False
    assert audit["observed_runtime_surface_presence"]["actual_normalised_event_rows_present"] is False
    assert audit["observed_runtime_surface_presence"]["single_mid_session_runtime_snapshot_present"] is False
    assert any("option-chain snapshot rows" in item for item in audit["missing_raw_surfaces"])
    assert any("next_event_at" in item for item in audit["missing_or_unreliable_derived_surfaces"])
