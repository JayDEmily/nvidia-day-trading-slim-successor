from __future__ import annotations

from pathlib import Path

from nvda_desk.schemas.dataset import PreparedRuntimeFixturePack
from nvda_desk.services.chain_to_cognition import ChainToCognitionService
from nvda_desk.services.real_data_loader import RealDataLoaderService

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PACK_PATH = REPO_ROOT / "fixtures" / "real_data" / "gate_e_prepared_runtime_fixture_pack.json"
RAW_BUNDLE_PATH = REPO_ROOT / "fixtures" / "real_data" / "gate_101_canonical_raw_runtime_bundle.json"


def _fixture_pack() -> PreparedRuntimeFixturePack:
    return RealDataLoaderService().load_fixture_pack(FIXTURE_PACK_PATH)


def test_gate115_fixture_pack_carries_normalised_features_and_coverage() -> None:
    pack = _fixture_pack()

    assert pack.sanity_report.normalised_feature_snapshot_coverage_pct == 100.0
    first = pack.prepared_dataset.snapshots[0]
    third = pack.prepared_dataset.snapshots[-1]

    assert first.normalised_features is not None
    assert first.normalised_features.intraday_move_vs_rolling_range_5m == 0.2504
    assert first.normalised_features.atm_straddle_vs_spot_pct == 7.069
    assert first.normalised_features.front_iv_vs_front_realised_vol_ratio is None
    assert third.normalised_features is not None
    assert third.normalised_features.intraday_move_vs_price_realised_vol_15m == 4.644
    assert third.normalised_features.front_iv_vs_front_realised_vol_ratio == 1.8438
    assert third.normalised_features.provenance["near_spot_front_volume_share"] == [
        "front_volume_near_spot",
        "front_expiry_total_volume",
    ]


def test_gate115_raw_bundle_rebuilds_normalised_features_deterministically() -> None:
    service = RealDataLoaderService()
    bundle = service.load_json_bundle(RAW_BUNDLE_PATH)
    rebuilt = service.prepare_runtime_dataset(bundle, dataset_id="gate-e-prepared-runtime-dataset")
    pack = _fixture_pack()

    assert rebuilt == pack.prepared_dataset


def test_gate115_chain_to_cognition_preserves_normalised_feature_carriage() -> None:
    pack = _fixture_pack()
    converted = ChainToCognitionService().convert_snapshot(pack.prepared_dataset.snapshots[-1])

    assert converted.normalised_features == pack.prepared_dataset.snapshots[-1].normalised_features
    assert converted.normalised_features is not None
    assert converted.normalised_features.next_iv_vs_next_realised_vol_ratio == 1.7157
