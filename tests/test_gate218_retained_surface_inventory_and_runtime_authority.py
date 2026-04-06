"""Gate 218 retained-surface inventory and runtime-authority closeout checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
AGENTS = REPO_ROOT / "AGENTS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_EXECUTION_LOG_v1.md"
MANIFEST = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_RETAINED_SURFACE_MANIFEST_AND_CUTOVER_RULES_v1.md"
RUNTIME_NOTE = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_RUNTIME_SURFACE_AUDIT_READ_TRIGGER_AND_AUTHORITY_ADOPTION_v1.md"
DIFF_NOTE = REPO_ROOT / "docs/planning/2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_07_SOURCE_DIFF_AND_AGENTS_READ_TRIGGER_NOTE_v1.md"
RUNTIME_LEDGER = REPO_ROOT / "docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md"

ACTIVE_BRANCH = "work/gate-218-retained-surface-inventory-and-runtime-authority-20260406"
PROOF_COMMAND = (
    "/home/jds/dev/nvidia-day-trading/target_repo_gate201_evidence_inventory_and_provenance_planning_main_fullgit_2026-04-05/"
    ".venv/bin/python -m pytest -q tests/test_gate218_retained_surface_inventory_and_runtime_authority.py "
    "tests/test_planning_state_integrity.py"
)


def test_gate218_closeout_freezes_inventory_and_runtime_authority() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    payload = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    manifest = MANIFEST.read_text(encoding="utf-8")
    runtime_note = RUNTIME_NOTE.read_text(encoding="utf-8")
    diff_note = DIFF_NOTE.read_text(encoding="utf-8")
    runtime_ledger = RUNTIME_LEDGER.read_text(encoding="utf-8")

    assert "## Gate 218 successor inventory freeze" in manifest
    assert "Exact tracked top-level tree frozen on `work/gate-218-retained-surface-inventory-and-runtime-authority-20260406`" in manifest

    for entry in [
        ".env.example",
        ".gitignore",
        "AGENTS.md",
        "CHANGELOG.jsonl",
        "Makefile",
        "PLANS.md",
        "README.md",
        "alembic/",
        "alembic.ini",
        "backlog/",
        "config/",
        "data/",
        "docker-compose.yml",
        "docs/",
        "fixtures/",
        "hypothesis/",
        "pyproject.toml",
        "schemas/",
        "scripts/",
        "src/",
        "tests/",
        "uv.lock",
    ]:
        assert f"- `{entry}`" in manifest

    assert "No required runtime, doctrine, operator, fixture, or test surface named in the abstract retain list was missing" in manifest
    assert "`backlog/` is present in the successor repo" in manifest
    assert "`docs/audit/`, `docs/legacy/`, and `docs/status/` are present in the successor repo" in manifest
    assert "`hypothesis/` is present and tracked in the successor repo" in manifest
    assert "`docs/BUILD_PLAN.md`, `docs/RUNBOOK.md`, `docs/reference/`, and `docs/vocabulary/` are present and retained" in manifest
    assert "`.git/` is repo metadata" in manifest
    assert "`.pytest_cache/` is an untracked local cache" in manifest

    assert "the installed `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` contains the rescoped rewrite markers" in runtime_note
    assert "This Gate 218 verification binds the later audit to the installed successor doctrine surfaces only." in runtime_note
    assert "Gate 218 successor verification result" in diff_note
    assert "It does not claim that runtime semantics changed during Gate 218." in diff_note

    assert "## 0. Classification and read-trigger" in runtime_ledger
    assert "## 1.1 Relation to the wider doc stack" in runtime_ledger
    assert "## 1.2 Maintenance law" in runtime_ledger
    assert "specialised runtime authority ledger" in agents
    assert "not a universal front-door doctrine file" in agents
    assert "runtime surface ownership" in agents
    assert "stage packet versus workflow packet authority" in agents
    assert "compatibility surface or compatibility carriage law" in agents
    assert "downstream runtime reader permissions" in agents
    assert "replay or bounded-trace or review seam interpretation" in agents
    assert "API compatibility wrappers that preserve older read shapes over newer canonical runtime truth" in agents

    assert "- next active gate: `Gate 219`" in plans
    assert (
        "- active pack: slim active-repo cutover and substantive test-audit bootstrap pack "
        f"with Gate 218 complete on `{ACTIVE_BRANCH}`; Gate 219 not yet activated"
    ) in plans

    assert "Version: v1.31" in gate_map
    assert (
        "Current active gate: **none — Gate 218 in the slim active-repo cutover and substantive "
        f"test-audit bootstrap pack is complete on `{ACTIVE_BRANCH}`, and Gate 219 is planned but not yet activated.**"
    ) in gate_map
    assert f"Gate 218 | complete on `{ACTIVE_BRANCH}`" in gate_map
    assert "Gate 219 | planned" in gate_map
    assert "Gate 220 | planned" in gate_map
    assert "Gate 221 | planned" in gate_map

    assert (
        "Status: slim-successor planning pack with Gate 218 complete on "
        f"`{ACTIVE_BRANCH}`; Gates 219-221 planned, Gate 219 not yet activated."
    ) in gates

    assert payload["execution_status"] == "gate_218_complete_on_work_branch_gate_219_not_yet_activated"
    assert (
        payload["active_gate"]
        == "none — Gate 218 complete on work/gate-218-retained-surface-inventory-and-runtime-authority-20260406; Gate 219 not yet activated"
    )
    assert payload["completed_gate_ids"] == ["Gate 217", "Gate 218"]
    assert {"LEAF-G218-001", "LEAF-G218-002"} <= set(payload["completed_leaf_ids"])
    assert payload["pending_gate_ids"] == ["Gate 219", "Gate 220", "Gate 221"]
    assert set(payload["remaining_leaf_ids"]) == {
        "LEAF-G219-001",
        "LEAF-G219-002",
        "LEAF-G220-001",
        "LEAF-G220-002",
        "LEAF-G221-001",
        "LEAF-G221-002",
    }

    assert (
        "Status: successor execution log for slim active-repo cutover and substantive test-audit "
        f"bootstrap; Gate 218 complete on `{ACTIVE_BRANCH}`, Gates 219-221 planned, Gate 219 not yet activated."
    ) in execution_log
    assert "### LEAF-G218-001" in execution_log
    assert "### LEAF-G218-002" in execution_log
    assert PROOF_COMMAND in execution_log
    assert "repo-local successor environment still unavailable because /home/jds/dev/nvidia-day-trading-slim-successor/.venv/bin/python does not exist" in execution_log
    assert "Gate 218 is complete on `work/gate-218-retained-surface-inventory-and-runtime-authority-20260406`." in execution_log
    assert "Gate 219 remains planned and is not yet activated." in execution_log
    assert "runtime semantics changed during Gate 218" not in execution_log
