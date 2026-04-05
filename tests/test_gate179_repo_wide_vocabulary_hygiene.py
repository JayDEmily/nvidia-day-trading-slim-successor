"""Gate 179 repo-wide vocabulary and workbook-path hygiene checks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from nvda_desk.schemas.parallel_risk import ParallelRiskLanePacket

REPO_ROOT = Path(__file__).resolve().parents[1]

VOCAB = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE179_REPO_WIDE_VOCABULARY_HYGIENE.md"
CANONICAL_WORKBOOK = "data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx"
OLD_WORKBOOK = "docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx"
ALLOWED_ALIAS_FILES = {
    "scripts/build_canonical_vocabulary.py",
    "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json",
    "tests/test_gate157_parallel_risk_lane_foundation_bootstrap.py",
    "tests/test_gate158_co_resident_parallel_risk_lane_law.py",
    "tests/test_gate179_repo_wide_vocabulary_hygiene.py",
    "docs/planning/2026-04-02_GATE179_REPO_WIDE_VOCABULARY_HYGIENE.md",
    "docs/planning/2026-04-02_GATE180_MASTER_CHILD_INTEGRATION_AUDIT_AND_CLOSEOUT.md",
}
ALLOWED_OLD_WORKBOOK_FILES = {
    "CHANGELOG.jsonl",
    "tests/test_testing_phase0_foundation.py",
    "tests/test_gate95_phase0_closeout.py",
    "tests/test_gate157_coefficient_architecture_consolidation_pack_planning.py",
    "tests/test_gate157_parallel_risk_lane_foundation_bootstrap.py",
    "tests/test_gate159_workbook_lineage_and_consolidation_audit.py",
    "tests/test_gate173_child_planning_reference_data_merge.py",
    "tests/test_gate179_repo_wide_vocabulary_hygiene.py",
    "docs/planning/2026-03-30_PHASE0_SIGNAL_WORKBOOK_AUDIT.json",
    "docs/planning/2026-03-30_PHASE0_SIGNAL_WORKBOOK_AUDIT.md",
    "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md",
    "docs/planning/2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_SCOPE_NOTE_v1.md",
    "docs/planning/2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_GATES_v1.md",
    "docs/planning/2026-04-02_GATE157_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_PACK_BOOTSTRAP.md",
    "docs/planning/2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_DOCUMENT_TOUCH_CHECKLIST_v1.md",
    "docs/planning/2026-04-02_COEFFICIENT_ARCHITECTURE_CONSOLIDATION_LEAVES_v1.json",
    "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_GATES_v1.md",
    "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_SCOPE_NOTE_v1.md",
    "docs/planning/2026-04-02_POLICY_TEMPORAL_OBSERVABILITY_SUCCESSOR_DOCUMENT_TOUCH_CHECKLIST_v1.md",
    "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_GATES_v1.md",
    "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_LEAVES_v1.json",
    "docs/planning/2026-04-02_GATE159_WORKBOOK_LINEAGE_AND_CONSOLIDATION_AUDIT.md",
    "docs/planning/2026-04-02_GATE160_GOVERNED_SIGNAL_COEFFICIENT_REFERENCE_WORKBOOK_LAW.md",
    "docs/planning/2026-04-02_GATE164_PARALLEL_RISK_LANE_FOUNDATION_ANTI_DRIFT_CLOSEOUT.md",
    "docs/planning/2026-04-02_GATE173_CHILD_PLANNING_REFERENCE_DATA_MERGE.md",
    "docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md",
    "docs/planning/2026-04-02_GATE179_REPO_WIDE_VOCABULARY_HYGIENE.md",
    "docs/planning/2026-04-02_GATE180_MASTER_CHILD_INTEGRATION_AUDIT_AND_CLOSEOUT.md",
}
ALLOWED_DISALLOWED_PHRASE_FILES = {
    "docs/01_NORMATIVE.md",
    "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md",
    "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_GATES_v1.md",
    "docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_LEAVES_v1.json",
    "scripts/build_canonical_vocabulary.py",
    "tests/test_gate157_parallel_risk_lane_foundation_bootstrap.py",
    "tests/test_gate158_co_resident_parallel_risk_lane_law.py",
    "tests/test_gate174_parallel_risk_lane_input_contract.py",
    "src/nvda_desk/services/parallel_risk_lane.py",
    "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_GATES_v1.md",
    "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_LEAVES_v1.json",
    "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_SCOPE_NOTE_v1.md",
    "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_EXECUTION_LOG_v1.md",
    "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_GATES_v1.md",
    "docs/planning/2026-04-02_PARALLEL_RISK_LANE_FOUNDATION_LEAVES_v1.json",
    "docs/planning/2026-04-02_GATE157_PARALLEL_RISK_LANE_FOUNDATION_BOOTSTRAP.md",
    "docs/planning/2026-04-02_GATE158_CO_RESIDENT_PARALLEL_RISK_LANE_LAW.md",
    "docs/planning/2026-04-02_GATE174_PARALLEL_RISK_LANE_INPUT_CONTRACT.md",
    "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json",
    "tests/test_gate179_repo_wide_vocabulary_hygiene.py",
    "tests/test_gate190_capital_deployment_authority_integration.py",
    "docs/planning/2026-04-02_GATE179_REPO_WIDE_VOCABULARY_HYGIENE.md",
    "docs/planning/2026-04-02_GATE180_MASTER_CHILD_INTEGRATION_AUDIT_AND_CLOSEOUT.md",
}

def _entries_by_slug() -> dict[str, dict[str, object]]:
    entries = cast(list[dict[str, object]], json.loads(VOCAB.read_text(encoding="utf-8"))["entries"])
    return {cast(str, entry["canonical_slug"]): entry for entry in entries}

def _text_occurrence_files(term: str) -> set[str]:
    matches: set[str] = set()
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".xlsx", ".zip", ".pyc"}:
            continue
        if any(part in {".pytest_cache", "__pycache__", ".git", ".venv", ".hypothesis", ".mypy_cache", ".ruff_cache"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if term in text:
            matches.add(path.relative_to(REPO_ROOT).as_posix())
    return matches

def test_gate179_uses_canonical_dictionary_entries_for_lane_and_workbook() -> None:
    entries = _entries_by_slug()
    lane = cast(dict[str, Any], entries["independent_parallel_risk_lane"])
    workbook = cast(dict[str, Any], entries["signal_coefficient_reference_workbook"])

    assert lane["canonical_label"] == "Independent Parallel Risk Lane"
    assert "parallel risk pipeline" in lane["allowed_aliases"]
    assert "co-resident risk lane" in lane["allowed_aliases"]
    assert "step_1_1" in lane["disallowed_phrases"]
    assert "step_8" in lane["disallowed_phrases"]
    assert "eighth_stage" in lane["disallowed_phrases"]
    assert workbook["maps_to_contract"] == CANONICAL_WORKBOOK
    assert ParallelRiskLanePacket.model_fields["lane_id"].default == "independent_parallel_risk_lane"

def test_gate179_active_authority_surfaces_point_to_canonical_workbook() -> None:
    files = [
        REPO_ROOT / "docs/01_NORMATIVE.md",
        REPO_ROOT / "config/README.md",
        REPO_ROOT / "docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md",
        REPO_ROOT / "scripts/build_canonical_vocabulary.py",
        REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json",
        REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_GATES_v1.md",
        REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_LEAVES_v1.json",
    ]
    for path in files:
        assert CANONICAL_WORKBOOK in path.read_text(encoding="utf-8")

def test_gate179_alias_and_legacy_workbook_occurrences_are_classified_not_ambient() -> None:
    assert _text_occurrence_files("parallel risk pipeline") <= ALLOWED_ALIAS_FILES
    assert _text_occurrence_files("co-resident risk lane") <= ALLOWED_ALIAS_FILES
    assert _text_occurrence_files(OLD_WORKBOOK) <= ALLOWED_OLD_WORKBOOK_FILES
    assert _text_occurrence_files("step_1_1") <= ALLOWED_DISALLOWED_PHRASE_FILES
    assert _text_occurrence_files("step_8") <= ALLOWED_DISALLOWED_PHRASE_FILES
    assert _text_occurrence_files("eighth_stage") <= ALLOWED_DISALLOWED_PHRASE_FILES

def test_gate179_receipt_records_repo_wide_scan_and_vocabulary_boundaries() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    assert "Independent Parallel Risk Lane" in receipt
    assert "Signal-Coefficient Reference Workbook" in receipt
    assert CANONICAL_WORKBOOK in receipt
    assert OLD_WORKBOOK in receipt
    assert "allowed aliases" in receipt.lower()
    assert "disallowed phrases" in receipt.lower()
    assert "whole-repo scan" in receipt.lower()
