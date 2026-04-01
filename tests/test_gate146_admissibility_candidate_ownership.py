"""Gate 146 admissibility-versus-candidate-ownership runtime checks."""

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


def test_gate146_admissibility_surface_stays_on_stage5_while_execution_owns_lead_selection() -> None:
    result = _run_runtime()

    assert result.eligibility.admissibility_surface is not None
    assert result.eligibility.admissibility_surface.permission_state.value == "allow"
    assert result.eligibility.admissibility_surface.admissible_family_ids == ["trend_continuation"]
    assert result.eligibility.admissibility_surface.admissible_setup_variant_ids == [
        "opening_drive_continuation"
    ]
    assert result.eligibility.admissibility_surface.admissible_playbook_ids == ["continuation_ladder"]
    assert result.execution.candidate_ownership is not None
    assert result.execution.candidate_ownership.admitted_playbook_ids == ["continuation_ladder"]
    assert result.execution.candidate_ownership.adjudicated_playbook_ids == ["continuation_ladder"]
    assert result.execution.candidate_ownership.lead_playbook_id == "continuation_ladder"
    assert result.execution.candidate_ownership.contradiction_resolution == "single_candidate_clear"
    assert result.review.review_packet["eligibility"]["admissibility_surface"]["admissible_playbook_ids"] == [
        "continuation_ladder"
    ]
    assert result.review.review_packet["execution"]["candidate_ownership"]["lead_playbook_id"] == "continuation_ladder"



def test_gate146_posture_block_leaves_stage5_with_no_admitted_playbooks_and_stage6_with_no_lead() -> None:
    result = _run_runtime(
        inventory_update={
            "existing_inventory_pct": 80.0,
            "fresh_cash_pct": 5.0,
            "capital_lockup_pct": 80.0,
        }
    )

    assert result.eligibility.admissibility_surface is not None
    assert result.eligibility.admissibility_surface.permission_state.value == "block"
    assert result.eligibility.admissibility_surface.no_trade_reasons == ["permission_blocked"]
    assert result.eligibility.admissibility_surface.admissible_playbook_ids == []
    assert result.execution.candidate_ownership is not None
    assert result.execution.candidate_ownership.admitted_playbook_ids == []
    assert result.execution.candidate_ownership.adjudicated_playbook_ids == []
    assert result.execution.candidate_ownership.lead_playbook_id is None
    assert "execution_skipped_after_posture_block" in result.execution.candidate_ownership.notes
