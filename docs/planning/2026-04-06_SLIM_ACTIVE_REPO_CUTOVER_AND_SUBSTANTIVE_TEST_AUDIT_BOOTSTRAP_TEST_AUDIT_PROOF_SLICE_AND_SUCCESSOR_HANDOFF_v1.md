# 2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_AUDIT_PROOF_SLICE_AND_SUCCESSOR_HANDOFF_v1

## Purpose

Freeze the bounded proof order for the successor bootstrap pack and define the next execution-pack boundary after the first substantive test audit is classified.

## Ordered proof slice for this bootstrap pack

1. Successor-pack bootstrap coherence:
   - `pytest -q tests/test_gate217_slim_successor_pack_planning.py`
2. Retained-surface inventory and specialised runtime-authority adoption:
   - `pytest -q tests/test_gate218_retained_surface_inventory_and_runtime_authority.py`
3. Retained-test inventory and ownership mapping:
   - `pytest -q tests/test_gate219_test_inventory_classification.py`
4. Decision register and disagreement-memory law:
   - `pytest -q tests/test_gate220_test_audit_decision_register.py`
5. Successor handoff and proof-order coherence:
   - `pytest -q tests/test_gate221_successor_test_audit_handoff.py`

## What this proof slice deliberately excludes

- broad repo-wide `make check` unless a gate expands into runtime/shared code;
- full runtime pytest across unrelated modules;
- mypy, ruff, or Alembic proof unless a gate explicitly moves those surfaces;
- test rewrites, deletions, or moves before Gate 220 decision outcomes are frozen.

## Stop conditions that force replanning

- the retained test inventory cannot be stated without guessing which surfaces moved in the cutover;
- a decision outcome cannot name its authoritative inputs cleanly;
- the adopted `07` ledger and `docs/03_DOMAIN_MODEL.md` disagree materially on a retained runtime surface;
- a proposed next execution pack would require runtime change inside this bootstrap pack.

## Successor handoff rule

This bootstrap pack closes only when:
- the retained-surface manifest is frozen;
- the adopted `07` ledger is in place;
- the retained test inventory and first-pass decision register exist;
- the proof slice above is green; and
- the next successor execution pack boundary is explicit.

## Expected next execution pack after this bootstrap

The next pack should execute only the first bounded set of audit decisions that satisfy all of the following:
- they are already classified in the Gate 220 decision register;
- they do not require unplanned runtime or contract changes;
- they can be proved with targeted successor-repo tests;
- they do not reopen the source repo's routing or historical closeout surfaces.
