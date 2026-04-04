# 2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_SCOPE_NOTE_v1

Status: active bounded-scope note for the Phase 3 main-target repair programme on `work/gate-192-phase3-main-target-repair-pack-20260404`

## Purpose

Carry the truthful scope split for the Phase 3 main-target repair programme and freeze the execution boundaries that stop runtime semantics, governance truth, vocabulary repair, and static cleanup from bleeding into one another.

## Verified evidence inputs

- target repo closed through Gate 191 on `main`
- external Phase 2B handoff reports establishing the executed defect harvest and repair-prep bridge
- no active pack routed inside the target repo at tranche start
- H v2 repair-prep bridge establishing seven default repair tranches

## Main-target defect-family baseline carried into this pack

1. vocabulary generator drift
2. repo-wide vocabulary hygiene leakage
3. control-surface router and gate-map drift
4. options-flow harness expectation drift
5. higher-order context stress-behaviour drift
6. import-structure and formatting debt
7. financial-calendar typing seam
8. untyped helper pressure in strict test contexts
9. Alembic warning-only suspicious pass

## Explicitly included in execution scope

- repairing the seven Phase 3 tranche families already normalised by H v2
- re-checking only the proofs required to close each bounded family honestly
- keeping vocabulary, governance, runtime, and static families separate unless new evidence proves they are tightly coupled
- updating repo-native planning/router surfaces as each gate closes
- using the inspected source surfaces as the repair boundary for each family, with tests treated as evidence rather than authority:
  - Gate 193: `scripts/build_canonical_vocabulary.py`, `src/nvda_desk/schemas/vocabulary.py`, `src/nvda_desk/services/playbook_registry.py`, and the committed vocabulary artifact
  - Gate 194: the lane/workbook entries in the generator and committed artifact plus `src/nvda_desk/schemas/cognition.py`, `src/nvda_desk/services/capital_deployment_authority.py`, `src/nvda_desk/services/cognition_runtime.py`, and `src/nvda_desk/services/review_explanation.py`
  - Gate 195: repo-root `PLANS.md`, the canonical gate map, `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`, and the exact late-pack closeout/control docs implicated by the executed drift
  - Gate 196: `src/nvda_desk/services/options_flow_context.py`, `src/nvda_desk/schemas/cognition.py`, `src/nvda_desk/services/playbook_eligibility.py`, and `src/nvda_desk/services/imported_modules/posture_enrichers.py`
  - Gate 197: `src/nvda_desk/schemas/financial_calendar.py` plus `src/nvda_desk/services/financial_calendar_projection.py`
  - Gate 198: `tests/contract_chain_fixtures.py`, `tests/_successor_pack_helpers.py`, and any directly coupled helper modules proven necessary during execution
  - Gate 199: `alembic/env.py`, `alembic.ini`, the specific Alembic/migration files named by lint output, repo-root-path test imports, and `src/nvda_desk/config_models.py`

## Explicitly excluded from this tranche

- new architecture expansion or stage admission
- coefficient redesign or tuning work
- side-repo B/C packaging blockers from the external handoff unless later proven to block a main-target repair gate
- opportunistic UI/reporting redesign
- broad refactors with no evidence linkage to the harvested defect families

## Default repair order carried into this pack

1. vocabulary generator reconciliation
2. vocabulary hygiene leakage reconciliation
3. control-surface router and gate-map reconciliation
4. runtime semantic drift reconciliation
5. financial-calendar typing seam reconciliation
6. typed helper pressure reduction
7. static hygiene and Alembic warning cleanup

## Non-goals that must remain non-goals in code review

- Do not mix runtime-semantic repair with broad static cleanup in the same gate.
- Do not let vocabulary or router truth drift be “fixed” implicitly by editing downstream tests only.
- Do not treat warning-only constraints as hard runtime failures.
- Do not relabel rediscovery as repair.

## Source-truth rule

Before any repair leaf changes a downstream test expectation, that leaf must name the governing source modules/contracts/docs and state whether the test is trusted, stale, or mixed evidence.
