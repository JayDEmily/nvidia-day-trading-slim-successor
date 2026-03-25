# NVIDIA Day Trading — Build Plan v1
**Date:** 2026-03-18  
**Status:** Gated implementation plan

## Objective

Turn the now-frozen operating model into a buildable project scaffold without inventing final risk numbers too early.

## Gate 0 — freeze documents
**Pass condition**
- master operating-model document exists;
- technical architecture document exists;
- `pyproject.toml` exists for Python 3.13;
- repo skeleton exists.

**Failure condition**
- architecture or responsibility boundaries remain ambiguous.

## Gate 1 — scaffold the repo
**Work**
- create Python package tree;
- create config module layout;
- create docs folder;
- create tests folder;
- create migrations folder.

**Pass condition**
- tree exists and imports resolve.

## Gate 2 — freeze contracts
**Work**
- module schema;
- risk-policy schema;
- evaluation schema;
- broker adapter interface;
- market-state retrieval contracts.

**Pass condition**
- schemas compile and can be serialised.

## Gate 3 — data backbone
**Work**
- PostgreSQL schema for raw_vendor, canonical_market, derived_features, research_artefacts, execution_records;
- Alembic migration base;
- one-minute bar canonical tables;
- option contract and bounded option snapshot tables.

**Pass condition**
- local migrations run cleanly;
- tables can be created and queried.

## Gate 4 — service core
**Work**
- market-state retrieval services;
- research artefact persistence services;
- module registry services;
- risk gateway service;
- replay/evaluation service stubs.

**Pass condition**
- service interfaces stable and testable without UI.

## Gate 5 — API-first research surface
**Work**
- FastAPI routes for narrow read/write tools;
- Responses API orchestration layer;
- basic chat/research UI integration path.

**Pass condition**
- research questions can retrieve compact state and persist artefacts.

## Gate 6 — deterministic runtime skeleton
**Work**
- module loader;
- signal/veto/sizing/execution pipeline;
- pre-trade risk gateway;
- broker adapter stub;
- execution/event ledger writes.

**Pass condition**
- runtime can simulate a no-live broker cycle end to end.

## Gate 7 — evaluation/replay
**Work**
- historical replay harness;
- evaluation metrics calculation;
- promotion decision recording.

**Pass condition**
- a module can move from spec -> code -> replay result -> decision record.

## Gate 8 — MCP later
**Work**
- add MCP server wrapping the same domain services;
- expose only narrow tool contracts;
- keep UI payload split between structuredContent and _meta.

**Pass condition**
- no duplicated business logic between FastAPI and MCP layers.

## Stopping rule

Do not add:
- full news ingestion,
- multi-broker support,
- wide symbol universes,
- excessive UI work,
- live-trading autonomy,

until Gates 0–7 are genuinely complete.

## Immediate deliverables from this pass

Done in this pass:
- canonical master document;
- canonical technical architecture document;
- Python 3.13 `pyproject.toml`;
- repo scaffold.
