# 2026-04-04_GATE197_FINANCIAL_CALENDAR_TYPING_SEAM_RECONCILIATION

Status: Gate 197 complete on `work/gate-197-financial-calendar-typing-seam-reconciliation-20260404`; Gate 198 is the next active gate in the Phase 3 main-target repair programme.

## Purpose

Repair the concentrated financial-calendar typing seam by reading the schema constructors and projection consumers first, then clearing only the directly coupled typing/test fallout required by that source-truth decision.

## Source-truth decision

The controlling source surfaces were:
- `src/nvda_desk/schemas/financial_calendar.py`
- `src/nvda_desk/services/financial_calendar_reference.py`
- `src/nvda_desk/services/financial_calendar_import.py`
- `src/nvda_desk/services/financial_calendar_projection.py`
- `src/nvda_desk/services/temporal_context.py`

The concentrated seam was real and code-side:
- the `default_financial_calendar_crosswalk()` constructor family relied on an untyped `common` kwargs dictionary that mypy could not prove safe against `FinancialCalendarCrosswalkRecord`;
- the reference/import/projection seam still exposed untyped function boundaries; and
- adjacent financial-calendar consumers carried small typed-fallout surfaces that needed explicit return typing or precise payload narrowing.

The runtime semantics were already lawful. The failing calendar pytest slice was green before repair, so this gate remained a typing-contract repair rather than a behavioural rewrite.

## Bounded repair applied

- introduced a typed `_FinancialCalendarCrosswalkCommon` helper in `src/nvda_desk/schemas/financial_calendar.py` so the repeated constructor kwargs are lawful under strict mypy
- typed `financial_calendar_crosswalk()` and `FinancialCalendarImportService.build_reference_packet()`
- typed `FinancialCalendarProjectionService.build_live_event_snapshot()` and narrowed the imported payload/test seams with explicit casts where the DMP compatibility view is intentionally generic
- added typed event-context helpers in `src/nvda_desk/services/temporal_context.py` so the calendar-driven temporal surfaces no longer degrade into broad `dict[str, str | int | None]` ambiguity
- tightened the adjacent Gate 89/90/92 tests only where strict typing needed explicit payload narrowing or `None` handling
- did not change the underlying calendar projection/runtime behaviour

## Validation commands

- `PYTHONPATH=/opt/pyvenv/lib/python3.13/site-packages:/home/oai/.cache/uv/archive-v0/kjEjRQLxE1FauZkT7JNEW:/home/oai/.cache/uv/archive-v0/SH68GFG4S1Wlt5XlBXQbN:/home/oai/.cache/uv/archive-v0/O1rBpgTus1i3oF2SBPHDP uvx --offline mypy src/nvda_desk/schemas/financial_calendar.py src/nvda_desk/services/financial_calendar_projection.py tests/test_gate89_financial_calendar_crosswalk_and_dmp_lane.py tests/test_gate90_financial_calendar_reference_import.py tests/test_gate91_financial_calendar_canonical_projection.py tests/test_gate92_financial_calendar_temporal_transition.py`
- `PYTHONPATH=src:/opt/pyvenv/lib/python3.13/site-packages:/home/oai/.cache/uv/archive-v0/kjEjRQLxE1FauZkT7JNEW:/home/oai/.cache/uv/archive-v0/SH68GFG4S1Wlt5XlBXQbN:/home/oai/.cache/uv/archive-v0/O1rBpgTus1i3oF2SBPHDP pytest -q tests/test_gate89_financial_calendar_crosswalk_and_dmp_lane.py tests/test_gate90_financial_calendar_reference_import.py tests/test_gate91_financial_calendar_canonical_projection.py tests/test_gate92_financial_calendar_temporal_transition.py tests/test_financial_calendar_planning_v3.py`

## Validation result

- targeted Gate 197 mypy slice passed: `Success: no issues found in 6 source files`
- targeted Gate 197 calendar pytest slice passed: `22 passed in 1.92s`

## What Gate 197 does not claim

- It does not reopen runtime-semantic repair from Gate 196.
- It does not start the broader helper-typing tranche from Gate 198.
- It does not claim global static closure; it closes only the concentrated financial-calendar typing seam.
