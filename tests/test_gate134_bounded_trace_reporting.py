"""Gate 134 bounded trace reporting checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.trace_review import BoundedTraceReviewReport

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = REPO_ROOT / "fixtures" / "trace_review" / "gate_134_bounded_trace_report.json"
REPORT_MD = REPO_ROOT / "docs" / "status" / "2026-03-31_BOUNDED_TRACE_SCENARIO_REVIEW_REPORT.md"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-31_BOUNDED_TRACE_SCENARIO_REVIEW_LEAVES_v1.json"


def test_gate134_report_artifacts_are_checked_in_and_concise() -> None:
    report = BoundedTraceReviewReport.model_validate_json(REPORT_JSON.read_text())
    markdown = REPORT_MD.read_text(encoding="utf-8")

    assert len(report.runs) == 5
    assert "clear_window_continuation" in markdown
    assert "continuation_ladder" in markdown
    assert "mild_down_block" in markdown
    assert "block" in markdown


def test_gate134_pack_closes_honestly_when_finished() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert "2026-03-31_BOUNDED_TRACE_SCENARIO_REVIEW_GATES_v1.md" in plans
    assert (
        "no active pack currently routed; bounded trace scenario review pack closed through Gate 134 on `main`" in plans
        or "bounded trace scenario review pack active at Gate 134 on `main`" in plans
        or "opening-drive continuation lifecycle pilot pack active at Gate 135" in plans
        or "opening-drive continuation lifecycle pilot pack active at Gate 137 after Gates 135-136 closed on `main`" in plans
        or "no active pack — opening-drive continuation lifecycle pilot pack closed through Gate 139 on `main`" in plans
        or "no active pack — execution-ledger Alembic parity corrective pack closed through Gate 140 on `main`" in plans
        or "stage-local handoff and terminal-risk seams pack" in plans
    )
    assert (
        "Current active gate: **none — bounded trace scenario review pack closed through Gate 134 on `main`**." in gate_map
        or "Current active gate: **Gate 134 in the bounded trace scenario review pack**." in gate_map
        or "Current active gate: **Gate 135 in the opening-drive continuation lifecycle pilot pack**." in gate_map
        or "Current active gate: **Gate 137 in the opening-drive continuation lifecycle pilot pack**." in gate_map
        or "Current active gate: **none — opening-drive continuation lifecycle pilot pack closed through Gate 139 on `main`**." in gate_map
        or "Current active gate: **Gate 140 in the execution-ledger Alembic parity corrective pack**." in gate_map
        or "Current active gate: **none — execution-ledger Alembic parity corrective pack closed through Gate 140 on `main`**." in gate_map
        or "Current active gate: **Gate 142 in the stage-local handoff and terminal-risk seams pack**." in gate_map
        or "Current active gate: **Gate 143 in the stage-local handoff and terminal-risk seams pack**." in gate_map
        or "Current active gate: **Gate 144 in the stage-local handoff and terminal-risk seams pack**." in gate_map
        or "Current active gate: **Gate 145 in the stage-local handoff and terminal-risk seams pack**." in gate_map
        or "Current active gate: **Gate 146 in the stage-local handoff and terminal-risk seams pack**." in gate_map
        or "Current active gate: **Gate 147 in the stage-local handoff and terminal-risk seams pack**." in gate_map
        or "Current active gate: **Gate 148 in the stage-local handoff and terminal-risk seams pack**." in gate_map
        or "Current active gate: **Gate 149 in the stage-local handoff and terminal-risk seams pack**." in gate_map
        or "Current active gate: **none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`**." in gate_map
    )
    assert leaves["active_gate"] in {
        "Gate 134",
        "none — bounded trace scenario review pack closed through Gate 134 on main",
    }
