# 2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_AUDIT_PROOF_SLICE_AND_SUCCESSOR_HANDOFF_v1

Status: Gate 221 proof-order and successor-handoff surface for the slim active-repo cutover and substantive test-audit bootstrap pack on `work/gate-221-successor-proof-slice-and-handoff-20260406`.

## Purpose

Freeze the bounded proof order for the first successor execution pack after this bootstrap closes, and define the exact handoff boundary without claiming that the next pack has already started.

## Ordered proof slice for the first successor execution pack after bootstrap closeout

1. Handoff and router preflight before any retained-test mutation:
   - `pytest -q tests/test_gate221_successor_test_audit_handoff.py tests/test_planning_state_integrity.py`
2. Execute exactly one grouped execution family from the queued Gate 220 decision register.
3. Run only the targeted successor-repo tests that govern the chosen execution family and the touched control surfaces.
4. Re-run `pytest -q tests/test_gate221_successor_test_audit_handoff.py tests/test_planning_state_integrity.py` after the family-specific mutations land.
5. Stop and close the execution pack without widening to broad blind execution unless the chosen family proves that the blast radius escaped its bounded queue.

## Broad proof explicitly excluded from the first execution pack

- broad repo-wide `make check` by default;
- full runtime pytest across unrelated modules that the chosen execution family did not touch;
- mypy, ruff, or Alembic proof unless the chosen execution family materially expands into those surfaces;
- executing more than one grouped execution family in the same first post-bootstrap pack;
- any source-repo mutation, rerouting, or evidence-host rewrite.

## Stop conditions that force replanning before or during execution

- the chosen execution family cannot be stated without guessing which Gate 220 decision rows it owns;
- a move, rewrite, or retirement action cannot name its replacement authority, archive destination, or preserved evidence anchor cleanly;
- the adopted `07` ledger and `docs/03_DOMAIN_MODEL.md` disagree materially on a retained runtime surface that the chosen family needs to mutate;
- the first execution pack would need to touch more than one grouped execution family to stay truthful;
- the work would require source-repo mutation or source-repo rerouting;
- the targeted successor-repo proof slice expands into broad blind execution without a concrete blast-radius reason.

## Deterministic next execution-pack boundary

The next pack after this bootstrap is the **first successor retained-test execution pack**.

That pack:
- is successor-repo-only;
- must be created or routed later as a new pack rather than inferred from this bootstrap closeout alone;
- may execute exactly one grouped family from the Gate 220 decision register at a time; and
- must stop before any second grouped family begins.

## Non-source-repo boundary

The next execution pack and every queued family named by Gate 221 must remain inside the successor repo.

This handoff does not:
- reopen or reroute the source/archive repo;
- treat the source repo as the destination for archive-evidence moves; or
- claim that any keep / retire / rewrite / move action has already executed.
