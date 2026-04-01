"""Gate 144 posture hard-invariant and local-envelope runtime checks."""

from __future__ import annotations

from nvda_desk.config import Settings
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture


def _run_runtime(*, inventory_update: dict[str, float] | None = None):
    fixture = supportive_runtime_fixture()
    inventory_state = fixture.inventory_state
    if inventory_update:
        inventory_state = inventory_state.model_copy(update=inventory_update)
    return DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )


def test_gate144_posture_split_preserves_base_surface_and_annotations() -> None:
    result = _run_runtime()

    assert result.posture.hard_invariants is not None
    assert result.posture.hard_invariants.block_active is False
    assert result.posture.local_envelope is not None
    assert result.posture.local_envelope.base_permission_state.value == "allow"
    assert result.posture.local_envelope.base_posture_label == "probe"
    assert result.posture.downstream_annotations == [
        "contract:signal_conflict_detector:aligned",
        "contract:model_confidence_scorer:high",
        "contract:conviction_tier_allocator:tier_2",
    ]
    assert result.review.review_packet["posture"]["local_envelope"]["base_permission_state"] == "allow"
    assert result.review.review_packet["stage_local_handoff"]["cited_posture_pre_modifier"]["downstream_annotations"] == [
        "contract:signal_conflict_detector:aligned",
        "contract:model_confidence_scorer:high",
        "contract:conviction_tier_allocator:tier_2",
    ]


def test_gate144_hard_block_surface_exposes_capital_lockup_block() -> None:
    result = _run_runtime(
        inventory_update={
            "existing_inventory_pct": 80.0,
            "fresh_cash_pct": 5.0,
            "capital_lockup_pct": 80.0,
        }
    )

    assert result.posture.permission_state.value == "block"
    assert result.posture.hard_invariants is not None
    assert result.posture.hard_invariants.block_active is True
    assert "capital_locked" in result.posture.hard_invariants.hard_block_reasons
    assert result.posture.hard_invariants.zero_deployable_required is True
    assert result.posture.local_envelope is not None
    assert result.posture.local_envelope.base_permission_state.value == "block"
    assert result.posture.local_envelope.base_posture_label == "capital_locked"
