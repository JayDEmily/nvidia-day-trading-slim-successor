# BUILD PLAN

## Current status

The repo already contains:
- contracts;
- DB backbone and migrations;
- narrow API surface;
- deterministic dev seed;
- replay engine;
- paper broker stub;
- research orchestration boundary;
- promotion persistence.

## Immediate next build sequence

1. verify real local Postgres boot from zero;
2. run a real OpenAI smoke with credentials;
3. implement the first real IBKR adapter behind `BrokerAdapter`;
4. strengthen replay/eval and post-trade attribution;
5. add MCP surface without duplicating business logic;
6. only then add a chat-style frontend if still needed.

## Near-term gates

### Gate A — real local service boot
Pass when:
- `make db-up`
- `make migrate`
- `make seed-dev`
- `make check`
- `make run-api`

all work cleanly in the real environment.

### Gate B — real OpenAI orchestration
Pass when:
- a credentialed call can produce a structured research note + module draft;
- the artefact persists cleanly.

### Gate C — live broker boundary implementation
Pass when:
- the IBKR adapter can read account state and place paper-safe orders through the broker boundary;
- the ledger stays intact.

### Gate D — better attribution
Pass when:
- evaluation artefacts distinguish signal quality from execution quality;
- slippage and veto effectiveness are recorded.

## Anti-rabbit-hole rules

Do not add these before the above gates pass:
- wide symbol universes;
- news-pipeline sprawl;
- multiple brokers;
- heavy UI rebuilds;
- direct GPT-to-order shortcuts.
