from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from nvda_desk.config import Settings
from nvda_desk.schemas.dataset import PreparedRuntimeRegimePacket
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.upstream_signal_ingress import (
    build_market_regime_input,
    build_participation_baseline_packet,
)
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_EXECUTION_LOG_v1.md"
CLOSEOUT = REPO_ROOT / "docs/planning/2026-04-09_GATE252_UPSTREAM_SIGNAL_COMPLETION_CLOSEOUT.md"
CHECKLIST = REPO_ROOT / "docs/planning/2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_DOCUMENT_TOUCH_CHECKLIST_v1.md"
SCOPE = REPO_ROOT / "docs/planning/2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_SCOPE_NOTE_v1.md"
CONTRADICTION = REPO_ROOT / "docs/planning/2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_CONTRADICTION_REPORT_v1.md"


def _supportive_runtime_with_upstream_truth() -> tuple[dict[str, object], dict[str, object]]:
    fixture = supportive_runtime_fixture()
    regime_packet = PreparedRuntimeRegimePacket(
        source_family="fixture_regime_capture",
        source_symbols=["NVDA", "NQ", "ES", "SOX", "VIX", "VVIX", "US10Y", "US2Y", "USDJPY"],
        observed_at=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
        aligned_to_runtime_ts=datetime(2026, 3, 23, 14, 15, tzinfo=UTC),
        alignment_age_seconds=0,
        nvda_return_pct=0.8,
        nq_return_pct=0.5,
        es_return_pct=0.3,
        sox_return_pct=0.9,
        breadth_score=0.67,
        concentration_score=0.41,
        vix_level=18.4,
        vvix_level=84.0,
        us10y=4.22,
        us2y=4.04,
        usdjpy=148.9,
        completeness_state="complete_for_live_ingress",
    )
    regime_input = build_market_regime_input(regime_packet)
    participation_packet = build_participation_baseline_packet(
        ts=fixture.temporal_input.ts,
        interval_volume_shares=1200.0,
        relative_volume_ratio=1.5,
        settings=Settings(),
        calendar_owner_present=True,
        observed_spread_bps=12.5,
        observed_trade_count=42,
    )

    runtime = DeskCognitionRuntime(Settings())
    result = runtime.run(
        temporal_input=fixture.temporal_input.model_copy(
            update={
                "session_bucket_label": participation_packet.session_bucket_label,
                "same_bucket_interval_volume_share_baseline": participation_packet.baseline_interval_volume_share,
                "relative_volume_ratio": participation_packet.relative_volume_ratio,
            }
        ),
        regime_input=regime_input,
        options_flow_input=fixture.options_flow_input.model_copy(
            update={
                "same_bucket_spread_bps": participation_packet.observed_spread_bps,
                "same_bucket_trade_count": participation_packet.observed_trade_count,
            }
        ),
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )
    return (
        {
            "regime_input_present": regime_input is not None,
            "breadth_score": None if regime_input is None else regime_input.breadth_score,
            "concentration_score": None if regime_input is None else regime_input.concentration_score,
            "session_bucket_label": participation_packet.session_bucket_label,
            "baseline_interval_volume_share": participation_packet.baseline_interval_volume_share,
            "observed_spread_bps": participation_packet.observed_spread_bps,
            "observed_trade_count": participation_packet.observed_trade_count,
        },
        {
            "target_fresh_deployable_pct": result.execution.target_fresh_deployable_pct,
            "inventory_action": result.execution.inventory_action,
            "fresh_capital_action": result.execution.fresh_capital_action,
            "review_present": result.review is not None,
        },
    )


def _require_gate252_closeout_state(
    *,
    plans: str,
    gate_map: str,
    leaves: dict[str, object],
    execution_log: str,
    closeout: str,
    checklist: str,
    scope: str,
    contradiction: str,
) -> None:
    if "## Active pack\n\n- none" not in plans:
        raise RuntimeError("CHECKPOINT_FAILURE:gate252.router.no_active_pack")
    if (
        (
            "closed through Gate 252" not in plans
            or "closed through Gate 252" not in gate_map
        )
        and (
            "live prepared-handoff reconciliation pack is closed through Gate 255" not in plans
            or "| Gate 252 | imported prepared handoff state reconciled in the live repo |" not in gate_map
        )
    ):
        raise RuntimeError("CHECKPOINT_FAILURE:gate252.router.closeout_missing")
    if leaves.get("active_gate") != "none":
        raise RuntimeError("CHECKPOINT_FAILURE:gate252.leaves.no_active_gate")
    if leaves.get("pending_gate_ids") != []:
        raise RuntimeError("CHECKPOINT_FAILURE:gate252.leaves.no_pending_gates")
    if leaves.get("remaining_leaf_ids") != []:
        raise RuntimeError("CHECKPOINT_FAILURE:gate252.leaves.no_remaining_leaves")
    if leaves.get("completed_gate_ids") != ["Gate 247", "Gate 248", "Gate 249", "Gate 250", "Gate 251", "Gate 252"]:
        raise RuntimeError("CHECKPOINT_FAILURE:gate252.leaves.completed_gates")
    if "Status: closed execution log retained as evidence" not in execution_log:
        raise RuntimeError("CHECKPOINT_FAILURE:gate252.execution_log.closed_status")
    if "- routing state: `closed`" not in execution_log:
        raise RuntimeError("CHECKPOINT_FAILURE:gate252.execution_log.closed_state")
    if "- active gate: `none`" not in execution_log:
        raise RuntimeError("CHECKPOINT_FAILURE:gate252.execution_log.no_active_gate")
    if "Gate 252 closeout proof receipt" not in execution_log:
        raise RuntimeError("CHECKPOINT_FAILURE:gate252.execution_log.closeout_receipt")
    if "PENDING_FILL_WITH_OBSERVED_RESULT" in closeout:
        raise RuntimeError("CHECKPOINT_FAILURE:gate252.closeout.pending_counts")
    if "closeout-reconciled checklist retained as evidence" not in checklist:
        raise RuntimeError("CHECKPOINT_FAILURE:gate252.checklist.closed_status")
    if "Status: closed support note retained as evidence" not in scope:
        raise RuntimeError("CHECKPOINT_FAILURE:gate252.scope.closed_status")
    if "Status: closed contradiction report retained as evidence" not in contradiction:
        raise RuntimeError("CHECKPOINT_FAILURE:gate252.contradiction.closed_status")


def test_gate252_bounded_sanity_traces_preserve_corrected_runtime_and_ingress_truth() -> None:
    """Positive proof for bounded cross-asset and participation sanity traces."""

    ingress, runtime = _supportive_runtime_with_upstream_truth()

    assert ingress == {
        "regime_input_present": True,
        "breadth_score": 0.67,
        "concentration_score": 0.41,
        "session_bucket_label": "mid_session",
        "baseline_interval_volume_share": 800.0,
        "observed_spread_bps": 12.5,
        "observed_trade_count": 42,
    }
    assert runtime == {
        "target_fresh_deployable_pct": 35.0,
        "inventory_action": "add",
        "fresh_capital_action": "add",
        "review_present": True,
    }


def test_gate252_pack_closeout_control_surfaces_are_truthful() -> None:
    """Positive proof for the final closeout router and support state."""

    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    closeout = CLOSEOUT.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    scope = SCOPE.read_text(encoding="utf-8")
    contradiction = CONTRADICTION.read_text(encoding="utf-8")

    _require_gate252_closeout_state(
        plans=plans,
        gate_map=gate_map,
        leaves=leaves,
        execution_log=execution_log,
        closeout=closeout,
        checklist=checklist,
        scope=scope,
        contradiction=contradiction,
    )


def test_gate252_negative_proof_turns_red_when_closeout_counts_or_router_state_drift() -> None:
    """Negative proof for the Gate 252 closeout checkpoint."""

    plans = PLANS.read_text(encoding="utf-8").replace("## Active pack\n\n- none", "## Active pack\n\n- gates: stale")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8").replace("- active gate: `none`", "- active gate: `Gate 252`")
    closeout = CLOSEOUT.read_text(encoding="utf-8").replace("gate252_targeted: 3 passed in 1.66s", "gate252_targeted: PENDING_FILL_WITH_OBSERVED_RESULT")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    scope = SCOPE.read_text(encoding="utf-8")
    contradiction = CONTRADICTION.read_text(encoding="utf-8")

    with pytest.raises(RuntimeError, match="gate252.router.no_active_pack|gate252.execution_log.no_active_gate|gate252.closeout.pending_counts"):
        _require_gate252_closeout_state(
            plans=plans,
            gate_map=gate_map,
            leaves=leaves,
            execution_log=execution_log,
            closeout=closeout,
            checklist=checklist,
            scope=scope,
            contradiction=contradiction,
        )
