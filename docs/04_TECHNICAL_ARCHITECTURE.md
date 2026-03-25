# 04_TECHNICAL_ARCHITECTURE

## Current implementation path

The current repo is one FastAPI-backed codebase with shared domain logic, contracts, and database shape.

## Frozen technical choices

- Python 3.13
- PostgreSQL primary long-term database
- FastAPI backend
- OpenAI Responses API for research orchestration
- Pydantic v2 for strict contracts
- Alembic migrations
- Polars-first analytics stack
- IBKR behind an internal broker interface

## Top-level layout

```text
market vendors / broker / calendars
        |
        v
raw_vendor -> canonical_market -> derived_features
        |             |                 |
        +-------------+-----------------+
                      |
                      v
             desk cognition services layer
          /            |            |            \
         v             v            v             v
   FastAPI routes   replay/evals   broker boundary   review/explanation
```

## Service boundaries

The current service layer includes:
- `MarketStateService`
- `EventsService`
- `ResearchService`
- `ModuleRegistryService`
- `PromotionService`
- `EvaluationLogService`
- `ExperimentLogService`
- `RiskGatewayService`
- `CapitalAllocatorService`
- `ExecutionRecordsService`
- `ReviewPacketService`
- `ReviewExplanationService`
- `ReplayService`
- `ReplayComparisonService`
- `ConfigSurfaceService`
- desk-cognition services for temporal, regime, options/flow, posture/risk, playbook eligibility, and execution expression

Route handlers remain thin and delegate to services.

## Current database domains

### `raw_vendor`
Current stub: raw broker and vendor-shaped intake.

### `canonical_market`
Current tables include market bars, option contracts, option snapshots, calendars, and market events.

### `research_artefacts`
Current tables include research notes, module specs, evaluation runs, experiment runs, and promotion decisions.

### `execution_records`
Current tables include signal events, veto events, risk blocks, order events, fill events, positions, capital state, and daily PnL reports.

## Current API surfaces

The current API exposes route families for:
- health and configuration;
- market state, events, and replay phases;
- research notes and module specs;
- module promotions and evaluation logging;
- risk decisions and allocation;
- execution records and paper broker flow;
- review packets and module health.

## Broker path

The runtime speaks to `BrokerAdapter`, not directly to broker-specific code from strategy modules.
The current repo includes an in-memory paper broker path. No live broker adapter is implemented in the repo state.

## Deployment assumptions

### Local development
- Docker Postgres
- `.env` configuration
- `make` entrypoints
- FastAPI local development server
- SQLite-backed deterministic dev path where explicitly configured

## Technical anti-goals for v1

- no multi-broker orchestration;
- no wide symbol universe;
- no free-form SQL tool exposure to GPT;
- no direct live-order path from the model;
- no premature UI-heavy rebuild.
