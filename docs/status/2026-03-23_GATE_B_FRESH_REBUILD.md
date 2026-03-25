# 2026-03-23 Gate B Fresh Rebuild

## Outcome

Gate B was rebuilt fresh from frozen source baselines instead of trusting previously enriched registry output.

## What changed

- added frozen Gate-B source baselines:
  - `docs/planning/2026-03-23_GATE_B_SOURCE_REGISTRY.jsonl`
  - `docs/planning/2026-03-23_GATE_B_SOURCE_GRAMMAR_MAPPING.json`
- expanded `src/nvda_desk/schemas/import_registry.py` with seed models plus enriched Gate-B fields for readiness, blockers, contract status, and affinity
- rewrote `src/nvda_desk/services/import_registry.py` so refreshes rebuild enriched registry and grammar artefacts from the frozen seed baselines
- regenerated deterministic Gate-B outputs:
  - `docs/planning/canonical_import_registry.jsonl`
  - `docs/planning/canonical_grammar_mapping.json`
  - `docs/planning/canonical_import_registry_summary.json`
  - `docs/planning/canonical_grammar_mapping_summary.json`
  - `docs/planning/2026-03-23_CANONICAL_RUNTIME_DEPTH_REPORT.json`
  - `docs/planning/2026-03-23_EXECUTABLE_IMPORT_BACKLOG.json`
  - `docs/planning/2026-03-23_PROVENANCE_DEPTH_AUDIT.json`
  - `docs/planning/2026-03-23_IMPORT_DEPTH_BY_DESK_ROLE.json`
- strengthened `tests/test_import_registry_and_mapping.py` to prove the refresh path ignores stale enriched fields and rebuilds from the source baseline

## Validation

- `.venv/bin/python -m nvda_desk.services.import_registry`
- `.venv/bin/python -m pytest -q tests/test_import_registry_and_mapping.py`
- `make check`
