"""Gate 133 bounded trace-review regime checks."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.testing.bounded_trace_review import BoundedTraceReviewService

REPO_ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = REPO_ROOT / "fixtures" / "trace_review" / "gate_132_bounded_trace_fixture_pack.json"
TESTING_DOC = REPO_ROOT / "docs" / "TESTING_AND_PROMOTION.md"


def test_gate133_testing_doctrine_names_the_bounded_trace_review_phase() -> None:
    text = TESTING_DOC.read_text(encoding="utf-8")
    assert "Phase 6 — bounded sibling trace review from one admitted real-data anchor" in text
    assert "4-6 scenarios" in text or "4-6 sibling scenarios" in text
    assert "semantic review evidence only" in text


def test_gate133_runtime_trace_pack_freezes_broad_human_sanity_outcomes() -> None:
    report = BoundedTraceReviewService(Settings()).run_fixture_pack(PACK_PATH)
    runs = {run.scenario_id: run for run in report.runs}

    assert report.scenario_ids == [
        "anchor_event_imminent",
        "clear_window_continuation",
        "lunch_flattened",
        "imminent_pin_derisk",
        "mild_down_block",
    ]
    assert runs["anchor_event_imminent"].final_risk_action == "derisk"
    assert runs["anchor_event_imminent"].active_playbook_ids == []

    assert runs["clear_window_continuation"].final_risk_action == "allow"
    assert runs["clear_window_continuation"].active_playbook_ids == ["continuation_ladder"]
    assert round(runs["clear_window_continuation"].target_fresh_deployable_pct, 4) == 55.0

    assert runs["lunch_flattened"].final_risk_action == "allow"
    assert runs["lunch_flattened"].active_playbook_ids == []

    assert runs["imminent_pin_derisk"].final_risk_action == "derisk"
    assert runs["mild_down_block"].final_risk_action == "block"
    assert runs["mild_down_block"].permission_state == "derisk"
