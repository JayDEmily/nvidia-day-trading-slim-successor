# 04_TECHNICAL_ARCHITECTURE

## 1. Current implementation path

The current repo is one FastAPI-backed codebase with shared domain logic, strict typed contracts, SQLAlchemy persistence, and deterministic runtime/review services.

The current implementation path is:

- one local development spine inside a single Python codebase;
- FastAPI as the application surface;
- SQLAlchemy models plus Pydantic contracts as the persistence and interface boundary;
- a deterministic desk-cognition runtime that evaluates approved stage contracts in serial order;
- a local SQLite-backed default development path for deterministic build-out;
- PostgreSQL as the intended long-term system of record;
- an internal broker boundary;
- an explicit research-orchestration boundary.

## 2. Frozen technical choices

The current frozen technical choices are:

- Python 3.13
- PostgreSQL as the primary long-term database
- FastAPI backend
- OpenAI Responses API as the intended research orchestration boundary
- Pydantic v2 for strict contracts
- Alembic migrations
- Polars-first analytics stack
- IBKR behind an internal broker interface

## 3. Top-level system layout

The current system has four top-level paths that meet in the service layer:

1. market and calendar ingestion/retrieval;
2. research artefact capture and governed module/evaluation state;
3. deterministic desk-cognition runtime and review packet construction;
4. broker-facing paper execution and execution-record persistence.

```text id="fuqi3n"
market vendors / calendars / broker boundary / research boundary
        |                 |                 |                 |
        v                 v                 v                 v
raw vendor-shaped intake  session/event     BrokerAdapter     OpenAIOrchestrator
        |                 state             boundary          boundary
        +-----------------+-----------------+-----------------+
                          |
                          v
          canonical market persistence + prepared/derived runtime inputs
                          |
          +---------------+------------------+-------------------+
          |               |                  |                   |
          v               v                  v                   v
   FastAPI routes   desk cognition runtime   replay/evals   review/explanation
                          |
                          v
                   execution decisions
                          |
                          v
                  paper broker flow
                          |
                          v
                 execution_records persistence
```

### 3.1 External inputs and boundaries

External and quasi-external boundaries currently include:

- market and option data retrieval through market-state services;
- event/calendar data capture and retrieval through event services;
- broker interaction through `BrokerAdapter`;
- research orchestration through `OpenAIOrchestrator`.

Runtime and strategy logic do not speak broker-specific code directly. The execution runtime does not embed a direct live OpenAI call path.

### 3.2 Canonical data path

The current logical data path is:

- vendor-shaped intake and event/calendar ingestion;
- canonical market persistence;
- prepared/derived runtime inputs;
- deterministic runtime evaluation;
- review/explanation and execution-record persistence.

Current database domains are:

- `canonical_market`
- `research_artefacts`
- `execution_records`

Prepared/derived features in current repo state are carried primarily through schemas and services rather than a separately named first-class database domain.

### 3.3 Service and API path

FastAPI route handlers delegate to service objects. Services own retrieval, evaluation, review, replay, and persistence logic. Typed schemas define the API/service contracts and the runtime packet boundaries.

## 4. Service boundaries

The current service layer is service-first.

### 4.1 Market and event services

Current market and event services include:

- `MarketStateService`
- `EventsService`
- `EventIngestionService`
- `EventStoreService`
- `ReplayService`
- `ReplayComparisonService`
- `FinancialCalendarImportService`
- `FinancialCalendarProjectionService`
- `ChainToCognitionService`
- `RealDataLoaderService`

These services own:

- session-clock and temporal-state retrieval;
- market snapshot and intraday retrieval;
- option-surface retrieval;
- market-event and calendar-event capture/query;
- replay session grouping and replay comparison;
- prepared runtime ingress construction from canonical and real-data surfaces.

### 4.2 Research, module-registry, promotion, and evaluation services

Current research and governed module services include:

- `ResearchService`
- `ModuleRegistryService`
- `PlaybookRegistryService`
- `PromotionService`
- `EvaluationLogService`
- `ExperimentLogService`
- `DeskCognitionRuntimeRegistryService`
- `CanonicalImportRegistryService`

There are also promoted and bounded evaluator and replay services in the current repo state, including:

- `StrategicLadderValidatorService`
- `StrategicLadderMarketService`
- `StrategicLadderReplayService`
- `StrategicLadderExperimentService`
- `OvernightCarryEvaluatorService`
- `OvernightCarryMarketService`
- `OvernightCarryReplayService`

These services own:

- research-note capture and retrieval;
- module-spec persistence and listing;
- promotion-decision persistence and listing;
- evaluation and experiment logging;
- bounded evaluator and replay harnesses for promoted module families;
- import-registry and runtime-registry artefacts.

### 4.3 Desk-cognition runtime services

The current deterministic runtime services include:

- `TemporalContextService`
- `MarketRegimeContextService`
- `OptionsFlowContextService`
- `ParallelRiskLaneService`
- `PostureRiskService`
- `PlaybookEligibilityService`
- `ExecutionExpressionService`
- `StateConditionedModifierService`
- `RiskGatewayService`
- `ReviewExplanationService`

The current runtime also integrates bounded imported-contract services including:

- `TrancheAUpstreamContractService`
- `TrancheASelectorContractService`

These services own:

- stage-local evaluation outputs;
- preserved and compatibility seam surfaces;
- modifier evaluation and application;
- overlay-risk evaluation and final-risk application;
- review-packet construction and review explanations.

### 4.4 Review, replay, and configuration services

Current review, replay, and configuration services include:

- `ReviewPacketService`
- `ReviewExplanationService`
- `ReplayService`
- `ReplayComparisonService`
- `ConfigSurfaceService`

These services own:

- daily review packet generation;
- module-health packet generation;
- review explanations from runtime outputs;
- replay sessions and replay comparisons;
- runtime, evaluation, coefficient, and config surface retrieval.

### 4.5 Broker and execution-record services

Current broker and execution services include:

- `ExecutionRecordsService`
- `RiskGatewayService`
- `CapitalAllocatorService`

These services own:

- signal, veto, and risk-block recording;
- paper order capture;
- order, fill, position, and account-state retrieval;
- capital allocation decisions;
- execution-record persistence.

### 4.6 Thin-route rule

FastAPI route handlers delegate to services. The architecture uses service-owned logic and contract-owned interfaces rather than route-owned behaviour.

## 5. Current deterministic runtime spine

The current desk-cognition runtime is a serial seven-stage spine with additive side surfaces. The runtime order is fixed.

### 5.1 Seven-stage serial order

The current serial stage order is:

1. temporal
2. regime
3. options_flow
4. posture
5. eligibility
6. execution
7. review

### 5.2 Current runtime evaluation flow

The current runtime flow is:

1. evaluate temporal context;
2. evaluate market regime context;
3. evaluate options and flow context;
4. evaluate the initial parallel-risk lane packet from temporal ingress and temporal output;
5. enrich the parallel-risk lane with regime and options-flow translation;
6. evaluate posture and risk;
7. evaluate selector-contract citations and attach posture citations;
8. evaluate state-conditioned modifiers;
9. apply modifier consequences to posture;
10. evaluate playbook eligibility;
11. attach selector-contract citations to eligibility;
12. evaluate execution expression using temporal, regime, options-flow, posture, eligibility, modifier packet, parallel-risk lane packet, and bounded position context;
13. apply modifier consequences to execution;
14. evaluate overlay risk;
15. build terminal-risk application from overlay decision plus posture permission;
16. enrich the parallel-risk lane with candidate semantics and evaluation-preparation surfaces;
17. build additive preserved stage-local handoff surfaces;
18. apply the final risk join to execution;
19. evaluate review and explanation from the full runtime state.

### 5.3 Parallel-risk lane placement

The parallel-risk lane is co-resident with the serial seven-stage runtime. It is not an eighth stage and it is not an alternative arbiter.

Its current placement is:

- initial read after temporal evaluation;
- market-translation enrichment after regime and options-flow;
- candidate-semantics enrichment after execution and risk evaluation;
- carriage into posture, execution, and review surfaces.

### 5.4 Modifier and terminal-risk application flow

The current mutation path is:

- posture is evaluated;
- a `ModifierRuntimePacket` is built;
- modifier consequences are applied to posture;
- eligibility reads the modifier-shaped posture state;
- execution reads posture, eligibility, modifier packet, and parallel-risk lane packet;
- modifier consequences are then applied to execution;
- overlay risk is evaluated on the execution state;
- a terminal-risk application surface is built;
- the final risk join is applied to execution before review.

### 5.5 Review and explanation outputs

The review stage consumes:

- temporal;
- regime;
- options_flow;
- posture;
- eligibility;
- execution;
- modifier runtime packet;
- parallel-risk lane packet;
- stage-local handoff surface;
- temporal ingress;
- imported-contract citations.

### 5.6 DMP lineage and packet boundaries

The runtime builds DMP v2 stage packets for each binding stage. Those packets are keyed by stage name and carry:

- grammar role;
- schema identity;
- summary information;
- lineage and dependency information;
- stage packet ids.

Current binding stages mapped into DMP packet construction are:

- temporal
- regime
- options_flow
- posture
- eligibility
- execution
- review

The review packet is the review and reference packet for the runtime result. The execution packet is the decision packet for the runtime result.

## 6. Current runtime ownership and compatibility seams

The current repo has explicit preserved and compatibility surfaces.

### 6.1 Stage ownership

Current stage ownership is:

- temporal owns session, time, and event-timing interpretation;
- regime owns the market-regime interpretation surface;
- options_flow owns the options and flow interpretation surface;
- posture owns posture permission, hard invariants, and local envelope;
- eligibility owns admissibility;
- execution owns candidate adjudication, lead-selection, execution geometry, lifecycle plan, and pre-final-risk execution expression;
- review owns explanation and review-facing packet composition.

### 6.2 Preserved stage-local handoff surface

The current runtime constructs a `StageLocalHandoffSurface` that preserves:

- cited posture before modifier mutation;
- cited eligibility;
- execution before modifier mutation;
- execution after modifier mutation but before terminal-risk application;
- overlay-risk decision;
- terminal-risk application;
- terminal-risk decision.

### 6.3 Compatibility bridges and final-risk joins

The current runtime and schemas preserve bounded compatibility surfaces including:

- `ModifierCompatibilityBridgeSurface`
- `FinalRiskJoinSurface`
- `TerminalRiskApplicationSurface`
- `EligibilityAdmissibilitySurface`
- `ExecutionCandidateOwnershipSurface`

## 7. Current database domains

### 7.1 `raw_vendor`

Current architectural meaning: vendor-shaped and broker-shaped raw intake.

This remains a useful architectural raw-ingress concept in `04`. The current SQLAlchemy model set is not organised as a separately named `raw_vendor` model namespace in `src/nvda_desk/db/models.py`.

### 7.2 `canonical_market`

Current tables include:

- `instrument`
- `bar_1m`
- `option_snapshot`
- `session_calendar`
- `market_event`

### 7.3 `research_artefacts`

Current tables include:

- `research_note`
- `evaluation_run`
- `experiment_run`
- `risk_decision_log`
- `module_spec`
- `promotion_decision`

### 7.4 `execution_records`

Current tables include:

- `module_signal_event`
- `module_veto_event`
- `risk_block_event`
- `order_intent`
- `order_event`
- `fill_event`
- `position_snapshot`
- `position_instance_snapshot`
- `capital_state_snapshot`
- `daily_pnl_report`

## 8. Current API surfaces

The current API exposes route families for the following surfaces.

### 8.1 Health and configuration

Current routes include:

- `/health`
- `/config/runtime-settings`
- `/config/evaluation-settings`
- `/config/coefficients`
- `/config/coefficients/{group_key}`
- `/config/strategy-variants`
- `/config/strategy-variants/{variant_name}`

### 8.2 Market state, events, and replay

Current routes include:

- `/market/temporal-state`
- `/market/session-clock`
- `/market/snapshot`
- `/market/intraday`
- `/market/options-surface`
- `/events/calendar` `POST`
- `/events/calendar` `GET`
- `/events/market` `POST`
- `/events/market` `GET`
- `/events/proximity`
- `/replay/session-phases`

### 8.3 Research notes and module specs

Current routes include:

- `/research/notes` `POST`
- `/research/notes` `GET`
- `/modules/specs` `POST`
- `/modules/specs` `GET`

### 8.4 Promotions and evaluation logging

Current routes include:

- `/modules/promotions` `POST`
- `/modules/promotions` `GET`
- `/modules/strategic-ladder-validator/evaluate`
- `/modules/strategic-ladder-validator/evaluate-from-market`
- `/modules/strategic-ladder-validator/replay-from-market`
- `/modules/overnight-carry-evaluator/evaluate`
- `/modules/overnight-carry-evaluator/evaluate-from-market`
- `/evals/runs`
- `/evals/experiments`
- `/evals/strategic-ladder-validator`
- `/evals/strategic-ladder-validator/from-market`
- `/evals/strategic-ladder-validator/replay-from-market`
- `/evals/strategic-ladder-validator/walk-forward-from-market`
- `/evals/strategic-ladder-validator/fragility-from-market`
- `/evals/strategic-ladder-validator/batch-rank-from-market`
- `/evals/overnight-carry-evaluator`
- `/evals/overnight-carry-evaluator/from-market`
- `/evals/overnight-carry-evaluator/replay-from-market`

### 8.5 Risk decisions and allocation

Current routes include:

- `/risk/evaluate`
- `/risk/decisions`
- `/allocation/module-regime`

### 8.6 Execution records and paper broker flow

Current routes include:

- `/execution/signals` `POST`
- `/execution/signals` `GET`
- `/execution/vetoes` `POST`
- `/execution/vetoes` `GET`
- `/execution/risk-blocks` `POST`
- `/execution/risk-blocks` `GET`
- `/execution/daily-pnl` `POST`
- `/execution/daily-pnl` `GET`
- `/broker/orders/paper`
- `/broker/order-events`
- `/broker/fill-events`
- `/broker/positions`
- `/broker/position-instances`
- `/broker/account-state`

### 8.7 Review packets and module health

Current routes include:

- `/review/module-health/{module_id}`
- `/review/daily-packet`

## 9. Broker path

The runtime speaks to `BrokerAdapter`, not directly to broker-specific code from strategy modules.

Current broker-path state is:

- protocol boundary: `BrokerAdapter`
- current implementation path: `InMemoryBrokerAdapter`
- current order and account models at the boundary: `OrderIntent`, `BrokerOrderRef`, `OrderEvent`, `AccountState`, `Position`
- current repo state supports paper and offline broker flow only
- no live broker adapter is implemented in the repo state

## 10. Research orchestration path

The research-orchestration seam is explicit and separate from the execution runtime.

Current research-orchestration state is:

- protocol boundary: `OpenAIOrchestrator`
- request and response contracts: `OpenAIResponseRequest` and `OpenAIResponseArtifact`
- current implementation path: `NullOpenAIOrchestrator`
- no live OpenAI Responses API call is attempted in current repo state

## 11. Deployment assumptions

### 11.1 Local development

Current local development assumptions are:

- Docker Postgres
- `.env` configuration
- `make` entrypoints
- FastAPI local development server
- SQLite-backed deterministic dev path in the current default config

### 11.2 Current local toolchain

Current repo tooling includes:

- `uv` for environment sync
- `make install`
- `make init-db`
- `make seed-dev`
- `make run-api`
- `make check`
- `docker compose up -d db`

### 11.3 Configuration surfaces

Current runtime and configuration surfaces include:

- environment-backed `Settings`
- playbook registry path
- coefficient authority path
- runtime-settings config API surface
- evaluation-settings config API surface
- coefficient and strategy-variant config API surfaces

## 12. Technical anti-goals for v1

Current anti-goals remain:

- no multi-broker orchestration
- no wide symbol universe
- no free-form SQL tool exposure to GPT
- no direct live-order path from the model
- no premature UI-heavy rebuild

## 13. Interpretation rule for this document

This document is the current technical architecture description for the repo state on `main`.

It describes:

- the currently implemented FastAPI, service, schema, persistence, and runtime shape;
- the currently implemented paper-path broker seam;
- the currently implemented review, replay, and evaluation surfaces;
- the intended long-term promoted database target where that target differs from the current default local implementation path.

It does not authorise bypassing the normative docs, the operating model, or the domain model.
