"""Gate 114 research-mode clarity microtranche checks."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NORMATIVE = REPO_ROOT / "docs/01_NORMATIVE.md"
OPERATING_MODEL = REPO_ROOT / "docs/02_OPERATING_MODEL.md"
PROCESS_LAW = REPO_ROOT / "docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md"
AGENTS = REPO_ROOT / "AGENTS.md"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-30_RESEARCH_MODE_CLARITY_MICROTRANCHE_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-30_RESEARCH_MODE_CLARITY_MICROTRANCHE_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-30_RESEARCH_MODE_CLARITY_MICROTRANCHE_EXECUTION_LOG_v1.md"
CLOSEOUT = REPO_ROOT / "docs/planning/2026-03-30_GATE114_RESEARCH_MODE_CLARITY_CLOSEOUT.md"
README = REPO_ROOT / "docs/planning/tranche_briefing_template_pack/README.md"
HOWTO = REPO_ROOT / "docs/planning/tranche_briefing_template_pack/HOW_TO_USE_THESE_DOCUMENTS.md"

ALLOWED_CURRENT_GATE_MARKERS = {
    "Current active gate: **none — research-mode clarity microtranche closed through Gate 114 on `main`**.",
    "Current active gate: **Gate 115 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 116 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 117 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 118 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 119 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 120 in the historical-evaluation readiness pack**.",
    "Current active gate: **Gate 121 in the historical-evaluation readiness pack**.",
    "Current active gate: **none — historical-evaluation readiness pack closed through Gate 121 on `main`**.",
}


def test_research_mode_rule_is_explicit_in_authority_docs() -> None:
    normative = NORMATIVE.read_text(encoding="utf-8")
    operating_model = OPERATING_MODEL.read_text(encoding="utf-8")
    process_law = PROCESS_LAW.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")

    assert "research-mode ideation must seek asymmetry, dislocation, and edge before discussing implementation readiness" in normative
    assert "implementation-state caveats are mandatory in reporting and promotion judgment, but they must not pre-empt ideation unless the user asks" in normative
    assert "when the operator is in research or brainstorm mode, GPT should push for edge, asymmetry, and candidate setup discovery before discussing implementation readiness" in operating_model
    assert "Research-mode discussion is therefore idea-first" in operating_model
    assert "## Research-mode versus reporting-mode law" in process_law
    assert "avoid polluting idea generation with implementation-readiness, promotion, or live-operability caveats unless the operator asks" in process_law
    assert "Keep research-mode ideation separate from reporting-mode caveats" in agents
    assert "Do not contaminate ideation with implementation-readiness or live-operability caveats unless the user asks" in agents


def test_planning_templates_and_closed_pack_reflect_gate114() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    closeout = CLOSEOUT.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    howto = HOWTO.read_text(encoding="utf-8")

    assert ("## Active pack\n\n- none" in plans) or ("2026-03-30_HISTORICAL_EVALUATION_READINESS_GATES_v1.md" in plans)
    assert "2026-03-30_RESEARCH_MODE_CLARITY_MICROTRANCHE_GATES_v1.md" in plans
    assert "2026-03-30_RESEARCH_MODE_CLARITY_MICROTRANCHE_EXECUTION_LOG_v1.md" in plans
    assert any(marker in gate_map for marker in ALLOWED_CURRENT_GATE_MARKERS)
    assert "| Gate 114 | complete on `main` |" in gate_map
    assert "Status: closed research-mode clarity microtranche on `main`; Gate 114 complete, no active gate" in gates
    assert leaves["execution_status"] == "research_mode_clarity_microtranche_closed_through_gate_114_on_main"
    assert leaves["active_gate"] == "none — research-mode clarity microtranche closed through Gate 114 on main"
    assert leaves["global_rules"]["research_mode_must_seek_edge_before_readiness_commentary"] is True
    assert leaves["global_rules"]["readiness_caveats_belong_to_reporting_mode_unless_requested"] is True
    assert "Status: closed execution log for the research-mode clarity microtranche; Gate 114 complete on `main`, no active gate" in execution_log
    assert "Gate 114 complete on `main`; research-mode clarity microtranche closed honestly" in closeout
    assert "nvda_repo_research_mode_clarity_microtranche_closed_gate114_main_2026-03-30.zip" in closeout
    assert "Research-thread reminder" in readme
    assert "candidate edge and asymmetry" in readme
    assert "In brainstorming mode, optimise the planning brief for candidate edge and asymmetry before writing implementation-readiness commentary" in howto
