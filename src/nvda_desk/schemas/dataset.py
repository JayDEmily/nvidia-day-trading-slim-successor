"""Typed contracts for deterministic real-data runtime preparation.

Gate E promotes the real-data path from bundle validation to prepared runtime
snapshots, explicit source lineage, cognition-ready conversion, and auditable
sanity reporting.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.cognition import OptionsFlowContextInput, TemporalContextInput
from nvda_desk.schemas.events import LiveEventSnapshot, NormalisedEventRecord


class ProvenanceRecord(BaseModel):
    """Provenance metadata for one imported dataset artifact."""

    model_config = ConfigDict(extra="forbid")

    source_name: str
    source_type: str
    captured_at: datetime
    symbol: str
    note: str = ""


class BarRecord(BaseModel):
    """One replay-ready OHLCV bar."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = Field(ge=0.0)


class OptionQuote(BaseModel):
    """One option quote inside a replay-ready chain snapshot."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    expiry: datetime
    strike: float
    side: str
    bid: float
    ask: float
    last: float | None = None
    iv: float | None = None
    delta: float | None = None
    gamma: float | None = None
    oi: float | None = None
    volume: float | None = None


class OptionSnapshotSequence(BaseModel):
    """Repeated-snapshot metadata for intraday chain sequences."""

    model_config = ConfigDict(extra="forbid")

    sequence_id: str
    snapshot_index: int = Field(ge=0)
    snapshot_count: int = Field(ge=1)
    window_minutes: int | None = Field(default=None, ge=0)


class OptionChainSnapshot(BaseModel):
    """Replay-ready option-chain snapshot for one symbol and timestamp."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    symbol: str
    sequence: OptionSnapshotSequence | None = None
    quotes: list[OptionQuote] = Field(default_factory=list)


class EventRecord(NormalisedEventRecord):
    """Replay-ready scheduled event record with preserved event richness."""


class RealDataBundle(BaseModel):
    """Replay-ready dataset bundle with explicit provenance."""

    model_config = ConfigDict(extra="forbid")

    provenance: ProvenanceRecord
    bars: list[BarRecord] = Field(default_factory=list)
    option_chain_snapshots: list[OptionChainSnapshot] = Field(default_factory=list)
    events: list[EventRecord] = Field(default_factory=list)


class PreparedStrikeCluster(BaseModel):
    """Prepared nearby strike cluster retained for downstream options logic."""

    model_config = ConfigDict(extra="forbid")

    strike: float
    side: str
    open_interest: float = Field(ge=0.0)
    volume: float = Field(ge=0.0)
    distance_to_spot_pct: float


class PreparedSequencePoint(BaseModel):
    """Prepared repeated-snapshot point derived from one chain sequence item."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    front_atm_iv: float
    next_atm_iv: float
    put_call_skew: float
    gamma_pressure_score: float
    spot_to_pin_distance_pct: float


class PreparedTenorPoint(BaseModel):
    """Prepared tenor point derived from one expiry on one chain snapshot."""

    model_config = ConfigDict(extra="forbid")

    tenor_dte: int = Field(ge=0)
    atm_iv: float = Field(ge=0.0)


class PreparedPinProgressionPoint(BaseModel):
    """Prepared distance-to-pin observation over a repeated snapshot sequence."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    distance_to_pin_pct: float


class PreparedRuntimeLineage(BaseModel):
    """Explicit lineage retained for one prepared runtime snapshot."""

    model_config = ConfigDict(extra="forbid")

    source_name: str
    source_type: str
    captured_at: datetime
    chain_ts: datetime
    aligned_bar_ts: datetime
    bar_age_seconds: int = Field(ge=0)
    event_ids: list[str] = Field(default_factory=list)
    event_lineage_keys: list[str] = Field(default_factory=list)
    sequence_id: str | None = None


class PreparedRuntimeSnapshot(BaseModel):
    """Runtime-ready snapshot distilled from aligned bars plus chain state."""

    model_config = ConfigDict(extra="forbid")

    ts: datetime
    symbol: str
    aligned_bar_ts: datetime
    bar_age_seconds: int = Field(ge=0)
    spot_price: float
    prior_close_price: float | None = None
    session_open_price: float
    interval_volume_shares: float = Field(ge=0.0, default=0.0)
    cumulative_session_volume: float = Field(ge=0.0, default=0.0)
    session_vwap: float | None = None
    distance_to_vwap_pct: float | None = None
    vwap_slope_5m_pct: float | None = None
    opening_range_high_5m: float | None = None
    opening_range_low_5m: float | None = None
    opening_range_break_count: int = Field(ge=0, default=0)
    price_realised_vol_5m_pct: float | None = None
    price_realised_vol_15m_pct: float | None = None
    relative_volume_ratio: float | None = None
    rolling_range_5m_pct: float | None = None
    impulse_age_bars: int | None = None
    intraday_move_pct: float
    prior_session_return_pct: float = 0.0
    front_expiry: datetime
    next_expiry: datetime
    front_dte: int = Field(ge=0)
    next_dte: int = Field(ge=0)
    front_atm_iv: float
    next_atm_iv: float
    put_call_skew: float
    gamma_pressure_score: float = Field(ge=0.0, le=1.0)
    call_put_imbalance: float = Field(ge=-1.0, le=1.0)
    oi_concentration: float = Field(ge=0.0, le=1.0)
    atm_straddle_value: float = Field(ge=0.0)
    front_realised_vol: float = Field(ge=0.0, default=0.0)
    next_realised_vol: float = Field(ge=0.0, default=0.0)
    snapshot_sequence_id: str | None = None
    snapshot_index: int = Field(ge=0, default=0)
    snapshot_count: int = Field(ge=1, default=1)
    snapshot_window_minutes: int | None = Field(default=None, ge=0)
    dominant_strike: float | None = None
    spot_to_pin_distance_pct: float = 0.0
    pin_progression_bias: str = "untracked"
    next_event_at: datetime | None = None
    live_event_snapshot: LiveEventSnapshot | None = None
    call_oi_near_spot: float = Field(ge=0.0, default=0.0)
    put_oi_near_spot: float = Field(ge=0.0, default=0.0)
    front_volume_near_spot: float = Field(ge=0.0, default=0.0)
    next_volume_near_spot: float = Field(ge=0.0, default=0.0)
    nearby_strike_clusters: list[PreparedStrikeCluster] = Field(default_factory=list)
    repeated_snapshot_sequence: list[PreparedSequencePoint] = Field(default_factory=list)
    tenor_iv_curve: list[PreparedTenorPoint] = Field(default_factory=list)
    pin_progression_sequence: list[PreparedPinProgressionPoint] = Field(default_factory=list)
    lineage: PreparedRuntimeLineage


class PreparedRuntimeDataset(BaseModel):
    """Prepared runtime dataset retaining all snapshots and source provenance."""

    model_config = ConfigDict(extra="forbid")

    dataset_id: str
    symbol: str
    provenance: ProvenanceRecord
    snapshots: list[PreparedRuntimeSnapshot] = Field(default_factory=list)


class RuntimeSnapshotSanityReport(BaseModel):
    """Deterministic audit report for prepared runtime snapshots."""

    model_config = ConfigDict(extra="forbid")

    report_id: str
    symbol: str
    total_bars: int = Field(ge=0)
    total_chain_snapshots: int = Field(ge=0)
    prepared_snapshot_count: int = Field(ge=0)
    repeated_sequence_count: int = Field(ge=0)
    max_sequence_length: int = Field(ge=0)
    orphan_bar_count: int = Field(ge=0)
    orphan_chain_count: int = Field(ge=0)
    duplicate_bar_ts_count: int = Field(ge=0)
    duplicate_chain_ts_count: int = Field(ge=0)
    aligned_bar_coverage_pct: float = Field(ge=0.0, le=100.0)
    aligned_chain_coverage_pct: float = Field(ge=0.0, le=100.0)
    max_bar_age_seconds: int = Field(ge=0)
    monotonic_snapshot_timestamps: bool
    event_linked_snapshot_count: int = Field(ge=0)
    reasons: list[str] = Field(default_factory=list)


class PreparedRuntimeFixturePack(BaseModel):
    """Deterministic fixture pack for repeated prepared-runtime ingestion tests."""

    model_config = ConfigDict(extra="forbid")

    pack_id: str
    bundle: RealDataBundle
    prepared_dataset: PreparedRuntimeDataset
    sanity_report: RuntimeSnapshotSanityReport


class RealDataCognitionInputs(BaseModel):
    """Cognition-ready inputs derived from one prepared runtime snapshot."""

    model_config = ConfigDict(extra="forbid")

    snapshot_ts: datetime
    lineage: PreparedRuntimeLineage
    temporal_input: TemporalContextInput
    options_flow_input: OptionsFlowContextInput
