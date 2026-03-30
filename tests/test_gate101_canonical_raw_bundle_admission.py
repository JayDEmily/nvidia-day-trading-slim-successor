"""Gate 101 canonical raw-bundle admission tests."""

from __future__ import annotations

import json
from pathlib import Path

from nvda_desk.schemas.dataset import RealDataBundle
from nvda_desk.services.real_data_loader import RealDataLoaderService

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_BUNDLE_PATH = REPO_ROOT / "fixtures/real_data/gate_101_canonical_raw_runtime_bundle.json"
FIXTURE_PACK_PATH = REPO_ROOT / "fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json"
ADMISSION_DOC = REPO_ROOT / "docs/planning/2026-03-30_GATE101_CANONICAL_RAW_BUNDLE_ADMISSION.md"


def test_gate101_admitted_raw_bundle_matches_checked_in_fixture_pack_bundle() -> None:
    raw_bundle = json.loads(RAW_BUNDLE_PATH.read_text(encoding="utf-8"))
    fixture_pack = json.loads(FIXTURE_PACK_PATH.read_text(encoding="utf-8"))
    validated = RealDataBundle.model_validate(raw_bundle)

    assert validated.model_dump(mode="json") == fixture_pack["bundle"]
    assert validated.provenance.symbol == "NVDA"
    assert len(validated.bars) == 4
    assert len(validated.option_chain_snapshots) == 3
    assert len(validated.events) == 2


def test_gate101_raw_bundle_rebuilds_the_checked_in_prepared_dataset_and_sanity_report() -> None:
    service = RealDataLoaderService()
    raw_bundle = service.load_json_bundle(RAW_BUNDLE_PATH)
    fixture_pack = service.load_fixture_pack(FIXTURE_PACK_PATH)

    rebuilt_dataset = service.prepare_runtime_dataset(
        raw_bundle, dataset_id=fixture_pack.prepared_dataset.dataset_id
    )
    rebuilt_report = service.build_runtime_snapshot_sanity_report(raw_bundle, rebuilt_dataset)

    assert rebuilt_dataset == fixture_pack.prepared_dataset
    assert rebuilt_report == fixture_pack.sanity_report


def test_gate101_admission_doc_freezes_the_repo_truth_basis() -> None:
    admission = ADMISSION_DOC.read_text(encoding="utf-8")

    assert "Status: Gate 101 complete on `main`; Gate 102 is the next active gate" in admission
    assert "It was **not** reconstructed from the workbook" in admission
    assert "fixtures/real_data/gate_101_canonical_raw_runtime_bundle.json" in admission
    assert "RealDataLoaderService.prepare_runtime_dataset(...)" in admission
