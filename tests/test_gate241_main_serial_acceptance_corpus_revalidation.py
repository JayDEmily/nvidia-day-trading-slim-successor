"""Gate 241 acceptance-corpus revalidation and pack-closeout checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.testing.bounded_trace_review import BoundedTraceReviewService

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = REPO_ROOT / "fixtures" / "trace_review" / "gate_132_bounded_trace_fixture_pack.json"
REPORT_JSON = REPO_ROOT / "fixtures" / "trace_review" / "gate_134_bounded_trace_report.json"
REPORT_MD = REPO_ROOT / "docs" / "status" / "2026-03-31_BOUNDED_TRACE_SCENARIO_REVIEW_REPORT.md"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_EXECUTION_LOG_v1.md"


def test_gate241_pack_closeout_control_surfaces_are_truthful() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "- none" in plans
    assert "main serial stack Steps 3-6 corrective implementation pack is closed through Gate 241" in plans
    assert "Current active gate: **No active pack currently routed. The main serial stack Steps 3-6 corrective implementation pack is closed through Gate 241 in the uploaded workspace copy.**" in gate_map
    assert leaves["active_gate"] == "none"
    assert leaves["pending_gate_ids"] == []
    assert leaves["remaining_leaf_ids"] == []
    assert leaves["completed_gate_ids"] == [
        "Gate 236",
        "Gate 237",
        "Gate 238",
        "Gate 239",
        "Gate 240",
        "Gate 241",
    ]
    assert execution_log.startswith("# 2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_EXECUTION_LOG_v1")
    assert "Status: closed execution log retained as evidence" in execution_log
    assert "Gate 241 closeout proof" in execution_log


def test_gate241_pre_fix_or_regression_witness_is_recorded_as_a_corrected_acceptance_outcome() -> None:
    report = BoundedTraceReviewService(Settings()).run_fixture_pack(PACK_PATH)
    runs = {run.scenario_id: run for run in report.runs}

    assert runs["clear_window_continuation"].active_playbook_ids == ["continuation_ladder"]
    assert runs["clear_window_continuation"].target_fresh_deployable_pct == 35.0
    assert runs["clear_window_continuation"].final_risk_action == "allow"
    assert runs["mild_down_block"].final_risk_action == "block"
    assert runs["mild_down_block"].permission_state == "derisk"


def test_gate241_trace_revalidation_matches_checked_in_acceptance_artifacts() -> None:
    service = BoundedTraceReviewService(Settings())
    report = service.run_fixture_pack(PACK_PATH)
    actual_json = json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True) + "\n"
    actual_md = service.render_markdown_report(report) + "\n"

    assert REPORT_JSON.read_text(encoding="utf-8") == actual_json
    assert REPORT_MD.read_text(encoding="utf-8") == actual_md


def test_gate241_perturbation_or_repeatability_slice_is_deterministic() -> None:
    service = BoundedTraceReviewService(Settings())
    first = service.run_fixture_pack(PACK_PATH).model_dump(mode="json")
    second = service.run_fixture_pack(PACK_PATH).model_dump(mode="json")

    assert first == second
