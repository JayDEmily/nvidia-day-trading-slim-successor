# 2026-03-19 — Sandbox Execution to Exhaustion Plan

This document is the concrete execution spec for the remaining work that can be done honestly inside the sandbox. It should be read together with the repo-root `PLANS.md`, which defines the execution rules and acceptance discipline.

## Mission

Advance the canonical repo as far as possible **without** requiring live external systems. The target is not a finished trading product; the target is a much stronger local research/runtime spine that is ready to move into the user's VS Code environment with minimal structural ambiguity.

## Current starting point

Verified current baseline:
- executable repo exists in the canonical tree;
- local `.venv` can be created via `uv sync --extra dev`;
- `make check` is passing locally;
- SQLite + Alembic path works locally;
- admitted legacy option snapshots are seeded into the DB;
- market-backed SLV routes and tests exist;
- merged backlog/config/fixture/doctrine salvage from legacy archives is present in the repo.

## Success condition for this plan

At plan completion, the repo should have:
- a fuller fixture pack and fixture loader discipline;
- a replayable, persisted SLV with market-backed and replay-backed evidence surfaces;
- phase-aware replay/eval outputs across the current module surfaces;
- a persisted overnight carry advisory surface;
- a typed deterministic risk gateway with veto/de-risk logging;
- stronger replay/eval artefacts for promotion/retirement decisions;
- config surfaces that are parseable and aligned with wired code;
- external boundaries left ready but explicitly unverified.

## Work packages

### WP1 — Fixture pack completion

#### Objective
Convert admitted legacy values into stable, provenance-tagged fixtures for options and related market-state examples.

#### Tasks
- expand `fixtures/legacy/fixtures_manifest.jsonl`;
- add any additional admitted CSV/JSON/JSONL fixture files that survived the extraction passes;
- add helper loaders in code where needed;
- ensure fixtures can seed or feed replay/eval paths.

#### Evidence
- fixture parse checks;
- targeted tests for loader + seeding.

#### Done when
- fixture pack is machine-readable and actually exercised by tests.

### WP2 — SLV replay and attribution

#### Objective
Make SLV more than a point-in-time evaluator by giving it replay-backed ladder outcome evidence.

#### Tasks
- add replay input shape for ladder windows;
- define rung-level outcomes and failure reasons;
- persist richer SLV evaluation artefacts;
- expose replay-backed SLV eval/service outputs.

#### Evidence
- targeted tests for rung outcome attribution;
- replay tests over seeded bars + option snapshots;
- migration checks if schema changes.

#### Done when
- SLV can be run from persisted market state, replayed, and attributed with stable outputs.

### WP3 — Macro/volatility supervisory overlays for SLV

#### Objective
Add the first supervisory surfaces that can dampen or veto SLV under extreme conditions.

#### Tasks
- implement the first low-regret overlay(s), likely:
  - `vvix_ladder_shaper`,
  - `macro_shock_responder`;
- define how overlays modify confidence, veto status, or allowable action;
- keep logic deterministic and test-covered.

#### Evidence
- unit tests for overlay logic;
- integration tests showing overlay changes SLV outcome.

#### Done when
- at least one overlay can materially and deterministically alter SLV evaluation.

### WP4 — Session-clock hardening

#### Objective
Make phase-aware behaviour part of replay/eval evidence, not just metadata.

#### Tasks
- centralise phase derivation;
- include phase in evaluation artefacts;
- add tests showing phase-sensitive behaviour changes.

#### Evidence
- unit tests for phase labels;
- replay tests with phase-grouped outputs.

#### Done when
- phase appears in persisted eval/replay outputs and affects at least one module path.

### WP5 — Overnight Carry Evaluator implementation

#### Objective
Promote carry logic from planning into persisted advisory evaluation.

#### Tasks
- add persisted carry evaluation model if needed;
- wire carry service into current market/eval surface;
- add session-boundary replay cases;
- keep output advisory and clearly separated from execution.

#### Evidence
- carry tests;
- replay tests across close-to-next-open behaviour;
- API tests if route is added.

#### Done when
- carry recommendations are replayable, persisted, and attribution-ready.

### WP6 — Risk gateway implementation

#### Objective
Give the repo a deterministic veto/de-risk surface rather than leaving vetoes mostly implicit.

#### Tasks
- define typed risk-policy objects;
- implement evaluation of volatility shock, stale data, no-trade, and exposure gates;
- log structured reasons;
- ensure policies can override module outputs.

#### Evidence
- policy unit tests;
- integration tests for veto precedence;
- replay/eval tests showing blocked recommendations.

#### Done when
- module outputs can be allowed/blocked/de-risked with explicit machine-readable reasons.

### WP7 — Replay/eval strengthening

#### Objective
Make promotion decisions more evidence-backed.

#### Tasks
- enrich evaluation artefacts with module/phase/veto attribution;
- add simple friction placeholders only where the inputs support them;
- improve persistence of decision traces.

#### Evidence
- replay/eval integration tests;
- persisted trace assertions.

#### Done when
- replay/eval outputs are strong enough to support promote/tune/retire decisions.

### WP8 — Config wiring discipline

#### Objective
Wire only the config surfaces that now touch real code, and keep the rest as examples.

#### Tasks
- validate or typed-load any now-live config fields;
- keep runtime/eval/coefficients/variants separated;
- update config README/examples if code changed.

#### Evidence
- YAML parse checks;
- typed-load tests where applicable.

#### Done when
- config examples match the code paths they claim to represent.

### WP9 — Boundary preparation only

#### Objective
Keep external-system interfaces ready without pretending the sandbox can verify them.

#### Tasks
- maintain Postgres/Alembic compatibility;
- isolate OpenAI orchestration boundaries cleanly;
- preserve IBKR adapter contracts;
- continue to defer MCP/frontend.

#### Evidence
- compile/type checks;
- offline migration SQL generation;
- explicit unverified status notes where relevant.

#### Done when
- interfaces are clean and ready for later real-environment work.

## Execution order

Run work packages in this exact order unless a hard dependency forces a local swap:
1. WP1 fixture pack completion
2. WP2 SLV replay and attribution
3. WP3 SLV supervisory overlays
4. WP4 session-clock hardening
5. WP5 overnight carry evaluator
6. WP6 risk gateway
7. WP7 replay/eval strengthening
8. WP8 config wiring discipline
9. WP9 boundary preparation only

## Per-pass test matrix

### Always after material code change
- `make check`

### When DB or migration changes
- `NVDA_DESK_DATABASE_URL=sqlite+pysqlite:///./var/plan_verify.db .venv/bin/alembic upgrade head`
- `NVDA_DESK_DATABASE_URL=sqlite+pysqlite:///./var/plan_verify_sql.db .venv/bin/alembic upgrade head --sql > var/alembic_offline.sql`

### When fixtures change
- JSONL/CSV/YAML parse checks for changed fixture/config artefacts;
- targeted `pytest` for loaders/seeding.

### When API/routes change
- targeted `pytest tests/test_api.py -q`

### When replay/eval logic changes
- targeted replay/eval tests;
- if needed, direct smoke via `TestClient`.

## Failure policy

If a work package introduces drift or breaks the green baseline:
- stop;
- restore passing state;
- write the failure and the blocking reason into the status note or changelog;
- only then proceed.

## What success will look like

When this plan is exhausted, the repo should still not claim live broker/OpenAI/MCP verification. But it should have:
- materially stronger local fixtures,
- deeper SLV evidence,
- phase-aware attribution,
- an implemented carry advisory surface,
- a deterministic risk gateway,
- richer replay/eval evidence,
- and cleaner typed/configured boundaries for the next environment.
