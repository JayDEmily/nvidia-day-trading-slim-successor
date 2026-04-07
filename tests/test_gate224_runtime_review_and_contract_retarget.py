"""Gate 224 runtime review and contract-family retarget invariants."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_SUCCESSOR_RETAINED_TEST_CLEANUP_EXECUTION_PACK_EXECUTION_LOG_v1.md"
GATE125_TEST = REPO_ROOT / "tests/test_gate125_review_visible_lineage.py"
GATE132_TEST = REPO_ROOT / "tests/test_gate132_bounded_trace_scenario_pack.py"
GATE134_TEST = REPO_ROOT / "tests/test_gate134_bounded_trace_reporting.py"
GATE123_TEST = REPO_ROOT / "tests/test_gate123_coefficient_authority.py"
GATE124_TEST = REPO_ROOT / "tests/test_gate124_mutable_surface_authority.py"
GATE126_TEST = REPO_ROOT / "tests/test_gate126_temporal_threshold_authority.py"
GATE113_TEST = REPO_ROOT / "tests/test_gate113_execution_authority_microtranche.py"
GATE152_TEST = REPO_ROOT / "tests/test_gate152_stage5_stage6_authority_replan.py"
GATE153_TEST = REPO_ROOT / "tests/test_gate153_overlay_terminal_final_join_authority_replan.py"


def test_gate224_control_surfaces_track_activation_and_closeout_truthfully() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    completed = set(payload["completed_leaf_ids"])

    if "LEAF-G224-004" in completed:
        assert payload["execution_status"] == (
            "gate_224_complete_on_work_branch_gate_225_not_yet_activated"
        )
        assert payload["active_gate"] == (
            "none — Gate 224 complete on "
            "work/gate-224-runtime-review-and-contract-retarget-20260406; "
            "Gate 225 not yet activated"
        )
        assert payload["completed_gate_ids"] in (["Gate 222", "Gate 223", "Gate 224"], ["Gate 222", "Gate 223", "Gate 224", "Gate 225"])
        assert payload["pending_gate_ids"] in (["Gate 225"], [])
        assert "Gate 224 is complete on `work/gate-224-runtime-review-and-contract-retarget-20260406`" in plans
        assert ("Current active gate: **No active gate under the successor retained-test cleanup execution pack. Gate 224 is complete on `work/gate-224-runtime-review-and-contract-retarget-20260406`; Gate 225 is not yet activated.**" in gate_map) or ("Current active gate: **No active pack currently routed. The successor retained-test cleanup execution pack is closed through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`.**" in gate_map)
        assert "Gate 224 complete on `work/gate-224-runtime-review-and-contract-retarget-20260406`." in execution_log
        assert ("Gate 225 remains planned and is not yet activated." in execution_log) or ("cleanup pack closed through Gate 225" in execution_log)
    else:
        assert payload["execution_status"] in {
            "gate_224_active_on_work_branch",
            "gate_224_active_leaf_g224_001_complete",
            "gate_224_active_leaf_g224_002_complete",
            "gate_224_active_leaf_g224_003_complete",
        }
        assert payload["active_gate"] == "Gate 224"
        assert payload["completed_gate_ids"] == ["Gate 222", "Gate 223"]
        assert payload["pending_gate_ids"] == ["Gate 224", "Gate 225"]
        assert "successor retained-test cleanup execution pack; Gate 224 is active on `work/gate-224-runtime-review-and-contract-retarget-20260406`" in plans
        assert "Current active gate: **Gate 224 active on `work/gate-224-runtime-review-and-contract-retarget-20260406` under the successor retained-test cleanup execution pack.**" in gate_map
        assert "Gate 224 is active on `work/gate-224-runtime-review-and-contract-retarget-20260406`." in execution_log


def test_gate224_retarget_targets_track_leaf_progress() -> None:
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    completed = set(payload["completed_leaf_ids"])

    if "LEAF-G224-001" in completed:
        for path in [GATE125_TEST, GATE132_TEST, GATE134_TEST]:
            text = path.read_text(encoding="utf-8")
            assert "successor retained-test cleanup execution pack" in text
            assert "Gate 224" in text or "Gate 225" in text

    if "LEAF-G224-002" in completed:
        for path in [
            GATE123_TEST,
            GATE124_TEST,
            GATE126_TEST,
            GATE113_TEST,
            GATE152_TEST,
            GATE153_TEST,
        ]:
            text = path.read_text(encoding="utf-8")
            assert (
                "successor retained-test cleanup execution pack" in text
                or "Gate 224" in text
                or "Gate 225" in text
            )

    if "LEAF-G224-003" in completed:
        execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
        assert "No guarded keep-as-is family fallout repair was required in Gate 224." in execution_log
