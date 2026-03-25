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
