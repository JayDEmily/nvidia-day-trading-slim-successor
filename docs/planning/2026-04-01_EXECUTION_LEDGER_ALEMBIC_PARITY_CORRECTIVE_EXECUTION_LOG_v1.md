# 2026-04-01_EXECUTION_LEDGER_ALEMBIC_PARITY_CORRECTIVE_EXECUTION_LOG_v1

Status: closed execution log for the execution-ledger Alembic parity corrective pack; Gate 140 complete on `main`, no active gate

## Scope

This log records the audit-driven corrective gate that restored Alembic parity for the bounded Gate 139 execution-ledger specimen surfaces.

## Receipt: Gate 140

- Branch: `work/gate-140-execution-ledger-alembic-parity-20260401`
- Start state audited from `main` at commit `6512960`
- Drift found before execution: clean Alembic head lacked `position_instance_snapshot` and nine specimen columns on `order_intent`
- Implementation surfaces:
  - `alembic/versions/20260401_0006_execution_ledger_position_instance_parity.py`
  - `tests/test_gate140_execution_ledger_alembic_parity.py`
  - router / gate-map / corrective-pack docs / guard tests
- Validation receipts:
  - `.venv/bin/python -m pytest -q tests/test_gate140_execution_ledger_alembic_parity.py tests/test_second_wave_records_and_events.py tests/test_carry_review_cli_and_legacy.py tests/test_gate135_opening_drive_continuation_lifecycle_planning.py tests/test_gate134_bounded_trace_reporting.py tests/test_gate128_post_flight_repo_consistency_planning.py tests/test_gate122_signal_coefficient_authority_planning.py tests/test_gate115_historical_evaluation_readiness_planning.py tests/test_gate114_research_mode_clarity_microtranche.py tests/test_gate113_execution_authority_microtranche.py tests/test_gate112_governance_closeout.py tests/test_gate111_governance_guardrails.py tests/test_gate110_agents_reading_order.py tests/test_gate109_template_pack_governance.py tests/test_gate108_router_only_control_surface.py tests/test_gate107_repo_process_governance.py tests/test_document_hygiene.py` -> 37 passed in 6.49s
  - `NVDA_DESK_DATABASE_URL=sqlite+pysqlite:////tmp/nvda_gate140_upgrade.db .venv/bin/python -m alembic upgrade head` -> passed
  - `NVDA_DESK_DATABASE_URL=sqlite+pysqlite:////tmp/nvda_gate140_upgrade_sql.db .venv/bin/python -m alembic upgrade head --sql` -> passed; offline SQL rendered to /tmp/nvda_gate140_offline.sql (465 lines)
- Closeout requirement: `PLANS.md`, canonical gate map, corrective leaves ledger, and this execution log must move together on the same branch.
