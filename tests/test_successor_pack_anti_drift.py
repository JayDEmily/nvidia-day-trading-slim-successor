"""Anti-drift checks for successor-pack closeout alignment."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
AGENTS = REPO_ROOT / "AGENTS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_LOG_v3.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v6.json"


def test_successor_pack_status_surfaces_agree_on_completed_tranche_and_next_gate() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert leaves["completed_gate_ids"] == [
        "Gate 59",
        "Gate 60",
        "Gate 61",
        "Gate 62",
        "Gate 63",
        "Gate 64",
    ]
    assert leaves["active_gate"] == "Gate 65"
    assert leaves["execution_status"] == "gate_64_complete_on_main_successor_pack_active_from_gate_65"

    assert "- Gates 59–64 — complete on `main`" in plans
    assert "closed through Gate 64" in plans
    assert "Gates 46–64 are merged on `main`" in plans

    assert "Current active gate: **Gate 65 in the V6 successor pack**. Gates 59–64 are complete on `main`" in gate_map


def test_execution_log_contains_successor_pack_receipt_recovery_block() -> None:
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "### Anti-drift receipt recovery — Gates 59–64 successor-pack closeout" in execution_log
    assert "Source merge commit: `000cc98`" in execution_log
    assert "Source merge commit: `ba37c55`" in execution_log
    assert "Source merge commit: `0765452`" in execution_log
    assert "This repair does not create a new numbered gate. It hardens the repo against status drift before Gate 65." in execution_log


def test_agents_file_freezes_the_four_surface_closeout_protocol() -> None:
    agents = AGENTS.read_text(encoding="utf-8")

    assert "## Anti-drift closeout protocol" in agents
    assert "repo-root `PLANS.md`" in agents
    assert "2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md" in agents
    assert "active leaf ledger" in agents
    assert "2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_LOG_v3.md" in agents
    assert "A gate is not closed if any one of those still points at the older active gate or older completed tranche." in agents
