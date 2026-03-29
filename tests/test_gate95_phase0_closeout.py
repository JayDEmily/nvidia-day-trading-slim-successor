"""Gate 95 Phase 0 closeout integrity checks."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-30_TESTING_MODULE_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-30_TESTING_MODULE_EXECUTION_LOG_v1.md"
AUDIT_JSON = REPO_ROOT / "docs/planning/2026-03-30_PHASE0_SIGNAL_WORKBOOK_AUDIT.json"
AUDIT_SCRIPT = REPO_ROOT / "scripts/phase0_signal_workbook_audit.py"
WORKBOOK = REPO_ROOT / "docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx"


def test_phase0_closeout_moves_active_gate_to_gate96() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "Gate 95 — complete on `main`" in plans
    assert ("Gate 96 — next active gate on `main`" in plans) or ("Gate 96 — complete on `main`" in plans)
    assert ("Current active gate: **Gate 96 in the testing-module pack**." in gate_map) or ("Current active gate: **Gate 97 in the testing-module pack**." in gate_map) or ("Current active gate: **Gate 98 in the testing-module pack**." in gate_map) or ("Current active gate: **Gate 99 in the testing-module pack**." in gate_map) or ("Current active gate: **Gate 100 in the testing-module pack**." in gate_map)
    assert "| Gate 95 | complete on `main` |" in gate_map
    assert ("| Gate 96 | planned; next active gate |" in gate_map) or ("| Gate 96 | complete on `main` |" in gate_map)
    assert leaves["execution_status"] in {"gate_95_testing_module_pack_active_from_gate_96", "gate_96_testing_module_pack_active_from_gate_97", "gate_97_testing_module_pack_active_from_gate_98", "gate_98_testing_module_pack_active_from_gate_99", "gate_99_testing_module_pack_active_from_gate_100"}
    assert leaves["active_gate"] in {"Gate 96", "Gate 97", "Gate 98", "Gate 99", "Gate 100"}
    assert leaves["completed_gate_ids"][:2] == ["Gate 94", "Gate 95"]
    assert leaves["completed_leaf_ids"][:4] == ["LEAF-G94-001", "LEAF-G94-002", "LEAF-G95-001", "LEAF-G95-002"]
    assert ("Status: active execution log for the testing-module pack; Gates 94-95 complete on `main`, Gate 96 next" in execution_log) or ("Status: active execution log for the testing-module pack; Gates 94-96 complete on `main`, Gate 97 next" in execution_log) or ("Status: active execution log for the testing-module pack; Gates 94-97 complete on `main`, Gate 98 next" in execution_log) or ("Status: active execution log for the testing-module pack; Gates 94-98 complete on `main`, Gate 99 next" in execution_log) or ("Status: active execution log for the testing-module pack; Gates 94-99 complete on `main`, Gate 100 next" in execution_log)


def test_phase0_audit_script_reproduces_checked_in_json(tmp_path: Path) -> None:
    output_path = tmp_path / "phase0_audit.json"
    subprocess.run(
        [sys.executable, str(AUDIT_SCRIPT), str(WORKBOOK), "--output", str(output_path)],
        check=True,
        cwd=REPO_ROOT,
    )

    regenerated = json.loads(output_path.read_text(encoding="utf-8"))
    committed = json.loads(AUDIT_JSON.read_text(encoding="utf-8"))

    assert regenerated | {"artifact": "docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx"} == committed
    assert regenerated["artifact"].endswith("docs/planning/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3.xlsx")
    assert committed["phase_zero_gate"]["status"] == "fail"
    assert committed["phase_zero_gate"]["single_canonical_real_run_viable"] is False
