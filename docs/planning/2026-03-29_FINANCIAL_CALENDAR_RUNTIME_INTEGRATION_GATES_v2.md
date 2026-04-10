Status: closed on `main`; Gates 91-93 complete on `main`; no later active gate declared in-repo

# 2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_GATES_v2.md

## Purpose

Define the next financial-calendar tranche after Gate 90 so the repo moves from controlled ingress to effective runtime use through canonical projection, bounded temporal derivation, downstream consumer alignment, and honest closeout.

## Why v2 exists

The prior v1 pack was conceptually correct but not fully granular enough. In particular, it grouped distinct event families, runtime carriers, temporal transitions, and downstream consumers into leaves that were too wide. This v2 pack keeps the same gate order but splits those wide leaves into smaller bounded units.

## Scope

In scope:
- canonical projection of imported financial-calendar facts into desk-calendar, canonical event, shared event-store, live-event, and precursor runtime surfaces;
- bounded temporal-context and carry-routing amendments so rich calendar/event meaning survives long enough to affect lawful runtime state;
- downstream consumer alignment for playbook eligibility, state-conditioned modifier, and review explanation so they read richer bounded state rather than raw import-stage records or a single compressed event anchor;
- control-surface closeout for Gates 91-93.

Out of scope:
- new alpha modules or coefficient search;
- direct behavioural reads from raw bundle files or import-stage records;
- replay-wide or walk-forward-wide model retuning;
- changing the normative meaning of event taxonomy, desk-calendar authority, or precursor authority already frozen in earlier gates.

## Supersession and active authority

- This document is the reviewed successor to the standalone v1 next-tranche pack.
- It supersedes:
  - `2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_GATES_v1.md`
  - `2026-03-29_FINANCIAL_CALENDAR_RUNTIME_INTEGRATION_LEAVES_v1.json`
- It does not reopen or reinterpret Gates 88-90.

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/02_OPERATING_MODEL.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/04_TECHNICAL_ARCHITECTURE.md`
- `docs/05_GUARDRAILS.md`
- `AGENTS.md`
- `PLANS.md`
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/planning/2026-03-24_DMP_V2_NORMATIVE_SPEC.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/08_TESTING_AND_PROMOTION.md`
- `src/nvda_desk/schemas/financial_calendar.py`
- `src/nvda_desk/services/financial_calendar_reference.py`
- `src/nvda_desk/services/financial_calendar_import.py`
- `src/nvda_desk/schemas/session_clock.py`
- `src/nvda_desk/schemas/events.py`
- `src/nvda_desk/schemas/market.py`
- `src/nvda_desk/schemas/cognition.py`
- `src/nvda_desk/services/event_ingestion.py`
- `src/nvda_desk/services/event_store.py`
- `src/nvda_desk/services/chain_to_cognition.py`
- `src/nvda_desk/services/temporal_context.py`
- `src/nvda_desk/services/carry_handoff.py`
- `src/nvda_desk/services/playbook_eligibility.py`
- `src/nvda_desk/services/state_conditioned_modifier.py`
- `src/nvda_desk/services/review_explanation.py`

## Workflow placement

This tranche sits between reference/import truth and downstream runtime/review consumers.

It is not a new decision module.
It is the bridge that turns imported calendar facts into lawful runtime truth.

Explicitly:
- Gate 91 is canonical projection.
- Gate 92 is bounded temporal derivation and carry-session routing.
- Gate 93 is downstream consumer alignment and honest closeout.

Later consumers must read:
- preserved runtime packets and canonical records; and
- bounded temporal outputs derived from those packets.

Later consumers must not read directly:
- raw bundle JSON files;
- import-stage records as if they were runtime truth;
- `next_event_at` as the sole event system.

## Intent and workflow anchor

The governing lens is the repo's tier-one desk cognition model.

The financial calendar is upstream information authority. It describes what kind of session and event environment the desk is in. It does not directly assign coefficients or act as a free-standing playbook. It must first become canonical desk-calendar and event truth, then bounded temporal state, then lawful downstream policy input.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- `nvda_desk.schemas.session_clock.DeskCalendarAuthorityPacket`
- `nvda_desk.schemas.events.RawEventSourceObservation`
- `nvda_desk.schemas.events.NormalisedEventRecord`
- `nvda_desk.services.event_ingestion.EventIngestionService`
- `nvda_desk.services.event_store.EventStoreService`
- `nvda_desk.schemas.events.LiveEventSnapshot`
- `nvda_desk.schemas.market.PrecursorRuntimePacket`
- `nvda_desk.services.chain_to_cognition.ChainToCognitionService`
- `nvda_desk.services.temporal_context.TemporalContextService`

### Retire from authority (compatibility-only unless later removed)
- `session_clock` outward surfaces as canonical step-1 truth
- `PreparedRuntimeSnapshot.next_event_at` as the primary event system
- `SessionCalendarCreate` and `MarketEventCreate` as the canonical sink for imported calendar truth
- archived compatibility-era consumer shortcuts that proxy event truth only from `next_event_at` and `event_window_state`

### Mandatory amendments
- extend canonical event records so venue, jurisdiction, source status, retained tag families, and layer identity survive projection where needed for runtime or review;
- add a canonical projection layer from imported financial-calendar records into desk-calendar, event, event-store, live-event, and precursor runtime surfaces;
- widen temporal derivation so event overlap, cooling-off, memory, carry sensitivity, and venue-state truth are derived from rich canonical packets rather than a single timestamp anchor;
- amend carry/session routing so next-session logic uses desk-calendar authority rather than weekday heuristics;
- amend downstream consumers so they distinguish macro, company, expiry, venue-session, and precursor stress via bounded runtime state;
- amend review explanation so overlap classes and preserved runtime packets survive explanation.

### New additions
- deterministic canonical projection service for financial-calendar records
- projection-specific schema extensions for retained rich meaning
- bounded tests proving downstream consumers read richer bounded state without direct raw-record coupling
- closeout anti-drift proof that Gates 91-93 cannot be claimed complete while control surfaces still point at older gate truth

## Vocabulary discipline

- The existing vocabulary authority must be read before writing any new planning term, file name, class name, field name, or gate title.
- The following repo terms are binding for this tranche and must be reused rather than paraphrased loosely:
  - `desk_calendar_contract`
  - `event_taxonomy`
  - `shared_event_store`
  - `precursor_runtime_packet`
  - `event_window_state`
  - `session_clock` (compatibility-only)
  - `carry_handoff`
  - `playbook_eligibility`
  - `state_conditioned_modifier`
- If a needed term is missing, propose it explicitly and add it to the vocabulary authority before merge.

## Packet / contract discipline

- `docs/planning/2026-03-24_DMP_V2_NORMATIVE_SPEC.md` is mandatory reading for any leaf that changes packet carriage, lineage, validation, or compatibility.
- Gate 91 may preserve richer event meaning through canonical models and runtime packets, but it must not invent a parallel packet contract outside the repo's DMP v2 law.
- External examples or bundle-native labels must not be copied verbatim if they conflict with repo-native compatibility or bounded event taxonomy.

## Testing and promotion discipline

- Repo-local environment required: `.venv`
- Each leaf must have a bounded validation slice.
- Each gate must have a minimum gate-wide validation slice.
- A gate is not complete until tests ran green, planning control surfaces moved together, and a new full-history zip exists from the exact green repo state.

## Gate sequencing summary

### Gate 91 sequencing summary
1. Project venue/session facts into desk-calendar authority.
2. Project macro/policy and company/expiry families separately into canonical event records.
3. Project precursor venue-state into precursor runtime surfaces.
4. Extend event-store and live-event carriers so retained meaning survives.
5. Prove thin CRUD sinks and raw import records remain subordinate and non-canonical.

### Gate 92 sequencing summary
1. Widen runtime carriage into cognition input.
2. Amend temporal event-window derivation.
3. Amend temporal venue/session derivation.
4. Amend carry routing to use desk-calendar truth.
5. Preserve compatibility hints explicitly while proving they are non-canonical.
6. Prove bounded temporal outputs retain rich meaning needed by later consumers.

### Gate 93 sequencing summary
1. Align playbook eligibility.
2. Align state-conditioned modifier.
3. Align review explanation.
4. Close the tranche honestly across plans, gate map, leaves ledger, and execution log.
5. Add final anti-drift proof and produce the full-history zip.

## Gates

### Gate 91: Canonical projection from imported financial-calendar truth into desk-calendar, event, live-event, and precursor surfaces

**Objective**
- Turn imported financial-calendar records into lawful repo-native desk-calendar authority, canonical event records, shared event-store truth, live-event runtime surfaces, and precursor runtime packets without collapsing into thin CRUD sinks.

**Definition of done**
- imported financial-calendar records project deterministically into desk-calendar authority, canonical event records, event-store/live-event truth, and precursor runtime surfaces;
- retained rich fields survive projection where runtime or review later need them;
- tests prove the projection path does not treat `SessionCalendarCreate`, `MarketEventCreate`, or raw import records as the sole runtime truth sink.

### Gate 92: Temporal-context and carry-routing transition onto rich canonical truth  
Status: complete on `main` via `work/gate-92-financial-calendar-temporal-transition-20260329`

**Objective**
- Amend step-1 temporal derivation so it uses rich canonical calendar/event truth and desk-calendar-aware session routing instead of a single anchor timestamp plus weekday heuristics.

**Definition of done**
- temporal context derives bounded runtime state from rich canonical packets rather than a lone `next_event_at` anchor;
- carry/session routing uses desk-calendar truth for next-session logic and half-day/holiday handling;
- compatibility hints remain available explicitly but are proven non-canonical.

### Gate 93: Downstream consumer alignment, review semantics, and tranche closeout
Status: complete on `main` via `work/gate-93-financial-calendar-downstream-alignment-20260329`

**Objective**
- Align downstream consumers and review surfaces with the richer bounded temporal/runtime state, then close the tranche honestly across the planning control surfaces.

**Definition of done**
- downstream consumers read richer bounded runtime state without direct dependency on raw bundle files or import-stage records;
- review explanation preserves overlap class, carry sensitivity, and retained runtime packet meaning;
- `PLANS.md`, the gate map, the active leaves ledger, and the active execution log all point to Gate 93 closeout together, and a fresh full-history zip exists from that exact green state.


## Gate 91 closeout note

Gate 91 is complete on `main` once desk-calendar authority projection, canonical event projection, precursor runtime projection, retained-field live-event enrichment, subordinate-thin-sink proof, and the active planning-control updates all exist together.
