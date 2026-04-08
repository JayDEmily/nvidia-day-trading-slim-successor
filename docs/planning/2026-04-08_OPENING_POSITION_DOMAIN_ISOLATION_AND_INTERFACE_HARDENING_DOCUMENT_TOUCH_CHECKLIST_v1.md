# 2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_DOCUMENT_TOUCH_CHECKLIST_v1

## Purpose

Declare the live and frozen control surfaces checked while drafting this pack, and the surfaces that must move later if execution proceeds.

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
- [x] latest closed retained pack gates master
- [x] latest closed retained pack leaves ledger
- [x] latest closed retained pack execution log
- [x] bounded-scope note and contradiction report named by repo-root `PLANS.md`

## Template-source surfaces checked

- [x] `docs/planning/tranche_briefing_template_pack/README.md`
- [x] `docs/planning/tranche_briefing_template_pack/HOW_TO_USE_THESE_DOCUMENTS.md`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v2.md`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_GATE_TEMPLATE_v2.md`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_LEAVES_TEMPLATE_v2.json`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-30_GENERIC_EXECUTION_LOG_TEMPLATE_v1.md`

## If execution proceeds later, these surfaces must be amended

### Mandatory planning quartet
- [x] repo-root `PLANS.md`
- [x] `docs/planning/2026-03-24_CANONICAL_VISION_GATE_MAP_v1.md`
- [x] `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_LEAVES_v1.json`
- [x] `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_EXECUTION_LOG_v1.md`

### Tranche-specific live docs
- [x] `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_GATES_v1.md`
- [x] `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_SCOPE_NOTE_v1.md`
- [x] `docs/planning/2026-04-08_OPENING_POSITION_DOMAIN_ISOLATION_AND_INTERFACE_HARDENING_CONTRADICTION_REPORT_v1.md`
- [ ] `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` if later execution changes surface ranking or consumer permissions
- [ ] `docs/03_DOMAIN_MODEL.md` if later execution changes packet, schema, or domain-contract truth
- [ ] `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` only if later execution proves new governed vocabulary is genuinely required

## State-integrity invariants checked

- [x] `completed_leaf_ids` and `remaining_leaf_ids` are disjoint in draft state
- [x] every referenced leaf id exists in the leaves map
- [x] Gate 226 closeout state uses a lawful no-active-gate-between-gates string rather than the closed-pack `active_gate = none` terminal state
- [x] later planning-guard tests are expected to permit lawful later valid states

## Notes

- This checklist was drafted during planning and then used in Gate 226 to route the active pack truthfully.
- The latest closed retained pack was inspected as evidence input only, not reused as the structural template.
- Opening-position-only scope remains explicit. No close-position, capital-displacement, carry, or arbiter logic belongs in this pack.
- Gate 229 and Gate 230 freeze the non-cumulative serial decision-risk rule so later coding addresses the current carried-forward generic-veto defect directly.
