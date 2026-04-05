"""Gate 126 temporal-threshold authority checks."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.config_models import (
    CoefficientAuthorityDocument,
    TemporalThresholdId,
    TimingParameterId,
)
from nvda_desk.domain.session_clock import SessionClockPhase
from nvda_desk.domain.temporal_state import TemporalSignalInput, TemporalStateClassifier

REPO_ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = REPO_ROOT / "config/coefficient_authority.v1.yaml"
PLANS = REPO_ROOT / "PLANS.md"
GATE_MAP = REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
GATES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_GATES_v1.md"
LEAVES = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_LEAVES_v1.json"
EXECUTION_LOG = REPO_ROOT / "docs/planning/2026-03-31_SIGNAL_COEFFICIENT_AUTHORITY_EXECUTION_LOG_v1.md"
RECEIPT = REPO_ROOT / "docs/planning/2026-03-31_GATE126_BOUNDED_TEMPORAL_THRESHOLD_AUTHORITY.md"


def test_gate126_temporal_classifier_reads_governed_thresholds_and_timing_windows() -> None:
    authority = CoefficientAuthorityDocument.from_yaml_path(AUTHORITY)
    classifier = TemporalStateClassifier(Settings())

    threshold_index = authority.temporal_threshold_index()
    timing_index = authority.timing_parameter_index()
    assert threshold_index[TemporalThresholdId.ANCHOR_VWAP_DIST_BPS_MAX].baseline == 35
    assert timing_index[TimingParameterId.POWER_HOUR_WINDOW_MIN].baseline == 60
    assert timing_index[TimingParameterId.UNWIND_WINDOW_MIN].baseline == 30

    anchor = classifier.classify(
        TemporalSignalInput(
            ts=__import__("datetime").datetime(2026, 3, 31, 15, 0, tzinfo=__import__("datetime").timezone.utc),
            distance_to_vwap_pct=0.0020,
            price_realised_vol_5m_pct=0.50,
            price_realised_vol_15m_pct=0.60,
            relative_volume_ratio=1.00,
            rolling_range_5m_pct=0.30,
            opening_range_break_count=0,
            impulse_age_bars=5,
            vwap_slope_5m_pct=0.02,
        )
    )

    assert anchor.phase is SessionClockPhase.EARLY_ANCHOR
    assert any(tag.startswith("threshold_authority_version:") for tag in anchor.evidence_tags)

    power_hour = classifier.classify(
        TemporalSignalInput(
            ts=__import__("datetime").datetime(2026, 3, 31, 19, 10, tzinfo=__import__("datetime").timezone.utc),
            relative_volume_ratio=1.20,
        )
    )
    assert power_hour.phase is SessionClockPhase.POWER_HOUR
    assert any(tag.startswith("timing_authority_version:") for tag in power_hour.evidence_tags)


def test_gate126_closeout_advances_pack_to_gate127() -> None:
    plans = PLANS.read_text(encoding="utf-8")
    gate_map = GATE_MAP.read_text(encoding="utf-8")
    gates = GATES.read_text(encoding="utf-8")
    leaves = json.loads(LEAVES.read_text(encoding="utf-8"))
    execution_log = EXECUTION_LOG.read_text(encoding="utf-8")
    receipt = RECEIPT.read_text(encoding="utf-8")

    assert "Gates 122-126 complete and Gate 127 now active" in plans or "signal-coefficient authority pack closed through Gate 127" in plans
    assert (
        "Current active gate: **Gate 127 in the signal-coefficient authority pack**." in gate_map
        or "Current active gate: **none — signal-coefficient authority pack closed through Gate 127 on `main`**." in gate_map
        or "Current active gate: **Gate 128 in the post-flight repo consistency pack**." in gate_map
        or "Current active gate: **Gate 129 in the post-flight repo consistency pack**." in gate_map
        or "Current active gate: **Gate 130 in the post-flight repo consistency pack**." in gate_map
        or "Current active gate: **Gate 131 in the post-flight repo consistency pack**." in gate_map
        or "Current active gate: **none — post-flight repo consistency pack closed through Gate 131 on `main`**." in gate_map or "Current active gate: **Gate 149 in the stage-local handoff and terminal-risk seams pack**." in gate_map or "Current active gate: **none — stage-local handoff and terminal-risk seams pack closed through Gate 149 on `main`**." in gate_map
    )
    assert "Status: active signal-coefficient authority pack; Gates 122-126 complete on `main`, Gate 127 active" in gates or "Status: closed signal-coefficient authority pack on `main`; Gates 122-127 complete, no active gate" in gates
    assert leaves["execution_status"] in {"gate_126_complete_gate_127_active_on_main", "signal_coefficient_authority_pack_closed_through_gate_127_on_main"}
    assert leaves["active_gate"] in {"Gate 127", "none — signal-coefficient authority pack closed through Gate 127 on main"}
    assert leaves["completed_gate_ids"][:5] == ["Gate 122", "Gate 123", "Gate 124", "Gate 125", "Gate 126"]
    assert "Status: active execution log for the signal-coefficient authority pack; Gates 122-126 complete on `main`, Gate 127 active" in execution_log or "Status: closed execution log for the signal-coefficient authority pack; Gates 122-127 complete on `main`, no active gate" in execution_log
    assert "Status: complete on `main`; Gate 127 is now the active gate" in receipt or "Status: complete on `main`; signal-coefficient authority pack is now closed through Gate 127" in receipt
