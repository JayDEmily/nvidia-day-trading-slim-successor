# 2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_DOCUMENT_TOUCH_CHECKLIST_v1

## Purpose

Declare the frozen, source, and successor control surfaces that must be checked before the successor bootstrap pack begins and amended if execution proceeds in the slim repo.

## Frozen law surfaces checked

- [x] `docs/01_NORMATIVE.md`
- [x] `docs/02_OPERATING_MODEL.md`
- [x] `docs/03_DOMAIN_MODEL.md`
- [x] `docs/04_TECHNICAL_ARCHITECTURE.md`
- [x] `docs/05_GUARDRAILS.md`
- [x] `docs/06_REPO_PROCESS_AND_TRANCHE_LAW.md`
- [x] `docs/08_TESTING_AND_PROMOTION.md`
- [x] `AGENTS.md`

## Source-repo routing and evidence surfaces checked

- [x] source repo-root `PLANS.md`
- [x] source canonical gate map
- [x] source latest closed gates master
- [x] source latest closed leaves ledger
- [x] source latest closed execution log
- [x] source Gate 210 cutover brief
- [x] Gate 202 evidence-governance artefacts
- [x] rescoped `07` ledger attachment
- [x] source-repo current `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md` versus rewrite diff

## Template-source surfaces checked

- [x] `docs/planning/tranche_briefing_template_pack/README.md`
- [x] `docs/planning/tranche_briefing_template_pack/HOW_TO_USE_THESE_DOCUMENTS.md`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_TRANCHE_BRIEFING_DOCTRINE_v2.md`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_GATE_TEMPLATE_v2.md`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-29_GENERIC_LEAVES_TEMPLATE_v2.json`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-30_GENERIC_EXECUTION_LOG_TEMPLATE_v1.md`
- [x] `docs/planning/tranche_briefing_template_pack/2026-03-30_GENERIC_DOCUMENT_TOUCH_CHECKLIST_TEMPLATE_v1.md`

## If successor execution proceeds, these surfaces must be amended

### Mandatory successor planning quartet
- [ ] successor repo-root `PLANS.md`
- [ ] successor canonical gate map
- [ ] active successor leaves ledger
- [ ] active successor execution log

### Tranche-specific live docs
- [ ] `docs/07_RUNTIME_SURFACE_OWNERSHIP_AND_DOWNSTREAM_CONSUMER_LEDGER.md`
- [ ] `AGENTS.md`
- [ ] `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_07_SOURCE_DIFF_AND_AGENTS_READ_TRIGGER_NOTE_v1.md`
- [ ] `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_RETAINED_SURFACE_MANIFEST_AND_CUTOVER_RULES_v1.md`
- [ ] `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_INVENTORY_CLASSIFICATION_AND_DECISION_RULES_v1.md`
- [ ] `2026-04-06_SLIM_ACTIVE_REPO_CUTOVER_AND_SUBSTANTIVE_TEST_AUDIT_BOOTSTRAP_TEST_AUDIT_PROOF_SLICE_AND_SUCCESSOR_HANDOFF_v1.md`
- [ ] `docs/08_TESTING_AND_PROMOTION.md` if proof order or test doctrine changes

## State-integrity invariants checked

- [x] `completed_leaf_ids` and `remaining_leaf_ids` are disjoint
- [x] every referenced leaf id exists in the leaves map
- [x] no source-repo control surface is rewritten to claim this successor pack is active there
- [x] later valid successor-routing states are intended to be machine-checkable
- [x] test decisions are required to preserve disagreement memory and explicit evidence anchors

## Notes

- The source repo remains the archive/evidence host and should remain unchanged by this bundle.
- This bundle is import-ready for the slim successor repo; it is not a routed active pack in the source repo.
- GitHub branch/commit/merge history remains the default routine execution ledger once the successor repo exists; full-history zip packaging is conditional only for backup, offline handoff, or sandbox transfer packaging.
