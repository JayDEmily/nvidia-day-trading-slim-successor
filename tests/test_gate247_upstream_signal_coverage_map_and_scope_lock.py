"""Gate 247 checkpoint tests for the upstream signal coverage and scope lock after pack closeout."""

from __future__ import annotations

import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


def _require_gate247_router_and_scope_state(
    *,
    plans: str,
    gate_map: str,
    coverage: str,
    leaves: dict[str, object],
) -> None:
    """Validate the retained coverage-map state after truthful pack closeout."""

    if (
        "UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_GATES_v1.md" not in plans
        and "UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_GATES_v1.md" not in gate_map
    ):
        raise RuntimeError("CHECKPOINT_FAILURE:gate247.router.routes_upstream_pack")
    if (
        "no active pack is currently routed" not in plans.lower()
        and "no active pack currently routed" not in plans.lower()
    ):
        raise RuntimeError("CHECKPOINT_FAILURE:gate247.router.no_active_pack_missing")
    if (
        (
            "closed through Gate 252" not in plans
            or "closed through Gate 252" not in gate_map
        )
        and (
            "live prepared-handoff reconciliation pack is closed through Gate 255" not in plans
            or "| Gate 252 | imported prepared handoff state reconciled in the live repo |" not in gate_map
        )
    ):
        raise RuntimeError("CHECKPOINT_FAILURE:gate247.router.gate252_closeout_missing")
    if "cross_asset_regime_core" not in coverage:
        raise RuntimeError("CHECKPOINT_FAILURE:gate247.coverage.cross_asset_regime_core_missing")
    if "same_bucket_spread_baseline | not raw-captured yet | Class A | deferred" not in coverage:
        raise RuntimeError("CHECKPOINT_FAILURE:gate247.coverage.spread_baseline_deferred_missing")
    if leaves.get("routing_status") != "upstream_signal_completion_pack_closed_no_active_pack_routed":
        raise RuntimeError("CHECKPOINT_FAILURE:gate247.leaves.closed_routing_missing")
    if leaves.get("active_gate") != "none":
        raise RuntimeError("CHECKPOINT_FAILURE:gate247.leaves.no_active_gate_missing")


def _require_gate247_vocab_entries(vocabulary: dict[str, object]) -> None:
    """Validate the bounded vocabulary additions using explicit checkpoint logic."""

    entries = {entry["canonical_slug"]: entry for entry in vocabulary["entries"]}
    if entries["prepared_runtime_regime_packet"]["maps_to_contract"] != (
        "nvda_desk.schemas.dataset.PreparedRuntimeRegimePacket"
    ):
        raise RuntimeError("CHECKPOINT_FAILURE:gate247.vocabulary.regime_packet_mapping")
    if entries["prepared_participation_baseline_packet"]["maps_to_contract"] != (
        "nvda_desk.schemas.dataset.PreparedParticipationBaselinePacket"
    ):
        raise RuntimeError("CHECKPOINT_FAILURE:gate247.vocabulary.participation_packet_mapping")


def test_gate247_routes_new_pack_and_freezes_coverage_map() -> None:
    """Positive proof for the retained coverage-map state after closeout."""

    plans = (REPO_ROOT / "PLANS.md").read_text(encoding="utf-8")
    gate_map = (
        REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
    ).read_text(encoding="utf-8")
    coverage = (
        REPO_ROOT
        / "docs/planning/2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_RAW_SIGNAL_COVERAGE_MAP_v1.md"
    ).read_text(encoding="utf-8")
    leaves = json.loads(
        (
            REPO_ROOT
            / "docs/planning/2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_LEAVES_v1.json"
        ).read_text(encoding="utf-8")
    )

    _require_gate247_router_and_scope_state(
        plans=plans,
        gate_map=gate_map,
        coverage=coverage,
        leaves=leaves,
    )


def test_gate247_negative_proof_turns_red_when_deferred_family_is_removed() -> None:
    """Negative proof for the deferred-family checkpoint."""

    plans = (REPO_ROOT / "PLANS.md").read_text(encoding="utf-8")
    gate_map = (
        REPO_ROOT / "docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md"
    ).read_text(encoding="utf-8")
    coverage = (
        REPO_ROOT
        / "docs/planning/2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_RAW_SIGNAL_COVERAGE_MAP_v1.md"
    ).read_text(encoding="utf-8").replace(
        "same_bucket_spread_baseline | not raw-captured yet | Class A | deferred",
        "same_bucket_spread_baseline | silently_promoted | Class B | in_scope",
    )
    leaves = json.loads(
        (
            REPO_ROOT
            / "docs/planning/2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_LEAVES_v1.json"
        ).read_text(encoding="utf-8")
    )

    with pytest.raises(RuntimeError, match="gate247.coverage.spread_baseline_deferred_missing"):
        _require_gate247_router_and_scope_state(
            plans=plans,
            gate_map=gate_map,
            coverage=coverage,
            leaves=leaves,
        )


def test_gate247_vocab_additions_are_lawful_and_bounded() -> None:
    """Positive proof for the admitted vocabulary additions."""

    vocabulary = json.loads(
        (
            REPO_ROOT
            / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"
        ).read_text(encoding="utf-8")
    )

    _require_gate247_vocab_entries(vocabulary)


def test_gate247_vocab_negative_proof_turns_red_when_contract_mapping_drifts() -> None:
    """Negative proof for the bounded vocabulary mapping checkpoint."""

    vocabulary = json.loads(
        (
            REPO_ROOT
            / "docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json"
        ).read_text(encoding="utf-8")
    )
    for entry in vocabulary["entries"]:
        if entry["canonical_slug"] == "prepared_runtime_regime_packet":
            entry["maps_to_contract"] = "nvda_desk.schemas.dataset.DriftedPacket"
            break

    with pytest.raises(RuntimeError, match="gate247.vocabulary.regime_packet_mapping"):
        _require_gate247_vocab_entries(vocabulary)
