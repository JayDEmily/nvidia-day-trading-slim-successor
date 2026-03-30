"""Gate 110 AGENTS stabilisation checks."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS = REPO_ROOT / "AGENTS.md"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"


def test_agents_includes_process_law_and_router_hierarchy() -> None:
    agents = AGENTS.read_text(encoding="utf-8")

    assert "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md" in agents
    assert "repo-root `PLANS.md`" in agents
    assert "governs **how planning packs are created, amended, routed, and closed**" in agents
    assert "active gate master under `docs/planning/` only if repo-root `PLANS.md` names one" in agents
    assert "Do not add tranche history to AGENTS" not in agents


def test_governance_pack_advances_to_gate111_or_later() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")

    assert ("- none" in plans) or ("Gate 111 — next active gate on `main` in the repo-process governance pack" in plans) or ("closed through Gate 112" in plans)
    assert ("Current active gate: **Gate 111 in the repo-process governance pack**." in gate_map) or ("Current active gate: **Gate 112 in the repo-process governance pack**." in gate_map) or ("Current active gate: **none — repo-process governance pack closed through Gate 112 on `main`**." in gate_map)
    assert "| Gate 110 | complete on `main` |" in gate_map
    assert ("| Gate 111 | planned; next active gate |" in gate_map) or ("| Gate 111 | complete on `main` |" in gate_map)
