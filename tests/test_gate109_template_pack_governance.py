"""Gate 109 template-pack canonisation checks."""

from __future__ import annotations

import json
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

ALLOWED_CURRENT_GATE_MARKERS = {
    "Current active gate: **Gate 110 in the repo-process governance pack**.",
    "Current active gate: **Gate 111 in the repo-process governance pack**.",
    "Current active gate: **Gate 112 in the repo-process governance pack**.",
    "Current active gate: **none — repo-process governance pack closed through Gate 112 on `main`**.",
    "Current active gate: **none — execution-authority microtranche closed through Gate 113 on `main`**.",
    "Current active gate: **none — research-mode clarity microtranche closed through Gate 114 on `main`**.",
    "Current active gate: **Gate 115 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 116 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 117 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 118 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 119 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 120 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 121 in the historical-evaluation readiness pack**.",
    "Current active gate: **none — historical-evaluation readiness pack closed through Gate 121 on `main`**.",
    "Current active gate: **Gate 122 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 123 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 124 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 125 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 126 in the signal-coefficient authority pack**.",
    "Current active gate: **Gate 127 in the signal-coefficient authority pack**.",
    "Current active gate: **none — signal-coefficient authority pack closed through Gate 127 on `main`**.",
}


def test_template_pack_includes_process_law_and_missing_templates() -> None:
    readme = README.read_text(encoding="utf-8")
    howto = HOWTO.read_text(encoding="utf-8")
    doctrine = DOCTRINE.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES_TEMPLATE.read_text(encoding="utf-8"))

    assert EXECUTION_LOG_TEMPLATE.is_file()
    assert DOCUMENT_TOUCH_TEMPLATE.is_file()
    assert "document-touch checklist" in readme
    assert "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md" in howto
    assert "Document-touch checklist requirement" in doctrine
    assert leaves["global_rules"]["document_touch_checklist_required"] is True


def test_governance_pack_advances_to_gate110_or_later() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")

    assert ("- none" in plans) or ("2026-03-30_HISTORICAL_EVALUATION_READINESS_GATES_v1.md" in plans) or ("closed through Gate 112" in plans)
    assert any(marker in gate_map for marker in ALLOWED_CURRENT_GATE_MARKERS)
    assert "| Gate 109 | complete on `main` |" in gate_map
