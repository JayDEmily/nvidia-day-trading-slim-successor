"""Gate 113 execution-authority microtranche checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROCESS_LAW = REPO_ROOT / "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md"
AGENTS = REPO_ROOT / "AGENTS.md"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-30_EXECUTION_AUTHORITY_MICROTRANCHE_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-30_EXECUTION_AUTHORITY_MICROTRANCHE_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-30_EXECUTION_AUTHORITY_MICROTRANCHE_EXECUTION_LOG_v1.md"
CLOSEOUT = REPO_ROOT / "docs/planning/2026-03-30_GATE113_EXECUTION_AUTHORITY_MICROTRANCHE_CLOSEOUT.md"
VOCAB = "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"
PACKET = "docs/03_DOMAIN_MODEL.md"


def test_execution_mode_and_agents_name_authority_rereads() -> None:
    process_law = PROCESS_LAW.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")

    assert VOCAB in process_law
    assert PACKET in process_law
    assert "the active vocabulary authority named by the active gates master" in process_law
    assert "the active packet/data contract authority named by the active gates master" in process_law
    assert "the active pack does not name its vocabulary authority or packet/data contract authority cleanly" in process_law

    assert VOCAB in agents
    assert PACKET in agents
    assert "the active vocabulary authority named by the active gate master" in agents
    assert "the active packet/data contract authority named by the active gate master" in agents


def test_routed_pack_or_latest_closed_pack_names_authorities_cleanly() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    closeout = CLOSEOUT.read_text(encoding="utf-8")

    assert "## Active pack\n\n- none" in plans
    assert "2026-03-30_EXECUTION_AUTHORITY_MICROTRANCHE_GATES_v1.md" in plans
    assert VOCAB in gates
    assert PACKET in gates
    assert leaves["global_rules"]["execution_thread_must_reread_named_vocabulary_authority"] is True
    assert leaves["global_rules"]["execution_thread_must_reread_named_packet_contract_authority"] is True
    assert leaves["execution_status"] == "execution_authority_microtranche_closed_through_gate_113_on_main"
    assert leaves["active_gate"] == "none — execution-authority microtranche closed through Gate 113 on main"
    assert ("Current active gate: **none — execution-authority microtranche closed through Gate 113 on `main`**." in gate_map) or ("Current active gate: **none — research-mode clarity microtranche closed through Gate 114 on `main`**." in gate_map)
    assert "Status: closed execution log for the execution-authority microtranche; Gate 113 complete on `main`, no active gate" in execution_log
    assert "Gate 113 complete on `main`; execution-authority microtranche closed honestly" in closeout
    assert "nvda_repo_execution_authority_microtranche_closed_gate113_main_2026-03-30.zip" in closeout
