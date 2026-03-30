"""Testing-module planning-pack authority checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-30_TESTING_MODULE_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-30_TESTING_MODULE_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-30_TESTING_MODULE_EXECUTION_LOG_v1.md"


def test_testing_module_pack_is_retained_as_predecessor_evidence() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")

    assert "2026-03-30_TESTING_MODULE_GATES_v1.md" in plans
    assert "2026-03-30_TESTING_MODULE_LEAVES_v1.json" in plans
    assert "2026-03-30_TESTING_MODULE_EXECUTION_LOG_v1.md" in plans
    assert "Current active gate: **Gate 111 in the repo-process governance pack**." in gate_map or "Current active gate: **Gate 112 in the repo-process governance pack**." in gate_map or "Current active gate: **Gate 115 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 116 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 117 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 118 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 119 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 120 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **Gate 121 in the historical-evaluation readiness pack**." in gate_map or "Current active gate: **none — historical-evaluation readiness pack closed through Gate 121 on `main`**." in gate_map or "Current active gate: **Gate 122 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 123 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 124 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 125 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 126 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **Gate 127 in the signal-coefficient authority pack**." in gate_map or "Current active gate: **none — signal-coefficient authority pack closed through Gate 127 on `main`**." in gate_map or "Current active gate: **none — repo-process governance pack closed through Gate 112 on `main`**." in gate_map
    assert "| Gate 94 | complete on `main` |" in gate_map
    assert "| Gate 100 | complete on `main` |" in gate_map


def test_testing_module_gates_doc_freezes_phase_order_and_scope_rules() -> None:
    gates = GATES.read_text(encoding="utf-8")

    assert "### Gate 95: Phase 0 workbook-viability closeout on `main`" in gates
    assert "### Gate 96: Canonical prepared-runtime full-chain harness" in gates
    assert "### Gate 100: Controlled scenario-matrix expansion and honest closeout" in gates
    assert "Do not broaden to a large scenario matrix before one canonical real-data path is stable" not in gates
    assert "Do not broaden to many scenarios before one lawful single-run harness is stable." in gates


def test_testing_module_leaves_mark_gate94_complete_and_gate95_next() -> None:
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert leaves["governing_plan"] == "docs/planning/2026-03-30_TESTING_MODULE_GATES_v1.md"
    assert leaves["execution_status"] in {"gate_94_testing_module_pack_active_from_gate_95", "gate_95_testing_module_pack_active_from_gate_96", "gate_96_testing_module_pack_active_from_gate_97", "gate_97_testing_module_pack_active_from_gate_98", "gate_98_testing_module_pack_active_from_gate_99", "gate_99_testing_module_pack_active_from_gate_100", "gate_100_testing_module_pack_closed_on_main"}
    assert leaves["active_gate"] in {"Gate 95", "Gate 96", "Gate 97", "Gate 98", "Gate 99", "Gate 100", "none — testing-module pack closed through Gate 100 on main"}
    assert leaves["completed_gate_ids"][:1] == ["Gate 94"]
    assert leaves["completed_leaf_ids"][:2] == ["LEAF-G94-001", "LEAF-G94-002"]
    assert leaves["global_rules"]["phase0_failure_must_remain_honest"] is True


def test_testing_module_execution_log_records_gate94_receipts() -> None:
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert ("Status: active execution log for the testing-module pack; Gate 94 complete on `main`, Gate 95 next" in execution_log) or ("Status: active execution log for the testing-module pack; Gates 94-95 complete on `main`, Gate 96 next" in execution_log) or ("Status: active execution log for the testing-module pack; Gates 94-96 complete on `main`, Gate 97 next" in execution_log) or ("Status: active execution log for the testing-module pack; Gates 94-97 complete on `main`, Gate 98 next" in execution_log) or ("Status: active execution log for the testing-module pack; Gates 94-98 complete on `main`, Gate 99 next" in execution_log) or ("Status: active execution log for the testing-module pack; Gates 94-99 complete on `main`, Gate 100 next" in execution_log) or ("Status: closed execution log for the testing-module pack; Gates 94-100 complete on `main`, no active gate" in execution_log)
    assert "### LEAF-G94-001 — Promote the testing doctrine and testing-module planning pair onto main" in execution_log
    assert "### LEAF-G94-002 — Install active planning pointers and anti-drift proof for Gate 94 closeout" in execution_log
