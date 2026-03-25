# 2026-03-19 Master Value Migration Plan

## Purpose
Create one controlled migration path that moves validated value from the legacy archives into the NVIDIA day-trading project without importing conversational sludge, unverifiable implementation claims, or raw screenshot noise as production truth.

This plan is the working document for the next migration phase.

## Why this plan exists
The project now has two real asset classes:

1. **A doctrine / backlog / extraction surface** already captured in this repo.
2. **A richer executable implementation surface** created in the later `impl_pass*.zip` bundles.

The risk is not lack of ideas. The risk is uncontrolled merging of:
- old conversational claims,
- screenshot-derived numbers,
- half-specified module names,
- and architecture fragments from different eras.

This plan freezes the order of operations so that value is migrated deliberately.

## OpenAI-aligned implementation doctrine
This migration should follow the same API/doctrine choices already adopted for the project:
- Responses API as the primary LLM surface.
- Structured outputs / typed schemas for machine-readable artefacts.
- Narrow tool contracts instead of broad free-form model access.
- Retrieval of compact state slices rather than giant raw payloads.
- MCP only after the API-first path is solid.

Note: I did **not** find official OpenAI documentation for a special standalone “plans input” primitive to rely on here. The relevant official guidance is the standard combination of GPT-5.4 + Responses API + structured outputs + function calling / tool schemas.

## Migration objective
At the end of this migration programme, the project should have:
- one canonical doctrine/backlog/docs tree,
- one canonical executable repo tree,
- one merged machine-readable backlog of validated module and feature candidates,
- one admitted legacy fixture pack for testing,
- and a clear promotion queue from legacy evidence -> feature/module contract -> implementation.

## Source sets to migrate from
### Source set A — current doctrine repo
This repo already contains:
- first-class docs and guardrails,
- T1 desk extraction outputs,
- remaining-documents extraction outputs,
- initial legacy backlogs,
- top-3 promotion plans.

### Source set B — implementation snapshots
Primary executable source:
- `nvidia_day_trading_v1_20260318_impl_pass5.zip`

This contains the richer code-bearing implementation path that is not currently unpacked into this repo directory.

### Source set C — structured archive salvage
Primary structured salvage source:
- `nvda_master_archive_structured_plus_sources.zip`

Highest-value files already identified from that archive:
- `part1_master_architecture_and_trees.md`
- `part4_clean_build_plan_and_completion_order.md`
- `part5_module_registry_draft.yaml`
- `runtime_settings_starter.yaml`
- `evaluation_config_starter.yaml`
- `coefficients_registry_starter.yaml`
- `strategy_variants_starter.yaml`

### Source set D — raw legacy corpora
Already triaged and partially extracted:
- `My tier 1 desk Lol not GS (1).pdf`
- `Comprehensive Deep-Dive_ What's Really Happening Today in NVDA_ (1).pdf`
- `of trading days below VWAP.pdf`
- `Options Data CSV Output.pdf`
- `NVDA GPT Framework Review.pdf`

## Non-negotiable migration rules
1. No raw legacy item becomes production truth without provenance.
2. No legacy implementation claim is treated as real code unless the code exists.
3. No module name enters runtime simply because it sounds good.
4. No fixture data is treated as canonical market history.
5. No code merge happens before doctrine/backlog reconciliation.
6. The current repo remains the doctrine source of truth until the executable merge is complete.

## Canonical target shape
The target should end up as a **single repo** with four coordinated surfaces:

### 1. Doctrine surface
Human-readable project truth:
- README
- NORMATIVE / GUARDRAILS / RUNBOOK / TESTING docs
- project architecture / operating model docs
- legacy extraction and promotion docs

### 2. Machine-readable planning surface
Strict artefacts:
- merged module backlog JSONL
- merged feature backlog JSONL
- admitted data fixture manifest JSONL
- changelog JSONL
- schemas for validation

### 3. Executable surface
Code and tests:
- API
- DB models / migrations
- services
- replay/eval
- module contracts
- Makefile entrypoints

### 4. Legacy archive surface
Preserved but quarantined source evidence:
- page maps
- value capture docs
- archive manifests
- source PDF provenance notes

## Ordered migration phases

## Phase 0 — freeze the canonical target
### Goal
Decide which repo tree becomes the base target.

### Action
Use the current doctrine repo as the canonical working tree, then import the executable surface from `impl_pass5.zip` into a controlled merge workspace.

### Output
- `docs/planning/CANONICAL_TARGET_DECISION.md`
- one unpacked merge workspace for executable code

### Pass condition
There is one declared target tree, not multiple competing zips.

## Phase 1 — merge executable surface into the doctrine repo
### Goal
Recover the richest code-bearing implementation into the current repo without overwriting doctrine.

### Action
Unpack `impl_pass5.zip` into a merge workspace and compare:
- code paths,
- Makefile,
- pyproject,
- docs/status,
- changelog,
- schemas.

### Required output
- file-level diff summary
- conflict log
- controlled merge plan

### Pass condition
The current repo can represent both doctrine and executable code in one tree.

## Phase 2 — merge and de-duplicate backlog items
### Goal
Create one authoritative module and feature backlog.

### Action
Combine:
- current `legacy_module_backlog.jsonl`
- current `legacy_feature_backlog.jsonl`
- remaining-doc additions
- top-3 promotion candidates
- structured archive module candidates from `part5_module_registry_draft.yaml`

### Rules
Each entry must carry:
- source set,
- provenance,
- status,
- duplicate-of if applicable,
- promotion readiness,
- required recompute/test tags.

### Output
- `backlog/module_backlog_merged.jsonl`
- `backlog/feature_backlog_merged.jsonl`
- `docs/planning/BACKLOG_MERGE_REPORT.md`

### Pass condition
No duplicate module/feature names survive without explicit resolution.

## Phase 3 — build the admitted legacy fixture pack
### Goal
Turn the real data-bearing remnants into safe test fixtures.

### Action
Start with:
- `Options Data CSV Output.pdf`
- admitted blocks from `of trading days below VWAP.pdf`

### Rules
Every fixture block must include:
- source document,
- page range,
- provenance,
- confidence,
- fields present,
- whether values are screenshot-derived, OCR-cleaned, or reconstructed.

### Output
- `fixtures/legacy/options_snapshots/`
- `fixtures/legacy/vwap_cases/`
- `fixtures/legacy/fixtures_manifest.jsonl`
- `docs/legacy/LEGACY_FIXTURE_PACK_SPEC.md`

### Pass condition
Fixtures are usable for tests while remaining clearly non-canonical.

## Phase 4 — salvage structured archive config value
### Goal
Harvest useful config/variant structure from the master archive without importing stale code.

### Action
Extract and normalise the useful fields from:
- `runtime_settings_starter.yaml`
- `evaluation_config_starter.yaml`
- `coefficients_registry_starter.yaml`
- `strategy_variants_starter.yaml`

### Output
- `docs/planning/CONFIG_AND_VARIANTS_CROSSWALK.md`
- candidate merged config schemas
- candidate coefficient registry shape

### Pass condition
Useful config structure is preserved without dragging in archive-specific clutter.

## Phase 5 — promote the next module/feature tranche
### Goal
Choose the next high-confidence implementation items after session clock.

### Current likely queue
1. Strategic Ladder Validator
2. Overnight Carry Evaluator
3. Asia / precursor context features
4. Composite signal scoring support
5. Macro filter / volatility veto expansions

### Action
For each candidate, decide:
- docs only,
- backlog only,
- contract-ready,
- implementation-ready.

### Output
- `docs/planning/NEXT_PROMOTION_TRANCHE.md`

### Pass condition
One implementation order exists.

## Phase 6 — implementation only after reconciliation
### Goal
Turn selected promoted items into code.

### Rule
No implementation begins until Phases 0–5 are complete.

### First implementation candidate
Legacy fixture pack + Strategic Ladder Validator using admitted fixture data and current replay/eval path.

## Working classification model
Every migrated item must keep these fields:
- `source_document`
- `source_set`
- `page_range`
- `item_type`
- `provenance`
- `confidence`
- `repo_layer`
- `recompute_required`
- `promotion_status`

## Repo-layer mapping
- `raw_vendor`
- `canonical_market`
- `derived_features`
- `research_artefacts`
- `execution_records`
- `docs_only`

## Stopping rules
Stop a migration pass when one of these is true:
- the next merge would create unresolved duplicate truth,
- provenance cannot be preserved cleanly,
- the code/doc split becomes ambiguous,
- or the candidate item is not strong enough to justify promotion.

## Immediate next step
The literal next step after this plan is:
1. unpack `nvidia_day_trading_v1_20260318_impl_pass5.zip` into a merge workspace,
2. diff it against `/mnt/data/nvidia_day_trading_v1_20260318`,
3. write the canonical target decision and file-level merge report.

That is the correct starting point because the repo currently holds the doctrine/extraction surface, while the richer implementation exists in a separate snapshot.

## Success criteria
This migration programme is successful when:
- the repo is no longer split across “docs-only tree” and “implementation zip snapshots”,
- the backlog is merged and de-duplicated,
- the legacy fixture pack exists with provenance,
- the next promotion tranche is explicit,
- and implementation resumes from one canonical tree instead of from archive hunting.
