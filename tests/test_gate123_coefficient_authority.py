"""Gate 123 governed coefficient-authority checks."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from nvda_desk.config_models import CoefficientAuthorityDocument, load_config_bundle
from nvda_desk.schemas.state_policy import MutableRuntimeSurface

REPO_ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = REPO_ROOT / "config/coefficient_authority.v1.yaml"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_EXECUTION_LOG_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-03-31_GATE123_COEFFICIENT_AUTHORITY_CONTRACT.md"


def test_governed_coefficient_authority_file_loads_and_stays_narrow() -> None:
    document = CoefficientAuthorityDocument.from_yaml_path(AUTHORITY)

    assert document.schema_version == "coefficient_authority.v1"
    assert len(document.mutable_numeric_surfaces) == 7
    assert len(document.mutable_boolean_surfaces) == 1
    assert len(document.temporal_thresholds) == 16
    assert len(document.timing_parameters) == 2
    assert {item.surface_id.value for item in document.mutable_surface_index().values()} == {
        "entry_gate_score_floor",
        "zone_score_threshold",
        "distance_to_vwap_soft_limit_pct",
        "risk_vix_caution_threshold",
        "risk_vix_hot_threshold",
        "max_risk_per_trade",
        "target_fresh_deployable_pct",
        "hedge_required",
    }
    assert all("japan" not in item.surface_id.value for item in document.mutable_surface_index().values())


def test_config_bundle_loads_governed_authority_surface() -> None:
    bundle = load_config_bundle(REPO_ROOT / "config")

    assert bundle.runtime_settings.paths is not None
    assert bundle.runtime_settings.paths.coefficient_authority_path == "./config/coefficient_authority.v1.yaml"
    assert bundle.evaluation_config.paths.coefficient_authority_path == "./config/coefficient_authority.v1.yaml"
    assert (
        bundle.coefficient_authority.mutable_surface_index()[MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR].baseline
        == 0.65
    )


def test_invalid_authority_entries_fail_deterministically() -> None:
    base = CoefficientAuthorityDocument.from_yaml_path(AUTHORITY).model_dump(mode="json")

    broken_surface = json.loads(json.dumps(base))
    broken_surface["mutable_numeric_surfaces"][0]["surface_id"] = "made_up_surface"
    with pytest.raises(ValidationError):
        CoefficientAuthorityDocument.model_validate(broken_surface)

    broken_range = json.loads(json.dumps(base))
    broken_range["mutable_numeric_surfaces"][0]["maximum"] = 1.5
    with pytest.raises(ValidationError):
        CoefficientAuthorityDocument.model_validate(broken_range)

    broken_transform = json.loads(json.dumps(base))
    broken_transform["timing_parameters"][0]["transform_family"] = "state_conditioned_modifier"
    with pytest.raises(ValidationError):
        CoefficientAuthorityDocument.model_validate(broken_transform)


def test_gate123_closeout_advances_pack_to_gate124() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert (
        "Gates 122-123 complete and Gate 124 now active" in plans
        or "Gates 122-124 complete and Gate 125 now active" in plans
        or "Gates 122-125 complete and Gate 126 now active" in plans
        or "Gates 122-126 complete and Gate 127 now active" in plans
        or "signal-coefficient authority pack closed through Gate 127" in plans
        or "2026-03-31_POST_FLIGHT_REPO_CONSISTENCY_GATES_v1.md" in plans
        or "stage-local handoff and terminal-risk seams pack" in plans
        or "successor retained-test cleanup execution pack; Gate 224 is active" in plans
        or "Gate 224 is complete on `work/gate-224-runtime-review-and-contract-retarget-20260406`" in plans
        or "successor retained-test cleanup execution pack; Gate 225 is active" in plans
        or "no active pack currently routed" in plans
    )
    assert (
        "Current active gate: **Gate 124 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **Gate 125 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **Gate 126 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **Gate 127 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **none — signal-coefficient authority pack closed through Gate 127 on `main`**." in gate_map
        or "Current active gate: **Gate 128 in the post-flight repo consistency pack**." in gate_map
        or "Current active gate: **Gate 129 in the post-flight repo consistency pack**." in gate_map
        or "Current active gate: **Gate 130 in the post-flight repo consistency pack**." in gate_map
        or "Current active gate: **Gate 131 in the post-flight repo consistency pack**." in gate_map
        or "Current active gate: **none — post-flight repo consistency pack closed through Gate 131 on `main`**." in gate_map
        or "Current active gate: **Gate 149 in the stage-local handoff and terminal-risk seams pack**." in gate_map
        or "Current active gate: **none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`**." in gate_map
        or "Current active gate: **Gate 224 active on `work/gate-224-runtime-review-and-contract-retarget-20260406` under the successor retained-test cleanup execution pack.**" in gate_map
        or "Current active gate: **No active gate under the successor retained-test cleanup execution pack. Gate 224 is complete on `work/gate-224-runtime-review-and-contract-retarget-20260406`; Gate 225 is not yet activated.**" in gate_map
        or "Current active gate: **Gate 225 active on `work/gate-225-retained-test-cleanup-closeout-20260406` under the successor retained-test cleanup execution pack.**" in gate_map
        or "Current active gate: **No active gate under the successor retained-test cleanup execution pack. Gate 225 is complete on `work/gate-225-retained-test-cleanup-closeout-20260406`; cleanup pack closed.**" in gate_map
        or "Current active gate: **No active pack currently routed. The successor retained-test cleanup execution pack is closed through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`.**" in gate_map
    )
    assert (
        "Status: active signal-coefficient authority pack; Gates 122-123 complete on `main`, Gate 124 active, Gates 125-127 planned" in gates
        or "Status: active signal-coefficient authority pack; Gates 122-124 complete on `main`, Gate 125 active, Gates 126-127 planned" in gates
        or "Status: active signal-coefficient authority pack; Gates 122-125 complete on `main`, Gate 126 active, Gate 127 planned" in gates
        or "Status: active signal-coefficient authority pack; Gates 122-126 complete on `main`, Gate 127 active" in gates
        or "Status: closed signal-coefficient authority pack on `main`; Gates 122-127 complete, no active gate" in gates
    )
    assert leaves["execution_status"] in {
        "gate_123_complete_gate_124_active_on_main",
        "gate_124_complete_gate_125_active_on_main",
        "gate_125_complete_gate_126_active_on_main",
        "gate_126_complete_gate_127_active_on_main",
        "signal_coefficient_authority_pack_closed_through_gate_127_on_main",
    }
    assert leaves["active_gate"] in {
        "Gate 124",
        "Gate 125",
        "Gate 126",
        "Gate 127",
        "none — signal-coefficient authority pack closed through Gate 127 on main", "Gate 128", "Gate 129", "Gate 130", "Gate 131", "none — post-flight repo consistency pack closed through Gate 131 on main", "Gate 149", "none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on main",
    }
    assert leaves["completed_gate_ids"][:2] == ["Gate 122", "Gate 123"]
    assert leaves["completed_leaf_ids"][:6] == [
        "LEAF-G122-001",
        "LEAF-G122-002",
        "LEAF-G122-003",
        "LEAF-G123-001",
        "LEAF-G123-002",
        "LEAF-G123-003",
    ]
    assert len(leaves["remaining_leaf_ids"]) in {11, 8, 5, 2, 0}
    assert (
        "Status: active execution log for the signal-coefficient authority pack; Gates 122-123 complete on `main`, Gate 124 active, Gates 125-127 planned" in execution_log
        or "Status: active execution log for the signal-coefficient authority pack; Gates 122-124 complete on `main`, Gate 125 active, Gates 126-127 planned" in execution_log
        or "Status: active execution log for the signal-coefficient authority pack; Gates 122-125 complete on `main`, Gate 126 active, Gate 127 planned" in execution_log
        or "Status: active execution log for the signal-coefficient authority pack; Gates 122-126 complete on `main`, Gate 127 active" in execution_log
        or "Status: closed execution log for the signal-coefficient authority pack; Gates 122-127 complete on `main`, no active gate" in execution_log
    )
    assert (
        "Status: complete on `main`; Gate 124 is now the active gate" in receipt
        or "Status: complete on `main`; Gate 125 is now the active gate" in receipt
        or "Status: complete on `main`; Gate 126 is now the active gate" in receipt
        or "Status: complete on `main`; Gate 127 is now the active gate" in receipt
    )
