# NVIDIA Day Trading

A single-operator, tier-one-desk-inspired **research and deterministic playbook platform** for NVIDIA.

This repo is **not** an autonomous LLM trader.
It is a split system:
- a **research cockpit** where the human operator and GPT inspect market state, compare regimes, and design modules;
- a **deterministic runtime** that evaluates approved modules, applies posture and risk gates, records evaluation artefacts, and emits review packets.

## What the repo is now

The current repo contains a working local development spine plus a contract-first Desk Cognition Grammar scaffold:
- frozen typed contracts for modules, module specs, promotions, research notes, evaluations, replay, and market retrieval;
- local SQLAlchemy-backed persistence with a deterministic SQLite dev path;
- FastAPI routes for market, replay, research-note capture, module registry, promotion tracking, and evaluation logging;
- deterministic dev seed covering multiple intraday session phases;
- temporal-state classification with a session-clock compatibility wrapper, replay grouped by session phase, and two first promoted evaluators:
  - Strategic Ladder Validator;
  - Overnight Carry Evaluator;
- canonical import registry and Desk Cognition Grammar mapping artefacts under `docs/planning/`;
- a deterministic desk-grammar runtime scaffold for temporal context, market regime, options and flow, posture and risk, playbook eligibility, expression and execution, and review and explanation.

## First-class docs

Read these in order:
1. `docs/01_NORMATIVE.md`
2. `docs/02_OPERATING_MODEL.md`
3. `docs/03_DOMAIN_MODEL.md`
4. `docs/04_TECHNICAL_ARCHITECTURE.md`
5. `docs/05_GUARDRAILS.md`
6. `docs/TESTING_AND_PROMOTION.md`
7. repo-root `PLANS.md`
8. `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
9. the active corrective/successor pair named by `PLANS.md` (currently `docs/planning/2026-03-27_REVIEW_RECONSTRUCTION_CORRECTIVE_GATES_v1.md` and `docs/planning/2026-03-27_REVIEW_RECONSTRUCTION_CORRECTIVE_LEAVES_v1.json`)
10. `docs/planning/2026-03-24_CANONICAL_VISION_EXTENSION_EXECUTION_LOG_v3.md` when gate status or closeout truth matters
11. `AGENTS.md`

Completed predecessor packs may remain under `docs/planning/` as implementation evidence, but repo-root `PLANS.md` decides which planning artefacts are active. Historical design drafts and archived milestone artefacts live in `docs/legacy/`. Build-status notes live in `docs/status/`. Machine-readable repo history lives in `CHANGELOG.jsonl`.

## Quickstart

```bash
make install
cp .env.example .env
make init-db
make seed-dev
make check
make run-api
```

## Make targets

```bash
make install
make init-db
make seed-dev
make lint
make typecheck
make test
make test-unit
make check
make run-api
```

## Repo shape

```text
src/nvda_desk/
  api/          FastAPI entrypoints
  db/           local DB metadata, models, sessions, seeding
  domain/       deterministic domain logic such as temporal-state classification
  schemas/      Pydantic contracts
  services/     reusable market, research, evaluation, replay, and desk-grammar services
```

## Current boundaries

- GPT helps **read**, **reason**, and **draft**.
- GPT does not place live orders.
- The deterministic runtime is the only execution path.
- PostgreSQL remains the intended long-term system of record.
- The current implementation path uses a lightweight local SQLite backbone to accelerate deterministic build-out before Postgres/Alembic promotion.
- IBKR remains an adapter boundary, not the shape of the platform.
