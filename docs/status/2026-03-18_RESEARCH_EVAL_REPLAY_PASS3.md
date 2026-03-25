# 2026-03-18 Research / Evaluation / Replay Pass 3

## Scope
Promote the repo from a lightweight DB-backed market API into a broader local desk-memory spine with persisted research notes, persisted evaluation runs, and replay grouped by session phase.

## What changed
- added DB models:
  - `research_note`
  - `evaluation_run`
- added schemas:
  - `schemas/research.py`
  - `schemas/eval.py`
  - `schemas/replay.py`
- added services:
  - `ResearchService`
  - `EvaluationLogService`
  - `ReplayService`
- extended API dependencies to expose research, evaluation-log, and replay services
- added API routes:
  - `GET /replay/session-phases`
  - `POST /research/notes`
  - `GET /research/notes`
  - `POST /evals/strategic-ladder-validator`
  - `POST /evals/overnight-carry-evaluator`
- extended dev seed from 24 bars to 240 bars so seeded data spans multiple session phases
- refreshed `README.md` to match the actual repo state and current API surface

## Verified
```bash
.venv/bin/ruff check src tests
.venv/bin/mypy src tests
.venv/bin/pytest -q
```

Observed result:
- `ruff` passed
- `mypy` passed
- `pytest -q` returned `18 passed in 1.69s`

## Boundaries
This pass did **not** implement:
- PostgreSQL or Alembic migrations
- real market-data ingestion
- real OpenAI orchestration
- IBKR connectivity
- MCP or frontend surfaces

## Next step
Promote the local DB path into the intended architecture by adding:
1. Postgres + Alembic base,
2. persisted market/research/eval tables under the intended long-term domain layout,
3. replay and evaluation persistence layered on top of stored market state.
