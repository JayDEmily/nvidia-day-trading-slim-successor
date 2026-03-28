from __future__ import annotations

from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from nvda_desk.db import (
    Bar1m,
    Instrument,
    OptionSnapshot,
    create_engine_from_url,
    create_schema,
    seed_dev_data,
)


def test_seed_dev_populates_sqlite(tmp_path: Path) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'seed.db'}"
    create_schema(database_url)
    engine = create_engine_from_url(database_url)
    with Session(engine) as session:
        summary = seed_dev_data(session)
    assert summary.instrument_count == 5
    assert summary.bar_count == 720
    assert summary.option_snapshot_count == 18

    with Session(engine) as session:
        nvda = session.scalar(select(Instrument).where(Instrument.symbol == "NVDA"))
        vix = session.scalar(select(Instrument).where(Instrument.symbol == "VIX"))
        vvix = session.scalar(select(Instrument).where(Instrument.symbol == "VVIX"))
        assert nvda is not None and vix is not None and vvix is not None
        bars = session.scalars(
            select(Bar1m).where(Bar1m.instrument_id == nvda.id)
        ).all()
        vix_bars = session.scalars(
            select(Bar1m).where(Bar1m.instrument_id == vix.id)
        ).all()
        vvix_bars = session.scalars(
            select(Bar1m).where(Bar1m.instrument_id == vvix.id)
        ).all()
        option_snapshots = session.scalars(
            select(OptionSnapshot).where(OptionSnapshot.instrument_id == nvda.id)
        ).all()
    assert len(bars) == 240
    assert len(vix_bars) == 240
    assert len(vvix_bars) == 240
    assert len(option_snapshots) == 18
