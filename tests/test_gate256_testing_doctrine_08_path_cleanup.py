"""Gate 256 testing-doctrine numbered-08 path cleanup checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS = REPO_ROOT / "AGENTS.md"
PLANS = REPO_ROOT / "PLANS.md"
README = REPO_ROOT / "README.md"
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
PROCESS_LAW = REPO_ROOT / "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md"
TESTING = REPO_ROOT / "docs/08_TESTING_AND_PROMOTION.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-04-10_TESTING_DOCTRINE_08_PATH_CLEANUP_LEAVES_v1.json"
EXEC_LOG = REPO_ROOT / "docs/planning/2026-04-10_TESTING_DOCTRINE_08_PATH_CLEANUP_EXECUTION_LOG_v1.md"
CONTRADICTION = REPO_ROOT / "docs/planning/2026-04-10_TESTING_DOCTRINE_08_PATH_CLEANUP_CONTRADICTION_REPORT_v1.md"
OLD_TESTING = REPO_ROOT / ("docs/" + "TESTING_AND_PROMOTION.md")
RETIRED_NUMBERED_INTERACTIONS = REPO_ROOT / (
    "docs/" + "08_" + "GITHUB_OR_CHATGPT_GITHUB_INTERACTIONS.md"
)


def test_gate256_router_quartet_and_numbered_doctrine_path_are_closed_truthfully() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXEC_LOG.read_text(encoding="utf-8")

    assert TESTING.is_file()
    assert not OLD_TESTING.exists()
    assert "## Active pack\n\n- none" in plans
    assert "numbered-08 path cleanup pack is closed through Gate 256" in plans
    assert leaves["active_gate"] == "none"
    assert leaves["completed_gate_ids"] == ["Gate 256"]
    assert leaves["remaining_leaf_ids"] == []
    assert "Closed through Gate 256" in execution_log
    assert "Current active gate: **No active pack currently routed. The testing-doctrine numbered-08 path cleanup pack is closed through Gate 256" in gate_map


def test_gate256_live_authority_surfaces_use_the_numbered_testing_path() -> None:
    for path in [AGENTS, PLANS, README, NORMATIVE, PROCESS_LAW]:
        text = path.read_text(encoding="utf-8")
        assert "docs/08_TESTING_AND_PROMOTION.md" in text, path
        assert "docs/" + "TESTING_AND_PROMOTION.md" not in text, path


def test_gate256_retires_old_numbered_github_path_without_fabricating_file() -> None:
    contradiction = CONTRADICTION.read_text(encoding="utf-8")
    assert not RETIRED_NUMBERED_INTERACTIONS.exists()
    assert "old numbered GitHub/ChatGPT interactions path from repo references entirely" in contradiction
    for path in [AGENTS, PLANS, GATE_MAP, EXEC_LOG, CONTRADICTION]:
        assert (
            "docs/" + "08_" + "GITHUB_OR_CHATGPT_GITHUB_INTERACTIONS.md"
            not in path.read_text(encoding="utf-8")
        ), path
