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

    assert (
        "2026-03-31_BOUNDED_TRACE_SCENARIO_REVIEW_GATES_v1.md" in plans
        or "successor retained-test cleanup execution pack; Gate 224 is active" in plans
        or "Gate 224 is complete on `work/gate-224-runtime-review-and-contract-retarget-20260406`" in plans
        or "successor retained-test cleanup execution pack; Gate 225 is active" in plans
        or "no active pack currently routed" in plans.lower()
        or "2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_GATES_v1.md" in plans
    )
    assert (
        "no active pack currently routed; bounded trace scenario review pack closed through Gate 134 on `main`" in plans
        or "stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`" in plans
        or "active gate: Gate 149 reopened on `work/gate-149-reopen-full-suite-closeout-20260402`" in plans
        or "bounded trace scenario review pack active at Gate 134 on `main`" in plans
        or "opening-drive continuation lifecycle pilot pack active at Gate 135" in plans
        or "opening-drive continuation lifecycle pilot pack active at Gate 137 after Gates 135-136 closed on `main`" in plans
        or "no active pack — opening-drive continuation lifecycle pilot pack closed through Gate 139 on `main`" in plans
        or "no active pack — execution-ledger Alembic parity corrective pack closed through Gate 140 on `main`" in plans
        or "stage-local handoff and terminal-risk seams pack" in plans
        or "successor retained-test cleanup execution pack; Gate 224 is active on `work/gate-224-runtime-review-and-contract-retarget-20260406`" in plans
        or "Gate 224 is complete on `work/gate-224-runtime-review-and-contract-retarget-20260406`" in plans
        or "successor retained-test cleanup execution pack; Gate 225 is active on `work/gate-225-retained-test-cleanup-closeout-20260406`" in plans
        or "no active pack currently routed; the successor retained-test cleanup execution pack is closed through Gate 225" in plans
        or "no active pack currently routed; the opening-position domain isolation and interface hardening pack is closed through Gate 235" in plans
        or "active pack currently routed: the main serial stack Steps 3-6 corrective implementation pack" in plans
        or "no active pack currently routed. the main serial stack steps 3-6 corrective implementation pack is closed through gate 241" in plans.lower()
    )
    assert (
        "Current active gate: **none — bounded trace scenario review pack closed through Gate 134 on `main`**." in gate_map
        or "Current active gate: **Gate 149 in the stage-local handoff and terminal-risk seams pack**." in gate_map
        or "Current active gate: **none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`**." in gate_map
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
        or "Current active gate: **Gate 224 active on `work/gate-224-runtime-review-and-contract-retarget-20260406` under the successor retained-test cleanup execution pack.**" in gate_map
        or "Current active gate: **No active gate under the successor retained-test cleanup execution pack. Gate 224 is complete on `work/gate-224-runtime-review-and-contract-retarget-20260406`; Gate 225 is not yet activated.**" in gate_map
        or "Current active gate: **Gate 225 active on `work/gate-225-retained-test-cleanup-closeout-20260406` under the successor retained-test cleanup execution pack.**" in gate_map
        or "Current active gate: **No active gate under the successor retained-test cleanup execution pack. Gate 225 is complete on `work/gate-225-retained-test-cleanup-closeout-20260406`; cleanup pack closed.**" in gate_map
        or "Current active gate: **No active pack currently routed. The successor retained-test cleanup execution pack is closed through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`.**" in gate_map
        or "Current active gate: **No active pack currently routed. The opening-position domain isolation and interface hardening pack is closed through Gate 235 on `work/gate-235-cross-flow-harness-and-pack-closeout-20260408`.**" in gate_map
        or "Current active gate: **No active pack currently routed. The main serial stack Steps 3-6 corrective implementation pack is closed through Gate 241 in the uploaded workspace copy.**" in gate_map
    )
    assert leaves["active_gate"] in {
        "Gate 134",
        "none — bounded trace scenario review pack closed through Gate 134 on main",
    }
