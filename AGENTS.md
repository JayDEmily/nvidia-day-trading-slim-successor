# AGENTS.md

This file governs AI-assisted changes in this repo.

## Role of the repo

This repo builds a market-state warehouse, research cockpit, and deterministic playbook runtime for NVDA day trading.
It does **not** build an autonomous LLM trader.

## Authority order

1. `docs/01_NORMATIVE.md`
2. `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
3. repo-root `PLANS.md`
4. the active gates master named by repo-root `PLANS.md`, if one exists
5. the active leaf ledger named by repo-root `PLANS.md`, if one exists
6. the active execution log named by repo-root `PLANS.md`, if one exists
7. the bounded-scope note named by repo-root `PLANS.md`, if one exists
8. the active vocabulary authority named by the active gate master, or `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` when no active pack exists yet
9. the active packet/data contract authority named by the active gate master, or `docs/03_DOMAIN_MODEL.md` when no active pack exists yet
10. `CHANGELOG.jsonl` tail if historical context is needed
11. `README.md` for human onboarding context only

## Behaviour expectations

- Separate planning from execution. Planning defines bounded work; execution acts only on the approved active gate.
- Separate research-mode ideation from reporting-mode truth. Do not let reporting caveats contaminate ideation unless the operator asks for current-state or readiness judgment.
- Prefer bounded, gate-local proof over broad blind execution unless the active gate expands the blast radius.
- Do not guess missing authority, workflow rules, or repo state. Read the routed control surfaces instead of relying on chat memory.
- `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` is a specialised runtime authority ledger, not a universal front-door doctrine file.
- Read `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` whenever work touches runtime surface ownership, stage packet versus workflow packet authority, compatibility surface or compatibility carriage law, downstream runtime reader permissions, replay or bounded-trace or review seam interpretation, or API compatibility wrappers that preserve older read shapes over newer canonical runtime truth.
- Add a changelog entry when repo policy or explicit gate or user instructions require one.

## Anti-drift behaviour

- Do not treat a gate as closed until repo-root `PLANS.md`, the canonical gate map, the active leaf ledger, and the active execution log move together on the same branch.
- When a closeout is reconstructed after the fact, say so explicitly instead of presenting it as a real-time receipt.
- `AGENTS.md` is behavioural authority only. Detailed workflow and tranche law lives in `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`.
