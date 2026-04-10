"""Gate 254 workflow-law and template-pack refresh evidence checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAVES = REPO_ROOT / "docs/planning/2026-04-10_WORKFLOW_LAW_AND_TEMPLATE_PACK_REFRESH_LEAVES_v1.json"
EXEC_LOG = REPO_ROOT / "docs/planning/2026-04-10_WORKFLOW_LAW_AND_TEMPLATE_PACK_REFRESH_EXECUTION_LOG_v1.md"
CONTRADICTION = REPO_ROOT / "docs/planning/2026-04-10_WORKFLOW_LAW_AND_TEMPLATE_PACK_REFRESH_CONTRADICTION_REPORT_v1.md"
PROCESS_LAW = REPO_ROOT / "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md"


def test_gate254_evidence_pack_is_closed_in_its_own_surfaces() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXEC_LOG.read_text(encoding="utf-8")

    assert leaves["active_gate"] == "none"
    assert leaves["completed_gate_ids"] == ["Gate 254"]
    assert leaves["remaining_leaf_ids"] == []
    assert "Closed through Gate 254" in execution_log


def test_gate254_contradiction_and_continuity_additions_are_preserved() -> None:
    process_law = PROCESS_LAW.read_text(encoding="utf-8")
    contradiction = CONTRADICTION.read_text(encoding="utf-8")

    assert "docs/TESTING_AND_PROMOTION.md" in process_law
    assert "## Controlled continuity execution packs" in process_law
    assert "## Closed-world leaf requirement" in process_law
    assert "would therefore regress the later checkpoint-integrity/testing-doctrine authority" in contradiction


def test_gate254_template_pack_current_generation_exists() -> None:
    pack = REPO_ROOT / "docs/planning/tranche_briefing_template_pack"
    assert (pack / "2026-04-06_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v3.md").is_file()
    assert (pack / "2026-04-06_GENERIC_GATE_TEMPLATE_v3.md").is_file()
    assert (pack / "2026-04-06_GENERIC_LEAVES_TEMPLATE_v3.json").is_file()
    assert (pack / "2026-04-06_GENERIC_EXECUTION_LOG_TEMPLATE_v2.md").is_file()
    assert (pack / "2026-04-06_GENERIC_DOCUMENT_TOUCH_CHECKLIST_TEMPLATE_v2.md").is_file()
    assert (pack / "2026-04-06_WORKED_EXAMPLE_CONTROLLED_CONTINUITY_EXECUTION_PACK_SKELETON_v1.md").is_file()
