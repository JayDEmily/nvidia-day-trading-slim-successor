# YYYY-MM-DD_<TRANCHE_NAME>_DOCUMENT_TOUCH_CHECKLIST_v2

## Purpose

Declare the live and frozen control surfaces that must be checked before the tranche begins and amended if the tranche proceeds.

## Frozen law surfaces checked

- [ ] `docs/01_NORMATIVE.md`
- [ ] `docs/02_OPERATING_MODEL.md`
- [ ] `docs/03_DOMAIN_MODEL.md`
- [ ] `docs/04_TECHNICAL_ARCHITECTURE.md`
- [ ] `docs/05_GUARDRAILS.md`
- [ ] `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- [ ] `AGENTS.md`

## Live routing surfaces checked

- [ ] repo-root `PLANS.md`
- [ ] current active gate map
- [ ] current active gates master
- [ ] current active leaves ledger
- [ ] current active execution log
- [ ] bounded-scope note if one is named by `PLANS.md`

## Template-source surfaces checked

- [ ] `docs/planning/tranche_briefing_template_pack/README.md`
- [ ] `docs/planning/tranche_briefing_template_pack/HOW_TO_USE_THESE_DOCUMENTS.md`
- [ ] `docs/planning/tranche_briefing_template_pack/2026-04-06_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v3.md`
- [ ] `docs/planning/tranche_briefing_template_pack/2026-04-06_GENERIC_GATE_TEMPLATE_v3.md`
- [ ] `docs/planning/tranche_briefing_template_pack/2026-04-06_GENERIC_LEAVES_TEMPLATE_v3.json`
- [ ] `docs/planning/tranche_briefing_template_pack/2026-04-06_GENERIC_EXECUTION_LOG_TEMPLATE_v2.md`

## Continuity model checked

- [ ] default stop-after-each-gate or controlled continuity model is named explicitly
- [ ] pack-install proof before the first gate is named explicitly
- [ ] exact authorised gate sequence is named when controlled continuity is used
- [ ] merge-before-next-gate rule is named explicitly when controlled continuity is used
- [ ] exact stop conditions are named explicitly when controlled continuity is used
- [ ] final router state after the last authorised gate is named explicitly

## If execution proceeds, these surfaces must be amended

### Mandatory planning quartet
- [ ] repo-root `PLANS.md`
- [ ] current canonical gate map
- [ ] active leaves ledger
- [ ] active execution log

### Tranche-specific live docs
- [ ] <current active gates master>
- [ ] <testing doctrine if proof order changes>
- [ ] <vocabulary authority if naming changes>
- [ ] <packet/contract authority if interface or schema changes>

## State-integrity invariants checked

- [ ] `completed_leaf_ids` and `remaining_leaf_ids` are disjoint
- [ ] every referenced leaf id exists in the leaves map
- [ ] `active_gate = none` only when `remaining_leaf_ids` and `pending_gate_ids` are empty
- [ ] tests were updated or replaced if older proof files would reject the later valid state
- [ ] controlled continuity, if used, still preserves per-gate closeout and per-gate quartet movement

## Contradiction scan completed

- [ ] contradiction scan run before planning began
- [ ] contradiction report linked if material control-surface conflicts existed
- [ ] no unresolved contradiction survives into the active pack
