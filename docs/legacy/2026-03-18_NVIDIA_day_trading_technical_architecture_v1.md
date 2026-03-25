# NVIDIA Day Trading — Technical Architecture v1
**Date:** 2026-03-18  
**Status:** Canonical working draft  
**Scope:** Software architecture, schemas, repo structure, package choices, and implementation pattern

## 1. One recommended implementation path

Build one codebase with two client surfaces:

- **Surface A: API-first research console now**
- **Surface B: ChatGPT + MCP later**

The same domain logic, database schema, and promotion workflow must serve both.

## 2. Technical decisions frozen in this document

- **Language:** Python 3.13
- **Primary database:** PostgreSQL
- **Primary backend:** FastAPI
- **Model API:** OpenAI Responses API
- **Structured contracts:** Pydantic v2 + JSON Schema
- **Migrations:** Alembic
- **Broker adapter:** IBKR adapter behind an internal interface
- **Data frame engine:** Polars first
- **Execution discipline:** deterministic runtime only
- **ChatGPT integration path later:** MCP server exposing narrow tools

## 3. Why this stack

### PostgreSQL
Use PostgreSQL as the system of record because the project needs:
- relational integrity;
- auditability;
- time-sliced queries;
- joins across instruments, options, events, orders, fills, and module state;
- controlled writes and replayable state.

Do not add a vector database or extra infrastructure in v1.

### FastAPI
Use FastAPI because it gives:
- typed request/response contracts;
- clean async service endpoints;
- narrow internal tool handlers;
- easy OpenAPI documentation;
- straightforward path to both API clients and MCP-backed handlers.

### OpenAI Responses API
Use the Responses API as the canonical model surface for the API-first client because the current GPT-5.4 model is available there, supports tools/structured outputs, and OpenAI’s current documentation leans toward the Responses API for richer tool-heavy flows.

### MCP later
When ChatGPT-side MCP is ready on the surface you actually use, expose the same backend capabilities via MCP tools.
The server should return tight `structuredContent` for the model and keep bulky or sensitive UI payloads in `_meta`.

### Polars
Use Polars for feature engineering, replay analytics, and columnar processing.
Bring in pandas only when compatibility is unavoidable.

## 4. Top-level system diagram

```text
                        ┌───────────────────────────┐
                        │       Market Vendors      │
                        │  IBKR + calendar/events   │
                        └─────────────┬─────────────┘
                                      │
                                      ▼
                          ┌─────────────────────┐
                          │   Ingest Workers    │
                          │ raw_vendor capture  │
                          └─────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      PostgreSQL      │
                         │ system of record     │
                         └──────┬───────┬──────┘
                                │       │
                 derive features │       │ research / execution state
                                ▼       ▼
                       ┌────────────────────────┐
                       │   Domain Service Core  │
                       │ canonical + features   │
                       └──────┬────────┬────────┘
                              │        │
                API-first now │        │ MCP later
                              ▼        ▼
                     ┌────────────┐  ┌────────────┐
                     │ FastAPI    │  │ MCP Server │
                     │ tool layer │  │ tool layer │
                     └─────┬──────┘  └─────┬──────┘
                           │               │
                           ▼               ▼
                   ┌──────────────┐  ┌──────────────┐
                   │ Research UI  │  │ ChatGPT UI   │
                   │ / LibreChat  │  │ + widgets    │
                   └──────────────┘  └──────────────┘
```

## 5. Client-mode workflows

### 5.1 API-first workflow now

```text
You
 └─> research chat UI
      └─> backend session/orchestrator
           ├─> OpenAI Responses API
           │    └─> selects allowed tools
           └─> FastAPI tool handlers
                ├─> PostgreSQL queries
                ├─> feature summaries
                └─> research artefact writes
```

### 5.2 ChatGPT/MCP workflow later

```text
You in ChatGPT
 └─> GPT-5.4
      └─> MCP tool call
           └─> MCP server
                ├─> same domain services
                ├─> same PostgreSQL
                └─> tool result:
                     - structuredContent (tight JSON)
                     - content (narration)
                     - _meta (UI-only/bulky data)
```

## 6. Repo skeleton

```text
nvidia-day-trading/
├── docs/
│   ├── 2026-03-18_NVIDIA_day_trading_project_v1.md
│   ├── 2026-03-18_NVIDIA_day_trading_technical_architecture_v1.md
│   └── 2026-03-18_NVIDIA_day_trading_build_plan_v1.md
├── pyproject.toml
├── README.md
├── src/
│   └── nvda_desk/
│       ├── api/
│       ├── mcp/
│       ├── broker/
│       ├── config/
│       ├── data/
│       │   ├── ingest/
│       │   ├── canonical/
│       │   └── features/
│       ├── domain/
│       ├── research/
│       ├── modules/
│       ├── risk/
│       ├── execution/
│       ├── ledger/
│       ├── replay/
│       ├── evals/
│       ├── schemas/
│       └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── replay/
└── migrations/
```

## 7. Database domains

### 7.1 `raw_vendor`
Vendor-shaped intake, append-only where practical.

Examples:
- `raw_ibkr_market_ticks`
- `raw_ibkr_historical_bars`
- `raw_ibkr_option_computations`
- `raw_ibkr_account_snapshots`
- `raw_ibkr_order_events`

### 7.2 `canonical_market`
Normalised market facts.

Examples:
- `instrument`
- `session_calendar`
- `market_event`
- `bar_1m`
- `quote_snapshot_1m`
- `option_contract`
- `option_snapshot_1m`

### 7.3 `derived_features`
Calculated state used by modules and GPT.

Examples:
- `feature_vwap_1m`
- `feature_session_regime`
- `feature_opening_range`
- `feature_realized_vol`
- `feature_cross_market_context`
- `feature_option_surface_summary`

### 7.4 `research_artefacts`
Human + GPT outputs.

Examples:
- `research_note`
- `hypothesis`
- `module_spec`
- `playbook_revision`
- `experiment_run`

### 7.5 `execution_records`
Deterministic runtime state.

Examples:
- `module_signal_event`
- `module_veto_event`
- `risk_block_event`
- `order_intent`
- `order_event`
- `fill_event`
- `position_snapshot`
- `capital_state_snapshot`
- `daily_pnl_report`

## 8. Canonical schemas

### 8.1 Module schema

```yaml
module_id: str
name: str
version: str
status: enum[draft, coded, bug_gated, backtested, paper, approved, paused, retired]
class: enum[signal, veto, sizing, execution]
thesis: str
horizon: enum[intraday, overnight, weekend, event]
required_inputs:
  - str
parameters: object
regime_filters: object
trigger_logic_ref: str | null
veto_logic_ref: str | null
sizing_logic_ref: str | null
entry_logic_ref: str | null
exit_logic_ref: str | null
evaluation_spec_ref: str
risk_policy_ref: str
provenance:
  created_by: enum[user, gpt, mixed]
  conversation_ref: str | null
  source_note_refs: list[str]
```

### 8.2 Risk-policy schema

```yaml
risk_policy_id: str
version: str
max_daily_loss_pct: float | null
max_trade_risk_pct: float | null
max_gross_exposure_pct: float | null
max_position_notional_usd: float | null
max_open_positions: int | null
max_slippage_bps: float | null
stale_data_max_age_sec: int
block_on_pdt_violation: bool
block_on_insufficient_buying_power: bool
block_on_market_halt: bool
block_on_reject_storm: bool
kill_switch_modes:
  - manual
  - data_integrity
  - broker_disconnect
  - loss_limit
  - volatility_extreme
```

### 8.3 Evaluation schema

```yaml
evaluation_run_id: str
module_id: str
module_version: str
dataset_ref: str
run_type: enum[replay, backtest, paper, live_review]
metrics:
  signal_quality: object
  execution_quality: object
  veto_effectiveness: object
  drawdown: object
  capital_efficiency: object
  stack_interaction: object
decision:
  verdict: enum[fail, revise, pass]
  notes: str
```

## 9. Service boundaries

### 9.1 Domain services
Keep domain logic in reusable service classes or modules, not inside route handlers.

Core service areas:
- market state retrieval;
- option summary retrieval;
- event/calendar retrieval;
- research artefact persistence;
- module registry and promotion;
- risk gateway evaluation;
- replay and evaluation;
- broker adapter calls.

### 9.2 API routes
The API layer should be thin and typed.

Suggested route groups:
- `/health`
- `/market/*`
- `/options/*`
- `/events/*`
- `/research/*`
- `/modules/*`
- `/evals/*`
- `/execution/*`
- `/broker/*` (internal/admin only)

### 9.3 MCP tools later
Expose only narrow tools. Start with:
- `get_market_snapshot`
- `get_intraday_slice`
- `get_option_surface_summary`
- `get_session_analogue_set`
- `save_research_note`
- `save_module_spec`
- `list_active_modules`
- `get_post_trade_summary`

Do **not** expose arbitrary SQL tools to the model.

## 10. ASCII workflow — from idea to live eligibility

```text
Research conversation
    ↓
structured module spec
    ↓
deterministic implementation
    ↓
bug/test gates
    ↓
historical replay/backtest
    ↓
paper-trade evaluation
    ↓
approval decision
    ├─> approved into active stack
    ├─> revise and retest
    └─> retire / reject
```

## 11. ASCII workflow — deterministic runtime

```text
canonical market state + account state
        ↓
load approved module stack
        ↓
signal modules
        ↓
veto modules
        ↓
sizing modules
        ↓
pre-trade risk gateway
        ↓
execution modules
        ↓
broker adapter
        ↓
orders / fills / rejects
        ↓
ledger + attribution + review
```

## 12. Front-end recommendation

Use **LibreChat** as the bootstrap research UI if you want a mature, ChatGPT-like interface without rebuilding the front end from scratch.

Why this is the recommended path:
- it is explicitly ChatGPT-inspired;
- it supports OpenAI Responses API;
- it supports MCP tooling;
- it is MIT licensed;
- it avoids spending early project time on front-end reinvention.

Do **not** let the UI choice drive the backend design.
The backend contract must stay independent.

## 13. OpenAI integration pattern

### 13.1 API-first mode
Use the OpenAI Python SDK with the Responses API.
Keep the tool surface narrow.
Prefer strict tool schemas.
Persist conversation-linked artefacts and references outside the model.

### 13.2 MCP mode later
Use an MCP server that wraps the same domain services.
Return:
- tight `structuredContent` for the model;
- optional `content` narration;
- large or sensitive payloads in `_meta` for widgets only.

### 13.3 Prompting / orchestration rules
- use compact retrieval results, not giant tables;
- use JSON/YAML-like structured payloads;
- trim nested noise;
- after heavy tool results, provide a targeted follow-up hint/prompt at the orchestration layer where useful;
- keep tools idempotent.

## 14. Execution and broker integration

### 14.1 Broker adapter boundary
The execution runtime should call an internal broker interface, not IBKR directly from strategy code.

```python
class BrokerAdapter(Protocol):
    async def get_account_state(self) -> AccountState: ...
    async def get_positions(self) -> list[Position]: ...
    async def place_order(self, order: OrderIntent) -> BrokerOrderRef: ...
    async def cancel_order(self, order_id: str) -> None: ...
    async def stream_order_events(self) -> AsyncIterator[OrderEvent]: ...
```

### 14.2 IBKR-specific notes
Implement an IBKR adapter behind that interface.
Keep all IBKR pacing, entitlement, and paper/live differences isolated there.

## 15. Logging, audit, and replay

Every run that matters should persist:
- effective config version;
- module versions used;
- market-state snapshot references;
- tool inputs/outputs where relevant;
- order intents and broker responses;
- evaluation outputs;
- operator decisions.

Replay must be able to answer:
**What did the system know at 10:07, what did it decide, and why?**

## 16. Testing strategy

Use three layers:
- **unit tests** for pure logic;
- **integration tests** for database/service boundaries;
- **replay tests** for historical state and module behaviour.

Do not call live broker endpoints in standard CI.
Paper/live tests are explicit gated runs.

## 17. Deployment posture

### v1 recommended posture
- local development on Ubuntu / VS Code / uv;
- PostgreSQL locally or managed dev instance;
- API service + workers in Docker;
- object/filesystem artefact store for research files;
- no Kubernetes heroics.

### later
- move services to AWS only after the architecture stabilises;
- keep one database;
- keep one broker adapter;
- add managed observability only after the replay/eval loop exists.

## 18. References used in this technical pass

User-provided source material reviewed:
- `NVIDIA_day_trading_project_architecture_brief.md`
- `gpt_action_sql_database.md`
- `gpt_action_sql_database.ipynb`
- `data-retrieval.md`
- `structured-outputs.md`
- `latest-model.md`

External references to align with current docs:
- OpenAI function calling / strict mode / allowed tools
- OpenAI Apps SDK MCP server guidance
- OpenAI cookbook guidance for data-intensive apps
- IBKR API / market data / paper trading constraints
- LibreChat repository and docs

## 19. Bottom line

The software architecture is now simple enough to build and serious enough not to be a toy:
- one warehouse;
- one domain core;
- one deterministic runtime;
- two client surfaces;
- one promotion path from research to execution.

That is the right shape.
