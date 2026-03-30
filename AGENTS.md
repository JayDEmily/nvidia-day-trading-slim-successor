# AGENTS.md

This file governs AI-assisted changes in this repo.

## Role of the repo

This repo builds a market-state warehouse, research cockpit, and deterministic playbook runtime for NVDA day trading.
It does **not** build an autonomous LLM trader.

## Non-negotiable repo rules

1. **Makefile is the single front door.**
2. **Freeze contracts before adding behaviour.**
3. **GPT is upstream of execution.**
4. **Guardrails beat convenience.**
5. **Every meaningful change needs a changelog entry.**
6. **Do not duplicate business logic across delivery surfaces.**
7. **Every runtime-affecting output must remain traceable.**
8. **Broker-specific details stay behind adapter boundaries.**
9. **Direct SQL belongs in the DB and service layers, not random modules.**
10. **Keep research-mode ideation separate from reporting-mode caveats.**

## Frozen documentation order

1. `docs/01_NORMATIVE.md`
2. `docs/02_OPERATING_MODEL.md`
3. `docs/03_DOMAIN_MODEL.md`
4. `docs/04_TECHNICAL_ARCHITECTURE.md`
5. `docs/05_GUARDRAILS.md`
6. `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`

## Agent reading order

1. `docs/01_NORMATIVE.md`
2. `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
3. repo-root `PLANS.md`
4. active gate master under `docs/planning/` only if repo-root `PLANS.md` names one
5. active leaf ledger under `docs/planning/` only if repo-root `PLANS.md` names one
6. active execution log under `docs/planning/` only if repo-root `PLANS.md` names one
7. bounded-scope note under `docs/planning/` only if repo-root `PLANS.md` names one
8. the active vocabulary authority named by the active gate master, or `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` when no active pack exists yet
9. the active packet/data contract authority named by the active gate master, or `docs/03_DOMAIN_MODEL.md` when no active pack exists yet
10. `CHANGELOG.jsonl` tail if historical context is needed
11. `README.md` for human onboarding context only

## Research mode versus reporting mode

- In research or brainstorm mode, seek asymmetry, dislocation, candidate edge, and hidden causal structure first.
- Do not contaminate ideation with implementation-readiness or live-operability caveats unless the user asks for readiness, promotion, or current-state judgment.
- In reporting mode, describe current repo truth exactly and keep caveats there.
- Do not let reporting caution dull later ideation.

## Behaviour authority versus work authority

- `AGENTS.md` governs **agent behaviour in the repo**.
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md` governs **how planning packs are created, amended, routed, and closed**.
- repo-root `PLANS.md` plus the active planning control surfaces govern **what work is active now**.
- Completed predecessor packs may remain under `docs/planning/` as evidentiary receipts, but they are not active authority unless repo-root `PLANS.md` says so.

## Required checks before closing a change

At minimum, run the relevant targets from:
- `make check`
- `make alembic-sql`
- `make test-unit`

## Anti-drift closeout protocol

Before calling any gate closed or starting the next gate, update these four authority surfaces together on the same branch:
1. repo-root `PLANS.md`
2. `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
3. the active leaf ledger for the active pack
4. the active execution log named by repo-root `PLANS.md`

A gate is not closed if any one of those still points at the older active gate or older completed tranche.

When a closeout is reconstructed after the fact, mark it explicitly as a receipt-recovery / anti-drift repair rather than pretending it was logged in real time.

## Documentation precedence

Follow `docs/01_NORMATIVE.md` for final precedence rules.
