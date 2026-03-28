"""Tests for canonical import-registry, grammar-mapping, and Gate-B reports."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, cast

from nvda_desk.schemas.import_registry import (
    GrammarRole,
    ImplementationReadiness,
    RuntimeContractStatus,
)
from nvda_desk.services.import_registry import CanonicalImportRegistryService

EXPECTED_REPORT_INPUTS = {
    "mapping_seed": "docs/planning/2026-03-23_GATE_B_SOURCE_GRAMMAR_MAPPING.json",
    "registry_seed": "docs/planning/2026-03-23_GATE_B_SOURCE_REGISTRY.jsonl",
}


def test_gate_b_seed_files_exist_and_cover_the_same_universe() -> None:
    """Gate B should build from frozen source baselines, not prior enriched output."""
    service = CanonicalImportRegistryService(Path.cwd())
    registry_seed = service.load_registry_seed()
    mapping_seed = service.load_mapping_seed()
    assert len(registry_seed) == 129
    assert len(mapping_seed) == 129
    assert {item.canonical_id for item in registry_seed} == {
        item.canonical_id for item in mapping_seed
    }


def test_refresh_rebuilds_enriched_surfaces_from_seed_inputs() -> None:
    """Refreshing Gate B should ignore stale enriched values and rebuild from seed data."""
    source_root = Path.cwd()
    tmp_root = Path.cwd() / ".pytest_cache" / "gate_b_refresh_probe"
    if tmp_root.exists():
        shutil.rmtree(tmp_root)
    shutil.copytree(source_root / "docs" / "planning", tmp_root / "docs" / "planning")

    registry_path = tmp_root / "docs" / "planning" / "canonical_import_registry.jsonl"
    corrupted_rows = registry_path.read_text(encoding="utf-8").splitlines()
    corrupted_first = json.loads(corrupted_rows[0])
    corrupted_first["desk_role_priority"] = 999
    corrupted_first["implementation_readiness"] = "needs_scope_definition"
    corrupted_rows[0] = json.dumps(corrupted_first, separators=(",", ":"))
    registry_path.write_text("\n".join(corrupted_rows) + "\n", encoding="utf-8")

    service = CanonicalImportRegistryService(tmp_root)
    service.refresh_registry_surfaces()
    rebuilt_first = service.load_registry()[0]
    assert rebuilt_first.canonical_slug == "archetype_matcher"
    assert rebuilt_first.desk_role_priority == 50
    assert (
        rebuilt_first.implementation_readiness == ImplementationReadiness.READY_FOR_CONTRACT_IMPORT
    )


def test_canonical_registry_and_mapping_cover_the_same_universe() -> None:
    """Registry and mapping artefacts should cover the same canonical IDs."""
    service = CanonicalImportRegistryService(Path.cwd())
    registry = service.load_registry()
    mapping = service.load_mapping()
    registry_ids = {item.canonical_id for item in registry}
    mapping_ids = {item.canonical_id for item in mapping}
    assert len(registry) == 129
    assert registry_ids == mapping_ids
    assert service.coverage_summary()["orphan_count"] == 0


def test_canonical_mapping_populates_binding_grammar_roles() -> None:
    """The grammar mapping should populate all binding runtime roles."""
    service = CanonicalImportRegistryService(Path.cwd())
    mapping = service.load_mapping()
    roles = {item.grammar_role for item in mapping}
    assert GrammarRole.TEMPORAL_CONTEXT in roles
    assert GrammarRole.MARKET_REGIME_CONTEXT in roles
    assert GrammarRole.OPTIONS_FLOW_CONTEXT in roles
    assert GrammarRole.POSTURE_RISK_PERMISSION in roles
    assert GrammarRole.PLAYBOOK_ELIGIBILITY in roles
    assert GrammarRole.EXPRESSION_EXECUTION in roles
    assert GrammarRole.REVIEW_EXPLANATION in roles


def test_canonical_registry_summary_matches_preservation_split() -> None:
    """The canonical registry summary should expose stable preservation counts."""
    service = CanonicalImportRegistryService(Path.cwd())
    summary = cast(dict[str, Any], service.registry_summary())
    maturity_counts = cast(dict[str, int], summary["maturity_counts"])
    runtime_target_counts = cast(dict[str, int], summary["runtime_target_counts"])
    readiness_counts = cast(dict[str, int], summary["readiness_counts"])
    assert summary["total_items"] == 129
    assert summary["item_class_counts"] == {
        "cognition_fragment": 26,
        "feature": 32,
        "module": 71,
    }
    assert maturity_counts["conceptual_preserved"] >= 61
    assert runtime_target_counts["implemented_runtime"] == 10
    assert readiness_counts[ImplementationReadiness.READY_FOR_CONTRACT_IMPORT.value] >= 1
    assert summary["report_inputs"] == EXPECTED_REPORT_INPUTS


def test_canonical_registry_exposes_runtime_target_views_and_no_loss_check() -> None:
    """Runtime-target views should stay deterministic and preserve the full universe."""
    service = CanonicalImportRegistryService(Path.cwd())
    service.assert_no_loss(expected_total=129)
    implemented_ids = service.canonical_ids_for_runtime_target("implemented_runtime")
    evidence_ids = service.canonical_ids_for_runtime_target("evidence_only")
    assert len(implemented_ids) == 10
    assert len(evidence_ids) == 26
    assert implemented_ids == sorted(implemented_ids)


def test_registry_rows_expose_priority_readiness_and_affinity_fields() -> None:
    """Registry rows should expose Gate-B planning fields for import execution."""
    service = CanonicalImportRegistryService(Path.cwd())
    registry = service.load_registry()
    ladder_constructor = next(
        item for item in registry if item.canonical_slug == "ladder_constructor"
    )
    options_fragment = next(
        item for item in registry if item.canonical_slug == "options_flow_context_first_class"
    )
    macro_shock = next(item for item in registry if item.canonical_slug == "macro_shock_responder")

    assert ladder_constructor.primary_grammar_role == GrammarRole.PLAYBOOK_ELIGIBILITY
    assert ladder_constructor.desk_role_priority == 50
    assert (
        ladder_constructor.implementation_readiness
        == ImplementationReadiness.READY_FOR_CONTRACT_IMPORT
    )
    assert ladder_constructor.playbook_affinity == ["continuation_ladder"]
    assert ladder_constructor.options_affinity is True

    assert options_fragment.implementation_readiness == ImplementationReadiness.EVIDENCE_ONLY
    assert options_fragment.readiness_blockers == ["evidence_only_preservation"]
    assert options_fragment.options_affinity is True

    assert macro_shock.implementation_readiness == ImplementationReadiness.IMPLEMENTED_RUNTIME
    assert macro_shock.inventory_affinity is True


def test_canonical_grammar_mapping_summary_exposes_role_and_contract_coverage() -> None:
    """The grammar mapping summary should expose deterministic role coverage."""
    service = CanonicalImportRegistryService(Path.cwd())
    summary = cast(dict[str, Any], service.grammar_mapping_summary())
    runtime_target_counts = cast(dict[str, int], summary["runtime_target_counts"])
    grammar_role_counts = cast(dict[str, int], summary["grammar_role_counts"])
    architecture_role_counts = cast(dict[str, int], summary["architecture_role_counts"])
    contract_status_counts = cast(dict[str, int], summary["runtime_contract_status_counts"])
    gap_report = cast(dict[str, Any], summary["runtime_gap_report"])
    assert summary["total_items"] == 129
    assert runtime_target_counts["implemented_runtime"] == 10
    assert grammar_role_counts["review_explanation"] >= 26
    assert architecture_role_counts["evidence_component"] == 26
    assert contract_status_counts[RuntimeContractStatus.IMPLEMENTED_BINDING_CONTRACT.value] == 10
    assert gap_report["roles"]["options_flow_context"]["concept_contract"] >= 1
    assert summary["report_inputs"] == EXPECTED_REPORT_INPUTS


def test_mapping_rows_expose_contract_status_priority_and_affinity_fields() -> None:
    """Mapping rows should expose Gate-B contract and affinity fields."""
    service = CanonicalImportRegistryService(Path.cwd())
    mapping = service.load_mapping()
    macro_shock = next(item for item in mapping if item.canonical_slug == "macro_shock_responder")
    options_fragment = next(
        item for item in mapping if item.canonical_slug == "options_flow_context_first_class"
    )
    ladder_constructor = next(
        item for item in mapping if item.canonical_slug == "ladder_constructor"
    )

    assert macro_shock.runtime_contract_status == RuntimeContractStatus.IMPLEMENTED_BINDING_CONTRACT
    assert macro_shock.desk_role_priority == 40
    assert macro_shock.inventory_affinity is True
    assert (
        options_fragment.runtime_contract_status == RuntimeContractStatus.EVIDENCE_ONLY_NO_CONTRACT
    )
    assert options_fragment.options_affinity is True
    assert ladder_constructor.runtime_contract_status == RuntimeContractStatus.CONCEPT_CONTRACT_ONLY
    assert ladder_constructor.playbook_affinity == ["continuation_ladder"]


def test_runtime_depth_report_exposes_category_and_role_breakdown() -> None:
    """The runtime-depth report should show category, role, and runtime-target splits."""
    service = CanonicalImportRegistryService(Path.cwd())
    report = cast(dict[str, Any], service.runtime_depth_report())
    role_rows = cast(dict[str, dict[str, int]], report["by_grammar_role"])
    category_rows = cast(dict[str, dict[str, int]], report["by_category"])
    assert report["total_items"] == 129
    assert report["by_item_class"]["module"]["implemented_runtime"] == 10
    assert report["by_runtime_target"] == {
        "concept_contract": 93,
        "evidence_only": 26,
        "implemented_runtime": 10,
    }
    assert role_rows["temporal_context"]["priority"] == 10
    assert role_rows["options_flow_context"]["evidence_only"] == 5
    assert category_rows["market_state_requirement"]["evidence_only"] >= 1
    assert report["report_inputs"] == EXPECTED_REPORT_INPUTS


def test_gate_b_reports_exist_and_exclude_evidence_only_from_executable_backlog() -> None:
    """Gate-B reports should exist, remain parseable, and expose the expected splits."""
    service = CanonicalImportRegistryService(Path.cwd())
    depth_report = cast(dict[str, Any], service.runtime_depth_report())
    backlog_report = cast(dict[str, Any], service.executable_backlog_view())
    provenance_report = cast(dict[str, Any], service.provenance_depth_audit())
    role_report = cast(dict[str, Any], service.import_depth_target_report())

    assert depth_report["by_item_class"]["module"]["implemented_runtime"] == 10
    assert backlog_report["executable_backlog_count"] == 103
    assert backlog_report["excluded_evidence_only_count"] == 26
    assert backlog_report["by_readiness"]["implemented_runtime"] == 10
    assert backlog_report["items"][0]["desk_role_priority"] == 10
    assert (
        provenance_report["preservation_only_count"]
        + provenance_report["implemented_or_translated_count"]
        == 129
    )
    assert provenance_report["structured_source_count"] == 71
    assert role_report["roles"][0]["grammar_role"] == "temporal_context"
    assert role_report["roles"][0]["desk_role_priority"] == 10
    assert role_report["summary"]["implemented_runtime_count"] == 10

    for filename in [
        "2026-03-23_CANONICAL_RUNTIME_DEPTH_REPORT.json",
        "2026-03-23_EXECUTABLE_IMPORT_BACKLOG.json",
        "2026-03-23_PROVENANCE_DEPTH_AUDIT.json",
        "2026-03-23_IMPORT_DEPTH_BY_DESK_ROLE.json",
        "canonical_import_registry_summary.json",
        "canonical_grammar_mapping_summary.json",
        "2026-03-23_GATE_B_SOURCE_REGISTRY.jsonl",
        "2026-03-23_GATE_B_SOURCE_GRAMMAR_MAPPING.json",
    ]:
        assert (Path.cwd() / "docs/planning" / filename).exists()


TRANCHE_A_ITEM_ORDER = [
    "archive-module-006",
    "archive-module-009",
    "archive-module-018",
    "archive-module-014",
    "archive-module-011",
    "archive-module-010",
    "archive-module-016",
    "archive-evaluator-eval02",
    "archive-module-051",
    "archive-module-043",
    "archive-module-023",
    "archive-module-024",
    "archive-module-020",
]


def _load_tranche_a_manifest() -> dict[str, Any]:
    manifest_path = (
        Path.cwd() / "docs" / "planning" / "2026-03-24_CONTRACT_IMPORT_TRANCHE_A_MANIFEST.json"
    )
    return cast(dict[str, Any], json.loads(manifest_path.read_text(encoding="utf-8")))


def test_tranche_a_manifest_exists_and_remains_frozen_to_thirteen_items() -> None:
    """Gate 14 should freeze exactly the thirteen tranche-A contract-import items."""
    manifest = _load_tranche_a_manifest()
    assert manifest["manifest_id"] == "contract_import_tranche_a_v1"
    assert manifest["scope_boundary"]["grammar_order"] == [
        "temporal_context",
        "market_regime_context",
        "options_flow_context",
        "posture_risk_permission",
        "playbook_eligibility",
    ]
    items = cast(list[dict[str, Any]], manifest["items"])
    assert len(items) == 13
    assert [item["canonical_id"] for item in items] == TRANCHE_A_ITEM_ORDER
    assert {item["planned_leaf_outcome"] for item in items[:7]} == {"contract_surface_only"}
    assert {item["planned_leaf_outcome"] for item in items[7:]} == {"runtime_integrated_advisory"}
    assert manifest["outcome_bands"]["approved_live_runtime"] == "Forbidden inside tranche A."


def test_tranche_a_manifest_rows_match_backlog_readiness_blockers_and_role_order() -> None:
    """Gate 14 manifest rows should stay aligned to the executable backlog and grammar mapping."""
    service = CanonicalImportRegistryService(Path.cwd())
    registry = {item.canonical_id: item for item in service.load_registry()}
    mapping = {item.canonical_id: item for item in service.load_mapping()}
    manifest = _load_tranche_a_manifest()
    items = cast(list[dict[str, Any]], manifest["items"])

    last_priority = -1
    for row in items:
        canonical_id = cast(str, row["canonical_id"])
        registry_item = registry[canonical_id]
        mapping_item = mapping[canonical_id]
        assert (
            registry_item.implementation_readiness
            == ImplementationReadiness.READY_FOR_CONTRACT_IMPORT
        )
        assert row["primary_grammar_role"] == mapping_item.grammar_role.value
        assert row["runtime_contract_status"] == RuntimeContractStatus.CONCEPT_CONTRACT_ONLY.value
        assert row["readiness_blockers"] == registry_item.readiness_blockers
        assert row["dependencies"] == registry_item.known_dependencies
        assert row["known_inputs"] == registry_item.known_inputs
        assert row["known_outputs"] == registry_item.known_outputs
        assert int(row["desk_role_priority"]) >= last_priority
        last_priority = int(row["desk_role_priority"])

    assert (
        "No fifth playbook or named-playbook expansion inside tranche A."
        in manifest["scope_boundary"]["stop_rules"]
    )
