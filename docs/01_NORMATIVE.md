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
8. `docs/TESTING_AND_PROMOTION.md`
9. repo-root `PLANS.md`
10. dated execution plans under `docs/planning/`
11. `AGENTS.md`
12. `README.md`
13. `docs/status/*`
14. `docs/legacy/*`

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

## Desk Cognition Grammar (binding runtime order)

The deterministic runtime follows this order:

1. temporal context
2. market regime context
3. options and flow context
4. posture and risk permission
5. playbook eligibility
6. expression and execution
7. review and explanation

No module bypasses this order.

## Adaptation law

The repo preserves a stable cognition grammar and only allows bounded, approved change in operating posture. That means:

- historical replay is the research and discovery surface;
- live paper is the falsification and promotion surface for locked candidates;
- review does not imply change, and **no change** is a valid governed outcome;
- runtime never invents new coefficients or hidden policy in place;
- baseline coefficient changes happen only through reviewed release, never through runtime self-adjustment.

## Canonical terminology

- **module**: deterministic runtime component with a clear contract.
- **feature**: reusable input, derived value, or bounded signal consumed by one or more modules.
- **classifier**: deterministic component that labels or scores state without directly allocating capital.
- **overlay**: deterministic component that reshapes, caps, vetoes, or annotates downstream behaviour.
- **playbook**: named trading behaviour that becomes eligible only after posture and permission are known.
- **gate**: binding milestone or runtime veto surface that cannot be skipped.
- **review packet**: structured explanation artefact that reconstructs how the runtime reached a decision.
- **concept-contract**: preserved non-runtime idea expressed in typed form until dependencies are ready.

## Package-organisation rules

- `src/nvda_desk/schemas/` contains strict contracts only.
- `src/nvda_desk/services/` contains deterministic business logic only.
- `src/nvda_desk/domain/` contains stable domain primitives only.
- `src/nvda_desk/api/` remains thin and delegates to services.
- planning artefacts live under `docs/planning/`.
- preserved historical evidence remains outside active runtime packages unless imported through a typed contract.

## Docstring rules

Every new or refactored Python module includes a top-level module docstring.
Every public class and public function includes a docstring that states:

- purpose;
- required inputs;
- produced outputs;
- deterministic assumptions where relevant.

No touched Python file is merged without clear docstrings.

## Contract rules

Every imported runtime module defines or reuses a typed input contract and a typed output contract.
Every runtime output that affects posture, risk, playbook eligibility, execution, or review is traceable in a review packet.
No runtime module depends on implicit hidden state.
For enum-like vocabularies that exist in `src/nvda_desk/schemas/`, the schema values are authoritative over prose mirrors.

## What varies via config

These items vary via config without altering the architecture:

- risk thresholds;
- instrument subsets;
- bounded option-strip windows;
- module coefficients and parameters;
- no-trade windows;
- runtime feature toggles;
- OpenAI model choice within the supported API surface.

## Normative versus historical docs

- Files in `docs/` with stable names are normative unless they explicitly mark themselves as archived or historical context.
- Files in `docs/planning/` are active execution artefacts under repo-root `PLANS.md`.
- Files in `docs/status/` are dated implementation notes.
- Files in `docs/legacy/` are historical design artefacts kept for provenance.

## Naming rules

- Stable operational docs use stable names.
- Historical milestone notes use dated names.
- Changelog entries use UTC ISO time plus Unix milliseconds.
- Canonical import registries, grammar mappings, and leaf ledgers use dated filenames under `docs/planning/`.
