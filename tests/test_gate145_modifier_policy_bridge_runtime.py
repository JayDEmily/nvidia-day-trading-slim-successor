"""Gate 145 modifier emitted-policy compatibility-bridge checks."""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture
from tests.test_gate78_modifier_runtime_integration import _tightened_precursor_packet

REPO_ROOT = Path(__file__).resolve().parents[1]
RECEIPT = REPO_ROOT / "docs/planning/2026-04-01_GATE145_MODIFIER_EMITTED_POLICY_COMPATIBILITY_BRIDGE.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-01_STAGE_LOCAL_HANDOFF_AND_TERMINAL_RISK_SEAMS_LEAVES_v1.json"
DOMAIN_MODEL = REPO_ROOT / "docs/03_DOMAIN_MODEL.md"
VOCAB_PATH = REPO_ROOT / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"


def _tightened_runtime():
    fixture = supportive_runtime_fixture()
    return DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input.model_copy(
            update={
                "ts": datetime.fromisoformat("2026-03-23T15:20:00-04:00"),
                "next_event_at": datetime.fromisoformat("2026-03-24T08:30:00-04:00"),
                "precursor_runtime_packet": _tightened_precursor_packet(),
            }
        ),
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )


def test_gate145_posture_bridge_makes_packet_authority_explicit() -> None:
    result = _tightened_runtime()

    assert result.posture.local_envelope is not None
    assert result.posture.local_envelope.base_permission_state.value == "allow"
    assert result.posture.local_envelope.base_fresh_deployable_capital_pct == 55.0
    assert result.posture.permission_state.value == "derisk"
    assert result.posture.fresh_deployable_capital_pct == 20.625
    assert result.posture.modifier_compatibility_bridge is not None
    assert result.posture.modifier_compatibility_bridge.authority_source == "modifier_runtime_packet"
    assert "phase_carry:late_session:event_carry_setup" in result.posture.modifier_compatibility_bridge.applied_policy_ids
    assert "fresh_deployable_capital_pct" in result.posture.modifier_compatibility_bridge.overridden_fields
    assert result.posture.modifier_compatibility_bridge.target_fresh_deployable_capital_pct == 20.625
    assert "modifier_runtime_packet_authority" in result.posture.modifier_compatibility_bridge.notes


def test_gate145_execution_bridge_is_explicit_even_when_operatives_are_already_applied() -> None:
    result = _tightened_runtime()

    assert result.execution.modifier_compatibility_bridge is not None
    assert result.execution.modifier_compatibility_bridge.compatibility_bridge_active is True
    assert result.execution.modifier_compatibility_bridge.overridden_fields == []
    assert "execution_operative_surfaces_already_reflect_modifier_runtime_packet" in result.execution.modifier_compatibility_bridge.notes
    assert result.stage_local_handoff is not None
    assert result.stage_local_handoff.execution_post_modifier_pre_final_risk is not None
    assert result.stage_local_handoff.execution_post_modifier_pre_final_risk.modifier_compatibility_bridge is not None
    assert result.review.review_packet["execution"]["modifier_compatibility_bridge"]["authority_source"] == "modifier_runtime_packet"


def test_gate145_receipt_domain_model_and_vocabulary_are_present() -> None:
    receipt = RECEIPT.read_text(encoding="utf-8")
    domain_model = DOMAIN_MODEL.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    vocab = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    slugs = {entry["canonical_slug"] for entry in vocab["entries"]}

    assert "modifier_compatibility_bridge" in receipt
    assert "#### Gate 145 note: modifier compatibility bridge" in domain_model
    assert "modifier_compatibility_bridge" in slugs
    assert leaves["active_gate"] in {"Gate 145", "Gate 146", "Gate 147", "Gate 148"}
