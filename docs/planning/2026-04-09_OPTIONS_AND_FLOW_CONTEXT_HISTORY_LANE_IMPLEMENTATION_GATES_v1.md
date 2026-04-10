# 2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_GATES_v1

Status: closed implementation pack retained as evidence. The Options and Flow Context History Lane implementation pack is closed through Gate 246 in the uploaded workspace copy; no active pack is currently routed.

## Purpose

Plan the bounded implementation tranche that adds an adjacent observational history lane at the **Options and Flow Context** boundary. The lane records one timestamped bounded front/next expiry raw-surface subset plus the derived `OptionsFlowContextOutput`, while leaving the seven-stage desk-cognition grammar, DMP/DMP V2 stage order, recommendation authority, and **Capital Deployment Authority Service** semantics unchanged.

## Scope

In scope:
- vocabulary handling for the new observational-lane labels;
- one bounded observation-record contract and one bounded persistence model;
- one runtime tap at the **Options and Flow Context** boundary;
- one bounded raw front/next expiry extraction path;
- one bounded persistence path and non-interference proof slice;
- one bounded replay/closeout slice for the tranche.

Out of scope:
- changes to Step 1-6 authority or stage order;
- new DMP or DMP V2 stage carriage for the lane;
- analysis, scoring, recommendation, allocator, or portfolio logic;
- broad all-expiry option archival;
- live news ingestion, shock classification, or historical alpha research.

## Supersession and active authority

- This document is the active pack authority for the observational-lane tranche.
- Repo-root `PLANS.md`, the canonical gate map, the leaves ledger, and the execution log now route this pack together.
- The latest closed pack retained as evidence remains:
  - `docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_GATES_v1.md`
  - `docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_LEAVES_v1.json`
  - `docs/planning/2026-04-09_MAIN_SERIAL_STACK_STEPS_3_TO_6_CORRECTIVE_IMPLEMENTATION_EXECUTION_LOG_v1.md`
- The latest closed pack is evidence input only. It is not the structural template for this tranche.
- Gates 242-246 are complete in the uploaded workspace copy. No active pack is currently routed.

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
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/options_flow_context.py`
- `src/nvda_desk/services/chain_to_cognition.py`
- `src/nvda_desk/services/market_state.py`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/schemas/dataset.py`
- `src/nvda_desk/schemas/options.py`
- `src/nvda_desk/schemas/dmp_v2.py`
- `src/nvda_desk/db/models.py`

External behavioural inputs for this draft:
- `/mnt/data/options_and_flow_context_history_lane_architecture_brief_2026-04-09.md`
- `/mnt/data/options_and_flow_context_history_lane_gate_leaf_execution_brief_2026-04-09.md`

## Workflow placement

This tranche is an adjacent observational-lane implementation tranche.

It sits:
- downstream of `OptionsFlowContextService.evaluate(...)` as the chosen capture trigger;
- beside, not inside, the seven-stage desk-cognition grammar;
- outside DMP / DMP V2 stage order for this tranche;
- outside recommendation and allocator memory.

It is therefore:
- upstream of later analysis or replay consumers that may read the observational records;
- downstream of the current raw-to-prepared-to-cognition path that already forms `OptionsFlowContextOutput`;
- prohibited from feeding outputs back into the same runtime pass.

The five-gate sequence preserves granularity because each gate owns one distinct proof boundary:
1. meaning and vocabulary freeze;
2. record/store contract freeze;
3. runtime tap and raw-slice-source freeze;
4. persistence and non-interference proof;
5. bounded replay and truthful closeout.

## Intent and workflow anchor

The repo remains a deterministic desk-runtime system with explicit stage order and bounded downstream fresh-capital authority.
This tranche does not create a new stage.
This tranche does not create a new review-visible authority surface.
This tranche adds one observational lane that preserves later-readable option-surface history without changing current-pass recommendation or capital-deployment behaviour.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- `OptionsFlowContextOutput` as the canonical derived Step-3 output surface
- `PreparedRuntimeSnapshot` and `PreparedRuntimeLineage` as current prepared-runtime lineage authority
- `OptionSnapshotPayload` and persisted `OptionSnapshot` rows as existing raw option-row contract surfaces
- `pyproject.toml` and current `Settings.database_url` defaults as environment authority
- current DMP / DMP V2 stage order as unchanged

### Retire from authority (compatibility-only unless later removed)
- none in this tranche

### Mandatory amendments
- `docs/03_DOMAIN_MODEL.md` because a new observational record contract and store semantics will become live repo authority if execution proceeds
- `docs/04_TECHNICAL_ARCHITECTURE.md` because the adjacent observational lane becomes a bounded architecture surface if execution proceeds
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` because lawful readers, prohibited inference, and non-stage status must be recorded if execution proceeds
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` only if Gate 242 lawfully admits new labels rather than quarantining them
- `src/nvda_desk/db/models.py` and a new Alembic version because persistence shape changes if execution proceeds
- runtime services and tests that prove no recommendation or allocator interference if execution proceeds

### New additions
- one observational-record schema surface
- one bounded persistence surface for the lane
- one bounded runtime extraction/helper surface
- one bounded replay/acceptance proof slice
- tranche-local support docs: checklist, contradiction report, scope note, execution log

## Vocabulary discipline

- Existing vocabulary authority must be read before writing any new durable planning term, field name, class name, or gate title.
- The behavioural briefs propose three new labels:
  - **Options and Flow Context History Lane**
  - **Options Surface Observation Record**
  - **Options Surface Observation Store**
- Gate 242 must classify each of those through the Vocabulary Workflow as exactly one of:
  - `add_new`
  - `alias_only`
  - `quarantine`
- Until that leaf closes, repo-governing docs must not pretend the labels are already canonical.
- If vocabulary admission is not lawful in Gate 242, the pack must freeze exact temporary code-symbol usage explicitly and keep the prose labels evidence-only.

## Packet / contract discipline

- `docs/03_DOMAIN_MODEL.md` remains the baseline packet/data contract authority for this tranche.
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` remains the baseline runtime-reader and prohibited-inference authority for this tranche.
- The observational lane must not create a new DMP or DMP V2 stage in this tranche.
- The capture trigger is the fully formed `OptionsFlowContextOutput`, but the bounded raw front/next expiry subset is not currently carried inside that output contract.
- Gate 244 must therefore prove one lawful bounded raw-source path aligned by symbol, timestamp, expiry, and lineage. It must not improvise broad all-expiry archival or mutate `PreparedRuntimeSnapshot` into a hidden raw-chain warehouse.

## Contradiction scan and state-integrity rules

- The router quartet is now aligned on the active observational-lane pack.
- Gate 242 cleaned the earlier minor router hygiene semantics in repo-root `PLANS.md` and the canonical gate map.
- The material design tension is not router law. It is the raw-source boundary:
  - the runtime already forms `OptionsFlowContextOutput`;
  - the current `OptionsFlowContextInput` / `OptionsFlowContextOutput` contracts do not carry raw option rows;
  - `PreparedRuntimeSnapshot` preserves `chain_ts`, `front_expiry`, `next_expiry`, and lineage but not the raw quote rows themselves.
- Gate 244 must resolve that lawfully by proving one bounded raw-slice source keyed to the same observation rather than weakening the capture boundary.

Closeout invariants for the eventual active pack:
- `completed_leaf_ids` and `remaining_leaf_ids` are disjoint;
- every referenced leaf id exists in the leaves ledger;
- `active_gate = none` is lawful only when `remaining_leaf_ids` and `pending_gate_ids` are empty;
- later-proof tests must permit later valid states or be retired/replaced during closeout.

## Document-touch checklist

This tranche uses:
- `docs/planning/2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_DOCUMENT_TOUCH_CHECKLIST_v1.md`

Execution may not begin until the checklist is populated and the pack is routed truthfully.

## Testing and promotion discipline

- Repo-local environment required: `.venv`
- Bootstrap authority:
  - `make install`
  - `uv sync --extra dev`
- `pyproject.toml` is binding for Python, dependency, and database-driver expectations in this tranche.
- If sandbox dependency resolution later fails, use the operator-supplied dependency bundle without changing repo dependency law.

Planning-phase minimum validation:
- `python3 -m json.tool docs/planning/2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_LEAVES_v1.json`
- `python3 -m pytest -q tests/test_planning_state_integrity.py`

Execution-phase minimum validation must stay bounded and include:
- schema/model contract tests
- runtime tap correctness tests
- raw-slice boundary tests
- persistence tests
- recommendation/CDA non-interference tests
- bounded replay verification

## Gates

### Gate 242: Vocabulary admission and observational-lane freeze

**Objective**
- Freeze the lane as observational-only, classify the proposed new labels, and route or quarantine the vocabulary change explicitly before implementation semantics spread.

**In-scope surfaces**
- `/mnt/data/options_and_flow_context_history_lane_architecture_brief_2026-04-09.md`
- `/mnt/data/options_and_flow_context_history_lane_gate_leaf_execution_brief_2026-04-09.md`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
- `docs/planning/2026-04-09_OPTIONS_AND_FLOW_CONTEXT_HISTORY_LANE_IMPLEMENTATION_CONTRADICTION_REPORT_v1.md`
- router quartet surfaces when the draft pack is lawfully activated

**Definition of done**
- the observational lane meaning is frozen;
- vocabulary handling for the three proposed labels is explicit;
- the capture point and capture scope are frozen;
- router hygiene semantics are cleaned if the gate is executed and closed.

### Gate 243: Observation-record contract and persistence model

**Objective**
- Define one deterministic observation-record contract and one distinct persistence model for the lane, with no recommendation, inventory, or allocator semantics.

**In-scope surfaces**
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/schemas/dataset.py`
- `src/nvda_desk/schemas/options.py`
- `src/nvda_desk/db/models.py`
- `alembic/versions/`
- Gate 243 schema/model tests

**Definition of done**
- one deterministic observational record contract exists;
- one distinct persistence model exists;
- identity, lineage, raw-subset, derived-state, and partiality semantics are explicit;
- no recommendation or allocator semantics are present.

### Gate 244: Runtime tap and bounded raw-slice extraction

**Objective**
- Build the lawful runtime tap at the `OptionsFlowContextOutput` boundary and the bounded raw front/next expiry extraction path without changing stage order or authority.

**In-scope surfaces**
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/options_flow_context.py`
- `src/nvda_desk/services/market_state.py`
- `src/nvda_desk/services/chain_to_cognition.py`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/schemas/dataset.py`
- Gate 244 runtime and raw-slice tests

**Definition of done**
- one lawful observation-record build path exists per cycle;
- the raw subset is bounded to front and next expiries only;
- timestamp and lineage alignment are explicit;
- recommendation surfaces, prepared-runtime contracts, and DMP / DMP V2 stage order remain unchanged.

### Gate 245: Persistence path and non-interference proof

**Objective**
- Persist the observational record deterministically and prove that enabling the lane does not change recommendation or fresh-capital behaviour.

**In-scope surfaces**
- persistence service/store-write path
- `src/nvda_desk/services/cognition_runtime.py`
- `src/nvda_desk/services/review_explanation.py` only if a non-interference assertion needs explicit review-shape guarding
- DB verification tests
- recommendation/CDA non-interference tests

**Definition of done**
- persistence succeeds deterministically;
- persistence failure handling is explicit and non-authoritative;
- recommendation outputs are unchanged when the lane is enabled;
- **Capital Deployment Authority Service** inputs and outputs are unchanged when the lane is enabled;
- no new DMP packet or stage-order mutation appears.

### Gate 246: Bounded replay and truthful closeout

**Objective**
- Revalidate the lane through one bounded replay slice, prove no accidental all-expiry archival or hidden authority drift, and close the pack truthfully.

**In-scope surfaces**
- admitted fixture/replay path used for the bounded slice
- closeout note / retained evidence for the lane
- router quartet
- gate map closeout row
- bounded acceptance tests for the tranche

**Definition of done**
- each replayed cycle emits one derived-state block, one bounded raw front/next expiry subset, and deterministic lineage/timestamps;
- no all-expiry accidental archival occurs;
- no recommendation or allocator authority has been introduced;
- the repo closes the pack truthfully with no active-pack drift.
