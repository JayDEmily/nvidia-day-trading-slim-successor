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
