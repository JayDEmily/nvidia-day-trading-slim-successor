"""Gate 238 Step 5 decontamination checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.cognition import PlaybookEligibilityInput, PostureRiskInput
from nvda_desk.config import Settings
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.playbook_eligibility import PlaybookEligibilityService
from nvda_desk.services.posture_risk import PostureRiskService
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAVES_LEDGER = REPO_ROOT / "docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_LEAVES_v1.json"
PLAYBOOK_ELIGIBILITY = REPO_ROOT / "src/nvda_desk/services/playbook_eligibility.py"


def _eligibility_with_posture_overrides(fresh_capital: float, inventory_bias: str):
    fixture = supportive_runtime_fixture()
    temporal = TemporalContextService(Settings()).evaluate(fixture.temporal_input)
    regime = MarketRegimeContextService().evaluate(fixture.regime_input)
    options_flow = OptionsFlowContextService().evaluate(fixture.options_flow_input)
    posture = PostureRiskService().evaluate(
        PostureRiskInput(
            temporal=temporal,
            regime=regime,
            options_flow=options_flow,
            inventory=fixture.inventory_state,
            risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        )
    ).model_copy(update={
        "fresh_deployable_capital_pct": fresh_capital,
        "inventory_action_bias": inventory_bias,
    })
    return PlaybookEligibilityService().evaluate(
        PlaybookEligibilityInput(
            temporal=temporal,
            regime=regime,
            options_flow=options_flow,
            posture=posture,
        )
    )


def test_gate238_source_and_ledger_show_permission_driven_selection_only() -> None:
    payload = json.loads(LEAVES_LEDGER.read_text(encoding="utf-8"))
    assert "Gate 238" in payload["completed_gate_ids"]

    source = PLAYBOOK_ELIGIBILITY.read_text(encoding="utf-8")
    assert 'payload.posture.permission_state.value == "derisk"' in source
    assert "payload.posture.fresh_deployable_capital_pct" not in source
    assert "payload.posture.inventory_action_bias" not in source


def test_gate238_selection_is_invariant_to_step4_compatibility_echoes() -> None:
    supportive = _eligibility_with_posture_overrides(55.0, "add")
    distorted = _eligibility_with_posture_overrides(5.0, "hedge")

    assert supportive.active_family_ids == distorted.active_family_ids
    assert supportive.active_setup_variant_ids == distorted.active_setup_variant_ids
    assert supportive.add_candidates == distorted.add_candidates
    assert supportive.watch_only_candidates == distorted.watch_only_candidates
