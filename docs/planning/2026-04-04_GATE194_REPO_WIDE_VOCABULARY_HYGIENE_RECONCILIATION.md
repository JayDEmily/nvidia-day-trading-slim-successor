# 2026-04-04_GATE194_REPO_WIDE_VOCABULARY_HYGIENE_RECONCILIATION

## Purpose

Close the bounded residual vocabulary-hygiene family that remained after Gate 193 by classifying whether the surviving forbidden extra-stage phrase occurrences are lawful explicit prohibition/history surfaces or ambient leakage.

## Source-truth decision

- The residual occurrences did **not** indicate a new runtime stage.
- The controlling runtime and review surfaces remain:
  - `src/nvda_desk/services/parallel_risk_lane.py`
  - `src/nvda_desk/services/capital_deployment_authority.py`
  - `src/nvda_desk/services/cognition_runtime.py`
  - `src/nvda_desk/services/review_explanation.py`
  - `src/nvda_desk/schemas/cognition.py`
- Those surfaces show the parallel lane remains explicitly non-stage and the capital-deployment authority remains a bounded downstream review seam.
- The surviving repo text hits were therefore classified as:
  - lawful disallowed-phrase policy surfaces (`scripts/build_canonical_vocabulary.py`, committed vocabulary JSON, and the parallel-risk lane code/tests);
  - lawful explanatory or historical planning/router surfaces for the currently active repair programme; and
  - one lawful explanatory integration-test surface asserting that capital deployment does not create an extra numbered stage.

## Repair applied

- hardened `tests/test_gate179_repo_wide_vocabulary_hygiene.py` so repo-wide phrase scans ignore transient cache/git artefacts rather than treating them as repo truth
- admitted the current planning/router docs and the bounded capital-deployment integration test as lawful explicit prohibition/history surfaces for this phrase family
- did not modify runtime semantics, the vocabulary generator, or capital-deployment behaviour

## Scope holds

- no generator/artifact truth was reopened
- no router/control tranche work from Gate 195 was started
- no runtime semantic repair from Gate 196 was started

## Proofs

- `PYTHONPATH=src python -m pytest -q tests/test_gate179_repo_wide_vocabulary_hygiene.py tests/test_gate190_capital_deployment_authority_integration.py tests/test_document_hygiene.py`
  - result: `11 passed in 7.49s`

## Closeout truth

Gate 194 closes the bounded residual phrase-classification family only.
The next active gate is Gate 195.

### Post-closeout widened proof

- `PYTHONPATH=src python -m pytest -q tests/test_gate50_vocabulary_governance.py tests/test_gate55_vocabulary_governance.py tests/test_gate60_state_policy_ontology.py tests/test_gate62_stability_metric_corridors.py tests/test_gate63_review_eligibility_governance.py tests/test_gate64_candidate_adjudication_governance.py tests/test_gate67_event_window_semantics.py tests/test_gate68_precursor_universe.py tests/test_gate69_phase_carry_policy.py tests/test_gate70_event_options_stress_policy.py tests/test_gate71_modifier_control_law.py tests/test_gate72_event_ingestion_provenance.py tests/test_gate73_event_store_query.py tests/test_gate74_live_event_richness.py tests/test_gate75_precursor_stitching.py tests/test_gate76_precursor_runtime_binding.py tests/test_gate77_review_failure_taxonomy.py tests/test_gate78_modifier_runtime_integration.py tests/test_gate89_financial_calendar_crosswalk_and_dmp_lane.py tests/test_gate179_repo_wide_vocabulary_hygiene.py tests/test_gate190_capital_deployment_authority_integration.py tests/test_document_hygiene.py`
  - result: `89 passed in 7.76s`
- `python -m pytest -q tests/test_gate192_phase3_main_target_repair_pack_planning.py tests/test_tranche_briefing_template_pack.py tests/test_planning_state_integrity.py tests/test_document_hygiene.py`
  - result: `11 passed in 0.48s`
