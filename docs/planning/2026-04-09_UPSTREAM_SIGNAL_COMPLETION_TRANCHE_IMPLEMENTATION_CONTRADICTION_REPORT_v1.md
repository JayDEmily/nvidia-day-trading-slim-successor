# 2026-04-09_UPSTREAM_SIGNAL_COMPLETION_TRANCHE_IMPLEMENTATION_CONTRADICTION_REPORT_v1

Status: closed contradiction report retained as evidence under the upstream tranche pack closed through Gate 252 in the uploaded workspace copy.

## Purpose

Checkpoint extension authority: `/mnt/data/checkpoint_integrity_normative_extension.md` applies to modified upstream-tranche boundaries and gate-local tests.


Record the material tensions identified before planning this tranche so later gates do not improvise around them.

## Router state

- repo-root `PLANS.md` now records no active pack routed and retains the upstream tranche pack as the latest closed evidence
- the canonical gate map matches that closed-pack state
- the latest closed options-flow history pack remains predecessor evidence only

There is no router contradiction after Gate 252 closeout.

## Material runtime and contract tensions

1. `MarketRegimeContextInput` is richer than the live raw-to-cognition ingress path.
   - The schema already expects `nq_return_pct`, `es_return_pct`, `sox_return_pct`, `vix_level`, `vvix_level`, `us10y`, `us2y`, and `usdjpy`.
   - `RealDataCognitionInputs` and `ChainToCognitionService` currently carry `temporal_input`, `options_flow_input`, and `normalised_features`, but no live-built `regime_input` packet.

2. Same-bucket participation baseline doctrine exists, but live runtime wiring is thinner.
   - Gate 42 froze doctrine for same-bucket `volume`, `spread`, and `trade-count` baselines.
   - `PreparedRuntimeSnapshot` still exposes `relative_volume_ratio`, but not a lawful same-bucket baseline packet.

3. `PreparedNormalisedFeatureSet` is not a substitute for lawful regime ingress.
   - It preserves bounded derived fields and provenance.
   - It does not eliminate the need for a live `MarketRegimeContextInput` packet built from promoted upstream truth.

4. Optional top-of-book truth is attractive but unproven as cheap/admitted in the current repo surfaces.
   - The tranche must not smuggle it in as assumed scope.
   - Gate 248 must either admit it with proof or freeze deferral explicitly.

5. Class A versus Class B must stay separated.
   - Breadth, concentration, and dealer-flow drivers remain meaningful missing families.
   - They must not be hand-waved into this tranche merely because the schemas or downstream logic could consume them later.

## Required planning consequence

- Gate 247 must freeze one coverage map and one Class A / Class B truth split.
- Gate 248 through Gate 251 must use one lawful source path per promoted family.
- Gate 252 must log the still-missing Class A families explicitly rather than letting them disappear from closeout.
