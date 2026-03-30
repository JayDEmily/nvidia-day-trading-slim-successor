"""Gate 104 targeted property and stateful tests."""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, initialize, rule

from nvda_desk.config import Settings
from nvda_desk.schemas.cognition import GammaState, PermissionState
from nvda_desk.schemas.state_policy import (
    DegradationStep,
    KillSwitchCondition,
    MutableRuntimeSurface,
)
from nvda_desk.services.event_store import EventStoreService
from nvda_desk.services.market_regime_context import MarketRegimeContextService
from nvda_desk.services.options_flow_context import OptionsFlowContextService
from nvda_desk.services.playbook_eligibility import PlaybookEligibilityService
from nvda_desk.services.posture_risk import PostureRiskService
from nvda_desk.services.real_data_loader import RealDataLoaderService
from nvda_desk.services.state_conditioned_modifier import StateConditionedModifierService
from nvda_desk.services.temporal_context import TemporalContextService
from nvda_desk.schemas.cognition import PlaybookEligibilityInput, PostureRiskInput
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

RAW_BUNDLE_PATH = Path("fixtures/real_data/gate_101_canonical_raw_runtime_bundle.json")
GATE104_DOC = Path("docs/planning/2026-03-30_GATE104_PROPERTY_STATEFUL.md")


def _base_runtime_outputs():
    fixture = supportive_runtime_fixture()
    temporal = TemporalContextService(Settings()).evaluate(fixture.temporal_input)
    regime = MarketRegimeContextService().evaluate(fixture.regime_input)
    options = OptionsFlowContextService().evaluate(fixture.options_flow_input)
    posture = PostureRiskService().evaluate(
        PostureRiskInput(
            temporal=temporal,
            regime=regime,
            options_flow=options,
            inventory=fixture.inventory_state,
            risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        )
    )
    return fixture, temporal, regime, options, posture


def _resolved_numeric(packet, surface: MutableRuntimeSurface) -> float | None:
    for item in packet.resolved_surfaces:
        if item.target_surface is surface:
            return item.effective_numeric_value
    return None


def _resolved_boolean(packet, surface: MutableRuntimeSurface) -> bool | None:
    for item in packet.resolved_surfaces:
        if item.target_surface is surface:
            return item.effective_boolean_value
    return None


@settings(max_examples=40, deadline=None)
@given(
    event_window_state=st.sampled_from(["same_session_event_window", "event_live_window"]),
    options_behavior_cluster=st.sampled_from(
        ["balanced_options_state", "negative_gamma_flush", "event_suppressed"]
    ),
    gamma_state=st.sampled_from([GammaState.SUPPORTIVE, GammaState.DESTABILISING]),
)
def test_gate104_property_modifier_law_remains_bounded_and_ordered(
    event_window_state: str,
    options_behavior_cluster: str,
    gamma_state: GammaState,
) -> None:
    fixture, temporal, regime, options, posture = _base_runtime_outputs()
    temporal = temporal.model_copy(update={"event_window_state": event_window_state})
    options = options.model_copy(
        update={
            "gamma_state": gamma_state,
            "options_behavior_cluster": options_behavior_cluster,
        }
    )
    packet = StateConditionedModifierService().evaluate(
        temporal_input=fixture.temporal_input,
        temporal=temporal,
        regime=regime,
        options_flow=options,
        posture=posture,
    )
    target = _resolved_numeric(packet, MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT)
    hedge_required = _resolved_boolean(packet, MutableRuntimeSurface.HEDGE_REQUIRED)

    assert target is not None
    assert 0.0 <= target <= 55.0

    if event_window_state == "event_live_window":
        assert packet.triggered_kill_switch is KillSwitchCondition.EVENT_LIVE_HARD_BLOCK
        assert packet.degradation_step is DegradationStep.VETO
        assert target == 0.0
    elif (
        options_behavior_cluster == "event_suppressed"
        and gamma_state is GammaState.DESTABILISING
    ):
        assert packet.triggered_kill_switch is KillSwitchCondition.EVENT_SUPPRESSED_WITH_NEGATIVE_GAMMA
        assert packet.degradation_step is DegradationStep.VETO
        assert target == 0.0
    elif (
        options_behavior_cluster == "negative_gamma_flush"
        and gamma_state is GammaState.DESTABILISING
    ):
        assert hedge_required is True
        assert target < 55.0


@settings(max_examples=40, deadline=None)
@given(
    permission_state=st.sampled_from(
        [PermissionState.ALLOW, PermissionState.DERISK, PermissionState.BLOCK]
    ),
    event_window_state=st.sampled_from(
        ["same_session_event_window", "event_imminent_window", "event_live_window"]
    ),
    options_behavior_cluster=st.sampled_from(
        ["balanced_options_state", "event_suppressed", "negative_gamma_flush"]
    ),
)
def test_gate104_property_playbook_eligibility_freezes_no_trade_law(
    permission_state: PermissionState,
    event_window_state: str,
    options_behavior_cluster: str,
) -> None:
    _, temporal, regime, options, posture = _base_runtime_outputs()
    temporal = temporal.model_copy(update={"event_window_state": event_window_state})
    options = options.model_copy(update={"options_behavior_cluster": options_behavior_cluster})
    posture = posture.model_copy(
        update={
            "permission_state": permission_state,
            "fresh_deployable_capital_pct": 0.0 if permission_state is PermissionState.BLOCK else posture.fresh_deployable_capital_pct,
        }
    )

    eligibility = PlaybookEligibilityService().evaluate(
        PlaybookEligibilityInput(
            temporal=temporal,
            regime=regime,
            options_flow=options,
            posture=posture,
        )
    )

    if permission_state is PermissionState.BLOCK:
        assert eligibility.add_candidates == []
        assert "permission_blocked" in eligibility.no_trade_reasons
    if event_window_state in {"event_imminent_window", "event_live_window"}:
        assert eligibility.add_candidates == []
        assert "event_window_veto" in eligibility.no_trade_reasons
    if options_behavior_cluster == "event_suppressed":
        assert eligibility.add_candidates == []
        assert "options_surface_event_suppressed" in eligibility.no_trade_reasons


class EventStoreSequenceStateMachine(RuleBasedStateMachine):
    """Generated sequence checks for ordered event-store queries."""

    def __init__(self) -> None:
        super().__init__()
        raw_bundle = RealDataLoaderService().load_json_bundle(RAW_BUNDLE_PATH)
        self.store = EventStoreService(raw_bundle.events)
        self.expected_lineage_keys = {key for event in raw_bundle.events for key in event.lineage_keys}
        first_event_at = min(event.event_at for event in raw_bundle.events)
        self.base_requested_at = first_event_at - timedelta(minutes=180)
        self.current_requested_at = self.base_requested_at
        self.last_next_event_at = None

    @initialize()
    def init_machine(self) -> None:
        self.current_requested_at = self.base_requested_at
        self.last_next_event_at = None

    @rule(delta_minutes=st.integers(min_value=0, max_value=180))
    def advance_and_query(self, delta_minutes: int) -> None:
        self.current_requested_at += timedelta(minutes=delta_minutes)
        snapshot = self.store.build_live_event_snapshot(
            requested_at=self.current_requested_at,
            symbol="NVDA",
        )
        if self.last_next_event_at is None:
            assert snapshot.next_event is None or snapshot.next_event.event_at >= self.current_requested_at
        elif snapshot.next_event is None:
            assert self.current_requested_at >= self.last_next_event_at
        else:
            assert snapshot.next_event.event_at >= self.last_next_event_at
            assert snapshot.next_event.event_at >= self.current_requested_at
        self.last_next_event_at = None if snapshot.next_event is None else snapshot.next_event.event_at
        assert set(snapshot.lineage_keys).issubset(self.expected_lineage_keys)
        assert len(snapshot.material_events) <= len(snapshot.nearby_events)


TestEventStoreSequenceStateMachine = EventStoreSequenceStateMachine.TestCase


def test_gate104_doc_freezes_targeted_scope_only() -> None:
    doc = GATE104_DOC.read_text(encoding="utf-8")

    assert "Status: Gate 104 complete on `main`; Gate 105 is the next active gate in the successor testing pack" in doc
    assert "Hypothesis was added to the repo dev dependencies for this gate only because the active pack explicitly requires targeted property/stateful testing." in doc
    assert "Gate 105 may begin" in doc
