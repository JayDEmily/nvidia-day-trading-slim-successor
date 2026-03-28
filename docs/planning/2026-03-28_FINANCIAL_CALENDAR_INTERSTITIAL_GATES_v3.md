# 2026-03-28 Financial Calendar Interstitial Gates v3

Status: active on `main`; Gate 91 is the next executable gate  
Version: v3.0

## Purpose

This document is the single active planning surface for the post-Gate-87 financial-calendar tranche.

It exists to close one specific architectural gap:

- the repo already has canonical calendar, event-window, event-ingestion, event-store, live-event, precursor, and temporal-context surfaces;
- the supplied financial-calendar bundle adds richer scheduled-facts authority upstream of desk cognition;
- the repo does **not** yet have the deterministic bridge that carries that richer authority into the canonical surfaces without flattening it back into the older thin path.

This pack therefore does **not** introduce a new decision module. It defines how the financial-calendar reference bundle must become lawful upstream information substrate for tier-one desk cognition.

## Why v3 exists

The prior planning state was incomplete for three reasons:

1. it did not state early enough which existing modules remain canonical and which become compatibility-only;
2. it did not make the DMP v2 compatibility constraints explicit enough for repo-native packet producers;
3. it risked letting rich calendar truth enter the repo and then get squeezed back into timestamp-only or label-only legacy paths.

This v3 pack fixes those defects.

## Position in the planning stack

- Gates 0–87 remain complete on `main`.
- The corrective reconstruction tranche remains closed evidence, not active authority.
- This pack becomes the active planning authority from **Gate 88** onward.
- Execution remains one leaf at a time, one gate at a time, one branch per gate.

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `docs/TESTING_AND_PROMOTION.md`
- `PLANS.md`
- `AGENTS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/planning/2026-03-27_REVIEW_RECONSTRUCTION_CORRECTIVE_GATES_v1.md`
- `docs/planning/2026-03-27_REVIEW_RECONSTRUCTION_CORRECTIVE_LEAVES_v1.json`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `src/nvda_desk/schemas/dmp_v2.py`
- `src/nvda_desk/schemas/events.py`
- `src/nvda_desk/schemas/session_clock.py`
- `src/nvda_desk/schemas/temporal_surface.py`
- `src/nvda_desk/schemas/market.py`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/services/event_ingestion.py`
- `src/nvda_desk/services/event_store.py`
- `src/nvda_desk/services/temporal_context.py`
- `src/nvda_desk/services/carry_handoff.py`

## External tranche inputs

The following supplied artefacts are inputs to this planning pack, but they are **not** canonical repo authority until imported under repo-controlled paths:

- the financial calendar bundle master manifest and layer JSON artefacts;
- the supplied bundle README and DMP v2 binding-plan note;
- the supplied example DMP v2 bundle packet;
- the supplied workbook primitives used to reason about Step 0 / Step 1 calendar and event fields.

The planning pack must treat those artefacts as external tranche inputs that are later landed into repo-native checked-in locations under controlled names.

## Desk-cognition placement

The calendar bundle sits at the **upstream information** layer of desk cognition.

It is not:
- a playbook;
- a coefficient surface;
- an execution-expression module;
- a direct action scorer.

It is:
- bounded session truth;
- bounded scheduled event truth;
- bounded precursor venue-state truth;
- bounded review and evaluation slicing truth.

The lawful flow is therefore:

1. checked-in reference truth;
2. deterministic canonical projection;
3. preserved event / precursor runtime packets;
4. bounded temporal-state derivation;
5. downstream posture / permission / carry / review consumers.

## Workflow transition and module disposition

### Retain as canonical

The following remain canonical and must be enriched rather than bypassed:

- `DeskCalendarAuthorityPacket` and the `desk_calendar_contract` venue/session contracts;
- `EventWindowAuthorityPacket`, `TemporalStateFeaturePayload`, and `TemporalStateClassifier`;
- `PrecursorUniverseAuthorityPacket`, `PrecursorRuntimePacket`, `PreparedRuntimeSnapshot.precursor_runtime_packet`, and `TemporalContextInput.precursor_runtime_packet`;
- `EventIngestionService`, `RawEventSourceObservation`, and `NormalisedEventRecord`;
- `EventStoreService`, `LiveEventSnapshot`, `PreparedRuntimeSnapshot.live_event_snapshot`, and `TemporalContextInput.live_event_snapshot`;
- `TemporalContextService` as the bounded Step 1 derivation boundary.

### Retire from authority

The following may remain in the tree for compatibility, but they must no longer be treated as architectural truth for this tranche:

- outward `session_clock` compatibility surfaces, including `SessionClockCompatibilityPayload`;
- `SessionClockClassifier` as the governing truth surface for post-Gate-87 temporal work;
- `PreparedRuntimeSnapshot.next_event_at` and `TemporalContextInput.next_event_at` as anything more than compatibility hints;
- `SessionCalendarCreate` and `MarketEventCreate` as canonical destinations for rich financial-calendar authority.

Retire from authority does **not** mean blind deletion. It means compatibility-only unless and until a later gate removes the code explicitly.

### Mandatory amendments

The tranche must explicitly amend the following seams:

- provenance-bearing event records must preserve the rich calendar fields needed for downstream review and runtime use;
- live event references must stay rich enough to preserve event family meaning, not just a timestamp and a label;
- temporal derivation must stop collapsing all event meaning into one timestamp anchor where richer governed truth already exists;
- carry/session alignment must derive from desk-calendar authority rather than weekday heuristics;
- compatibility-era imported-module consumers must not set architecture by accident;
- `state_conditioned_modifier`, `playbook_eligibility`, `carry_handoff`, and review consumers must read bounded temporal outputs or preserved runtime packets, not raw bundle files or import-stage records.

## Vocabulary discipline

This pack must use canonical repo nouns where they already exist.

If an exact new noun is required, it must:
- be scoped narrowly;
- avoid conflicting with an existing canonical noun;
- be admitted into vocabulary governance before merge of the implementation gate that depends on it.

This pack therefore prefers existing repo terms such as `desk_calendar`, `event_window`, `live_event_snapshot`, `precursor_runtime_packet`, `temporal_state`, and `session_clock` compatibility wrapper.

## DMP v2 compatibility constraint

The supplied example bundle packet is useful as an external shape example, but it must **not** be copied verbatim into repo-native producers.

Before implementation begins, Gate 89 must freeze the repo-native DMP v2 producer identifiers for the financial-calendar reference-bundle lane, including:

- `grammar_role` values compatible with the current repo enums/helpers;
- `behaviour_class` values compatible with the current repo enums/helpers;
- `packet_schema_id` and payload-contract identifiers matching repo-native packet-builder conventions;
- `schema_identifiers` compatibility metadata for object-block payload recovery;
- explicit `DmpV2Lineage`, `DmpV2ExecutionContext`, `DmpV2Summary`, and `DmpV2Validation` surfaces rather than ad hoc extension fields;
- the lawful block mix of one compact metadata `object_block` plus referenced artefact blocks.

No implementation gate may proceed while the financial-calendar packet lane still depends on external example identifiers that the current repo helper layer would reject.

## Canonical transit rule

The financial-calendar bundle must travel through this canonical path:

1. checked-in reference artefacts under a repo-controlled reference-data path;
2. deterministic mapping into canonical calendar / event / precursor records;
3. shared event-store and runtime packet preservation through `LiveEventSnapshot` and `PrecursorRuntimePacket`;
4. bounded outputs from `TemporalContextService`;
5. downstream policy and review consumers reading the bounded outputs or the preserved runtime packets, not raw bundle files.

The bundle must **not** be flattened straight into `session_clock`, `next_event_at`, or a lone `event_window_state` label before canonical projection has preserved the richer meaning.

## Non-goals for this tranche

- inventing alpha conclusions from the calendar itself;
- turning the bundle into a live web-fetch subsystem;
- widening the calendar bundle into an unbounded news engine;
- replacing canonical runtime policy with raw bundle labels;
- letting downstream policy or review services read raw bundle files or import-stage records directly;
- silently deleting compatibility-era code without explicit doctrine and tests.

---

## Gate 88 — Workflow transition reset, authority disposition, and vocabulary freeze

Status: complete on `main`

Depends on: closed Gate 87

### Objective

Freeze the workflow transition early enough that later implementation cannot pipe the new rich calendar truth back through the old thin path.

### Scope

- promote this pack into the active planning control surfaces;
- freeze the retain / retire-from-authority / amend matrix for affected modules and surfaces by exact class and field name where the repo already has those names;
- freeze the source-of-truth hierarchy for the financial-calendar tranche;
- define vocabulary discipline for any new nouns required by this tranche;
- record the canonical transit rule and explicit non-goals;
- add anti-drift tests that fail if the active planning surfaces disagree about Gate 88 being complete and Gate 89 being next.

### Definition of done

The repo has one active financial-calendar planning pack and one coherent set of planning control surfaces, the workflow-transition matrix is explicit, and the active planning tests prove Gate 88 is complete on `main`, Gate 89 is the next gate, and rich calendar truth may not be flattened into compatibility-only surfaces by doctrine drift.

### Gate outputs

- this governing gates doc
- one supporting leaves ledger
- one execution log for this pack
- updates to repo-root planning pointers and anti-drift tests

### Gate 88 closeout note

Gate 88 is complete on `main` once the active control surfaces, leaf ledger, execution log, and anti-drift tests all agree that Gate 89 is the next executable gate and that the Gate 88 transition doctrine remains explicit by class, field, and workflow boundary.

## Gate 89 — Canonical crosswalk and DMP v2 producer freeze

Status: complete on `main`

Depends on: closed Gate 88

### Objective

Define the deterministic mapping contract from external financial-calendar facts into repo-native canonical calendar, event, precursor, and runtime packet surfaces.

### Scope

- freeze the crosswalk from bundle fact families to canonical target surfaces and bounded top-level event classes/subclasses;
- freeze how rich bundle fields survive canonical projection and review retention;
- freeze the repo-native DMP v2 producer identifiers, schema-identifiers compatibility metadata, and block layout for the reference-bundle lane;
- freeze required `summary`, `validation`, `lineage`, and `execution_context` population rules for that lane;
- define what remains additive compatibility versus what becomes canonical;
- define validation and proof required before any import code lands.

### Definition of done

The repo has one explicit deterministic crosswalk contract and one repo-native DMP v2 producer contract for the financial-calendar lane, with no dependence on incompatible external example identifiers.

### Gate 89 closeout note

Gate 89 closes only when the deterministic crosswalk, retained-field matrix, repo-native DMP v2 lane, vocabulary entries, and bounded validation proof all exist on `main` together.

## Gate 90 — Checked-in reference artefacts and provenance-bearing import seam

Status: complete on `main`

Depends on: closed Gate 89

### Objective

Land the financial-calendar reference artefacts under repo-native checked-in paths and add the bounded import seam that carries provenance-bearing raw facts into canonical records.

### Scope

- add checked-in reference artefact paths and manifest discipline;
- land the imported bundle artefacts under repo control;
- implement the raw import seam and provenance-bearing records for the imported facts;
- preserve venue, jurisdiction, layer identity, source status, and retained tag families required by review and runtime;
- prove that imported raw facts are not yet wired directly into behaviour.

### Definition of done

Reference artefacts are checked into the repo under governed paths, provenance-bearing import records exist, and tests prove the raw artefacts are reviewable without becoming direct runtime policy.

### Gate 90 closeout note

Gate 90 closes only when the checked-in artefacts, repo manifest, import-stage records, repo-controlled packet lane, and non-behavioural proof all exist on `main` together.

## Gate 91 — Canonical projection into desk calendar, event, and event-store surfaces

Status: planned; next active gate

Depends on: closed Gate 90

### Objective

Project the imported reference facts into the canonical calendar, event, and event-store surfaces without losing the rich meaning needed downstream.

### Scope

- map venue closures / half-days / bridge facts into desk-calendar authority surfaces;
- map macro, expiry, earnings, and precursor-state facts into provenance-bearing event records;
- extend canonical event-store records where needed so preserved review/runtime meaning survives projection;
- keep thin CRUD compatibility sinks subordinate rather than canonical;
- prove the shared event store reflects the new canonical projection lawfully.

### Definition of done

The shared event truth and calendar truth reflect the imported financial-calendar facts through canonical repo surfaces, and the retained rich fields remain available for runtime and review use.

## Gate 92 — Temporal transition amendment and bounded runtime projection

Status: planned

Depends on: closed Gate 91

### Objective

Amend the temporal bridge so it derives bounded runtime state from rich canonical event/calendar truth without collapsing back into timestamp-only legacy semantics.

### Scope

- amend temporal derivation so it consumes the richer canonical event/calendar truth;
- amend carry/session alignment so next-session logic comes from desk-calendar authority rather than weekday heuristics;
- keep `next_event_at` and `session_clock` compatibility explicit but non-canonical;
- project only the bounded runtime labels and packet enrichments required by downstream posture, permission, carry, and review consumers;
- prove that downstream modules still read bounded runtime state while richer preserved packets remain available for explanation and audit.

### Definition of done

Temporal context and carry/session routing lawfully consume the richer financial-calendar truth, compatibility hints remain explicit but subordinate, and tests prove the rich meaning is not flattened before bounded runtime projection.

## Gate 93 — Closeout, promotion, and anti-drift proof

Status: planned

Depends on: closed Gate 92

### Objective

Close the tranche cleanly, promote the active financial-calendar pack as completed evidence, and prove that repo status surfaces cannot drift.

### Scope

- update all active planning pointers and execution receipts together;
- close the execution log honestly for Gates 88–92;
- record any compatibility-only surfaces still retained in-tree after the tranche;
- add closeout anti-drift proof so the repo cannot claim completion while still pointing at an older active pack or older gate.

### Definition of done

The planning pack, repo-root pointers, active planning control surfaces, and tests agree on the closed financial-calendar tranche, and any retained compatibility surfaces are documented as such rather than silently treated as canonical.
