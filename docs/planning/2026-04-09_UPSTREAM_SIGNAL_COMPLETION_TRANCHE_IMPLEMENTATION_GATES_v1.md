# 2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_GATES_v1

Status: closed implementation pack retained as evidence. Closed through Gate 252 in the uploaded workspace copy. No active pack currently routed.

## Purpose

Plan the bounded upstream signal completion tranche that promotes already-lawful upstream regime and participation truth into the live runtime path without reopening the corrected main serial stack, without feeding the observational history lane back into the stack, and without changing Step 4-6 authority or DMP / DMP V2 stage order.

## Scope

In scope:
- one authoritative raw signal coverage map with Class A versus Class B classification;
- bounded promotion planning for cross-asset regime primitives into prepared runtime truth;
- bounded promotion planning for same-bucket participation / liquidity baseline truth;
- lawful raw-to-cognition wiring into `TemporalContextInput`, `MarketRegimeContextInput`, and participation-supporting ingress surfaces;
- bounded optional top-of-book promotion only if already cheaply available in the admitted capture substrate;
- bounded non-interference proof and sanity traces for the corrected Steps 3-6 path.

Out of scope:
- redesign of **Posture and Risk Permission**, **Playbook Eligibility**, **Execution Expression**, recommendation boundary, or **Capital Deployment Authority Service**;
- DMP / DMP V2 stage-order redesign;
- broad vendor-acquisition work for breadth, concentration, or dealer-flow raw drivers;
- history-lane analysis or replay redesign;
- optimisation, tuning, allocator redesign, or exit-strategy work.

## Supersession and active authority

- This document is the closed implementation pack retained as evidence for the upstream signal completion tranche in the uploaded workspace copy.
- Repo-root `PLANS.md`, the canonical gate map, the leaves ledger, and the execution log now record the pack as closed through Gate 252 with no active pack routed.
- The latest closed pack retained as evidence remains:
  - `docs/planning/2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_GATES_v1.md`
  - `docs/planning/2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_LEAVES_v1.json`
  - `docs/planning/2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_EXECUTION_LOG_v1.md`
- The latest closed pack is evidence input only. It is not the structural template for this tranche.
- Gates 247-252 are complete in the uploaded workspace copy. No active pack is currently routed.

## Governing inputs

Frozen doctrine and process:
- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `docs/08_TESTING_AND_PROMOTION.md`
- `AGENTS.md`
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`

Vocabulary and naming authority:
- `docs/vocabulary/README.md`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`

Environment and runtime authority:
- `pyproject.toml`
- `src/nvda_desk/config.py`
- `src/nvda_desk/db/session.py`

Live runtime and contract surfaces that this tranche must trace before implementation:
- `src/nvda_desk/schemas/dataset.py`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/services/chain_to_cognition.py`
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/market_regime_context.py`
- `src/nvda_desk/services/options_flow_context.py`
- `src/nvda_desk/services/temporal_context.py`
- `src/nvda_desk/services/replay_compare.py`
- `src/nvda_desk/testing/canonical_runtime_harness.py`
- `src/nvda_desk/testing/cognition_fixtures.py`

Prior doctrine and evidence inputs that this tranche must reuse rather than reinvent:
- `docs/planning/2026-03-25_GATE42_VOLUME_BASELINE_AND_OPTIONS_RAW_CAPTURE.md`
- `docs/planning/2026-03-30_PHASE0_SIGNAL_WORKBOOK_AUDIT.md`
- `docs/planning/2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_CONTRADICTION_REPORT_v1.md`

External behavioural inputs for this draft:
- `/mnt/data/upstream_signal_completion_tranche_architecture_brief_2026-04-09.md`
- `/mnt/data/upstream_signal_completion_tranche_gate_leaf_execution_brief_2026-04-09.md`
- `/mnt/data/checkpoint_integrity_normative_extension.md`

Template-pack inputs that remain mandatory for new-pack grammar:
- `docs/planning/tranche_briefing_template_pack/README.md`
- `docs/planning/tranche_briefing_template_pack/HOW_TO_USE_THESE_DOCUMENTS.md`

## Workflow placement

This tranche is upstream information authority and ingress promotion.

It sits:
- upstream of `ChainToCognitionService` and the seven-stage desk-cognition grammar;
- between raw/prepared-runtime truth and the cognition inputs that already expect regime and participation state;
- downstream of the current admitted raw/prepared-runtime path and any reused capture substrate the repo can lawfully promote;
- outside Step 4-6 decision authority, outside the observational history lane, and outside DMP / DMP V2 stage order.

Later consumers must be:
- `TemporalContextService` for lawful participation-aware temporal interpretation;
- `MarketRegimeContextService` for live regime classification;
- `OptionsFlowContextService` only for participation-supporting fields that already belong there.

What must not consume raw outputs directly:
- Step 4 **Posture and Risk Permission**;
- Step 5 **Playbook Eligibility**;
- Step 6 **Execution Expression**;
- **Capital Deployment Authority Service**;
- the observational history lane.

The six-gate sequence preserves granularity because each gate owns one distinct proof boundary:
1. coverage and scope freeze;
2. prepared-runtime contract freeze;
3. cross-asset promotion path;
4. same-bucket participation baseline promotion;
5. raw-to-cognition wiring;
6. non-interference and bounded sanity traces.

## Intent and workflow anchor

The repo remains a deterministic desk-runtime system with fixed stage order, bounded downstream fresh-capital authority, and explicit no-drift process law.
This tranche improves upstream market truth that the existing cognition grammar can already use.
It does not create a new business stage.
It does not create a hidden inference lane.
It does not authorise downstream redesign just because richer inputs become available.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- `MarketRegimeContextInput` as the canonical Step-2 ingress contract target
- `TemporalContextInput` as the canonical Step-1 ingress contract target
- `OptionsFlowContextInput` as the canonical Step-3 ingress contract target
- `PreparedRuntimeSnapshot` and `PreparedRuntimeLineage` as the baseline prepared-runtime contract surfaces
- `ChainToCognitionService` as the canonical prepared-runtime to cognition ingress boundary
- `pyproject.toml` and `Settings.database_url` defaults as environment authority
- current DMP / DMP V2 stage order as unchanged

### Retire from authority (compatibility-only unless later removed)
- `relative_volume_ratio` as a stand-alone participation proxy if same-bucket baseline truth is promoted; later gates must either demote it to explicit compatibility scaffolding or recompute it from the lawful baseline rather than letting it masquerade as full participation truth

### Mandatory amendments
- `docs/03_DOMAIN_MODEL.md` because promoted cross-asset and same-bucket baseline fields need lawful packet authority if execution proceeds
- `docs/04_TECHNICAL_ARCHITECTURE.md` because upstream ingress-promotion surfaces and their boundaries become live architecture if execution proceeds
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` because runtime-reader and prohibited-inference rules must record the new ingress truth if execution proceeds
- `src/nvda_desk/schemas/dataset.py` because `PreparedRuntimeSnapshot` is currently thinner than the regime and participation doctrine requires
- `src/nvda_desk/schemas/cognition.py` because the cognition ingress path already expects `MarketRegimeContextInput` richness that the live raw-to-cognition path does not yet populate
- `src/nvda_desk/services/chain_to_cognition.py` because it currently converts prepared snapshots into temporal and options-flow inputs only
- `src/nvda_desk/services/replay_compare.py` because replay/runtime comparison surfaces must remain truthful if regime ingress becomes live
- tests that prove Steps 3-6 remain untouched while upstream truth gets richer

### New additions
- one authoritative raw signal coverage-map artefact
- one bounded prepared-runtime contract extension for cross-asset regime and same-bucket participation/baseline truth
- one bounded promotion path for cross-asset regime data
- one bounded promotion path for same-bucket participation/liquidity baseline truth
- one bounded raw-to-cognition wiring proof slice for `MarketRegimeContextInput`
- tranche-local support docs: checklist, contradiction report, scope note, execution log

## Vocabulary discipline

- Existing vocabulary authority must be read before writing any new durable planning term, file name, class name, field name, or gate title.
- The behavioural briefs propose four tranche labels that are not yet confirmed canonical:
  - **Upstream Signal Completion Tranche**
  - **Cross-Asset Regime Promotion**
  - **Same-Bucket Participation Baseline**
  - **Raw Signal Coverage Map**
- Gate 247 must classify each of those through the Vocabulary Workflow as exactly one of:
  - `enrich_existing`
  - `add_new`
  - `alias_only`
  - `quarantine`
- Until that leaf closes, repo-governing docs must not pretend the labels are already canonical beyond bounded draft-planning use.
- If vocabulary admission is not lawful in Gate 247, the pack must freeze exact temporary code-symbol usage explicitly and keep the prose labels evidence-only.

## Checkpoint integrity and docstring compliance discipline

- The additive checkpoint extension at `/mnt/data/checkpoint_integrity_normative_extension.md` applies to every gate in this tranche.
- Any modified runtime boundary must expose at least one named checkpoint with deterministic exceptions, bounded observable state, and tranche-local negative proof.
- Any modified boundary module, class, or function must carry structured docstrings with Purpose, Inputs, Outputs, Side Effects, Failure Modes, and Checkpoints sections.
- Planning-only Gate 247 still requires explicit negative proof in its gate-local tests so scope drift and unlawful vocabulary admissions turn red.
- Existing repo tests outside the modified upstream tranche surfaces are not retroactively rewritten unless this tranche materially touches them.

## Packet / contract discipline

- `docs/03_DOMAIN_MODEL.md` remains the baseline packet/data contract authority for this tranche.
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` remains the baseline runtime-reader and prohibited-inference authority for this tranche.
- `PreparedRuntimeSnapshot` is currently rich for NVDA bar/option/event truth but does not yet carry the cross-asset regime primitives or same-bucket baseline packet that the new tranche requires.
- `RealDataCognitionInputs` and `ChainToCognitionService` currently carry `temporal_input`, `options_flow_input`, and `normalised_features`, but they do not carry a live-built `regime_input` surface.
- Gate 248 and Gate 251 must therefore prove one lawful promotion path from prepared runtime truth into `MarketRegimeContextInput` without creating a second hidden ingress path or mutating Steps 3-6 contracts.
- Gate 250 must decide whether `relative_volume_ratio` becomes a derived compatibility echo from same-bucket baseline truth or remains an explicitly bounded legacy scaffold. It must not remain ambiguous.
- Optional top-of-book fields must be promoted only if the current admitted capture substrate already exposes them cheaply and deterministically. Otherwise they remain explicit deferred scope.

## Contradiction scan and state-integrity rules

- The router quartet is clean before this draft begins: repo-root `PLANS.md` records no active pack and names the latest closed options-flow history pack as retained evidence.
- The material design tensions are runtime and contract tensions, not router tensions:
  - `MarketRegimeContextInput` already expects `nq_return_pct`, `es_return_pct`, `sox_return_pct`, `vix_level`, `vvix_level`, `us10y`, `us2y`, and `usdjpy`, but the live prepared-runtime and `ChainToCognitionService` path do not yet populate a regime-input packet from real promoted truth.
  - `PreparedRuntimeSnapshot.relative_volume_ratio` exists, but Gate 42 doctrine already says truthful same-bucket `volume`, `spread`, and `trade-count` baselines are required and loader wiring remained future work there.
  - `PreparedNormalisedFeatureSet` preserves bounded regime-aware fields, but it is not a substitute for a lawful live `MarketRegimeContextInput` packet.
  - Optional top-of-book truth may be attractive but is not currently proven as cheap/admitted in the live repo surfaces.
- Gate 247 must freeze Class A versus Class B explicitly so later gates do not hand-wave unavailable breadth/concentration/dealer-flow families into runtime truth.

Closeout invariants for the eventual active pack:
- `completed_leaf_ids` and `remaining_leaf_ids` are disjoint;
- every referenced leaf id exists in the leaves ledger;
- `active_gate = none` is lawful only when `remaining_leaf_ids` and `pending_gate_ids` are empty;
- later-proof tests must permit later valid states or be retired/replaced during closeout.

## Document-touch checklist

This tranche uses `docs/planning/2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_DOCUMENT_TOUCH_CHECKLIST_v1.md`.
If execution proceeds, it must track frozen doctrine, live router surfaces, vocabulary handling, the coverage-map artefact, prepared-runtime/cognition ingress surfaces, and the final non-interference proof slice.

## Testing and promotion discipline

- Repo-local environment required: `.venv` via `make install` / `uv sync --extra dev`, honouring `pyproject.toml`
- Minimum validation slice for the draft pack:
  - `python3 -m json.tool docs/planning/2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_LEAVES_v1.json`
  - `python3 -m pytest -q tests/test_planning_state_integrity.py`
- Planned execution-phase minimum validation slice:
  - `python3 -m pytest -q tests/test_gate247_upstream_signal_coverage_map_and_scope_lock.py`
  - `python3 -m pytest -q tests/test_gate248_upstream_prepared_runtime_contracts.py`
  - `python3 -m pytest -q tests/test_gate249_cross_asset_regime_ingestion.py`
  - `python3 -m pytest -q tests/test_gate250_same_bucket_participation_baseline.py`
  - `python3 -m pytest -q tests/test_gate251_upstream_raw_to_cognition_wiring.py`
  - `python3 -m pytest -q tests/test_gate252_upstream_non_interference_and_sanity_traces.py`
- A gate is not complete until:
  - tests ran green;
  - `PLANS.md`, the canonical gate map, the active leaves ledger, and the active execution log all moved together;
  - exact GitHub branch/commit receipts were recorded for the gate closeout when Git metadata is available;
  - a full-history zip is created only if the operator explicitly requests backup, offline handoff, or sandbox transfer packaging.

## Gates

### Gate 247: Raw signal coverage freeze and vocabulary/scope lock

**Objective**
- Freeze one authoritative coverage map, Class A versus Class B boundaries, and the in-scope versus deferred family list before any runtime promotion work begins.

**In-scope surfaces**
- `docs/planning/2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_GATES_v1.md`
- `docs/planning/2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_LEAVES_v1.json`
- `docs/planning/2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_RAW_SIGNAL_COVERAGE_MAP_v1.md`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
- targeted Gate 247 planning tests

**Definition of done**
- one authoritative raw signal coverage map exists and classifies every named family as already wired, captured but weak, schema-expected but unwired, or not raw-captured yet;
- Class A versus Class B status is explicit for each named family;
- vocabulary handling and deferred scope are frozen so later gates cannot back-door breadth, concentration, or dealer-flow into tranche one;
- Gate 247 tests include explicit red-turning negative proof for coverage-map and vocabulary-lock drift.

### Gate 248: Prepared-runtime contract and promotion boundary freeze

**Objective**
- Extend the prepared-runtime contract so promotable regime and participation truth have lawful places to live without creating speculative placeholders for deferred Class A families.

**In-scope surfaces**
- `src/nvda_desk/schemas/dataset.py`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`
- targeted Gate 248 schema/model tests

**Definition of done**
- `PreparedRuntimeSnapshot` or supporting typed structures have lawful fields for promoted cross-asset regime truth and same-bucket participation/baseline truth;
- optional top-of-book truth is either explicitly bounded and admitted or explicitly deferred;
- breadth, concentration, and dealer-flow raw drivers remain deferred rather than silently omitted or fake-populated;
- modified boundary contracts and docstrings expose checkpoint observation carriage explicitly.

### Gate 249: Cross-asset regime ingestion path

**Objective**
- Promote cross-asset regime truth into the live prepared-runtime path with deterministic alignment and truthful fallback behaviour.

**In-scope surfaces**
- prepared-runtime builder surfaces identified in execution
- `src/nvda_desk/schemas/dataset.py`
- `src/nvda_desk/services/replay_compare.py`
- targeted Gate 249 ingestion tests

**Definition of done**
- promoted regime primitives for ES, NQ, SOX, VIX, VVIX, US10Y, US2Y, and USDJPY can enter the live prepared-runtime path lawfully;
- timestamp and symbol/source identity alignment are deterministic and inspectable;
- explicit fallback behaviour exists when some non-critical upstream feeds are absent;
- live regime ingress raises a deterministic checkpoint failure if a packet claims complete live-ingress truth without breadth and concentration state.

### Gate 250: Same-bucket participation / liquidity baseline promotion

**Objective**
- Promote truthful same-bucket participation/liquidity baseline state and resolve the `relative_volume_ratio` compatibility question without pretending a recent-bar proxy is a full baseline.

**In-scope surfaces**
- prepared-runtime builder surfaces identified in execution
- `src/nvda_desk/schemas/dataset.py`
- `docs/03_DOMAIN_MODEL.md`
- targeted Gate 250 baseline tests

**Definition of done**
- same-bucket `volume`, `spread`, and `trade-count` baseline truth is promoted where lawfully available;
- lunch/open/close-style bucket differentiation is representable in the live runtime path;
- deterministic fallback exists when baseline history is absent and any retained `relative_volume_ratio` path is explicitly compatibility-only or baseline-derived;
- participation-baseline reconstruction raises deterministic checkpoint failures for non-positive ratio or false baseline-availability states.

### Gate 251: Raw-to-cognition wiring for regime and participation-aware context

**Objective**
- Feed the richer upstream truth into the cognition grammar that already expects it without redesigning downstream logic.

**In-scope surfaces**
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/services/chain_to_cognition.py`
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/temporal_context.py`
- `src/nvda_desk/services/options_flow_context.py`
- targeted Gate 251 wiring tests

**Definition of done**
- `MarketRegimeContextInput` is populated from live promoted truth rather than out-of-band fixture-only values;
- participation/liquidity truth enters lawful Step 1 / Step 2 / Step 3-supporting ingress surfaces only;
- Steps 4-6 code paths are still contract-compatible and not redesigned;
- chain-to-cognition outputs carry observable checkpoint traces proving regime and participation wiring plus red-turning negative proof for misrouted packets.

### Gate 252: Non-interference proof and bounded sanity traces

**Objective**
- Prove that richer upstream truth leaves the corrected serial stack intact and yields bounded new interpretive capacity without drifting into optimisation work.

**In-scope surfaces**
- `src/nvda_desk/testing/canonical_runtime_harness.py`
- `src/nvda_desk/testing/bounded_trace_review.py`
- targeted corrected-stack regression tests and tranche-local sanity traces
- router quartet closeout surfaces if execution reaches completion

**Definition of done**
- bounded corrected-stack acceptance slices still pass with the upstream promotions present;
- one bounded cross-asset trace and one bounded participation-baseline trace prove the richer truth is visible without changing downstream authority;
- still-missing Class A families are logged explicitly and the tranche closes truthfully;
- the final closeout note records checkpoint-extension adoption, final proof counts, and retained deferred families.
