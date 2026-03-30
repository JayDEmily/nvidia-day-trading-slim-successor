"""Gate 124 governed mutable-surface authority checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.config_models import CoefficientAuthorityDocument
from nvda_desk.schemas.state_policy import MutableRuntimeSurface
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.state_conditioned_modifier import StateConditionedModifierService
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = REPO_ROOT / "config/coefficient_authority.v1.yaml"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_EXECUTION_LOG_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-03-31_GATE124_EXTERNALISED_MUTABLE_SURFACE_AUTHORITY.md"


def test_gate124_runtime_reads_governed_authority_for_mutable_surfaces() -> None:
    authority = CoefficientAuthorityDocument.from_yaml_path(AUTHORITY)
    fixture = supportive_runtime_fixture()
    result = DeskCognitionRuntime(Settings()).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
    )

    assert result.execution.modifier_runtime_packet is not None
    surface_index = authority.mutable_surface_index()
    resolved_by_surface = {
        item.target_surface: item for item in result.execution.modifier_runtime_packet.resolved_surfaces
    }
    entry = resolved_by_surface[MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR]
    target = resolved_by_surface[MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT]
    hedge = resolved_by_surface[MutableRuntimeSurface.HEDGE_REQUIRED]

    assert not hasattr(StateConditionedModifierService, "_BASELINE_NUMERIC")
    assert entry.authority_version == authority.authority_version
    assert entry.owner_stage is surface_index[MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR].owner_stage
    assert entry.baseline_numeric_value == surface_index[MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR].baseline
    assert entry.minimum_numeric_value == surface_index[MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR].minimum
    assert entry.maximum_numeric_value == surface_index[MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR].maximum
    assert target.baseline_reference == (
        f"coefficient_authority:{authority.authority_version}:target_fresh_deployable_pct"
    )
    assert hedge.baseline_boolean_value is surface_index[MutableRuntimeSurface.HEDGE_REQUIRED].baseline


def test_gate124_closeout_advances_pack_but_allows_later_statuses() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert (
        "Gates 122-124 complete and Gate 125 now active" in plans
        or "Gates 122-125 complete and Gate 126 now active" in plans
        or "Gates 122-126 complete and Gate 127 now active" in plans
        or "signal-coefficient authority pack closed through Gate 127" in plans
    )
    assert (
        "Current active gate: **Gate 125 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **Gate 126 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **Gate 127 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **none — signal-coefficient authority pack closed through Gate 127 on `main`**." in gate_map
    )
    assert (
        "Status: active signal-coefficient authority pack; Gates 122-124 complete on `main`, Gate 125 active, Gates 126-127 planned" in gates
        or "Status: active signal-coefficient authority pack; Gates 122-125 complete on `main`, Gate 126 active, Gate 127 planned" in gates
        or "Status: active signal-coefficient authority pack; Gates 122-126 complete on `main`, Gate 127 active" in gates
        or "Status: closed signal-coefficient authority pack on `main`; Gates 122-127 complete, no active gate" in gates
    )
    assert leaves["execution_status"] in {
        "gate_124_complete_gate_125_active_on_main",
        "gate_125_complete_gate_126_active_on_main",
        "gate_126_complete_gate_127_active_on_main",
        "signal_coefficient_authority_pack_closed_through_gate_127_on_main",
    }
    assert leaves["active_gate"] in {
        "Gate 125",
        "Gate 126",
        "Gate 127",
        "none — signal-coefficient authority pack closed through Gate 127 on main",
    }
    assert leaves["completed_gate_ids"][:3] == ["Gate 122", "Gate 123", "Gate 124"]
    assert "Status: complete on `main`; Gate 125 is now the active gate" in receipt or "Status: complete on `main`; Gate 126 is now the active gate" in receipt
    assert "Status: active execution log for the signal-coefficient authority pack; Gates 122-124 complete on `main`, Gate 125 active, Gates 126-127 planned" in execution_log or "Status: active execution log for the signal-coefficient authority pack; Gates 122-125 complete on `main`, Gate 126 active, Gate 127 planned" in execution_log
