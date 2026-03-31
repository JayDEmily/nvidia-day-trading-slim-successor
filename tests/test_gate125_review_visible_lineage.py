"""Gate 125 review-visible coefficient lineage checks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from nvda_desk.config import Settings
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_EXECUTION_LOG_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-03-31_GATE125_REVIEW_VISIBLE_COEFFICIENT_LINEAGE.md"


def test_gate125_review_outputs_carry_resolved_surface_lineage() -> None:
    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    assert result.execution.modifier_runtime_packet is not None
    assert result.review.effective_policy is not None
    assert result.review.review_lineage is not None
    expected = [item.model_dump(mode="json") for item in result.execution.modifier_runtime_packet.resolved_surfaces]
    assert [item.model_dump(mode="json") for item in result.review.effective_policy.resolved_surfaces] == expected
    assert [item.model_dump(mode="json") for item in result.review.review_lineage.resolved_surfaces] == expected
    review_effective = cast(dict[str, Any], result.review.review_packet["effective_policy"])
    assert cast(list[dict[str, Any]], review_effective["resolved_surfaces"]) == expected
    first = cast(list[dict[str, Any]], review_effective["resolved_surfaces"])[0]
    assert set(first).issuperset({
        "baseline_reference",
        "baseline_numeric_value",
        "effective_numeric_value",
        "winning_precedence_band",
        "source_policy_ids",
        "clamped",
    })


def test_gate125_closeout_advances_pack_to_gate126() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert (
        "Gates 122-125 complete and Gate 126 now active" in plans
        or "Gates 122-126 complete and Gate 127 now active" in plans
        or "signal-coefficient authority pack closed through Gate 127" in plans
    )
    assert (
        "Current active gate: **Gate 126 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **Gate 127 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **none — signal-coefficient authority pack closed through Gate 127 on `main`**." in gate_map
    )
    assert (
        "Status: active signal-coefficient authority pack; Gates 122-125 complete on `main`, Gate 126 active, Gate 127 planned" in gates
        or "Status: active signal-coefficient authority pack; Gates 122-126 complete on `main`, Gate 127 active" in gates
        or "Status: closed signal-coefficient authority pack on `main`; Gates 122-127 complete, no active gate" in gates
    )
    assert leaves["execution_status"] in {
        "gate_125_complete_gate_126_active_on_main",
        "gate_126_complete_gate_127_active_on_main",
        "signal_coefficient_authority_pack_closed_through_gate_127_on_main",
    }
    assert leaves["active_gate"] in {
        "Gate 126",
        "Gate 127",
        "none — signal-coefficient authority pack closed through Gate 127 on main",
    }
    assert leaves["completed_gate_ids"][:4] == ["Gate 122", "Gate 123", "Gate 124", "Gate 125"]
    assert len(leaves["remaining_leaf_ids"]) in {5, 2, 0}
    assert (
        "Status: active execution log for the signal-coefficient authority pack; Gates 122-125 complete on `main`, Gate 126 active, Gate 127 planned" in execution_log
        or "Status: active execution log for the signal-coefficient authority pack; Gates 122-126 complete on `main`, Gate 127 active" in execution_log
        or "Status: closed execution log for the signal-coefficient authority pack; Gates 122-127 complete on `main`, no active gate" in execution_log
    )
    assert (
        "Status: complete on `main`; Gate 126 is now the active gate" in receipt
        or "Status: complete on `main`; Gate 127 is now the active gate" in receipt
        or "Status: complete on `main`; signal-coefficient authority pack is now closed through Gate 127" in receipt
    )
