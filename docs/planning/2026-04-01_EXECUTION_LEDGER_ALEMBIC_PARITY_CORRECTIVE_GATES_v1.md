Status: closed execution-ledger Alembic parity corrective pack on `main`; Gate 140 complete, no active gate
# 2026-04-01 Execution Ledger Alembic Parity Corrective Gates v1

## Purpose

Correct one post-closeout drift in the execution-ledger lifecycle work: the ORM and services for Gate 139 now require additive `order_intent` specimen columns plus the `position_instance_snapshot` table, but the Alembic chain still stopped at the pre-Gate-139 schema.

This pack exists to do four things only:
1. freeze the exact corrective scope so the repo does not pretend Gate 139 was fully migration-clean when it was not;
2. add one Alembic revision that restores schema parity for the bounded execution-ledger specimen surfaces;
3. prove parity both structurally and behaviourally on a clean migrated database;
4. close the corrective pack honestly and return the router to no-active-pack state.

## Why this pack exists

A post-flight audit of Gates 135-139 found that clean `alembic upgrade head` on a fresh SQLite database produced an `order_intent` table without the new specimen columns and did not create `position_instance_snapshot` at all. That means the bounded position-instance ledger worked only under `create_schema(...)` / metadata-creation paths, not under the repo's admitted migration path.

This pack is a corrective reset caused by an audit finding under `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md` planning-mode rule 67-72. It is intentionally narrow and does not reopen lifecycle logic, carry semantics, or packet meaning.

## Scope

In scope:
- one corrective planning pack for Gate 140 only;
- Alembic parity for `order_intent` specimen columns and `position_instance_snapshot`;
- one migration revision plus targeted parity tests and receipts;
- router, gate-map, leaves, execution-log, and changelog truth updates required to close the corrective gate honestly.

Out of scope:
- any new lifecycle behaviour;
- any change to packet/data semantics already frozen by the closed lifecycle pilot pack;
- broker-boundary broadening, live OMS semantics, or multi-leg execution work;
- unrelated planning rewrites.

## Supersession and active authority

- This document became the active gate authority for Gate 140 after the post-flight audit found Alembic drift.
- It supersedes the no-active-pack state that existed immediately after Gate 139 closeout.
- It does not reopen the closed lifecycle pilot pack except as evidence of the audited drift.

## Governing inputs

- `docs/01_NORMATIVE.md`
- `docs/03_DOMAIN_MODEL.md`
- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`
- `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/08_TESTING_AND_PROMOTION.md`
- `alembic/versions/20260320_0005_second_wave_records.py`
- `src/nvda_desk/db/models.py`
- `src/nvda_desk/schemas/execution_records.py`
- `src/nvda_desk/services/execution_records.py`
- `tests/test_second_wave_records_and_events.py`
- `tests/test_carry_review_cli_and_legacy.py`

## Active vocabulary authority for execution threads

`docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` remains the vocabulary authority for this corrective pack. No new governed vocabulary is introduced here.

## Active packet / data contract authority for execution threads

`docs/03_DOMAIN_MODEL.md` remains the packet/data contract authority for this corrective pack. This pack restores persistence parity only; it does not change packet meaning.

## Workflow placement

This corrective pack sits downstream of the closed lifecycle pilot. It does not add new stage behaviour. It restores the admitted migration path so the bounded execution-ledger specimen can be instantiated from clean database state without relying on metadata creation shortcuts.

## Retain / retire-from-authority / amend / add matrix

### Retain as canonical
- the closed Gate 135-139 lifecycle pilot contracts and behaviour;
- the bounded specimen terms already admitted for the execution-ledger pilot;
- the existing Alembic revision chain up to `20260320_0005` as the base migration spine.

### Retire from authority
- the assumption that Gate 139's persisted specimen state was migration-clean after closeout.

### Mandatory amendments
- repo-root `PLANS.md`;
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`;
- `CHANGELOG.jsonl`;
- planning guard tests that admit the new corrective gate state;
- Alembic revision history and parity tests.

### New additions
- `docs/planning/2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_GATES_v1.md`
- `docs/planning/2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_LEAVES_v1.json`
- `docs/planning/2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_EXECUTION_LOG_v1.md`
- `docs/planning/2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_DOCUMENT_TOUCH_CHECKLIST_v1.md`
- `alembic/versions/20260401_0006_execution_ledger_position_instance_parity.py`
- `tests/test_gate140_execution_ledger_alembic_parity.py`

## Document-touch checklist

Checklist file: `docs/planning/2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_DOCUMENT_TOUCH_CHECKLIST_v1.md`

## Testing and promotion discipline

- Repo-local environment required: `.venv` created via `uv sync --extra dev`
- Minimum corrective proof slice:
  - `.venv/bin/python -m pytest -q tests/test_gate140_execution_ledger_alembic_parity.py tests/test_second_wave_records_and_events.py tests/test_carry_review_cli_and_legacy.py tests/test_gate135_opening_drive_continuation_lifecycle_planning.py tests/test_gate134_bounded_trace_reporting.py tests/test_gate128_post_flight_repo_consistency_planning.py tests/test_gate122_signal_coefficient_authority_planning.py tests/test_gate115_historical_evaluation_readiness_planning.py tests/test_gate114_research_mode_clarity_microtranche.py tests/test_gate113_execution_authority_microtranche.py tests/test_gate112_governance_closeout.py tests/test_gate111_governance_guardrails.py tests/test_gate110_agents_reading_order.py tests/test_gate109_template_pack_governance.py tests/test_gate108_router_only_control_surface.py tests/test_gate107_repo_process_governance.py tests/test_document_hygiene.py`
- Migration parity proof is not complete until:
  - `alembic upgrade head` succeeds on a clean SQLite database;
  - `alembic upgrade head --sql` renders cleanly;
  - the new parity test proves both the schema and a bounded specimen write/read path on the migrated database.

## Gates

### Gate 140: Restore execution-ledger Alembic parity and close the corrective pack

**Status**
- complete on `main`

**Objective**
- Restore Alembic parity for the bounded Gate 139 execution-ledger specimen surfaces and close the corrective pack honestly.

**In-scope surfaces**
- `alembic/versions/20260401_0006_execution_ledger_position_instance_parity.py`
- `src/nvda_desk/db/models.py`
- `src/nvda_desk/schemas/execution_records.py`
- `src/nvda_desk/services/execution_records.py`
- `tests/test_gate140_execution_ledger_alembic_parity.py`
- `tests/test_second_wave_records_and_events.py`
- `tests/test_carry_review_cli_and_legacy.py`
- repo-root `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/planning/2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_LEAVES_v1.json`
- `docs/planning/2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_EXECUTION_LOG_v1.md`
- `CHANGELOG.jsonl`

**Definition of done**
- clean `alembic upgrade head` produces the `position_instance_snapshot` table and all required `order_intent` specimen columns;
- the new parity test proves a bounded specimen order can be written and then reconstructed through `list_position_instances(...)` on the migrated database;
- the corrective router, gate map, leaves ledger, and execution log all return to no-active-pack truth on the same branch.
