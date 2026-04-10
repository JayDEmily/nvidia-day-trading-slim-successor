"""Gate 236 Step 3 contract-isolation checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]
LEAVES_LEDGER = REPO_ROOT / "docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_LEAVES_v1.json"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_EXECUTION_LOG_v1.md"


def test_gate236_control_surfaces_show_pack_closed_through_gate241() -> None:
    plans_text = (REPO_ROOT / "PLANS.md").read_text(encoding="utf-8")
    assert "2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_GATES_v1.md" in plans_text

    payload = json.loads(LEAVES_LEDGER.read_text(encoding="utf-8"))
    assert payload["active_gate"] == "none"
    assert "Gate 236" in payload["completed_gate_ids"]
    assert payload["remaining_leaf_ids"] == []

    gate_map_text = GATE_MAP.read_text(encoding="utf-8")
    assert "Current active gate: **No active pack currently routed. The main serial stack Steps 3-6 corrective implementation pack is closed through Gate 241 in the uploaded workspace copy.**" in gate_map_text

    execution_log_text = EXECUTION_LOG.read_text(encoding="utf-8")
    assert "## Gate 236 closeout proof" in execution_log_text


def test_gate236_options_flow_output_stays_descriptive_only() -> None:
    fixture = supportive_runtime_fixture()
    output = OptionsFlowContextService().evaluate(fixture.options_flow_input)

    forbidden_tokens = ("permission", "deploy", "capital", "inventory_action", "authorised")
    for field_name in output.model_dump().keys():
        assert not any(token in field_name for token in forbidden_tokens), field_name
    for reason in output.reasons:
        reason_lower = reason.lower()
        assert not any(token in reason_lower for token in forbidden_tokens), reason

    assert output.options_behavior_cluster
    assert output.reasons
