from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path

from sqlalchemy.orm import Session

from nvda_desk.config import Settings
from nvda_desk.db.models import Instrument, OptionSnapshot
from nvda_desk.db.seed import create_schema
from nvda_desk.db.session import create_session_factory
from nvda_desk.testing.cognition_fixtures import supportive_runtime_fixture
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime


def _seed_rows(session: Session, *, as_of_date: date, front_expiry: date, next_expiry: date) -> None:
    instrument = Instrument(symbol='NVDA', asset_class='equity')
    session.add(instrument)
    session.flush()
    for expiry, strike in ((front_expiry, Decimal('120')), (next_expiry, Decimal('125'))):
        session.add(
            OptionSnapshot(
                instrument_id=instrument.id,
                as_of_date=as_of_date,
                expiry=expiry,
                option_type='Call',
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


def test_gate244_runtime_tap_builds_bounded_observation_record(tmp_path: Path) -> None:
    fixture = supportive_runtime_fixture()
    observed_at = fixture.temporal_input.ts.astimezone(UTC)
    db_url = f'sqlite+pysqlite:///{tmp_path / "gate244.db"}'
    create_schema(db_url)
    session_factory = create_session_factory(db_url)
    with session_factory() as session:
        _seed_rows(
            session,
            as_of_date=observed_at.date(),
            front_expiry=observed_at.date().fromordinal(observed_at.date().toordinal() + fixture.options_flow_input.front_dte),
            next_expiry=observed_at.date().fromordinal(observed_at.date().toordinal() + fixture.options_flow_input.next_dte),
        )

    runtime = DeskCognitionRuntime(Settings(database_url=db_url, options_flow_history_lane_enabled=True))
    result = runtime.run(
        temporal_input=fixture.temporal_input,
        regime_input=fixture.regime_input,
        options_flow_input=fixture.options_flow_input,
        inventory_state=fixture.inventory_state,
        risk_budget_remaining_pct=fixture.risk_budget_remaining_pct,
        symbol='NVDA',
    )

    observation = result.options_flow_history_observation
    assert observation is not None
    assert observation.derived_state == result.options_flow
    assert observation.lineage.raw_source_authority == 'persisted_option_snapshot'
    assert observation.front_expiry_rows and observation.next_expiry_rows
    assert {row.expiry for row in observation.front_expiry_rows} == {observation.front_expiry}
    assert {row.expiry for row in observation.next_expiry_rows} == {observation.next_expiry}
    assert result.options_flow_history_write_result is not None
    assert result.options_flow_history_write_result.status == 'persisted'
