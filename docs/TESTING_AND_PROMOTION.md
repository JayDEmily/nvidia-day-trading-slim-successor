# TESTING AND PROMOTION

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
