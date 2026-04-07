"""Anti-drift checks for successor-pack closeout alignment."""

from __future__ import annotations

import json
from pathlib import Path

from tests._successor_pack_helpers import successor_pack_position

REPO_ROOT = Path(__file__).resolve().parents[1]
PLANS = REPO_ROOT / "PLANS.md"
AGENTS = REPO_ROOT / "AGENTS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
EXECUTION_LOG = (
    REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_LOG_v3.md"
)
LEAVES = REPO_ROOT / "docs/planning/2026-03-27_COGNITIVE_WORKFLOW_MODIFICATION_LEAVES_v6.json"


def test_successor_pack_status_surfaces_agree_on_completed_tranche_and_next_gate() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))

    assert leaves["completed_gate_ids"][:6] == [
        "Gate 59",
        "Gate 60",
        "Gate 61",
        "Gate 62",
        "Gate 63",
        "Gate 64",
    ]
    assert successor_pack_position(leaves["active_gate"]) >= 65
    assert leaves["execution_status"].startswith("gate_") and (
        "_successor_pack_active_from_gate_" in leaves["execution_status"]
        or "_successor_pack_closed_after_gate_" in leaves["execution_status"]
    )

    assert ("signal-coefficient authority pack closed through Gate 127" in plans) or ("no active pack currently routed" in plans)
    assert (
        "post-flight repo consistency pack active at Gate 128" in plans
        or "post-flight repo consistency pack active at Gate 129" in plans
        or "post-flight repo consistency pack active at Gate 130" in plans
        or "post-flight repo consistency pack active at Gate 131" in plans
        or "no active pack currently routed; post-flight repo consistency pack closed through Gate 131 on `main`" in plans
        or "stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`" in plans
        or "active gate: Gate 149 reopened on `work/gate-149-reopen-full-suite-closeout-20260402`" in plans
        or "bounded trace scenario review pack active at Gate 133 on `main`" in plans
        or "bounded trace scenario review pack active at Gate 134 on `main`" in plans
        or "no active pack currently routed; bounded trace scenario review pack closed through Gate 134 on `main`" in plans
        or "stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`" in plans
        or "active gate: Gate 149 reopened on `work/gate-149-reopen-full-suite-closeout-20260402`" in plans
    )

    assert "Gates 59–79 are complete on `main`" in gate_map
    assert (
        ("Current active gate: **Gate 81 in the corrective reconstruction pack**." in gate_map)
        or (
            "Current active gate: **none — the V6 successor pack is closed through Gate 79 on `main`**."
            in gate_map
        )
        or (
            "Current active gate: **none — the corrective reconstruction pack is closed through Gate 87 on `main`**."
            in gate_map
        )
        or (
            "Current active gate: **Gate 88 in the financial-calendar interstitial pack**."
            in gate_map
        )
        or (
            "Current active gate: **Gate 89 in the financial-calendar interstitial pack**."
            in gate_map
        )
        or (
            "Current active gate: **Gate 90 in the financial-calendar interstitial pack**."
            in gate_map
        )
        or (
            "Current active gate: **Gate 91 in the financial-calendar interstitial pack**."
            in gate_map
        )
        or (
            "Current active gate: **Gate 92 in the financial-calendar runtime-integration pack**."
            in gate_map
        )
        or (
            "Current active gate: **Gate 93 in the financial-calendar runtime-integration pack**."
            in gate_map
        )
        or (
            "Current active gate: **none — the financial-calendar runtime-integration pack is closed through Gate 93 on `main`**."
            in gate_map
        )
        or (
            "Current active gate: **Gate 128 in the post-flight repo consistency pack**."
            in gate_map
        )
        or (
            "Current active gate: **Gate 129 in the post-flight repo consistency pack**."
            in gate_map
        )
        or (
            "Current active gate: **Gate 130 in the post-flight repo consistency pack**."
            in gate_map
        ) or (
            "Current active gate: **Gate 131 in the post-flight repo consistency pack**."
            in gate_map
        ) or (
            "Current active gate: **none — post-flight repo consistency pack closed through Gate 131 on `main`**." in gate_map
        ) or (
            "Current active gate: **Gate 149 in the stage-local handoff and terminal-risk seams pack**." in gate_map
        ) or (
            "Current active gate: **none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`**." in gate_map
        ) or (
            "Current active gate: **Gate 133 in the bounded trace scenario review pack**."
            in gate_map
        ) or (
            "Current active gate: **Gate 134 in the bounded trace scenario review pack**."
            in gate_map
        ) or (
            "Current active gate: **none — bounded trace scenario review pack closed through Gate 134 on `main`**." in gate_map
        ) or (
            "Current active gate: **Gate 149 in the stage-local handoff and terminal-risk seams pack**." in gate_map
        ) or (
            "Current active gate: **none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`**." in gate_map
        ) or (
            "Current active gate: **No active pack currently routed. The successor retained-test cleanup execution pack is closed through Gate 225 on `work/gate-225-retained-test-cleanup-closeout-20260406`.**" in gate_map
        )
    )


def test_execution_log_contains_successor_pack_receipt_recovery_block() -> None:
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")

    assert "### Anti-drift receipt recovery — Gates 59–64 successor-pack closeout" in execution_log
    assert "Source merge commit: `000cc98`" in execution_log
    assert "Source merge commit: `ba37c55`" in execution_log
    assert "Source merge commit: `0765452`" in execution_log
    assert (
        "This repair does not create a new numbered gate. It hardens the repo against status drift before Gate 65."
        in execution_log
    )


def test_agents_file_freezes_the_four_surface_closeout_protocol() -> None:
    agents = AGENTS.read_text(encoding="utf-8")

    assert ("## Anti-drift closeout protocol" in agents) or ("## Anti-drift behaviour" in agents)
    assert "repo-root `PLANS.md`" in agents
    assert "2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md" in agents
    assert "active leaf ledger" in agents
    assert "the active execution log named by repo-root `PLANS.md`" in agents
    assert (
        "A gate is not closed if any one of those still points at the older active gate or older completed tranche."
        in agents
    ) or (
        "Do not treat a gate as closed until repo-root `PLANS.md`, the canonical gate map, the active leaf ledger, and the active execution log move together on the same branch." in agents
    )
