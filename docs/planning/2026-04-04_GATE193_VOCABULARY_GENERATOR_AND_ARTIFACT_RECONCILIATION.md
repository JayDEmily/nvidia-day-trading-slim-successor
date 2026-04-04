# 2026-04-04_GATE193_VOCABULARY_GENERATOR_AND_ARTIFACT_RECONCILIATION

## Purpose

Reconcile the vocabulary generator with the committed canonical vocabulary artifact using source truth first, then re-anchor the harvested dependent vocabulary-governance tests.

## Source-truth decision

- `scripts/build_canonical_vocabulary.py` was stale.
- `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` was already aligned with the repo's lawful source surfaces for bounded downstream capital deployment.
- The decisive source surfaces were:
  - `src/nvda_desk/services/capital_deployment_authority.py`
  - `src/nvda_desk/schemas/cognition.py`
  - `src/nvda_desk/services/cognition_runtime.py`
  - `src/nvda_desk/services/review_explanation.py`

Those source surfaces define a first-class bounded downstream `CapitalDeploymentAuthorityService` and `CapitalDeploymentAuthorityDecision`, so the generator was required to emit corresponding canonical vocabulary entries.

## Repair applied

- added generator entries for:
  - `capital_deployment_authority_service`
  - `capital_deployment_authority_decision`
- regenerated `docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json` from the generator so the committed artifact exactly matches generated output again

## Scope holds

- no runtime semantics changed
- no router/control surfaces changed
- no repo-wide ambient vocabulary hygiene work was mixed into this gate

## Proofs

- `PYTHONPATH=src python -m pytest -q tests/test_gate50_vocabulary_governance.py tests/test_gate55_vocabulary_governance.py tests/test_gate60_state_policy_ontology.py tests/test_gate62_stability_metric_corridors.py tests/test_gate63_review_eligibility_governance.py tests/test_gate64_candidate_adjudication_governance.py tests/test_gate67_event_window_semantics.py tests/test_gate68_precursor_universe.py tests/test_gate69_phase_carry_policy.py tests/test_gate70_event_options_stress_policy.py`
  - result: `39 passed in 3.10s`
- `python -m pip install 'sqlalchemy>=2,<3'`
  - sandbox-only dependency step required to satisfy already-declared repo imports for the second proof slice
- `PYTHONPATH=src python -m pytest -q tests/test_gate71_modifier_control_law.py tests/test_gate72_event_ingestion_provenance.py tests/test_gate73_event_store_query.py tests/test_gate74_live_event_richness.py tests/test_gate75_precursor_stitching.py tests/test_gate76_precursor_runtime_binding.py tests/test_gate77_review_failure_taxonomy.py tests/test_gate78_modifier_runtime_integration.py tests/test_gate89_financial_calendar_crosswalk_and_dmp_lane.py`
  - result: `39 passed in 4.20s`

## Closeout truth

Gate 193 closes the generator/artifact truth seam only.
The next active gate is Gate 194.
