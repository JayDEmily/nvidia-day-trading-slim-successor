# 2026-04-05_TARGET_REPO_SNAPSHOT_HANDOFF_BRIEF_AND_INPUT_BUNDLE_CONTRACT_v1

Status: Gate 203 planning authority; target-snapshot handoff brief and input-bundle contract for later execution.

## Purpose

Freeze the exact identity block and handoff bundle that a later snapshot-and-collection thread must receive before it touches real-anchor evidence, prepared-runtime derivations, or market-persisted reference state.

## Evidence anchors read for this plan

- `docs/planning/2026-03-30_GATE101_CANONICAL_RAW_BUNDLE_ADMISSION.md`
- `fixtures/real_data/gate_101_canonical_raw_runtime_bundle.json`
- `fixtures/real_data/gate_e_prepared_runtime_fixture_pack.json`
- `src/nvda_desk/services/real_data_loader.py`
- `src/nvda_desk/db/models.py`
- `src/nvda_desk/services/slv_market.py`

## Snapshot identity block

Every later target snapshot handoff must carry these exact identity fields:

- `repo_commit_sha`
- `execution_branch_name`
- `active_pack_gates_path`
- `active_pack_leaves_path`
- `active_pack_execution_log_path`
- `raw_anchor_bundle_path`
- `prepared_runtime_fixture_pack_path`
- `snapshot_generation_service`
- `snapshot_generation_call`
- `market_persisted_reference_surface`
- `storage_owner_surface`

The canonical `snapshot_generation_call` for this pack is `RealDataLoaderService.prepare_runtime_dataset(...)`.

## Input-bundle contract

The later execution bundle must name, at minimum:

- the admitted raw bundle used as the upstream anchor;
- the prepared-runtime derivative pack used as the current deterministic preparation reference;
- the exact repo commit and branch receiving the later execution work;
- the runtime preparation service and provenance-preserving loader path;
- any candidate persisted market surfaces to inspect, including `option_snapshot`;
- the intended downstream consumer boundary for the collected evidence.

## Required handoff brief sections

The later handoff brief must answer:

1. which raw anchor is being used and why it is the right baseline;
2. which prepared derivative or persisted market reference surfaces are in scope;
3. which exact proof slice must run before any new anchor is called admitted;
4. which storage or loader surfaces will be touched if new evidence lands;
5. which current gaps the candidate snapshot is meant to close.

## Repo-native binding points

- `RealDataLoaderService.prepare_runtime_dataset(...)` is the current deterministic raw-to-prepared preparation seam.
- `OptionSnapshot` is the current market-persisted reference table named by the active pack.
- `StrategicLadderMarketService.get_option_surface(...)` is the current consumer path reading `option_snapshot`.

## What later work must not do

- hand off an unnamed repo state or unnamed evidence baseline;
- treat a prepared derivative as if it were a new raw anchor;
- omit `option_snapshot` when a collection proposal would touch persisted market reference state;
- rely on chat memory instead of an explicit identity block and handoff brief.
