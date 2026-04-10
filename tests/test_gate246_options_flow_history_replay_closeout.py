from __future__ import annotations

import json
import os
from datetime import UTC, timedelta, date
from decimal import Decimal
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy.orm import Session

from nvda_desk.config import Settings
from nvda_desk.db.models import Instrument, OptionSnapshot
from nvda_desk.db.session import create_session_factory
from nvda_desk.schemas.execution_records import CapitalStateSnapshotPayload
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.services.options_flow_history import OptionsFlowHistoryStore
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]
ALEMBIC_INI = REPO_ROOT / 'alembic.ini'
ALEMBIC_DIR = REPO_ROOT / 'alembic'
PLANS = REPO_ROOT / 'PLANS.md'
GATE_MAP = REPO_ROOT / 'docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md'
LEAVES = REPO_ROOT / 'docs/planning/2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_LEAVES_v1.json'
EXECUTION_LOG = REPO_ROOT / 'docs/planning/2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_EXECUTION_LOG_v1.md'
CLOSEOUT = REPO_ROOT / 'docs/planning/2026-04-09_GATE246_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_CLOSEOUT.md'
CHECKLIST = REPO_ROOT / 'docs/planning/2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_DOCUMENT_TOUCH_CHECKLIST_v1.md'
SCOPE = REPO_ROOT / 'docs/planning/2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_SCOPE_NOTE_v1.md'
CONTRADICTION = REPO_ROOT / 'docs/planning/2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_CONTRADICTION_REPORT_v1.md'


def _router_truth_preserves_gate246_closeout(*, plans: str, gate_map: str) -> bool:
    original_closeout = (
        'Options and Flow Context History Lane implementation pack closed through Gate 246' in plans
        and 'main serial stack Steps 3-6 corrective implementation pack closed through Gate 241' in plans
        and 'Current active gate: **No active pack currently routed. The Options and Flow Context History Lane implementation pack is closed through Gate 246 in the uploaded workspace copy.**' in gate_map
    )
    reconciled_gate255_state = (
        'live prepared-handoff reconciliation pack is closed through Gate 255' in plans
        and 'Current active gate: **No active pack currently routed. The live prepared-handoff reconciliation pack is closed through Gate 255' in gate_map
        and '| Gate 241 | imported prepared handoff state reconciled in the live repo |' in gate_map
        and '| Gate 246 | imported prepared handoff state reconciled in the live repo |' in gate_map
        and '2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_GATES_v1.md' in gate_map
    )
    return original_closeout or reconciled_gate255_state


def _upgrade_head(db_path: Path) -> str:
    database_url = f'sqlite+pysqlite:///{db_path}'
    config = Config(str(ALEMBIC_INI))
    config.set_main_option('script_location', str(ALEMBIC_DIR))
    previous = os.environ.get('NVDA_DESK_DATABASE_URL')
    os.environ['NVDA_DESK_DATABASE_URL'] = database_url
    try:
        command.upgrade(config, 'head')
    finally:
        if previous is None:
            os.environ.pop('NVDA_DESK_DATABASE_URL', None)
        else:
            os.environ['NVDA_DESK_DATABASE_URL'] = previous
    return database_url


def _seed_rows(session: Session, *, as_of_date: date, front_expiry: date, next_expiry: date, far_expiry: date) -> None:
    instrument = Instrument(symbol='NVDA', asset_class='equity')
    session.add(instrument)
    session.flush()
    for expiry, strike, option_type in (
        (front_expiry, Decimal('120'), 'Call'),
        (next_expiry, Decimal('125'), 'Put'),
        (far_expiry, Decimal('140'), 'Call'),
    ):
        session.add(
            OptionSnapshot(
                instrument_id=instrument.id,
                as_of_date=as_of_date,
                expiry=expiry,
                option_type=option_type,
                strike=strike,
                bid=Decimal('1.00'),
                ask=Decimal('1.10'),
                last=Decimal('1.05'),
                volume=10,
                open_interest=20,
                iv=Decimal('0.61'),
                delta=Decimal('0.44'),
                gamma=Decimal('0.06'),
                delta_change=Decimal('0.01'),
                provenance='fixture',
                confidence='high',
                source_document='fixture',
                source_pages='1',
            )
        )
    session.commit()


def test_gate246_bounded_replay_stays_front_next_only_and_is_deterministic(tmp_path: Path) -> None:
    fixture = supportive_runtime_fixture()
    observed_at = fixture.temporal_input.ts.astimezone(UTC)
    database_url = _upgrade_head(tmp_path / 'gate246_runtime.db')
    session_factory = create_session_factory(database_url)
    with session_factory() as session:
        _seed_rows(
            session,
            as_of_date=observed_at.date(),
            front_expiry=observed_at.date().fromordinal(observed_at.date().toordinal() + fixture.options_flow_input.front_dte),
            next_expiry=observed_at.date().fromordinal(observed_at.date().toordinal() + fixture.options_flow_input.next_dte),
            far_expiry=observed_at.date().fromordinal(observed_at.date().toordinal() + fixture.options_flow_input.next_dte + 7),
        )

    capital = CapitalStateSnapshotPayload(
        capital_state_snapshot_id=1,
        created_at=observed_at,
        snapshot_ts=observed_at,
        cash=10000,
        equity=10000,
        buying_power=20000,
        gross_exposure=0,
        net_exposure=0,
        source='fixture',
    )

    runtime = DeskCognitionRuntime(Settings(database_url=database_url, options_flow_history_lane_enabled=True))
    first = runtime.run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        capital_state_snapshot=capital,
        symbol='NVDA',
    )
    second_ts = fixture.temporal_input.ts + timedelta(minutes=1)
    second = runtime.run(
        temporal_input=fixture.temporal_input.model_copy(update={'ts': second_ts}),
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        capital_state_snapshot=capital,
        symbol='NVDA',
    )

    store = OptionsFlowHistoryStore(session_factory)
    first_replay = store.list_by_symbol('NVDA')
    second_replay = store.list_by_symbol('NVDA')

    assert len(first_replay) == 2
    expected_observed = [second_ts.replace(tzinfo=None), fixture.temporal_input.ts.replace(tzinfo=None)]
    assert [payload.record.observed_at for payload in first_replay] == expected_observed
    assert [payload.record.observed_at for payload in second_replay] == expected_observed
    assert [payload.record.model_dump(mode='json') for payload in first_replay] == [payload.record.model_dump(mode='json') for payload in second_replay]

    far_expiry = observed_at.date().fromordinal(observed_at.date().toordinal() + fixture.options_flow_input.next_dte + 7)
    expected_front = observed_at.date().fromordinal(observed_at.date().toordinal() + fixture.options_flow_input.front_dte)
    expected_next = observed_at.date().fromordinal(observed_at.date().toordinal() + fixture.options_flow_input.next_dte)
    expected_outputs = [second.options_flow, first.options_flow]
    for replayed, expected in zip(first_replay, expected_outputs):
        record = replayed.record
        assert record.derived_state == expected
        assert record.partiality_state == 'complete'
        assert record.record_completeness_flag is True
        assert record.lineage.raw_source_authority == 'persisted_option_snapshot'
        assert record.lineage.capture_trigger == 'options_flow_context_output'
        assert record.chain_ts == record.observed_at
        assert record.lineage.observed_at.replace(tzinfo=None) == record.observed_at
        assert record.lineage.chain_ts.replace(tzinfo=None) == record.chain_ts
        assert record.front_expiry == expected_front
        assert record.next_expiry == expected_next
        assert record.front_expiry_rows and record.next_expiry_rows
        assert {row.expiry for row in record.front_expiry_rows} == {expected_front}
        assert {row.expiry for row in record.next_expiry_rows} == {expected_next}
        assert far_expiry not in {row.expiry for row in [*record.front_expiry_rows, *record.next_expiry_rows]}


def test_gate246_pack_closeout_control_surfaces_are_truthful() -> None:
    plans = PLANS.read_text(encoding='utf-8')
    gate_map = GATE_MAP.read_text(encoding='utf-8')
    leaves = json.loads(LEAVES.read_text(encoding='utf-8'))
    execution_log = EXECUTION_LOG.read_text(encoding='utf-8')
    closeout = CLOSEOUT.read_text(encoding='utf-8')
    checklist = CHECKLIST.read_text(encoding='utf-8')
    scope = SCOPE.read_text(encoding='utf-8')
    contradiction = CONTRADICTION.read_text(encoding='utf-8')

    assert '## Active pack\n\n- none' in plans
    assert _router_truth_preserves_gate246_closeout(plans=plans, gate_map=gate_map)
    assert (
        'Latest closed pack retained as evidence paired files:' in gate_map
        or 'Paired files:' in gate_map
    )
    assert leaves['active_gate'] == 'none'
    assert leaves['pending_gate_ids'] == []
    assert leaves['remaining_leaf_ids'] == []
    assert leaves['completed_gate_ids'] == ['Gate 242', 'Gate 243', 'Gate 244', 'Gate 245', 'Gate 246']
    assert execution_log.startswith('# 2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_EXECUTION_LOG_v1')
    assert 'Status: closed execution log retained as evidence' in execution_log
    assert 'Gate 246 closeout proof' in execution_log
    assert closeout.startswith('# 2026-04-09_GATE246_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_CLOSEOUT')
    assert 'no active pack is currently routed' in closeout
    assert 'closeout-reconciled checklist retained as evidence' in checklist
    assert 'Status: closed scope note retained as evidence' in scope
    assert 'Status: closed contradiction report retained as evidence' in contradiction
