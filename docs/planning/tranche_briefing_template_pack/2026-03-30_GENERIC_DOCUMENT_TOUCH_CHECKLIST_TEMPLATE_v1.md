# YYYY-MM-DD_<TRANCHE_NAME>_DOCUMENT_TOUCH_CHECKLIST_v1

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
- [ ] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v2.md`
- [ ] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_GATE_TEMPLATE_v2.md`
- [ ] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_LEAVES_TEMPLATE_v2.json`
- [ ] `docs/planning/tranche_briefing_template_pack/2026-03-30_GENERIC_EXECUTION_LOG_TEMPLATE_v1.md`

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
- [ ] tests were updated to permit later valid states or retired/replaced

## Notes

- Add or strike items explicitly; do not leave implied control surfaces in chat memory.
- If a surface is intentionally unchanged, say so rather than omitting it.
- If a latest closed pack was inspected, record it as evidence input rather than the structural template for the new pack.
- GitHub branch/commit/merge history is the default routine execution ledger; full-history zip packaging is conditional only for backup, offline handoff, or sandbox transfer packaging.
