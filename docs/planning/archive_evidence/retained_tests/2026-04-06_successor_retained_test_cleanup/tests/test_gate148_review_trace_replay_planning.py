"""Gate 148 planning and closeout checks."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RECEIPT = (
    REPO_ROOT
    / "docs/planning/2026-04-01_GATE148_REVIEW_TRACE_REPLAY_AND_LEGACY_EXPECTATION_RECONCILIATION.md"
)
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"


def test_gate148_receipt_freezes_review_and_trace_consumer_scope_without_new_vocabulary() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "No new governed vocabulary is admitted in Gate 148." in receipt
    assert 'ReviewExplanationOutput.review_packet["admissibility_surface"]' in receipt
    assert "BoundedTraceRunResult.admissibility_surface" in receipt
    assert "BoundedTraceRunResult.terminal_risk_application" in receipt
    assert "final_risk_join" in receipt


def test_gate148_closeout_advances_router_truth() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")

    assert (
        "active gate: Gate 149 on `main`" in plans
        or "closed through Gate 149 on `main`" in plans
        or "active gate: Gate 149 reopened on `work/gate-149-reopen-full-suite-closeout-20260402`"
        in plans
        or "active gate: Gate 151 on `work/gate-150-corrective-successor-pack-20260402`" in plans
        or "active gate: Gate 152 on `main`" in plans
        or "active gate: Gate 153 on `main`" in plans
        or "active gate: Gate 154 on `main`" in plans
        or "active gate: Gate 155 on `main`" in plans
        or "active gate: Gate 156 on `main`" in plans
        or "no active pack currently routed; stage-local handoff corrective successor pack closed through Gate 156 on `main`"
        in plans
    )
    assert (
        "Current active gate: **Gate 149 in the stage-local handoff and terminal-risk seams pack**."
        in gate_map
        or "closed through Gate 149 on `main`" in gate_map
        or "Current active gate: **Gate 151 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 152 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 153 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 154 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 155 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **Gate 156 in the stage-local handoff corrective successor pack**."
        in gate_map
        or "Current active gate: **none — stage-local handoff corrective successor pack closed through Gate 156 on `main`**."
        in gate_map
    )
