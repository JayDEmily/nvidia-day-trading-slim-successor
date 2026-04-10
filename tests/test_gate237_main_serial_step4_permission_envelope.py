"""Gate 237 Step 4 permission-envelope checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.cognition import PostureRiskInput
from nvda_desk.config import Settings
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.posture_risk import PostureRiskService
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAVES_LEDGER = REPO_ROOT / "docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_LEAVES_v1.json"
DOC03 = REPO_ROOT / "docs/03_DOMAIN_MODEL.md"
DOC07 = REPO_ROOT / "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md"
VOCAB = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"
EXECUTION_SERVICE = REPO_ROOT / "src/nvda_desk/services/execution_expression.py"
CDA_SERVICE = REPO_ROOT / "src/nvda_desk/services/capital_deployment_authority.py"


def _supportive_posture():
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
    )
    return posture


def test_gate237_docs_and_vocabulary_shift_to_permission_envelope_authority() -> None:
    payload = json.loads(LEAVES_LEDGER.read_text(encoding="utf-8"))
    assert "Gate 237" in payload["completed_gate_ids"]

    assert "compatibility carriage only" in DOC03.read_text(encoding="utf-8")
    doc07_text = DOC07.read_text(encoding="utf-8")
    assert "Step 4 read rule" in doc07_text
    assert "Compatibility-only echoes still carried on the stage packet" in doc07_text

    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))
    notes = {entry["canonical_slug"]: entry.get("notes", []) for entry in vocab["entries"]}
    assert any("bounded local permission envelope" in note for note in notes["posture_risk_permission"])
    assert any("Legacy deployable-capital echoes remain compatibility-only" in note for note in notes["posture_local_envelope"])

    assert "payload.posture.fresh_deployable_capital_pct" not in EXECUTION_SERVICE.read_text(encoding="utf-8")
    assert "payload.posture.fresh_deployable_capital_pct" not in CDA_SERVICE.read_text(encoding="utf-8")


def test_gate237_posture_service_keeps_permission_state_as_active_step4_surface() -> None:
    posture = _supportive_posture()

    assert posture.local_envelope is not None
    assert posture.hard_invariants is not None
    assert posture.local_envelope.base_permission_state is posture.permission_state
    assert posture.hard_invariants.block_active is False
    assert posture.fresh_deployable_capital_pct == 55.0
