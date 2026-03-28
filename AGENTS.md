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

## Frozen documentation order

1. `docs/01_NORMATIVE.md`
2. `docs/02_OPERATING_MODEL.md`
3. `docs/03_DOMAIN_MODEL.md`
4. `docs/04_TECHNICAL_ARCHITECTURE.md`
5. `docs/05_GUARDRAILS.md`

## Agent reading order

1. `docs/01_NORMATIVE.md`
2. repo-root `PLANS.md`
3. active gate master under `docs/planning/`
4. active leaf ledger under `docs/planning/`
5. active execution log under `docs/planning/`
6. bounded-scope note under `docs/planning/` only if repo-root `PLANS.md` names one
7. `CHANGELOG.jsonl` tail if historical context is needed
8. `README.md` for human onboarding context only

## Behaviour authority versus work authority

- `AGENTS.md` governs **agent behaviour in the repo**.
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
