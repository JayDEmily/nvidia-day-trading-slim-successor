"""Gate 225 retained-test cleanup closeout invariants."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_EXECUTION_LOG_v1.md"
GATE151_TEST = REPO_ROOT / "tests/test_gate151_field_level_ownership_and_consumer_migration.py"
GATE155_TEST = REPO_ROOT / "tests/test_gate155_downstream_consequence_routing_and_successor_boundary.py"
GATE207_TEST = REPO_ROOT / "tests/test_gate207_router_and_doctrine_consolidation.py"
POSTURE_RUNTIME_TEST = REPO_ROOT / "tests/test_posture_risk_and_playbook.py"
TEMPORAL_RUNTIME_TEST = REPO_ROOT / "tests/test_temporal_context_runtime.py"


def test_gate225_control_surfaces_track_activation_and_closeout_truthfully() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    completed = set(payload["completed_leaf_ids"])

    if "LEAF-G225-004" in completed:
        assert payload["execution_status"] == "cleanup_pack_closed_no_active_pack_routed"
        assert payload["active_gate"] == "none"
        assert payload["pending_gate_ids"] == []
        assert payload["remaining_leaf_ids"] == []
        assert payload["completed_gate_ids"] == ["Gate 222", "Gate 223", "Gate 224", "Gate 225"]
        assert "## Active pack\n\n- none" in plans
        assert "no active pack currently routed" in plans
        assert "Current active gate: **No active pack currently routed. The successor retained-test cleanup execution pack is closed through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`.**" in gate_map
        assert "cleanup pack closed through Gate 225" in execution_log
    else:
        assert payload["execution_status"] in {
            "gate_225_active_on_work_branch",
            "gate_225_active_leaf_g225_001_complete",
            "gate_225_active_leaf_g225_002_complete",
            "gate_225_active_leaf_g225_003_complete",
        }
        assert payload["active_gate"] == "Gate 225"
        assert payload["completed_gate_ids"] == ["Gate 222", "Gate 223", "Gate 224"]
        assert payload["pending_gate_ids"] == ["Gate 225"]
        assert "successor retained-test cleanup execution pack; Gate 225 is active on `work/gate-225-retained-test-cleanup-closeout-20260406`" in plans
        assert "Current active gate: **Gate 225 active on `work/gate-225-retained-test-cleanup-closeout-20260406` under the successor retained-test cleanup execution pack.**" in gate_map
        assert "Gate 225 is active on `work/gate-225-retained-test-cleanup-closeout-20260406`." in execution_log


def test_gate225_targeted_retarget_and_runtime_confirmation_track_leaf_progress() -> None:
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    completed = set(payload["completed_leaf_ids"])

    if "LEAF-G225-001" in completed:
        for path in [GATE151_TEST, GATE155_TEST, GATE207_TEST]:
            text = path.read_text(encoding="utf-8")
            assert (
                "successor retained-test cleanup execution pack" in text
                or "Gate 225" in text
                or "no active pack currently routed" in text
            )

    if "LEAF-G225-002" in completed:
        execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
        assert "runtime-scenario and keep-as-is family slice remained green" in execution_log
        for path in [POSTURE_RUNTIME_TEST, TEMPORAL_RUNTIME_TEST]:
            assert path.exists()

    if "LEAF-G225-003" in completed:
        execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
        assert "executed-row state is frozen explicitly" in execution_log
