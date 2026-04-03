# 2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_DOCUMENT_TOUCH_CHECKLIST_v1

## Purpose

Declare the live and frozen control surfaces checked before the options-trace repair tranche begins and the surfaces that must move if execution proceeds.

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
- [x] latest closed gates/leaves/execution-log/checklist/scope-note surfaces for the Gate 171-180 pack
- [x] active pack status: none currently routed before Gate 181 bootstrap

## Template-source surfaces checked

- [x] `docs/planning/tranche_briefing_template_pack/README.md`
- [x] `docs/planning/tranche_briefing_template_pack/HOW_TO_USE_THESE_DOCUMENTS.md`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v2.md`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_GATE_TEMPLATE_v2.md`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_LEAVES_TEMPLATE_v2.json`

## Findings-verification surfaces checked

- [x] `nvda_options_trace_findings_report_2026-04-03.md`
- [x] `src/nvda_desk/services/options_flow_context.py`
- [x] `src/nvda_desk/services/real_data_loader.py`
- [x] `src/nvda_desk/services/chain_to_cognition.py`
- [x] `src/nvda_desk/services/market_state.py`
- [x] `src/nvda_desk/schemas/dataset.py`
- [x] `src/nvda_desk/schemas/cognition.py`
- [x] `src/nvda_desk/schemas/options.py`
- [x] `src/nvda_desk/db/models.py`
- [x] `tests/test_options_flow_context.py`

## If execution proceeds, these surfaces must be amended

### Mandatory planning quartet
- [x] repo-root `PLANS.md`
- [x] current canonical gate map
- [x] active leaves ledger
- [x] active execution log

### Tranche-specific live docs
- [x] `docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_GATES_v1.md`
- [x] `docs/planning/2026-04-03_OPTIONS_TRACE_INTEGRITY_REPAIR_SCOPE_NOTE_v1.md`
- [ ] vocabulary authority if Gate 185 freezes a new canonical term
- [x] packet/contract authority if Gate 182-185 change canonical field contracts

## Current planned sequence

options-trace integrity repair pack closed through Gate 186 on `main`.

## State-integrity invariants checked

- [x] `completed_leaf_ids` and `remaining_leaf_ids` are disjoint
- [x] every referenced leaf id exists in the leaves map
- [x] active pack remains lawful when Gate 181 closes and Gate 182 becomes active
- [x] earlier-gate planning tests were updated to permit this later valid state

## Notes

- The latest closed Gate 171-180 pack was inspected as evidence input only, not as the structural template for this pack.
- F5 is intentionally excluded from execution scope.

- Gate 185 did not amend the canonical vocabulary file; `surface_anchor_to_spot_pct` was frozen as a schema-field contract rather than a new stage/playbook taxonomy term.
- Gate 183 required persistence/API parity surfaces plus a migration to keep raw-row claims lawful.
