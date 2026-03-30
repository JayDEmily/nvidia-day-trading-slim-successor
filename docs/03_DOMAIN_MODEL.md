# 03_DOMAIN_MODEL

## Purpose

This document describes the important domain objects, canonical vocabularies, and interface boundaries.

For enum-like vocabularies that also exist in `src/nvda_desk/schemas/`, the schema values are authoritative. This document mirrors them in prose.

## Core object families

### 1. Market-state objects
Persistent facts and near-facts used for retrieval.

Key examples:
- `SessionCalendarPayload`
- `MarketSnapshotResponse`
- `IntradayBarsResponse`
- `OptionSurfaceResponse`
- `EventProximityResponse`
- `ReplaySessionResponse`

Ownership:
- persistence in `canonical_market`
- retrieval through `MarketStateService`, `EventsService`, and `ReplayService`

### 2. Research objects
Human and GPT artefacts.

Key examples:
- `ResearchNoteCreate`
- `ResearchNotePayload`
- `ResearchNoteListResponse`

Ownership:
- persistence in `research_artefacts`
- orchestration through `ResearchService`

### 3. Module and promotion objects
Formal playbook units and their promotion record.

Key examples:
- `ModuleDescriptor`
- `ModuleSpecCreate`
- `ModuleSpecPayload`
- `ModuleClass`
- `ModuleStatus`
- `PromotionDecisionCreate`
- `PromotionDecisionPayload`

Canonical module classes:
- `signal`
- `veto`
- `sizing`
- `execution`

Canonical module statuses:
- `planned`
- `draft`
- `coded`
- `backtested`
- `paper_candidate`
- `approved`
- `retired`

### 4. Desk Cognition Grammar objects
Typed contracts for the runtime stages.

Key examples:
- `TemporalContextInput` / `TemporalContextOutput`
- `MarketRegimeContextInput` / `MarketRegimeContextOutput`
- `OptionsFlowContextInput` / `OptionsFlowContextOutput`
- `PostureRiskInput` / `PostureRiskOutput`
- `PlaybookEligibilityInput` / `PlaybookEligibilityOutput`
- `ExecutionExpressionInput` / `ExecutionExpressionOutput`
- `ReviewExplanationInput` / `ReviewExplanationOutput`

### 4a. State-policy authority objects
Typed contracts that freeze what may vary, what state may be read, and how effective policy is derived.

Key examples:
- `RuntimeSurfaceClass`
- `CanonicalStateVectorField`
- `StateVectorFieldSpec`
- `ModifierPolicySpec`
- `EffectiveCoefficientLineage`
- `StatePolicyAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4b. Non-action and conflict governance objects
Typed contracts that freeze stand-down classes, conflict severity, degradation steps, and override boundaries before later policy matrices are written.

Key examples:
- `NonActionClass`
- `SignalConflictClass`
- `DegradationStep`
- `OverrideDisposition`
- `ConflictResolutionPolicy`
- `NonActionAuthorityPacket`
- `ReviewGovernanceSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py` and `src/nvda_desk/schemas/review.py`
- review exposure through `ReviewExplanationOutput`


### 4c. Stability metric and corridor objects
Typed contracts that freeze the multi-axis scorecard, corridor zones, persistence law, and slice coverage used before later review or candidate comparison gates.

Key examples:
- `ScorecardAxis`
- `StabilityMetricFamily`
- `MetricTriggerMode`
- `CorridorZone`
- `CorridorBreachSeverity`
- `BehaviourStabilityState`
- `SurfaceStabilityScorecard`
- `StabilityAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- review hooks through `ReviewExplanationOutput`

### 4d. Review-eligibility governance objects
Typed contracts that freeze evidence floors, trigger classes, downstream review outcomes, and bounded change budgets.

Key examples:
- `ReviewSurfaceClass`
- `ReviewTriggerClass`
- `ReviewOutcome`
- `ReviewChangeBudget`
- `EvidenceFloorSpec`
- `ReviewEvidenceBlock`
- `ReviewEligibilityAuthorityPacket`
- `ReviewEligibilitySurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py` and `src/nvda_desk/schemas/review.py`
- review exposure through `ReviewExplanationOutput`

### 4e. Candidate governance and adjudication objects
Typed contracts that freeze candidate-set size, role semantics, adjudication disposition, and governed comparison outcomes.

Key examples:
- `CandidateRole`
- `CandidateComparisonOutcome`
- `AdjudicationDisposition`
- `CandidateSetShape`
- `CandidateLedgerRecord`
- `CandidateGovernanceAuthorityPacket`
- `CandidateGovernanceSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py` and `src/nvda_desk/schemas/review.py`
- review and ledger hooks through `ReviewExplanationOutput`

### 4f. Event taxonomy objects
Typed contracts that freeze event class, subclass, materiality, and semantic-phase law before later event plumbing or policy matrices.

Key examples:
- `DeskEventClass`
- `EventSemanticPhase`
- `EventMaterialityTier`
- `CompanyEventSubclass`
- `MacroEventSubclass`
- `PolicyEventSubclass`
- `EventTaxonomyAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4g. Desk-calendar and venue objects
Typed contracts that freeze venue calendars, timezone authority, closure classes, and bridge rules before later routing and precursor binding.

Key examples:
- `TradingVenue`
- `VenueTimezone`
- `SessionTemplate`
- `CalendarClosureClass`
- `SessionBridgeRule`
- `VenueSessionContract`
- `DeskCalendarAuthorityPacket`
- `ExpiryCalendarInteraction`
- `CalendarAwareEventContract`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/session_clock.py` and `src/nvda_desk/schemas/events.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4h. Temporal event-window objects
Typed contracts that freeze event proximity, window, overlap, risk-timing, and carry-sensitivity semantics before later posture matrices or runtime binding.

Key examples:
- `EventProximityState`
- `EventWindowState`
- `EventOverlapClass`
- `EventRiskTimingClass`
- `EventCarrySensitivity`
- `EventWindowContract`
- `EventWindowAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/temporal_surface.py`
- review hook in `src/nvda_desk/schemas/review.py` and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

Gate 116 note: `TemporalContextOutput.event_timing_profile` and `TemporalEventWindowSurface.timing_profile` make event-class timing law explicit so macro, company, expiry, and venue-session windows stop sharing one hidden generic countdown rule.

### 4i. Precursor-universe objects
Typed contracts that freeze which ex-US precursor venues, raw fields, derived fields, and session-alignment expectations are lawful before stitching or runtime binding begins.

Key examples:
- `PrecursorVenueUniverse`
- `PrecursorSourceClass`
- `RawPrecursorField`
- `DerivedPrecursorField`
- `SessionAlignmentExpectation`
- `ExcludedPrecursorSource`
- `PrecursorVenueContract`
- `PrecursorUniverseAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/market.py`
- review hook in `src/nvda_desk/schemas/review.py` and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5a. Phase-and-carryover policy objects
Typed contracts that freeze ordinary day-phase and carryover posture law before later event-stress matrices or runtime integration.

Key examples:
- `DayPhaseState`
- `CarryHorizonState`
- `PhaseBehaviourClass`
- `PhaseNoActionBias`
- `PhaseCarryPolicyRecord`
- `PhaseCarryoverPolicyAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/risk.py`
- state-vector linkage in `src/nvda_desk/schemas/state_policy.py` and `src/nvda_desk/schemas/cognition.py`
- review hook in `src/nvda_desk/schemas/review.py` and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5b. Event/options-stress policy objects
Typed contracts that freeze imminent/live event risk and options-stress posture law before global precedence or runtime wiring begins.

Key examples:
- `EventOptionsStressState`
- `EventOptionsStressFamily`
- `PolicyEffectType`
- `EventOptionsBehaviourClass`
- `EventOptionsStressPolicyRecord`
- `EventOptionsStressAuthorityPacket`
- `EventOptionsStressPolicySurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects

### 4l. Live event-richness objects

`LiveEventReference` carries compact event identity, timing, materiality, provenance count, and lineage keys for one nearby event. `LiveEventSnapshot` carries the requested timestamp, query window, next-event reference, nearby/material event summaries, and deduplicated lineage keys. `PreparedRuntimeSnapshot.live_event_snapshot` and `TemporalContextInput.live_event_snapshot` preserve this packet into the live cognition path while `PreparedRuntimeLineage.event_lineage_keys` keeps the provenance keys auditable.

Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 5b. Event/options-stress policy objects
Typed contracts that freeze imminent/live event risk and options-stress posture law before global precedence or runtime wiring begins.

Key examples:
- `EventOptionsStressState`
- `EventOptionsStressFamily`
- `PolicyEffectType`
- `EventOptionsBehaviourClass`
- `EventOptionsStressPolicyRecord`
- `EventOptionsStressAuthorityPacket`
- `EventOptionsStressPolicySurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 5a. Phase-and-carryover policy objects
Typed contracts that freeze ordinary day-phase and carryover posture law before later event-stress matrices or runtime integration.

Key examples:
- `DayPhaseState`
- `CarryHorizonState`
- `PhaseBehaviourClass`
- `PhaseNoActionBias`
- `PhaseCarryPolicyRecord`
- `PhaseCarryoverPolicyAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/risk.py`
- state-vector linkage in `src/nvda_desk/schemas/state_policy.py` and `src/nvda_desk/schemas/cognition.py`
- review hook in `src/nvda_desk/schemas/review.py` and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5b. Event/options-stress policy objects
Typed contracts that freeze imminent/live event risk and options-stress posture law before global precedence or runtime wiring begins.

Key examples:
- `EventOptionsStressState`
- `EventOptionsStressFamily`
- `PolicyEffectType`
- `EventOptionsBehaviourClass`
- `EventOptionsStressPolicyRecord`
- `EventOptionsStressAuthorityPacket`
- `EventOptionsStressPolicySurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 5b. Event/options-stress policy objects
Typed contracts that freeze imminent/live event risk and options-stress posture law before global precedence or runtime wiring begins.

Key examples:
- `EventOptionsStressState`
- `EventOptionsStressFamily`
- `PolicyEffectType`
- `EventOptionsBehaviourClass`
- `EventOptionsStressPolicyRecord`
- `EventOptionsStressAuthorityPacket`
- `EventOptionsStressPolicySurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4i. Precursor-universe objects
Typed contracts that freeze which ex-US precursor venues, raw fields, derived fields, and session-alignment expectations are lawful before stitching or runtime binding begins.

Key examples:
- `PrecursorVenueUniverse`
- `PrecursorSourceClass`
- `RawPrecursorField`
- `DerivedPrecursorField`
- `SessionAlignmentExpectation`
- `ExcludedPrecursorSource`
- `PrecursorVenueContract`
- `PrecursorUniverseAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/market.py`
- review hook in `src/nvda_desk/schemas/review.py` and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5a. Phase-and-carryover policy objects
Typed contracts that freeze ordinary day-phase and carryover posture law before later event-stress matrices or runtime integration.

Key examples:
- `DayPhaseState`
- `CarryHorizonState`
- `PhaseBehaviourClass`
- `PhaseNoActionBias`
- `PhaseCarryPolicyRecord`
- `PhaseCarryoverPolicyAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/risk.py`
- state-vector linkage in `src/nvda_desk/schemas/state_policy.py` and `src/nvda_desk/schemas/cognition.py`
- review hook in `src/nvda_desk/schemas/review.py` and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5b. Event/options-stress policy objects
Typed contracts that freeze imminent/live event risk and options-stress posture law before global precedence or runtime wiring begins.

Key examples:
- `EventOptionsStressState`
- `EventOptionsStressFamily`
- `PolicyEffectType`
- `EventOptionsBehaviourClass`
- `EventOptionsStressPolicyRecord`
- `EventOptionsStressAuthorityPacket`
- `EventOptionsStressPolicySurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 5b. Event/options-stress policy objects
Typed contracts that freeze imminent/live event risk and options-stress posture law before global precedence or runtime wiring begins.

Key examples:
- `EventOptionsStressState`
- `EventOptionsStressFamily`
- `PolicyEffectType`
- `EventOptionsBehaviourClass`
- `EventOptionsStressPolicyRecord`
- `EventOptionsStressAuthorityPacket`
- `EventOptionsStressPolicySurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 5a. Phase-and-carryover policy objects
Typed contracts that freeze ordinary day-phase and carryover posture law before later event-stress matrices or runtime integration.

Key examples:
- `DayPhaseState`
- `CarryHorizonState`
- `PhaseBehaviourClass`
- `PhaseNoActionBias`
- `PhaseCarryPolicyRecord`
- `PhaseCarryoverPolicyAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/risk.py`
- state-vector linkage in `src/nvda_desk/schemas/state_policy.py` and `src/nvda_desk/schemas/cognition.py`
- review hook in `src/nvda_desk/schemas/review.py` and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5b. Event/options-stress policy objects
Typed contracts that freeze imminent/live event risk and options-stress posture law before global precedence or runtime wiring begins.

Key examples:
- `EventOptionsStressState`
- `EventOptionsStressFamily`
- `PolicyEffectType`
- `EventOptionsBehaviourClass`
- `EventOptionsStressPolicyRecord`
- `EventOptionsStressAuthorityPacket`
- `EventOptionsStressPolicySurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 5b. Event/options-stress policy objects
Typed contracts that freeze imminent/live event risk and options-stress posture law before global precedence or runtime wiring begins.

Key examples:
- `EventOptionsStressState`
- `EventOptionsStressFamily`
- `PolicyEffectType`
- `EventOptionsBehaviourClass`
- `EventOptionsStressPolicyRecord`
- `EventOptionsStressAuthorityPacket`
- `EventOptionsStressPolicySurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 5c. Modifier-control-law objects
Typed contracts that freeze precedence, compatible combination algebra, caps/floors, vetoes, and kill-switches before runtime integration begins.

Key examples:
- `ModifierPriorityBand`
- `CombinationLaw`
- `KillSwitchCondition`
- `ModifierClampRule`
- `ModifierVetoRule`
- `ModifierControlLawAuthorityPacket`
- `ModifierControlLawSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py`
- config/review hooks in `src/nvda_desk/schemas/config.py`, `src/nvda_desk/schemas/review.py`, and `src/nvda_desk/schemas/cognition.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4j. Event-ingestion and provenance objects
Typed contracts that freeze supported event-source inventory, provenance fields, freshness/confidence semantics, and outage/conflict handling before shared event store/query surfaces land.

Key examples:
- `EventSourceClass`
- `SupportedEventSource`
- `EventFreshnessState`
- `EventConfidenceTier`
- `SourceConflictDisposition`
- `SourceOutagePolicy`
- `EventSourceProvenance`
- `RawEventSourceObservation`
- `NormalisedEventRecord`
- `EventIngestionAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- normalisation service in `src/nvda_desk/services/event_ingestion.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
### 4k. Shared event-store and query objects


Typed contracts that freeze shared event persistence and query semantics before live event-rich packets are wired into cognition.

Key examples:
- `ReplayEventConsumerMode`
- `EventQueryWindow`
- `EventStoreQueryResult`
- `EventStoreAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/events.py`
- shared consumer service in `src/nvda_desk/services/event_store.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 5. Risk and capital objects
### 5. Risk and capital objects
Deterministic checks that sit in front of execution.

Key examples:
- `RiskPolicyInput`
- `RiskDecision`
- `RiskDecisionPayload`
- `CapitalStateSnapshotPayload`
- `DailyPnlReportPayload`

### 6. Broker and execution-record objects
Boundary objects for paper execution and recorded outcomes.

Key examples:
- `BrokerOrderPayload`
- `BrokerOrderEventPayload`
- `BrokerFillEventPayload`
- `PositionSnapshotPayload`
- `ModuleSignalEventPayload`
- `ModuleVetoEventPayload`
- `RiskBlockEventPayload`

### 7. Evaluation and review objects
Objects that describe whether a module advances, is compared, or is explained under governed review.

Key examples:
- `EvaluationRunPayload`
- `ExperimentRunPayload`
- `ComparisonReport`
- `StackDefinition`
- `CoefficientSet`
- `DailyReviewPacket`
- `ModuleHealthPacket`

## Interface boundaries

### GPT boundary
GPT receives compact summaries and returns structured research artefacts.
GPT is not the execution boundary.

### Service boundary
Application logic lives in services. API handlers stay thin.

### Broker boundary
Only the broker adapter layer knows broker-specific details.

### Persistence boundary
Pydantic contracts define the shape crossing service and API layers. SQLAlchemy models define the persisted shape.

### 4m. Precursor-stitching objects

Typed contracts that freeze precursor venue ordering, timestamp discipline, stale/degraded fallback, contradiction classes, and pre-policy posture meaning before runtime packet binding lands.

Key examples:
- `PrecursorTimestampDiscipline`
- `PrecursorFreshnessState`
- `PrecursorFallbackDisposition`
- `PrecursorContradictionClass`
- `PrecursorPostureState`
- `PrecursorVenueSlice`
- `PrecursorStitchingResult`
- `PrecursorStitchingAuthorityPacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/market.py`
- deterministic assembly service in `src/nvda_desk/services/market_state.py`
- prose mirror in `docs/01_NORMATIVE.md` and `docs/02_OPERATING_MODEL.md`

### 4n. Precursor runtime-binding objects

Typed contracts that preserve stitched precursor truth through prepared runtime snapshots, cognition ingress, and review reconstruction without creating a second hidden precursor path.

Key examples:
- `PrecursorRuntimePacket`
- `PreparedRuntimeSnapshot.precursor_runtime_packet`
- `TemporalContextInput.precursor_runtime_packet`
- `PrecursorRuntimeBindingSurface`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/market.py`, `src/nvda_desk/schemas/dataset.py`, and `src/nvda_desk/schemas/cognition.py`
- conversion/runtime bridge in `src/nvda_desk/services/chain_to_cognition.py`
- review exposure in `src/nvda_desk/services/review_explanation.py`

#### Gate 115 note: normalised prepared-runtime feature carriage

`PreparedNormalisedFeatureSet` freezes one bounded feature-carriage packet for regime-aware normalised fields derived during raw-to-prepared conversion. It is carried on `PreparedRuntimeSnapshot.normalised_features` and preserved into `RealDataCognitionInputs.normalised_features` so later gates can use richer cross-regime inputs without inventing a second hidden feature path. The packet also keeps per-feature provenance field names explicit rather than hiding formula ancestry in prose.

#### Gate 119 note: candidate adjudication carriage

`CandidateAdjudicationRecord` freezes the scored ranking record for each eligible playbook candidate. It is carried on `ExecutionExpressionOutput.candidate_adjudication` together with `contradiction_resolution`, `lead_selection_score`, and `lead_selection_reasons` so lead selection stops hiding behind registry order when multiple candidates are live.

#### Gate 120 note: execution geometry carriage

`ExecutionExpressionOutput` now also carries bounded execution-geometry fields so the runtime can express how a lead idea would actually be deployed rather than only which idea won. The governed geometry surface includes `passive_aggressive_bias`, `ladder_spacing_bps`, `max_chase_distance_bps`, `stop_distance_bps`, `take_profit_distance_bps`, `hedge_ratio`, `per_slice_risk_pct`, and `geometry_notes`.

#### Gate 121 note: final-risk join carriage

`ExecutionExpressionOutput` now also carries `pre_final_risk_active_playbook_ids`, `pre_final_risk_lead_playbook_id`, `pre_final_risk_entry_style`, and `final_risk_join` so the runtime can show exactly what execution looked like before the final risk join and how the join allowed, derisked, or veto-blocked the output. `FinalRiskJoinSurface` freezes the final disposition, reasons, lineage tags, and execution effect so review packets stop hiding the last authority step.

### 4o. Review failure-taxonomy objects

Typed contracts that let review packets distinguish failure class, resolution class, economic accountability, and promotion evidence without collapsing everything to raw P&L pain.

Key examples:
- `ReviewFailureClass`
- `ReviewResolutionClass`
- `EconomicContributionTag`
- `ReviewLineagePacket`
- `ReviewFailurePacket`
- `EconomicContributionPacket`
- `PromotionEvidencePacket`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/review.py` and `src/nvda_desk/schemas/cognition.py`
- review packet builder in `src/nvda_desk/services/review_explanation.py`
- review packet rendering helpers in `src/nvda_desk/services/review_packets.py`


### 5d. Runtime modifier integration objects

Typed contracts that let runtime apply bounded modifier law once, expose the effective result honestly, and preserve governed resolved-surface lineage across posture, execution, and review.

Key examples:
- `ResolvedRuntimeSurfaceValue`
- `ModifierRuntimePacket`
- `PostureRiskOutput.modifier_runtime_packet`
- `ExecutionExpressionOutput.modifier_runtime_packet`
- `ReviewExplanationOutput.effective_policy`
- `ReviewLineagePacket.resolved_surfaces`

Ownership:
- binding schema authority in `src/nvda_desk/schemas/state_policy.py` and `src/nvda_desk/schemas/cognition.py`
- runtime integration in `src/nvda_desk/services/state_conditioned_modifier.py` and `src/nvda_desk/services/cognition_runtime.py`
- review exposure in `src/nvda_desk/services/review_explanation.py`

### 5e. Governed coefficient-authority objects

Typed config contracts that freeze which admitted coefficient surfaces exist before runtime promotion reads them.

Key examples:
- `CoefficientAuthorityDocument`
- `MutableNumericSurfaceAuthoritySpec`
- `MutableBooleanSurfaceAuthoritySpec`
- `TemporalThresholdAuthoritySpec`
- `TimingParameterAuthoritySpec`

Ownership:
- binding schema authority in `src/nvda_desk/config_models.py`
- governed file surface in `config/coefficient_authority.v1.yaml`
- runtime promotion for the eight admitted mutable surfaces now occurs through `StateConditionedModifierService`; later gates still govern temporal-threshold activation

The governed authority file is not the same surface as the legacy `coefficients_registry.example.yaml`. The former freezes the admitted tranche-one authority chain; the latter remains salvage/example structure only.

## Gate 79 domain additions

The domain now includes explicit walk-forward window contracts, horizon-discovery outputs, fragility/ablation reports, and downstream consumer bindings so review-horizon evidence is typed rather than implied.
