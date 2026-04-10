from __future__ import annotations

import os
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path

from alembic.config import Config
from sqlalchemy import create_engine, inspect, select, func
from sqlalchemy.orm import Session

from alembic import command
from nvda_desk.config import Settings
from nvda_desk.db.models import Instrument, OptionSnapshot, OptionsFlowHistoryObservation
from nvda_desk.db.session import create_session_factory
from nvda_desk.schemas.execution_records import CapitalStateSnapshotPayload
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture

REPO_ROOT = Path(__file__).resolve().parents[1]
ALEMBIC_INI = REPO_ROOT / 'alembic.ini'
ALEMBIC_DIR = REPO_ROOT / 'alembic'


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


def _seed_rows(session: Session, *, as_of_date: date, front_expiry: date, next_expiry: date) -> None:
    instrument = Instrument(symbol='NVDA', asset_class='equity')
    session.add(instrument)
    session.flush()
    for expiry, strike, option_type in (
        (front_expiry, Decimal('120'), 'Call'),
        (next_expiry, Decimal('125'), 'Put'),
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


def test_gate245_alembic_head_includes_options_flow_history_observation_table(tmp_path: Path) -> None:
    database_url = _upgrade_head(tmp_path / 'gate245_schema.db')
    inspector = inspect(create_engine(database_url))
    assert 'options_flow_history_observation' in inspector.get_table_names()
    columns = {column['name'] for column in inspector.get_columns('options_flow_history_observation')}
    assert {
        'symbol', 'observed_at', 'chain_ts', 'front_expiry', 'next_expiry',
        'partiality_state', 'record_completeness_flag', 'raw_source_authority',
        'lineage_json', 'derived_state_json', 'front_expiry_rows_json', 'next_expiry_rows_json'
    } <= columns


def test_gate245_persistence_is_append_only_and_runtime_outputs_do_not_change(tmp_path: Path) -> None:
    fixture = supportive_runtime_fixture()
    observed_at = fixture.temporal_input.ts.astimezone(UTC)
    database_url = _upgrade_head(tmp_path / 'gate245_runtime.db')
    session_factory = create_session_factory(database_url)
    with session_factory() as session:
        _seed_rows(
            session,
            as_of_date=observed_at.date(),
            front_expiry=observed_at.date().fromordinal(observed_at.date().toordinal() + fixture.options_flow_input.front_dte),
            next_expiry=observed_at.date().fromordinal(observed_at.date().toordinal() + fixture.options_flow_input.next_dte),
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

    disabled = DeskCognitionRuntime(Settings(database_url=database_url, options_flow_history_lane_enabled=False)).run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        capital_state_snapshot=capital,
        symbol='NVDA',
    )
    enabled_runtime = DeskCognitionRuntime(Settings(database_url=database_url, options_flow_history_lane_enabled=True))
    enabled_first = enabled_runtime.run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        capital_state_snapshot=capital,
        symbol='NVDA',
    )
    enabled_second = enabled_runtime.run(
        temporal_input=fixture.temporal_input.model_copy(update={'ts': fixture.temporal_input.ts.replace(minute=fixture.temporal_input.ts.minute + 1)}),
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        capital_state_snapshot=capital,
        symbol='NVDA',
    )

    assert enabled_first.execution == disabled.execution
    assert enabled_first.review == disabled.review
    assert enabled_first.capital_deployment_authority == disabled.capital_deployment_authority
    assert [packet.producer.stage_name for packet in enabled_first.stage_packets] == [packet.producer.stage_name for packet in disabled.stage_packets]
    assert enabled_first.options_flow_history_write_result is not None
    assert enabled_first.options_flow_history_write_result.status == 'persisted'
    with session_factory() as session:
        count = session.scalar(select(func.count()).select_from(OptionsFlowHistoryObservation))
        assert count == 2


def test_gate245_write_failure_is_bounded_and_non_authoritative(tmp_path: Path) -> None:
    fixture = supportive_runtime_fixture()
    runtime = DeskCognitionRuntime(Settings(database_url=f'sqlite+pysqlite:///{tmp_path / "missing.db"}', options_flow_history_lane_enabled=True))
    result = runtime.run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        symbol='NVDA',
    )
    assert result.options_flow_history_write_result is not None
    assert result.options_flow_history_write_result.status == 'write_failed'
    assert result.execution is not None
