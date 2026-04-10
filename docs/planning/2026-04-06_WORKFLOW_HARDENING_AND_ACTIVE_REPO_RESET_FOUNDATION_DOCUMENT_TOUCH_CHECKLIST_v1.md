# 2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_DOCUMENT_TOUCH_CHECKLIST_v1

## Purpose

Declare the live and frozen control surfaces that were checked before the tranche began and the surfaces that must be amended if execution proceeds.

## Frozen law surfaces checked

- [x] `docs/01_NORMATIVE.md`
- [x] `docs/02_OPERATING_MODEL.md`
- [x] `docs/03_DOMAIN_MODEL.md`
- [x] `docs/04_TECHNICAL_ARCHITECTURE.md`
- [x] `docs/05_GUARDRAILS.md`
- [x] `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- [x] `AGENTS.md`

## Live routing surfaces checked

- [x] repo-root `PLANS.md`
- [x] current canonical gate map
- [ ] current active gates master — none currently routed when this pack was written
- [ ] current active leaves ledger — none currently routed when this pack was written
- [ ] current active execution log — none currently routed when this pack was written
- [ ] bounded-scope note named by `PLANS.md` — no active pack, so none named
- [x] latest closed pack retained as evidence input only

## Template-source surfaces checked

- [x] `docs/planning/tranche_briefing_template_pack/README.md`
- [x] `docs/planning/tranche_briefing_template_pack/HOW_TO_USE_THESE_DOCUMENTS.md`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v2.md`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_GATE_TEMPLATE_v2.md`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_LEAVES_TEMPLATE_v2.json`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-30_GENERIC_EXECUTION_LOG_TEMPLATE_v1.md`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-30_GENERIC_DOCUMENT_TOUCH_CHECKLIST_TEMPLATE_v1.md`

## Operator-surface inputs checked

- [x] `README.md`
- [x] `Makefile`

## If execution proceeds, these surfaces must be amended

### Mandatory planning quartet
- [x] repo-root `PLANS.md`
- [x] current canonical gate map
- [x] active leaves ledger
- [x] active execution log

### Tranche-specific live docs
- [x] active gates master for this tranche
- [x] contradiction report for this tranche
- [x] scope note for this tranche
- [ ] `docs/08_TESTING_AND_PROMOTION.md` — amend only if proof-order doctrine genuinely changes
- [ ] `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` — amend only if a new governed term is admitted
- [ ] `docs/03_DOMAIN_MODEL.md` — amend only if later gates discover a packet/contract boundary defect
- [x] `README.md`
- [x] `Makefile`
- [x] `docs/planning/tranche_briefing_template_pack/*`
- [x] `AGENTS.md`
- [x] `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`

## State-integrity invariants checked

- [x] `completed_leaf_ids` and `remaining_leaf_ids` are disjoint
- [x] every referenced leaf id exists in the leaves map
- [x] `active_gate = none` only when `remaining_leaf_ids` and `pending_gate_ids` are empty
- [x] no active pack is currently routed, so a new pack is required before later execution starts
- [x] the latest closed pack was treated as evidence input only, not as the structural template for this new pack

## Notes

- The material contradictions that justify this tranche are recorded in `docs/planning/2026-04-06_WORKFLOW_HARDENING_AND_ACTIVE_REPO_RESET_FOUNDATION_CONTRADICTION_REPORT_v1.md`.
- The latest closed 2026-04-05 successor pack was inspected as evidence input only.
- If a surface is intentionally unchanged during execution, that decision must be stated explicitly in the execution log rather than left implicit.
