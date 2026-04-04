# 2026-04-04_PHASE3_MAIN_TARGET_REPAIR_PROGRAM_DOCUMENT_TOUCH_CHECKLIST_v1

Status: active document-touch checklist for the Phase 3 main-target repair programme on `work/gate-192-phase3-main-target-repair-pack-20260404`

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

## Authority surfaces likely to move in later gates

- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json`
- `docs/03_DOMAIN_MODEL.md` if runtime-semantic repair requires explicit contract clarification
- `docs/04_TECHNICAL_ARCHITECTURE.md` if control-surface repair requires architecture wording to converge on the implemented truth
- any closeout receipt or gate receipt added during Gates 192-199

## Runtime/schema/test surfaces likely to move in later gates

- vocabulary generator surfaces and dependent vocabulary-governance tests
- `PLANS.md` and gate-map-adjacent planning/control tests
- options-flow clustering semantics and harness expectation surfaces
- higher-order context detector semantics and related tests
- `src/nvda_desk/schemas/financial_calendar.py` and adjacent financial-calendar services/tests
- helper typing surfaces used across strict test contexts
- Alembic configuration and remaining static-quality surfaces

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
