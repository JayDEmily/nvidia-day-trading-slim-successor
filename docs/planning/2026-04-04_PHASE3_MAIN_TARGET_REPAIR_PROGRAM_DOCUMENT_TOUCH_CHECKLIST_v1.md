# 2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_DOCUMENT_TOUCH_CHECKLIST_v1

Status: active document-touch checklist for the Phase 3 main-target repair programme; Gate 192 complete on `work/gate-192-phase3-main-target-repair-pack-20260404`, Gate 193 active

## Frozen/process surfaces that must move if this pack changes them

- `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- `AGENTS.md`

## Live routing and planning surfaces that must move before closeout

- `PLANS.md`
- `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_GATES_v1.md`
- `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_LEAVES_v1.json`
- `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_EXECUTION_LOG_v1.md`
- `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_SCOPE_NOTE_v1.md`
- `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_EVIDENCE_BASELINE_v1.md`
- `docs/planning/2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_SOURCE_TRUTH_MATRIX_v1.md`

## Authority surfaces likely to move in later gates

- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/03_DOMAIN_MODEL.md` if runtime-semantic repair requires explicit contract clarification
- `docs/04_TECHNICAL_ARCHITECTURE.md` if control-surface repair requires architecture wording to converge on the implemented truth
- any closeout receipt or gate receipt added during Gates 192-199

## Runtime/schema/test surfaces likely to move in later gates

- vocabulary generator surfaces, vocabulary schema/registry surfaces, and dependent vocabulary-governance tests
- `PLANS.md`, the canonical gate map, repo process law, and gate-map-adjacent planning/control tests
- options-flow clustering semantics, typed cognition output surfaces, adjacent runtime consumers, and harness evidence
- higher-order context detector semantics and related tests
- `src/nvda_desk/schemas/financial_calendar.py` plus adjacent financial-calendar services/tests
- helper definitions and return-shape surfaces used across strict test contexts
- Alembic configuration, Alembic env/migration files, and remaining static-quality surfaces

## Explicit exclusions preserved by this checklist

- side-repo B/C blocker repair is excluded from first-line main-target Phase 3 work
- new stage/module expansion is excluded
- coefficient/tuning redesign is excluded
- UI/reporting redesign is excluded unless a later gate proves it is necessary to close one of the admitted repair families

## Current planned sequence

- Gate 192 — Phase 3 repair pack bootstrap and evidence bridge
- Gate 193 — Vocabulary generator and artifact truth reconciliation
- Gate 194 — Repo-wide vocabulary hygiene leakage reconciliation
- Gate 195 — Control-surface router and gate-map reconciliation
- Gate 196 — Runtime semantic drift reconciliation
- Gate 197 — Financial-calendar typing seam reconciliation
- Gate 198 — Typed helper pressure reduction
- Gate 199 — Static hygiene, Alembic warning cleanup, and Phase 3 closeout


## Exact inspected surfaces that informed leaf tightening

- Gate 193: `scripts/build_canonical_vocabulary.py`; `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`; vocabulary-governance tests in the `50-89` range.
- Gate 194: `scripts/build_canonical_vocabulary.py`; `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`; `src/nvda_desk/schemas/cognition.py`; `src/nvda_desk/services/capital_deployment_authority.py`; `src/nvda_desk/services/cognition_runtime.py`; `src/nvda_desk/services/review_explanation.py`; evidence tests `tests/test_gate179_repo_wide_vocabulary_hygiene.py` and `tests/test_gate190_capital_deployment_authority_integration.py`.
- Gate 195: repo-root `PLANS.md`; `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`; `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`; the late-pack planning/control docs for gates `149-156`, `163-165`, `170-172`, `180`, and `181`.
- Gate 196: `src/nvda_desk/services/options_flow_context.py`; `src/nvda_desk/schemas/cognition.py`; `src/nvda_desk/services/playbook_eligibility.py`; `src/nvda_desk/services/imported_modules/posture_enrichers.py`; evidence tests `tests/test_gate31_higher_order_context_composites.py`, `tests/test_gate96_canonical_runtime_harness.py`, `tests/test_gate102_raw_runtime_harness.py`, `tests/test_real_data_loader.py`, and `tests/test_options_flow_context.py`.
- Gate 197: `src/nvda_desk/schemas/financial_calendar.py`; `src/nvda_desk/services/financial_calendar_projection.py`; tests `89-92` plus `tests/test_financial_calendar_planning_v3.py`.
- Gate 198: `tests/contract_chain_fixtures.py`; `tests/_successor_pack_helpers.py`; evidence tests `tests/test_gate97_runtime_invariants.py`, `tests/test_gate103_raw_prepared_parity.py`, and `tests/test_gate104_property_stateful.py`; helper modules/fixtures proven necessary during execution.
- Gate 199: `alembic/env.py`; exact Alembic environment/migration files named by lint output; `alembic.ini`; repo-root path insertion test files; `src/nvda_desk/config_models.py`.
