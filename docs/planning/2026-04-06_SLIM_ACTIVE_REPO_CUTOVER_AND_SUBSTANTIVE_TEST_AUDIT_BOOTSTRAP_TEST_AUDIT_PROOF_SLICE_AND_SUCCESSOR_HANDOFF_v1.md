# 2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_AUDIT_PROOF_SLICE_AND_SUCCESSOR_HANDOFF_v1

Status: closed-pack proof-order, successor execution-queue, and handoff surface for the slim active-repo cutover and substantive test-audit bootstrap pack through Gate 221 on `work/gate-221-successor-proof-slice-and-handoff-20260406`.

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

## Grouped successor execution-pack queue from the Gate 220 decision register

### 1. Archive-evidence move family

This family is queued for a later successor execution pack and must remain outside the source repo.

- decision ids:
  - `planning_governance__closed_source_or_historical_pack_receipts`
  - `review_or_trace__historical_planning_review_receipts`
  - `migration_or_closeout_guard__historical_closeout_receipts`
- execution boundary:
  - move only to the dedicated archive-evidence destination named by the later execution pack;
  - preserve evidence anchors and disagreement memory; and
  - do not treat the source/archive repo as the move target.

### 2. Successor-boundary rewrite family

- decision ids:
  - `migration_or_closeout_guard__successor_cutover_boundary_rule`
- execution boundary:
  - rewrite only the retained successor-local assertion surface named by Gate 220;
  - preserve the rejected source-era interpretation in the decision register memory; and
  - do not execute the rewrite unless the later pack can prove successor-local authority inputs explicitly.

### 3. Duplicate-retirement family

- decision ids:
  - `replay_regression__research_shadow_replays`
- execution boundary:
  - retire only after the canonical retained replay guards remain green in the successor repo; and
  - preserve the rejected interpretation that argued for keeping the research shadow rows.

### 4. Retained keep and retarget family

This family is the retained successor queue and may be executed only after a later pack decides which bounded subset to touch first.

- `keep_as_is` decision ids:
  - `control_surface_integrity__successor_router_quartet`
  - `data_path_or_fixture__retained_reference_and_loader_surfaces`
  - `planning_governance__live_successor_process_controls`
  - `repo_hygiene__retained_repo_boundary_surfaces`
  - `runtime_scenario__retained_runtime_paths`
- `keep_but_retarget_authority` decision ids:
  - `compatibility_wrapper__preserved_reader_shapes`
  - `invariant_or_lawful_output__repo_native_law_and_ownership`
  - `replay_regression__canonical_replay_compare_guards`
  - `review_or_trace__runtime_review_and_trace_surfaces`
  - `runtime_contract__current_packet_and_service_contracts`
- execution boundary:
  - any later pack must choose one bounded subset of these retained rows, not the whole retained family queue at once;
  - retargeted rows must prove the adopted successor authority inputs before any test rewrite lands; and
  - keep-as-is rows still require targeted successor proof when they are materially touched.

## Non-source-repo boundary

The next execution pack and every queued family named by Gate 221 must remain inside the successor repo.

This handoff does not:
- reopen or reroute the source/archive repo;
- treat the source repo as the destination for archive-evidence moves; or
- claim that any keep / retire / rewrite / move action has already executed.

## Router-closeout result

This bootstrap pack closes through Gate 221 with **no active pack currently routed**.

A later thread must create or route the appropriate new successor execution pack before any queued family above may execute.
