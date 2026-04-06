# 2026-04-05_TARGET_REPO_REAL_ANCHOR_COLLECTION_AND_ADMISSION_DOSSIER_RULES_v1

Status: Gate 203 planning authority; real-anchor collection and admission dossier rules for later execution.

## Purpose

Define the mandatory dossier fields, provenance checks, and repo-surface bindings that later real-anchor collection must satisfy before any new anchor can join the admitted evidence portfolio.

## Mandatory admission dossier fields

Every later real-anchor admission dossier must record:

- `candidate_anchor_id`
- `collection_window`
- `repo_commit_sha`
- `collector_branch_name`
- `source_system_or_document`
- `raw_anchor_output_path`
- `preparation_service`
- `prepared_derivative_output_paths`
- `lineage_statement`
- `storage_binding_surfaces`
- `named_downstream_consumers`
- `admission_reviewer`
- `admission_outcome`

## Authority and provenance checks

Before any later candidate anchor is called admitted, the dossier must prove:

- the candidate is tied to an exact raw source and collection window;
- the raw anchor is immutable once admitted;
- every prepared derivative names its upstream raw anchor and preparation call;
- any persisted market-state surfaces affected by the candidate are named explicitly;
- the collection thread did not bypass the active pack proof order.

## Storage and loader binding rules

Later real-anchor work must bind itself to the current repo-native surfaces:

- raw-to-prepared derivation is governed by `RealDataLoaderService.prepare_runtime_dataset(...)`;
- persisted option-market reference state is governed by `OptionSnapshot`;
- consumer reads of that persisted state are represented today by `StrategicLadderMarketService.get_option_surface(...)`.

If a candidate collection would change those bindings, the dossier must say so explicitly before admission.

## Explicit stop rules

Stop and replan if any of the following become true:

- the candidate cannot name one exact upstream raw source;
- a proposed collection would write persisted market state with no named loader or consumer boundary;
- a dossier would treat a prepared derivative as the admission object instead of the raw anchor;
- provenance would have to be reconstructed from memory rather than from named repo surfaces.

## What later work must not do

- admit a new real anchor without a dossier;
- omit the `option_snapshot` binding when persisted market state is implicated;
- treat collection output as canonical before review and admission;
- hide loader or storage implications in prose without naming the current repo-native surfaces.
