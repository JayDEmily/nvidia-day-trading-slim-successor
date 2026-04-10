# 01_NORMATIVE

## Purpose

This file defines the binding authority hierarchy, frozen invariants, terminology, package-organisation rules, and contract rules for this repo.

## Document precedence

If documents disagree, use this order:

1. `docs/01_NORMATIVE.md`
2. machine-readable contracts under `src/nvda_desk/schemas/`
3. DB metadata and Alembic migrations
4. `docs/02_OPERATING_MODEL.md`
5. `docs/03_DOMAIN_MODEL.md`
6. `docs/04_TECHNICAL_ARCHITECTURE.md`
7. `docs/05_GUARDRAILS.md`
8. `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
9. `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`
10. `docs/TESTING_AND_PROMOTION.md`
11. repo-root `PLANS.md`
12. dated execution plans under `docs/planning/`
13. `AGENTS.md`
14. `README.md`
15. `docs/status/*`
16. `docs/legacy/*`

`docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` is specialised latest-state authority for runtime surface ownership, compatibility carriage, downstream reader law, and prohibited inference.

## Frozen invariants

The following are frozen unless deliberately revised with a changelog entry:

- the system is split into research and deterministic execution;
- GPT is a research and drafting tool, not a live execution engine;
- the broker boundary sits behind an internal adapter interface;
- PostgreSQL is the primary long-term system of record;
- the current local SQLite backbone exists only to accelerate deterministic build-out;
- the Makefile is the single operational front door;
- contracts, interfaces, and promotion states are more stable than policy thresholds;
- all order paths pass through posture, risk, deployable-capital governance, and ledger surfaces;
- replayability, auditability, and explanation are first-class requirements;
- the human desk operator lens is the binding design lens for every module, feature, and coefficient.
- research-mode ideation must seek asymmetry, dislocation, and edge before discussing implementation readiness; implementation-state caveats belong to reporting mode unless the user explicitly asks for readiness, promotion, or live-operability judgment.

## Desk Cognition Grammar (binding runtime order)

The binding desk-cognition spine follows this order:

1. temporal context
2. market regime context
3. options and flow context
4. posture and risk permission
5. playbook eligibility
6. expression and execution

Review and explanation is handled independently as a downstream review surface. It does not alter the binding Stage 1-6 recommendation boundary.

No module bypasses this order.

## First-class co-resident independent parallel risk lane (planning law)

The repo may plan and later implement an **independent parallel risk lane** as a first-class co-resident lane that begins with session start. It is **not** a numbered stage, **not** `1.1`, **not** `step_8`, and **not** a bypass of the serial Stage 1-6 desk-cognition spine.

- the Stage 1-6 desk-cognition spine remains the only binding serial spine;
- the lane may read approved invariant surfaces directly from session start, limited to: desk cognition grammar order, stage ownership, desk calendar contract, calendar horizon routing outcome, financial-calendar scheduled-fact authority, event identity, raw market facts, and released coefficient authority;
- the lane may read approved stage outputs only after those stages have produced them; later implementation must prove those reads come from lawful stage outputs rather than a hidden bypass;
- the lane may not mutate grammar order, stage ownership, calendar truth, event identity, raw market facts, baseline coefficient values, playbook membership, or review lineage;
- the lane is not the arbiter, not a second playbook engine, and not runtime permission to invent looping semantics;
- future review surfaces must be able to reconstruct the lane's reasoning and state progression across the day without claiming that a runtime packet already exists today.
