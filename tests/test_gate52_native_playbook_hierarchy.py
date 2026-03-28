from __future__ import annotations

from datetime import datetime

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import (
    InventoryState,
    MarketRegimeContextInput,
    OptionsFlowContextInput,
    OptionsFlowMicroSnapshot,
    TemporalContextInput,
    TenorCurvePoint,
)
from nvda_desk.services.cognition_runtime import (
    DeskCognitionRuntime,
    DeskCognitionRuntimeResult,
)


def _supportive_runtime_result() -> DeskCognitionRuntimeResult:
    runtime = DeskCognitionRuntime(Settings())
    return runtime.run(
        temporal_input=TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-23T14:15:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-03-27T16:00:00-04:00"),
            next_event_at=datetime.fromisoformat("2026-03-23T17:00:00-04:00"),
            prior_session_return_pct=1.4,
            intraday_move_pct=0.8,
        ),
        regime_input=MarketRegimeContextInput(
            nvda_return_pct=0.8,
            nq_return_pct=0.5,
            es_return_pct=0.3,
            sox_return_pct=0.9,
            breadth_score=0.67,
            concentration_score=0.41,
            vix_level=18.4,
            vvix_level=84.0,
            us10y=4.22,
            us2y=4.04,
            usdjpy=148.9,
        ),
        options_flow_input=OptionsFlowContextInput(
            spot_price=118.0,
            front_dte=4,
            next_dte=11,
            front_atm_iv=59.0,
            next_atm_iv=60.0,
            front_realised_vol=60.0,
            next_realised_vol=61.0,
            put_call_skew=0.18,
            gamma_pressure_score=0.33,
            call_put_imbalance=-0.05,
            oi_concentration=0.44,
            atm_straddle_value=5.9,
            vix_level=18.4,
            vvix_level=84.0,
            spot_to_pin_distance_pct=1.9,
            vanna_proxy=0.02,
            charm_proxy=0.01,
            repeated_snapshot_sequence=[
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T18:10:00+00:00"),
                    front_atm_iv=59.8,
                    next_atm_iv=60.4,
                    put_call_skew=0.16,
                    gamma_pressure_score=0.36,
                    spot_to_pin_distance_pct=1.9,
                ),
                OptionsFlowMicroSnapshot(
                    ts=datetime.fromisoformat("2026-03-23T18:15:00+00:00"),
                    front_atm_iv=59.0,
                    next_atm_iv=60.0,
                    put_call_skew=0.18,
                    gamma_pressure_score=0.33,
                    spot_to_pin_distance_pct=1.9,
                ),
            ],
            tenor_iv_curve=[
                TenorCurvePoint(tenor_dte=4, atm_iv=59.0),
                TenorCurvePoint(tenor_dte=11, atm_iv=60.0),
                TenorCurvePoint(tenor_dte=25, atm_iv=60.8),
            ],
        ),
        inventory_state=InventoryState(
            existing_inventory_pct=10.0,
            fresh_cash_pct=70.0,
            overnight_inventory_pct=0.0,
            open_orders_count=0,
            capital_lockup_pct=12.0,
            cost_basis_gap_pct=0.5,
            thesis_state_input="valid",
            adverse_excursion_pct=-1.0,
            time_stop_minutes_remaining=180,
        ),
        risk_budget_remaining_pct=68.0,
    )


def test_gate52_emits_native_family_and_setup_variant_candidates() -> None:
    result = _supportive_runtime_result()
    eligibility = result.eligibility

    assert eligibility.active_family_ids == [
        "trend_continuation",
        "compression_release",
    ]
    assert eligibility.active_setup_variant_ids == [
        "opening_drive_continuation",
        "midday_compression_release",
    ]
    family_index = {candidate.family_id: candidate for candidate in eligibility.family_candidates}
    assert family_index["trend_continuation"].active_playbook_ids == ["continuation_ladder"]
    variant_index = {
        candidate.setup_variant_id: candidate for candidate in eligibility.setup_variant_candidates
    }
    assert variant_index["opening_drive_continuation"].legacy_playbook_id == "continuation_ladder"
    assert (
        variant_index["opening_drive_continuation"].execution_expression_id
        == "continuation_ladder_exec"
    )


def test_gate52_execution_tracks_family_and_setup_lineage() -> None:
    result = _supportive_runtime_result()
    execution = result.execution

    assert execution.active_playbook_ids == [
        "continuation_ladder",
        "compression_breakout",
    ]
    assert execution.active_setup_variant_ids == [
        "opening_drive_continuation",
        "midday_compression_release",
    ]
    assert execution.active_family_ids == ["trend_continuation", "compression_release"]
    assert execution.lead_playbook_id == "continuation_ladder"
    assert execution.lead_setup_variant_id == "opening_drive_continuation"
    assert execution.lead_family_id == "trend_continuation"
    assert execution.setup_variant_execution_styles == {
        "opening_drive_continuation": "trend_ladder_3_step",
        "midday_compression_release": "compression_release_ladder",
    }
