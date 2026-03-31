# TESTING AND PROMOTION

## Purpose

This file defines the binding testing doctrine for the repo and the promotion evidence expected when a runtime surface advances in maturity.

The testing doctrine is not a vanity-coverage programme. This repo is a deterministic desk-runtime system with explicit stage order, typed packets, bounded modifiers, and review lineage. The dangerous bugs are therefore usually not isolated helper bugs. They are boundary bugs, precedence bugs, packet-drift bugs, temporal-transition bugs, and lawful-output bugs where the repo produces a result that is internally consistent but normatively wrong.

## Testing doctrine

### 1. Bug-surface rule

Testing must follow the repo's actual bug surface.

That means the highest testing priority is:
- full-path deterministic scenario regression;
- invariant checks over posture, veto, deployable-capital, and lineage law;
- boundary checks over packet conversion and stage handoff;
- threshold and precedence checks where bounded policy is deformed by state;
- transition checks across adjacent snapshots and event windows.

Line coverage, branch coverage, and isolated unit counts are secondary diagnostics. They are not completion gates on their own.

### 2. Determinism rule

A test surface is preferred when the same inputs, coefficients, state packets, and fixtures produce the same outputs repeatedly.

For this repo, deterministic fixture packs, typed packets, and stable sequence windows are first-class testing assets.

### 3. Real-data rule

When a test claims to exercise the real-data path, it must use an admitted, timestamped, provenance-preserving bundle or prepared-runtime fixture pack.

A planning workbook, synthetic expansion sheet, or scenario-control spreadsheet is not by itself a real-data runtime bundle.

### 4. Entry-point discipline

The repo uses a `src/` layout and a repo-local `.venv` as the intended execution surface.

Required discipline:
- install the package into the repo environment before broad test execution;
- prefer `make install`, `make test`, `make check`, and targeted `make` or `pytest` commands executed through `.venv/bin/python`;
- do not treat a naked root-level `pytest` invocation on an uninstalled environment as authoritative proof about product correctness.

### 5. Sequential testing-module rule

Testing work follows the same sequential discipline as product gates.

Rules:
- testing work starts from a dedicated work branch;
- each testing phase closes with explicit pass/fail evidence before the next phase begins;
- no later testing phase is treated as complete because scaffolding exists;
- if Phase 0 fails, later phases that depend on true real-data ingress are blocked until the missing raw capture is supplied.

## Ordered testing phases

### Phase 0 — one canonical real-data snapshot viability audit

Purpose:
- decide whether the current checked-in signal workbook and related real-data artefacts can support one lawful deterministic run without invented raw inputs.

Phase 0 must:
- inspect the workbook authority layers and separate raw from derived surfaces;
- identify the actual raw signals required by the checked-in real-data runtime path;
- verify timestamp and session anchoring;
- identify missing raw signals explicitly;
- identify missing derived signals explicitly;
- calculate only those derived signals that are mechanically derivable from present raw truth;
- fail cleanly if required raw truth is absent.

Phase 0 closes only when one of these verdicts is recorded:
- `pass`
- `pass_with_controlled_derived_build`
- `fail_missing_raw_truth`

### Phase 1 — deterministic full-runtime scenario harness from one canonical real-data snapshot

Purpose:
- prove one complete start-to-finish runtime path using a single admitted real-data snapshot path.

Phase 1 must:
- use one canonical real-data or prepared-runtime input set;
- run the cognition grammar in order;
- assert the key runtime outputs and review lineage;
- freeze the scenario as a deterministic regression surface.

Do not broaden to many scenarios before one lawful single-run harness is stable.

### Phase 2 — invariant and lawful-output testing

Purpose:
- test the laws of the runtime, not just one hand-picked example.

Phase 2 must add assertions such as:
- hard veto implies no fresh deployable capital;
- blocked permission implies no eligible execution path;
- review lineage preserves stage order;
- modifier lineage remains visible where effective coefficients change;
- event-live or stand-down states cannot leak into permissive execution silently.

### Phase 3 — targeted property and threshold-edge testing

Purpose:
- attack threshold, clamping, coercion, and precedence edges where example-based tests are thin.

Phase 3 is targeted, not repo-wide.

Priority surfaces:
- state-conditioned modifiers;
- temporal/event-window semantics;
- event ingestion and event-store boundaries;
- playbook-eligibility threshold edges;
- typed ingress surfaces where coercion versus strictness matters.

### Phase 4 — transition and adjacent-snapshot testing

Purpose:
- catch bugs that only appear when the system moves from one state to the next.

Priority transitions:
- imminent event -> live event -> cooling window;
- orderly session -> late-session carry horizon;
- repeated options snapshots across pinning or pressure transitions;
- changes that should de-risk, then veto, without illegal sideways behaviour.

### Phase 5 — controlled scenario-matrix expansion

Purpose:
- broaden deterministic coverage after the single-run harness and invariant layers are already trustworthy.

The first expansion set should stay bounded. Add scenarios only when they represent materially different desk states.

### Phase 6 — bounded sibling trace review from one admitted real-data anchor

Purpose:
- run one human-readable logic review over a small sibling pack anchored to one admitted prepared-runtime snapshot.

Requirements:
- anchor one admitted prepared-runtime snapshot explicitly;
- perturb only coherent field clusters, not random isolated numbers;
- keep the sibling set bounded to 4-6 sibling scenarios;
- mark the sibling pack as semantic review evidence only, not runtime authority or tuning truth.

Success criteria:
- every sibling scenario has explicit perturbation receipts and rationale;
- the runtime trace outputs remain bounded, deterministic, and human-readable;
- the simplified report says whether the runtime acted normal, derisked, or blocked without exploding.

## What not to do

Do not:
- chase a coverage percentage as the primary truth metric;
- fabricate missing raw inputs just to get a green end-to-end test;
- keep Phase 0 failures honest: do not fabricate missing raw inputs once they are proven absent;
- blur raw signals and derived signals into one mixed authority layer;
- let synthetic spreadsheet surfaces masquerade as admitted runtime truth;
- add property-based testing indiscriminately across the repo;
- treat a bare scaffold test as completion of a testing phase;
- hide entry-point problems under "works on my machine" reasoning;
- broaden to a large scenario matrix before one canonical real-data path is stable.

## Test classes

### Unit
Fast contract and service checks.

Targets:
- `make test-unit`

### Repository validation
Repo-wide checks for lint, typing, and tests.

Targets:
- `make check`
- `make alembic-sql`

### Leaf-specific validation
Targeted pytest commands and file validations defined in the active leaf ledger.

### Testing-module phase validation
Targeted proofs for Phase 0 through Phase 6 closeout.

Examples:
- workbook viability audit output exists and matches the repo's current ingress requirements;
- canonical real-data harness emits stable outputs for the admitted snapshot;
- invariant tests close lawful-output gaps without widening scope prematurely.

## Core repo gate

Use:

```bash
make check
```

That means:
- lint
- typecheck
- tests

## Leaf execution rule

A leaf is complete only when:
- scoped implementation or documentation is complete;
- leaf-specific tests or validations exist;
- relevant targeted tests or validations pass;
- full-suite runs pass when the blast radius requires them.

A downstream gate is not marked complete on scaffold existence alone.
A downstream gate is not marked complete until its hard acceptance criteria in the canonical execution plan and the canonical leaf ledger are satisfied.

## Documentation and control-surface changes

Documentation-only changes still need proof when they alter authority, sequencing, closeout state, or testing doctrine. At minimum:
- run the targeted documentation or planning tests affected by the change;
- update the active planning quartet together when gate status changes;
- record the change in `CHANGELOG.jsonl` and the execution log if it changes gate truth rather than commentary only.

## Promotion state machine

The canonical promotion states are defined by `src/nvda_desk/schemas/module.py`:

```text
planned
  -> draft
  -> coded
  -> backtested
  -> paper_candidate
  -> approved
  -> retired
```

Revision, pause, or rollback decisions may happen operationally, but they are not separate canonical schema states in the current repo.

## Required promotion evidence

### `coded`
- contract-valid module spec exists;
- deterministic implementation exists;
- docstrings are present.

### `backtested`
- replay or backtest run exists;
- evaluation artefact persisted;
- rationale for pass, fail, or revise recorded.

### `paper_candidate`
- deterministic runtime path proven;
- broker stub or paper path exercised;
- ledger writes verified;
- review packets reconstruct decision flow.

### `approved`
- human approval recorded;
- risk policy attached;
- rollback path understood.

## Retirement triggers

A module is retired when:
- replay degrades materially;
- execution quality destroys signal edge;
- it becomes redundant in the active stack;
- it repeatedly fails updated risk criteria;
- its assumptions are no longer valid.
