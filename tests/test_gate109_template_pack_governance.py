"""Template-pack governance checks."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = REPO_ROOT / "docs/planning/tranche_briefing_template_pack"
README = PACK_DIR / "README.md"
HOWTO = PACK_DIR / "HOW_TO_USE_THESE_DOCUMENTS.md"
DOCTRINE = PACK_DIR / "2026-03-29_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v2.md"
LEAVES_TEMPLATE = PACK_DIR / "2026-03-29_GENERIC_LEAVES_TEMPLATE_v2.json"
EXECUTION_LOG_TEMPLATE = PACK_DIR / "2026-03-30_GENERIC_EXECUTION_LOG_TEMPLATE_v1.md"
DOCUMENT_TOUCH_TEMPLATE = PACK_DIR / "2026-03-30_GENERIC_DOCUMENT_TOUCH_CHECKLIST_TEMPLATE_v1.md"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"


CURRENT_GATE_PATTERN = re.compile(r"Current active gate: \*\*.+\*\*\.", re.DOTALL)


def test_template_pack_includes_process_law_and_state_integrity_templates() -> None:
    readme = README.read_text(encoding="utf-8")
    howto = HOWTO.read_text(encoding="utf-8")
    doctrine = DOCTRINE.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES_TEMPLATE.read_text(encoding="utf-8"))

    assert EXECUTION_LOG_TEMPLATE.is_file()
    assert DOCUMENT_TOUCH_TEMPLATE.is_file()
    assert "document-touch checklist" in readme
    assert "latest closed pack as evidence input only" in readme
    assert "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md" in howto
    assert "contradiction report" in howto
    assert "bounded-scope note" in doctrine
    assert "State-integrity law" in (REPO_ROOT / "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md").read_text(encoding="utf-8")
    assert leaves["global_rules"]["completed_and_remaining_leaf_sets_must_be_disjoint"] is True


def test_gate109_governance_row_persists_and_gate_map_uses_generic_current_gate_marker() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")

    assert "Current active gate: **" in gate_map
    assert (
        "Current active gate: **No active pack currently routed. The successor retained-test cleanup execution pack is closed through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`.**"
        in gate_map
        or "Current active gate: **No active pack currently routed. The opening-position domain isolation and interface hardening pack is closed through Gate 235 on `work/gate-235-cross-flow-harness-and-pack-closeout-20260408`.**"
        in gate_map
        or CURRENT_GATE_PATTERN.search(gate_map)
    )
    assert "| Gate 109 | complete on `main` |" in gate_map
    assert "## Active pack" in plans
