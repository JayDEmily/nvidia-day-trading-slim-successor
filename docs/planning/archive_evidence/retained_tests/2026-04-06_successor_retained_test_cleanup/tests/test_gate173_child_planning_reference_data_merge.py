"""Gate 173 child planning/reference-data merge checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAVES = REPO_ROOT / "docs/planning/2026-04-02_MASTER_CHILD_PARALLEL_RISK_INTEGRATION_LEAVES_v1.json"
RECEIPT = REPO_ROOT / "docs/planning/2026-04-02_GATE173_CHILD_PLANNING_REFERENCE_DATA_MERGE.md"
CONFIG = REPO_ROOT / "config/README.md"
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
OPERATING = REPO_ROOT / "docs/02_OPERATING_MODEL.md"
REF_DOC = REPO_ROOT / "docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md"
VOCAB_JSON = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"
WORKBOOK = REPO_ROOT / "data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx"
OLD_WORKBOOK = REPO_ROOT / "docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx"


def test_gate173_marks_child_merge_complete() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    assert "Gate 173" in leaves["completed_gate_ids"]
    assert all(
        leaves["leaves"][leaf_id]["status"] == "complete"
        for leaf_id in leaves["leaf_order"]
        if leaves["leaves"][leaf_id]["gate"] == "Gate 173"
    )


def test_gate173_merges_workbook_authority_and_vocab_surfaces() -> None:
    config = CONFIG.read_text(encoding="utf-8")
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating = OPERATING.read_text(encoding="utf-8")
    ref_doc = REF_DOC.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")
    vocab = json.loads(VOCAB_JSON.read_text(encoding="utf-8"))

    assert WORKBOOK.exists()
    assert OLD_WORKBOOK.exists()
    assert "signal_coefficient_reference_workbook" in config
    assert "governed live reference ledger" in normative
    assert "docs/reference/SIGNAL_WORKBOOK_AUTHORITY.md" in normative
    assert "starts with session start" in operating
    assert "canonical live reference ledger" in ref_doc
    assert "archive evidence only" in ref_doc
    assert "Generator/vocabulary surfaces" in receipt
    assert "Active-lineage rewires completed here" in receipt
    index = {entry["canonical_slug"]: entry for entry in vocab["entries"]}
    assert index["independent_parallel_risk_lane"]["category"] == "workflow"
    assert index["signal_coefficient_reference_workbook"]["maps_to_contract"] == str(WORKBOOK.relative_to(REPO_ROOT))
